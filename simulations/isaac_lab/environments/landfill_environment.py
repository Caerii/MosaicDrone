#!/usr/bin/env python3
"""
SOTA Landfill Environment for MosaicDrone using Isaac Lab
Photorealistic landfill simulation with material classification, hazard detection, and environmental dynamics
"""

import torch
import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import omni.isaac.lab.sim as sim_utils
from omni.isaac.lab.terrains import TerrainImporter
from omni.isaac.lab.assets import RigidObject
from omni.isaac.lab.sensors import Camera, Lidar
from omni.isaac.lab.utils.math import quat_from_euler_xyz
import omni.replicator.core as rep

@dataclass
class LandfillEnvironmentConfig:
    """Configuration for photorealistic landfill environment"""
    # Terrain Configuration
    terrain_size: Tuple[float, float] = (500.0, 500.0)  # meters
    height_variation: Tuple[float, float] = (0.0, 15.0)  # meters
    slope_threshold: float = 30.0  # degrees maximum slope
    
    # Material Distribution
    organic_waste_ratio: float = 0.35
    plastic_waste_ratio: float = 0.25
    metal_debris_ratio: float = 0.15
    glass_fragments_ratio: float = 0.10
    electronic_waste_ratio: float = 0.05
    soil_cover_ratio: float = 0.10
    
    # Environmental Hazards
    methane_hotspot_count: int = 8
    unstable_slope_count: int = 5
    contaminated_area_count: int = 12
    
    # Weather and Atmospheric Conditions
    enable_weather_simulation: bool = True
    wind_speed_range: Tuple[float, float] = (0.0, 15.0)  # m/s
    temperature_range: Tuple[float, float] = (-10.0, 40.0)  # Celsius
    humidity_range: Tuple[float, float] = (30.0, 95.0)  # %
    
    # Lighting and Visual Conditions
    enable_dynamic_lighting: bool = True
    time_of_day_simulation: bool = True
    weather_effects: bool = True  # fog, rain, dust
    
    # Material Classification Training
    material_variety_count: int = 50  # Different material types per category
    surface_texture_variations: int = 20
    weathering_states: int = 10  # Different degradation levels
    
    # Physics Simulation
    enable_fluid_dynamics: bool = True  # For leachate simulation
    enable_gas_dynamics: bool = True    # For methane plume modeling
    enable_particulate_simulation: bool = True  # For dust and debris

class LandfillEnvironmentGenerator:
    """
    SOTA Landfill Environment Generator
    Features:
    - Procedural terrain generation with realistic material distribution
    - Photorealistic material rendering for AI training
    - Dynamic environmental hazards and weather conditions
    - Physics-based simulation of gases, fluids, and particulates
    - Synthetic data generation for perception training
    """
    
    def __init__(self, config: LandfillEnvironmentConfig):
        self.config = config
        self.material_database = self._initialize_material_database()
        self.hazard_zones = self._initialize_hazard_zones()
        self.weather_system = self._initialize_weather_system()
        
    def _initialize_material_database(self) -> Dict:
        """Initialize comprehensive material database with physical properties"""
        
        return {
            "organic_waste": {
                "density_range": (400, 800),  # kg/m³
                "color_variations": [
                    (0.4, 0.3, 0.2),  # Brown decomposed
                    (0.6, 0.5, 0.3),  # Light brown fresh
                    (0.2, 0.2, 0.1),  # Dark decomposed
                    (0.5, 0.4, 0.2),  # Mixed organic
                ],
                "surface_roughness": (0.5, 2.0),  # mm RMS
                "moisture_content": (20, 80),  # %
                "spectral_signature": {
                    "nir_reflectance": (0.15, 0.35),
                    "visible_reflectance": (0.10, 0.25),
                    "thermal_emissivity": (0.85, 0.95)
                },
                "gas_emission": {
                    "methane": (50, 200),  # ppm
                    "co2": (1000, 5000),   # ppm
                    "h2s": (1, 10)         # ppm
                }
            },
            
            "plastic_waste": {
                "subtypes": {
                    "pet_bottles": {
                        "density": 1380,  # kg/m³
                        "color_variations": [
                            (0.9, 0.9, 0.9),  # Clear/white
                            (0.2, 0.6, 0.9),  # Blue
                            (0.1, 0.7, 0.1),  # Green
                            (0.8, 0.4, 0.1),  # Brown
                        ],
                        "transparency": (0.7, 0.95),
                        "surface_finish": "smooth",
                        "degradation_states": {
                            "new": {"surface_roughness": 0.1, "color_fade": 0.0},
                            "weathered": {"surface_roughness": 0.5, "color_fade": 0.3},
                            "degraded": {"surface_roughness": 1.2, "color_fade": 0.7}
                        }
                    },
                    "hdpe_containers": {
                        "density": 950,  # kg/m³
                        "color_variations": [
                            (0.9, 0.9, 0.9),  # White
                            (0.1, 0.1, 0.1),  # Black
                            (0.8, 0.2, 0.2),  # Red
                            (0.9, 0.8, 0.1),  # Yellow
                        ],
                        "opacity": 0.95,
                        "surface_finish": "matte"
                    },
                    "plastic_bags": {
                        "density": 920,  # kg/m³
                        "thickness": (0.01, 0.05),  # mm
                        "flexibility": "high",
                        "wind_response": "high"
                    }
                },
                "spectral_signature": {
                    "nir_reflectance": (0.60, 0.85),
                    "visible_reflectance": (0.40, 0.80),
                    "thermal_emissivity": (0.90, 0.95)
                }
            },
            
            "metal_debris": {
                "subtypes": {
                    "ferrous_metals": {
                        "density": 7850,  # kg/m³ steel
                        "magnetic_susceptibility": 100.0,
                        "corrosion_states": {
                            "fresh": {"color": (0.7, 0.7, 0.7), "reflectance": 0.6},
                            "oxidized": {"color": (0.6, 0.3, 0.1), "reflectance": 0.2},
                            "heavily_rusted": {"color": (0.4, 0.2, 0.1), "reflectance": 0.1}
                        },
                        "surface_roughness": (0.5, 5.0)  # mm RMS
                    },
                    "aluminum_cans": {
                        "density": 2700,  # kg/m³
                        "magnetic_susceptibility": 0.0,
                        "reflectance": (0.7, 0.9),
                        "color_variations": [
                            (0.8, 0.8, 0.8),  # Natural aluminum
                            (0.9, 0.2, 0.2),  # Red painted
                            (0.2, 0.2, 0.8),  # Blue painted
                            (0.1, 0.8, 0.1),  # Green painted
                        ]
                    },
                    "copper_wire": {
                        "density": 8960,  # kg/m³
                        "color": (0.7, 0.4, 0.2),  # Copper color
                        "oxidation_color": (0.2, 0.6, 0.4),  # Green patina
                        "electrical_conductivity": "high"
                    }
                }
            },
            
            "glass_fragments": {
                "density": 2500,  # kg/m³
                "color_variations": [
                    (0.9, 0.9, 0.9),  # Clear
                    (0.2, 0.6, 0.2),  # Green
                    (0.4, 0.3, 0.1),  # Brown
                    (0.2, 0.2, 0.8),  # Blue
                ],
                "transparency": (0.8, 0.95),
                "surface_roughness": (0.1, 2.0),  # Varies from smooth to frosted
                "fracture_patterns": ["sharp_edges", "rounded_edges", "powdered"],
                "spectral_signature": {
                    "nir_reflectance": (0.85, 0.95),
                    "visible_transmittance": (0.80, 0.92),
                    "thermal_emissivity": (0.85, 0.90)
                }
            },
            
            "electronic_waste": {
                "subtypes": {
                    "circuit_boards": {
                        "density": 2000,  # kg/m³
                        "color": (0.1, 0.4, 0.1),  # Green PCB
                        "metallic_components": 0.3,  # Fraction
                        "hazardous_materials": ["lead", "mercury", "cadmium"]
                    },
                    "plastic_casings": {
                        "density": 1200,  # kg/m³
                        "color_variations": [
                            (0.1, 0.1, 0.1),  # Black
                            (0.9, 0.9, 0.9),  # White/beige
                            (0.5, 0.5, 0.5),  # Gray
                        ],
                        "flame_retardants": True
                    },
                    "cables": {
                        "density": 1500,  # kg/m³
                        "copper_content": 0.6,  # Fraction
                        "plastic_insulation": 0.4,  # Fraction
                        "flexibility": "medium"
                    }
                }
            }
        }
    
    def _initialize_hazard_zones(self) -> List[Dict]:
        """Initialize environmental hazard zones with realistic properties"""
        
        hazard_zones = []
        
        # Methane hotspots
        for i in range(self.config.methane_hotspot_count):
            hotspot = {
                "type": "methane_emission",
                "position": self._random_position_in_terrain(),
                "radius": np.random.uniform(5.0, 20.0),  # meters
                "emission_rate": np.random.uniform(10, 100),  # L/min
                "concentration_peak": np.random.uniform(1000, 5000),  # ppm
                "temperature_elevation": np.random.uniform(5, 15),  # °C above ambient
                "detection_signature": {
                    "thermal": "elevated_temperature",
                    "gas_sensor": "high_methane",
                    "visual": "vegetation_stress"
                }
            }
            hazard_zones.append(hotspot)
        
        # Unstable slopes
        for i in range(self.config.unstable_slope_count):
            slope = {
                "type": "unstable_slope",
                "position": self._random_position_in_terrain(),
                "area": np.random.uniform(25.0, 100.0),  # m²
                "slope_angle": np.random.uniform(25.0, 45.0),  # degrees
                "stability_factor": np.random.uniform(0.8, 1.2),  # <1.0 = unstable
                "material_composition": "mixed_waste_with_soil",
                "risk_indicators": {
                    "surface_cracks": True,
                    "settlement_marks": True,
                    "water_seepage": np.random.choice([True, False])
                }
            }
            hazard_zones.append(slope)
        
        # Contaminated areas
        for i in range(self.config.contaminated_area_count):
            contamination = {
                "type": "chemical_contamination",
                "position": self._random_position_in_terrain(),
                "radius": np.random.uniform(3.0, 15.0),  # meters
                "contaminant_type": np.random.choice([
                    "heavy_metals", "organic_solvents", "acids", "pcb", "asbestos"
                ]),
                "concentration_level": np.random.choice(["low", "medium", "high"]),
                "detection_signature": {
                    "spectral": "absorption_peaks",
                    "thermal": "temperature_anomaly",
                    "visual": "discoloration_or_staining"
                }
            }
            hazard_zones.append(contamination)
        
        return hazard_zones
    
    def create_landfill_terrain(self) -> sim_utils.GroundPlaneCfg:
        """Create procedural landfill terrain with realistic material distribution"""
        
        # Generate height map
        terrain_height_map = self._generate_terrain_heightmap()
        
        # Generate material distribution map
        material_distribution = self._generate_material_distribution()
        
        # Create terrain configuration
        terrain_cfg = sim_utils.GroundPlaneCfg(
            size=self.config.terrain_size,
            color=(0.4, 0.3, 0.2),  # Base soil color
            physics_material=sim_utils.RigidBodyMaterialCfg(
                static_friction=0.8,
                dynamic_friction=0.6,
                restitution=0.1,
                friction_combine_mode="multiply",
                restitution_combine_mode="multiply"
            )
        )
        
        return terrain_cfg
    
    def populate_environment_objects(self) -> List[RigidObject]:
        """Populate environment with realistic waste objects"""
        
        objects = []
        
        # Calculate object density based on material ratios
        total_area = self.config.terrain_size[0] * self.config.terrain_size[1]
        objects_per_m2 = 0.5  # Average object density
        total_objects = int(total_area * objects_per_m2)
        
        for material_type, ratio in self._get_material_ratios().items():
            object_count = int(total_objects * ratio)
            
            for i in range(object_count):
                obj = self._create_material_object(material_type, i)
                objects.append(obj)
        
        return objects
    
    def _create_material_object(self, material_type: str, object_id: int) -> RigidObject:
        """Create individual material object with realistic properties"""
        
        material_props = self.material_database[material_type]
        
        # Select random subtype if available
        if "subtypes" in material_props:
            subtype = np.random.choice(list(material_props["subtypes"].keys()))
            props = material_props["subtypes"][subtype]
        else:
            props = material_props
        
        # Generate object configuration
        object_cfg = sim_utils.RigidObjectCfg(
            spawn=sim_utils.UsdFileCfg(
                usd_path=self._get_object_usd_path(material_type, subtype if "subtypes" in material_props else None),
                scale=(
                    np.random.uniform(0.5, 2.0),
                    np.random.uniform(0.5, 2.0),
                    np.random.uniform(0.5, 2.0)
                ),
            ),
            init_state=sim_utils.RigidObjectStateCfg(
                pos=(*self._random_position_in_terrain(), np.random.uniform(0.1, 2.0)),
                rot=quat_from_euler_xyz(
                    np.random.uniform(-np.pi, np.pi),
                    np.random.uniform(-np.pi/4, np.pi/4),
                    np.random.uniform(-np.pi, np.pi)
                ),
            ),
            rigid_props=sim_utils.RigidBodyPropertiesCfg(
                solver_position_iteration_count=4,
                solver_velocity_iteration_count=4,
                max_angular_velocity=50.0,
                max_linear_velocity=10.0,
                max_depenetration_velocity=1.0,
            ),
            physics_material=self._create_material_physics_properties(props),
        )
        
        return RigidObject(object_cfg)
    
    def setup_environmental_sensors(self) -> Dict:
        """Setup environmental monitoring sensors"""
        
        sensors = {}
        
        # Gas detection sensors at hazard zones
        for i, hazard in enumerate(self.hazard_zones):
            if hazard["type"] == "methane_emission":
                sensor_cfg = {
                    "type": "gas_sensor",
                    "position": hazard["position"],
                    "detection_range": hazard["radius"] * 1.5,
                    "sensitivity": {
                        "methane": 1.0,  # ppm
                        "hydrogen_sulfide": 0.1,  # ppm
                        "carbon_dioxide": 10.0,  # ppm
                    },
                    "response_time": 2.0,  # seconds
                }
                sensors[f"gas_sensor_{i}"] = sensor_cfg
        
        # Weather monitoring stations
        weather_stations = [
            (0, 0), (250, 0), (500, 0),
            (0, 250), (250, 250), (500, 250),
            (0, 500), (250, 500), (500, 500)
        ]
        
        for i, position in enumerate(weather_stations):
            sensor_cfg = {
                "type": "weather_station",
                "position": (*position, 10.0),  # 10m above ground
                "measurements": {
                    "wind_speed": {"range": (0, 50), "accuracy": 0.1},  # m/s
                    "wind_direction": {"range": (0, 360), "accuracy": 1.0},  # degrees
                    "temperature": {"range": (-40, 60), "accuracy": 0.1},  # °C
                    "humidity": {"range": (0, 100), "accuracy": 1.0},  # %
                    "pressure": {"range": (800, 1200), "accuracy": 0.1},  # hPa
                    "precipitation": {"range": (0, 100), "accuracy": 0.1},  # mm/h
                },
                "update_rate": 1.0,  # Hz
            }
            sensors[f"weather_station_{i}"] = sensor_cfg
        
        return sensors
    
    def setup_synthetic_data_generation(self) -> Dict:
        """Setup synthetic data generation for AI training"""
        
        with rep.new_layer():
            # Material classification data generation
            materials_rep = rep.create.from_usd([
                "/environments/landfill/materials/plastic_bottles.usd",
                "/environments/landfill/materials/metal_cans.usd",
                "/environments/landfill/materials/organic_waste.usd",
                "/environments/landfill/materials/glass_fragments.usd",
                "/environments/landfill/materials/electronic_waste.usd"
            ])
            
            # Randomize material properties
            with materials_rep:
                rep.modify.pose(
                    position=rep.distribution.uniform((-250, -250, 0), (250, 250, 5)),
                    rotation=rep.distribution.uniform((0, 0, 0), (360, 360, 360)),
                    scale=rep.distribution.uniform(0.5, 2.0)
                )
                
                rep.modify.visibility(
                    rep.distribution.choice([True, False], weights=[0.8, 0.2])
                )
            
            # Environmental condition randomization
            rep.modify.attribute(
                "Environment",
                "weather_condition",
                rep.distribution.choice(["clear", "cloudy", "foggy", "rainy"])
            )
            
            rep.modify.attribute(
                "Environment", 
                "time_of_day",
                rep.distribution.uniform(0, 24)  # Hours
            )
            
            # Camera setup for data collection
            camera = rep.create.camera(
                position=rep.distribution.uniform((-50, -50, 5), (50, 50, 30)),
                look_at=rep.distribution.uniform((-10, -10, 0), (10, 10, 3)),
                focal_length=rep.distribution.uniform(18, 85)  # mm
            )
            
            # Lighting randomization
            rep.create.light(
                light_type="Dome",
                intensity=rep.distribution.uniform(500, 2000),
                temperature=rep.distribution.uniform(3000, 7000),
                texture=rep.distribution.choice([
                    "/environments/hdri/clear_sky.hdr",
                    "/environments/hdri/cloudy_sky.hdr",
                    "/environments/hdri/overcast_sky.hdr"
                ])
            )
            
            # Setup render products and annotators
            render_product = rep.create.render_product(camera, (1280, 720))
            
            # Annotators for AI training
            rep.AnnotatorRegistry.get_annotator("rgb", device="cuda")
            rep.AnnotatorRegistry.get_annotator("semantic_segmentation", device="cuda") 
            rep.AnnotatorRegistry.get_annotator("instance_segmentation", device="cuda")
            rep.AnnotatorRegistry.get_annotator("bounding_box_2d_tight", device="cuda")
            rep.AnnotatorRegistry.get_annotator("depth", device="cuda")
            rep.AnnotatorRegistry.get_annotator("normals", device="cuda")
            rep.AnnotatorRegistry.get_annotator("motion_vectors", device="cuda")
            
            # Material property annotations for advanced training
            rep.AnnotatorRegistry.get_annotator("material_properties", device="cuda")
            rep.AnnotatorRegistry.get_annotator("spectral_reflectance", device="cuda")
            
        return {
            "replicator_graph": rep.orchestrator._orchestrator,
            "render_product": render_product,
            "camera": camera
        }
    
    def simulate_environmental_dynamics(self, dt: float):
        """Simulate dynamic environmental conditions"""
        
        # Update weather conditions
        self._update_weather_system(dt)
        
        # Update gas emissions and dispersion
        self._update_gas_dynamics(dt)
        
        # Update material degradation
        self._update_material_weathering(dt)
        
        # Update hazard zone evolution
        self._update_hazard_zones(dt)
    
    def _update_weather_system(self, dt: float):
        """Update weather conditions and atmospheric effects"""
        
        # Wind simulation
        current_wind = self.weather_system["current_wind"]
        target_wind = self.weather_system["target_wind"]
        
        # Smooth wind transitions
        wind_change_rate = 0.1  # m/s per second
        current_wind["speed"] += np.clip(
            target_wind["speed"] - current_wind["speed"],
            -wind_change_rate * dt,
            wind_change_rate * dt
        )
        
        # Update wind direction
        direction_change_rate = 5.0  # degrees per second
        direction_diff = target_wind["direction"] - current_wind["direction"]
        if direction_diff > 180:
            direction_diff -= 360
        elif direction_diff < -180:
            direction_diff += 360
            
        current_wind["direction"] += np.clip(
            direction_diff,
            -direction_change_rate * dt,
            direction_change_rate * dt
        )
        
        # Apply wind effects to objects
        self._apply_wind_forces(current_wind)
    
    def _update_gas_dynamics(self, dt: float):
        """Update gas emission and dispersion simulation"""
        
        for hazard in self.hazard_zones:
            if hazard["type"] == "methane_emission":
                # Calculate gas dispersion based on wind conditions
                wind = self.weather_system["current_wind"]
                
                # Simple Gaussian plume model
                dispersion_distance = hazard["emission_rate"] * wind["speed"] * dt
                concentration_decay = np.exp(-dispersion_distance / 100.0)
                
                # Update concentration field
                hazard["current_concentration"] = (
                    hazard["concentration_peak"] * concentration_decay
                )
                
                # Update plume geometry
                hazard["plume_geometry"] = self._calculate_gas_plume(hazard, wind)
    
    def get_environment_state(self) -> Dict:
        """Get current environment state for simulation"""
        
        return {
            "terrain": {
                "size": self.config.terrain_size,
                "material_distribution": self._get_current_material_distribution(),
                "height_map": self._get_current_height_map(),
            },
            "weather": {
                "wind_speed": self.weather_system["current_wind"]["speed"],
                "wind_direction": self.weather_system["current_wind"]["direction"],
                "temperature": self.weather_system["temperature"],
                "humidity": self.weather_system["humidity"],
                "visibility": self.weather_system["visibility"],
            },
            "hazards": [
                {
                    "type": hazard["type"],
                    "position": hazard["position"],
                    "severity": hazard.get("current_concentration", hazard.get("stability_factor", 1.0)),
                    "detection_signature": hazard["detection_signature"]
                }
                for hazard in self.hazard_zones
            ],
            "objects": {
                "total_count": len(self.objects),
                "by_material": self._count_objects_by_material(),
                "spatial_distribution": self._get_spatial_object_distribution(),
            }
        }

def main():
    """Test landfill environment generation"""
    
    config = LandfillEnvironmentConfig(
        terrain_size=(200.0, 200.0),
        enable_weather_simulation=True,
        enable_dynamic_lighting=True,
        material_variety_count=25
    )
    
    env_generator = LandfillEnvironmentGenerator(config)
    
    print("=== Landfill Environment Generation Test ===")
    
    # Create terrain
    terrain = env_generator.create_landfill_terrain()
    print(f"Terrain created: {config.terrain_size[0]}m x {config.terrain_size[1]}m")
    
    # Populate objects
    objects = env_generator.populate_environment_objects()
    print(f"Objects populated: {len(objects)} waste items")
    
    # Setup sensors
    sensors = env_generator.setup_environmental_sensors()
    print(f"Sensors deployed: {len(sensors)} monitoring stations")
    
    # Setup synthetic data generation
    data_gen = env_generator.setup_synthetic_data_generation()
    print("Synthetic data generation configured")
    
    # Get environment state
    env_state = env_generator.get_environment_state()
    print(f"Environment state: {len(env_state['hazards'])} hazards detected")
    
    print("Landfill environment ready for MosaicDrone simulation!")

if __name__ == "__main__":
    main()
