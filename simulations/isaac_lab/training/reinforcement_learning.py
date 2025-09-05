#!/usr/bin/env python3
"""
SOTA Reinforcement Learning for MosaicDrone Swarm using Isaac Lab
Advanced multi-agent RL with curriculum learning and domain randomization
"""

import torch
import torch.nn as nn
import numpy as np
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
import gymnasium as gym
from omni.isaac.lab.envs import ManagerBasedRLEnv, ManagerBasedRLEnvCfg
from omni.isaac.lab.managers import ObservationGroupCfg, ActionGroupCfg, RewardGroupCfg
from omni.isaac.lab.utils.math import quat_mul, quat_conjugate, quat_apply
import omni.isaac.lab.sim as sim_utils

@dataclass
class SwarmRLConfig:
    """Configuration for swarm reinforcement learning"""
    # Environment Configuration
    num_drones: int = 20
    max_episode_length: int = 2000  # steps
    control_frequency: float = 50.0  # Hz
    
    # Observation Space
    obs_history_length: int = 4  # timesteps
    neighbor_observation_range: float = 50.0  # meters
    max_neighbors_observed: int = 8
    
    # Action Space
    action_type: str = "continuous"  # continuous, discrete, hybrid
    action_clipping: bool = True
    action_noise_std: float = 0.1
    
    # Reward Configuration
    formation_reward_weight: float = 1.0
    task_completion_reward_weight: float = 3.0
    energy_efficiency_reward_weight: float = 0.5
    safety_reward_weight: float = 5.0
    exploration_reward_weight: float = 0.2
    
    # Curriculum Learning
    enable_curriculum: bool = True
    curriculum_stages: int = 5
    stage_advancement_threshold: float = 0.8  # success rate
    
    # Domain Randomization
    enable_domain_randomization: bool = True
    randomization_probability: float = 0.8
    
    # Training Configuration
    algorithm: str = "MAPPO"  # MAPPO, QMIX, MADDPG
    learning_rate: float = 3e-4
    batch_size: int = 512
    buffer_size: int = 100000
    update_frequency: int = 10  # episodes

class MosaicDroneRLEnvironment(ManagerBasedRLEnv):
    """
    SOTA Multi-Agent RL Environment for MosaicDrone Swarm
    Features:
    - Scalable multi-agent observation and action spaces
    - Hierarchical task decomposition
    - Curriculum learning progression
    - Domain randomization for robustness
    - Real-time performance optimization
    """
    
    def __init__(self, cfg: ManagerBasedRLEnvCfg, config: SwarmRLConfig):
        self.swarm_config = config
        self.current_curriculum_stage = 0
        self.episode_count = 0
        self.success_history = []
        
        # Initialize curriculum tasks
        self.curriculum_tasks = self._initialize_curriculum_tasks()
        
        # Initialize domain randomization
        self.randomization_params = self._initialize_randomization_params()
        
        super().__init__(cfg)
        
        # Setup multi-agent spaces
        self.observation_spaces = self._create_observation_spaces()
        self.action_spaces = self._create_action_spaces()
        
    def _initialize_curriculum_tasks(self) -> List[Dict]:
        """Initialize curriculum learning progression"""
        
        return [
            {
                "stage": 0,
                "name": "basic_hover",
                "description": "Learn stable hovering for individual drones",
                "formation_complexity": 1,  # Single drone
                "environmental_difficulty": 0.1,  # Calm conditions
                "task_objectives": ["maintain_altitude", "minimize_drift"],
                "success_criteria": {
                    "altitude_error": 0.5,  # meters
                    "position_drift": 2.0,  # meters
                    "episode_success_rate": 0.8
                }
            },
            {
                "stage": 1,
                "name": "formation_maintenance",
                "description": "Maintain simple formations with multiple drones",
                "formation_complexity": 4,  # 4 drones in square
                "environmental_difficulty": 0.2,  # Light wind
                "task_objectives": ["maintain_formation", "coordinate_movement"],
                "success_criteria": {
                    "formation_error": 1.0,  # meters
                    "inter_drone_distance": 5.0,  # meters minimum
                    "episode_success_rate": 0.8
                }
            },
            {
                "stage": 2,
                "name": "dynamic_reconfiguration",
                "description": "Learn to reconfigure formations dynamically",
                "formation_complexity": 8,  # 8 drones, changing formations
                "environmental_difficulty": 0.3,  # Moderate wind
                "task_objectives": ["formation_transitions", "collision_avoidance"],
                "success_criteria": {
                    "transition_time": 30.0,  # seconds
                    "collision_count": 0,
                    "episode_success_rate": 0.8
                }
            },
            {
                "stage": 3,
                "name": "cooperative_docking",
                "description": "Learn cooperative docking and load sharing",
                "formation_complexity": 12,  # 12 drones with docking
                "environmental_difficulty": 0.4,  # Wind gusts
                "task_objectives": ["successful_docking", "load_distribution"],
                "success_criteria": {
                    "docking_success_rate": 0.9,
                    "docking_time": 10.0,  # seconds
                    "episode_success_rate": 0.8
                }
            },
            {
                "stage": 4,
                "name": "complex_missions",
                "description": "Complete complex landfill mining missions",
                "formation_complexity": 20,  # Full swarm
                "environmental_difficulty": 0.6,  # Realistic conditions
                "task_objectives": ["material_classification", "area_coverage", "hazard_avoidance"],
                "success_criteria": {
                    "area_coverage": 0.95,  # 95% of target area
                    "classification_accuracy": 0.85,
                    "safety_violations": 0,
                    "episode_success_rate": 0.8
                }
            }
        ]
    
    def _create_observation_spaces(self) -> Dict:
        """Create multi-agent observation spaces"""
        
        # Individual drone observations
        drone_obs_dim = (
            6 +   # position and velocity (3+3)
            4 +   # orientation quaternion (4)
            3 +   # angular velocity (3)
            6 +   # motor states (6 motors)
            6 +   # arm angles (6 arms)
            1 +   # battery level (1)
            8 +   # docking states (8 contacts)
            4     # task progress (4 metrics)
        )
        
        # Neighbor observations (relative states)
        neighbor_obs_dim = (
            3 +   # relative position (3)
            3 +   # relative velocity (3)
            4 +   # relative orientation (4)
            2     # communication quality and role (2)
        ) * self.swarm_config.max_neighbors_observed
        
        # Environmental observations
        env_obs_dim = (
            3 +   # wind vector (3)
            1 +   # temperature (1)
            10 +  # nearby hazards (10 max)
            20    # material classification map (20 classes)
        )
        
        # Task-specific observations
        task_obs_dim = (
            3 +   # formation target position (3)
            4 +   # formation target orientation (4)
            1 +   # formation role/priority (1)
            5     # mission objectives (5 different types)
        )
        
        total_obs_dim = drone_obs_dim + neighbor_obs_dim + env_obs_dim + task_obs_dim
        
        return {
            "single_agent": gym.spaces.Box(
                low=-np.inf, high=np.inf, 
                shape=(total_obs_dim,), dtype=np.float32
            ),
            "multi_agent": gym.spaces.Dict({
                f"drone_{i}": gym.spaces.Box(
                    low=-np.inf, high=np.inf,
                    shape=(total_obs_dim,), dtype=np.float32
                )
                for i in range(self.swarm_config.num_drones)
            })
        }
    
    def _create_action_spaces(self) -> Dict:
        """Create multi-agent action spaces"""
        
        if self.swarm_config.action_type == "continuous":
            # Continuous action space: motor thrusts + arm angles
            action_dim = (
                6 +   # motor thrust commands (6 motors)
                6 +   # arm angle commands (6 arms)  
                3 +   # formation control (3D velocity command)
                1     # docking command (0=none, 1=initiate)
            )
            
            action_space = gym.spaces.Box(
                low=-1.0, high=1.0,
                shape=(action_dim,), dtype=np.float32
            )
            
        elif self.swarm_config.action_type == "discrete":
            # Discrete action space for simplified control
            action_space = gym.spaces.MultiDiscrete([
                11,  # thrust level (0-10)
                8,   # movement direction (8 directions + hover)
                5,   # formation mode (5 different modes)
                2    # docking command (0=none, 1=initiate)
            ])
            
        else:  # hybrid
            action_space = gym.spaces.Dict({
                "continuous": gym.spaces.Box(
                    low=-1.0, high=1.0,
                    shape=(12,), dtype=np.float32  # motors + arms
                ),
                "discrete": gym.spaces.MultiDiscrete([8, 5, 2])  # direction, mode, docking
            })
        
        return {
            "single_agent": action_space,
            "multi_agent": gym.spaces.Dict({
                f"drone_{i}": action_space
                for i in range(self.swarm_config.num_drones)
            })
        }
    
    def _get_observations(self) -> Dict[str, torch.Tensor]:
        """Get multi-agent observations"""
        
        observations = {}
        
        for i in range(self.swarm_config.num_drones):
            drone_obs = self._get_single_drone_observation(i)
            observations[f"drone_{i}"] = drone_obs
        
        return observations
    
    def _get_single_drone_observation(self, drone_id: int) -> torch.Tensor:
        """Get observation for a single drone"""
        
        # Get drone state
        drone_state = self._get_drone_state(drone_id)
        
        # Get neighbor observations
        neighbor_obs = self._get_neighbor_observations(drone_id)
        
        # Get environmental observations
        env_obs = self._get_environmental_observations(drone_id)
        
        # Get task-specific observations
        task_obs = self._get_task_observations(drone_id)
        
        # Concatenate all observations
        full_observation = torch.cat([
            drone_state,
            neighbor_obs,
            env_obs,
            task_obs
        ], dim=0)
        
        return full_observation
    
    def _get_drone_state(self, drone_id: int) -> torch.Tensor:
        """Get individual drone state vector"""
        
        drone = self.drone_swarm[drone_id]
        
        # Position and velocity
        position = drone["asset"].data.root_pos_w[0]  # World position
        velocity = drone["asset"].data.root_lin_vel_w[0]  # World velocity
        
        # Orientation and angular velocity
        orientation = drone["asset"].data.root_quat_w[0]  # Quaternion
        angular_velocity = drone["asset"].data.root_ang_vel_w[0]  # Angular velocity
        
        # Motor states (normalized thrust)
        motor_states = drone["state"]["motor_thrusts"] / drone["config"]["motor_specs"]["max_thrust"]
        
        # Arm angles (normalized)
        arm_angles = drone["state"]["arm_angles"] / (2 * np.pi)
        
        # Battery level (normalized)
        battery_level = torch.tensor([drone["state"]["battery_soc"]], dtype=torch.float32)
        
        # Docking states
        docking_states = torch.tensor(drone["state"]["docking_contacts"], dtype=torch.float32)
        
        # Task progress metrics
        task_progress = torch.tensor([
            drone["state"]["task_completion"],
            drone["state"]["formation_error"],
            drone["state"]["energy_efficiency"],
            drone["state"]["safety_score"]
        ], dtype=torch.float32)
        
        return torch.cat([
            position, velocity, orientation, angular_velocity,
            motor_states, arm_angles, battery_level, docking_states, task_progress
        ])
    
    def _get_neighbor_observations(self, drone_id: int) -> torch.Tensor:
        """Get observations of neighboring drones"""
        
        drone_pos = self.drone_swarm[drone_id]["asset"].data.root_pos_w[0]
        neighbor_obs = []
        
        # Find nearby drones
        neighbor_count = 0
        for other_id in range(self.swarm_config.num_drones):
            if other_id == drone_id or neighbor_count >= self.swarm_config.max_neighbors_observed:
                continue
                
            other_pos = self.drone_swarm[other_id]["asset"].data.root_pos_w[0]
            distance = torch.norm(other_pos - drone_pos)
            
            if distance <= self.swarm_config.neighbor_observation_range:
                # Relative position and velocity
                rel_pos = other_pos - drone_pos
                rel_vel = (self.drone_swarm[other_id]["asset"].data.root_lin_vel_w[0] - 
                          self.drone_swarm[drone_id]["asset"].data.root_lin_vel_w[0])
                
                # Relative orientation
                drone_quat = self.drone_swarm[drone_id]["asset"].data.root_quat_w[0]
                other_quat = self.drone_swarm[other_id]["asset"].data.root_quat_w[0]
                rel_quat = quat_mul(quat_conjugate(drone_quat), other_quat)
                
                # Communication quality and role
                comm_quality = torch.tensor([1.0 - distance / self.swarm_config.neighbor_observation_range])
                role_info = torch.tensor([self.drone_swarm[other_id]["state"]["formation_role"]])
                
                neighbor_info = torch.cat([rel_pos, rel_vel, rel_quat, comm_quality, role_info])
                neighbor_obs.append(neighbor_info)
                neighbor_count += 1
        
        # Pad with zeros if fewer neighbors than max
        while neighbor_count < self.swarm_config.max_neighbors_observed:
            neighbor_obs.append(torch.zeros(12))  # 3+3+4+1+1 = 12
            neighbor_count += 1
        
        return torch.cat(neighbor_obs)
    
    def _get_environmental_observations(self, drone_id: int) -> torch.Tensor:
        """Get environmental observations"""
        
        drone_pos = self.drone_swarm[drone_id]["asset"].data.root_pos_w[0]
        
        # Wind conditions
        wind_vector = torch.tensor(self.environment.weather_system["current_wind_vector"])
        
        # Temperature
        temperature = torch.tensor([self.environment.weather_system["temperature"]])
        
        # Nearby hazards
        hazard_obs = torch.zeros(10)  # Max 10 hazards
        hazard_count = 0
        
        for hazard in self.environment.hazard_zones:
            if hazard_count >= 10:
                break
                
            hazard_pos = torch.tensor(hazard["position"][:2])  # x, y only
            distance = torch.norm(hazard_pos - drone_pos[:2])
            
            if distance <= 50.0:  # 50m observation range
                hazard_obs[hazard_count] = 1.0 - distance / 50.0  # Normalized distance
                hazard_count += 1
        
        # Material classification map (simplified)
        material_map = torch.zeros(20)  # 20 material classes
        # This would be populated based on drone's sensor data
        
        return torch.cat([wind_vector, temperature, hazard_obs, material_map])
    
    def _get_task_observations(self, drone_id: int) -> torch.Tensor:
        """Get task-specific observations"""
        
        current_task = self.curriculum_tasks[self.current_curriculum_stage]
        drone = self.drone_swarm[drone_id]
        
        # Formation target position
        formation_target = torch.tensor(drone["state"]["formation_target_position"])
        
        # Formation target orientation
        formation_orientation = torch.tensor(drone["state"]["formation_target_orientation"])
        
        # Formation role/priority
        formation_role = torch.tensor([drone["state"]["formation_role"]])
        
        # Mission objectives progress
        mission_progress = torch.tensor([
            drone["state"]["coverage_progress"],
            drone["state"]["classification_progress"],
            drone["state"]["safety_compliance"],
            drone["state"]["energy_remaining"],
            drone["state"]["docking_availability"]
        ])
        
        return torch.cat([formation_target, formation_orientation, formation_role, mission_progress])
    
    def _apply_actions(self, actions: Dict[str, torch.Tensor]):
        """Apply multi-agent actions to the environment"""
        
        for i in range(self.swarm_config.num_drones):
            drone_action = actions[f"drone_{i}"]
            self._apply_single_drone_action(i, drone_action)
    
    def _apply_single_drone_action(self, drone_id: int, action: torch.Tensor):
        """Apply action to a single drone"""
        
        if self.swarm_config.action_type == "continuous":
            # Extract action components
            motor_commands = action[:6]  # Motor thrust commands
            arm_commands = action[6:12]  # Arm angle commands
            formation_commands = action[12:15]  # Formation control
            docking_command = action[15]  # Docking initiation
            
            # Apply motor commands
            self._apply_motor_commands(drone_id, motor_commands)
            
            # Apply arm commands
            self._apply_arm_commands(drone_id, arm_commands)
            
            # Apply formation commands
            self._apply_formation_commands(drone_id, formation_commands)
            
            # Apply docking command
            if docking_command > 0.5:
                self._initiate_docking(drone_id)
                
        elif self.swarm_config.action_type == "discrete":
            # Convert discrete actions to continuous commands
            thrust_level = action[0].item() / 10.0  # Normalize to [0, 1]
            direction = action[1].item()
            formation_mode = action[2].item()
            docking_command = action[3].item()
            
            # Convert to motor commands
            motor_commands = self._discrete_to_motor_commands(thrust_level, direction)
            self._apply_motor_commands(drone_id, motor_commands)
            
            # Apply formation mode
            self._set_formation_mode(drone_id, formation_mode)
            
            # Apply docking command
            if docking_command > 0:
                self._initiate_docking(drone_id)
    
    def _compute_rewards(self) -> Dict[str, torch.Tensor]:
        """Compute multi-agent rewards"""
        
        rewards = {}
        
        for i in range(self.swarm_config.num_drones):
            drone_reward = self._compute_single_drone_reward(i)
            rewards[f"drone_{i}"] = drone_reward
        
        return rewards
    
    def _compute_single_drone_reward(self, drone_id: int) -> torch.Tensor:
        """Compute reward for a single drone"""
        
        drone = self.drone_swarm[drone_id]
        
        # Formation maintenance reward
        formation_error = drone["state"]["formation_error"]
        formation_reward = torch.exp(-formation_error / 2.0)  # Exponential decay
        
        # Task completion reward
        task_progress = drone["state"]["task_completion"]
        task_reward = task_progress
        
        # Energy efficiency reward
        energy_efficiency = drone["state"]["energy_efficiency"]
        energy_reward = energy_efficiency
        
        # Safety reward
        safety_violations = drone["state"]["safety_violations"]
        safety_reward = torch.exp(-safety_violations)  # Exponential penalty
        
        # Exploration reward
        exploration_bonus = drone["state"]["exploration_bonus"]
        
        # Combine rewards
        total_reward = (
            self.swarm_config.formation_reward_weight * formation_reward +
            self.swarm_config.task_completion_reward_weight * task_reward +
            self.swarm_config.energy_efficiency_reward_weight * energy_reward +
            self.swarm_config.safety_reward_weight * safety_reward +
            self.swarm_config.exploration_reward_weight * exploration_bonus
        )
        
        return total_reward
    
    def _check_termination(self) -> Dict[str, bool]:
        """Check episode termination conditions"""
        
        # Global termination conditions
        episode_timeout = self.episode_step_count >= self.swarm_config.max_episode_length
        mission_completed = self._check_mission_completion()
        critical_failure = self._check_critical_failures()
        
        # Individual drone termination
        drone_terminations = {}
        for i in range(self.swarm_config.num_drones):
            drone_crashed = self._check_drone_crash(i)
            drone_lost = self._check_drone_communication_loss(i)
            
            drone_terminations[f"drone_{i}"] = drone_crashed or drone_lost
        
        # Environment termination
        global_termination = episode_timeout or mission_completed or critical_failure
        
        return {
            "global": global_termination,
            **drone_terminations
        }
    
    def _update_curriculum(self):
        """Update curriculum learning progression"""
        
        if not self.swarm_config.enable_curriculum:
            return
        
        # Check if current stage is mastered
        current_task = self.curriculum_tasks[self.current_curriculum_stage]
        recent_success_rate = np.mean(self.success_history[-100:]) if len(self.success_history) >= 100 else 0.0
        
        if recent_success_rate >= self.swarm_config.stage_advancement_threshold:
            if self.current_curriculum_stage < len(self.curriculum_tasks) - 1:
                self.current_curriculum_stage += 1
                print(f"Advanced to curriculum stage {self.current_curriculum_stage}: {self.curriculum_tasks[self.current_curriculum_stage]['name']}")
                
                # Reset environment for new stage
                self._reset_for_new_curriculum_stage()
    
    def _apply_domain_randomization(self):
        """Apply domain randomization for robustness"""
        
        if not self.swarm_config.enable_domain_randomization:
            return
        
        if np.random.random() < self.swarm_config.randomization_probability:
            # Randomize physical parameters
            self._randomize_drone_parameters()
            
            # Randomize environmental conditions
            self._randomize_environment_conditions()
            
            # Randomize sensor noise and failures
            self._randomize_sensor_characteristics()
    
    def reset(self) -> Dict[str, torch.Tensor]:
        """Reset the environment for a new episode"""
        
        # Update curriculum if needed
        self._update_curriculum()
        
        # Apply domain randomization
        self._apply_domain_randomization()
        
        # Reset drone states
        self._reset_drone_states()
        
        # Reset environment
        self._reset_environment_state()
        
        # Reset episode tracking
        self.episode_step_count = 0
        self.episode_count += 1
        
        # Get initial observations
        observations = self._get_observations()
        
        return observations
    
    def step(self, actions: Dict[str, torch.Tensor]) -> Tuple[Dict, Dict, Dict, Dict]:
        """Step the environment forward"""
        
        # Apply actions
        self._apply_actions(actions)
        
        # Step physics simulation
        self.sim.step()
        
        # Update environment dynamics
        self.environment.simulate_environmental_dynamics(self.physics_dt)
        
        # Update drone states
        self._update_drone_states()
        
        # Get observations
        observations = self._get_observations()
        
        # Compute rewards
        rewards = self._compute_rewards()
        
        # Check termination
        terminations = self._check_termination()
        
        # Generate info
        infos = self._generate_step_info()
        
        # Update episode tracking
        self.episode_step_count += 1
        
        return observations, rewards, terminations, infos

class MAPPOTrainer:
    """Multi-Agent PPO trainer for MosaicDrone swarm"""
    
    def __init__(self, env: MosaicDroneRLEnvironment, config: SwarmRLConfig):
        self.env = env
        self.config = config
        
        # Initialize policy networks
        self.policy_networks = self._create_policy_networks()
        
        # Initialize training components
        self.optimizer = torch.optim.Adam(
            self.policy_networks.parameters(),
            lr=config.learning_rate
        )
        
        # Training tracking
        self.training_step = 0
        self.episode_rewards = []
        self.success_rates = []
    
    def train(self, total_timesteps: int):
        """Train the multi-agent swarm policy"""
        
        print(f"Starting MAPPO training for {total_timesteps} timesteps")
        
        timestep = 0
        while timestep < total_timesteps:
            # Collect rollout data
            rollout_data = self._collect_rollout()
            timestep += len(rollout_data["observations"])
            
            # Update policy
            self._update_policy(rollout_data)
            
            # Log progress
            if self.training_step % 100 == 0:
                self._log_training_progress(timestep, total_timesteps)
            
            self.training_step += 1
        
        print("Training completed!")
        return self.policy_networks

def main():
    """Main training function"""
    
    # Configuration
    rl_config = SwarmRLConfig(
        num_drones=8,  # Start with smaller swarm for training
        enable_curriculum=True,
        enable_domain_randomization=True,
        algorithm="MAPPO"
    )
    
    # Create environment configuration
    env_cfg = ManagerBasedRLEnvCfg()
    # Configure environment settings here...
    
    # Create environment
    env = MosaicDroneRLEnvironment(env_cfg, rl_config)
    
    # Create trainer
    trainer = MAPPOTrainer(env, rl_config)
    
    # Train the policy
    trained_policy = trainer.train(total_timesteps=1000000)
    
    # Save the trained model
    torch.save(trained_policy.state_dict(), "mosaic_drone_swarm_policy.pth")
    
    print("Training completed and model saved!")

if __name__ == "__main__":
    main()
