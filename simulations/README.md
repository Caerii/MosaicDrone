# Simulations

## Environments
- Gazebo: worlds, plugins, ROS 2 bridges
- MuJoCo: dynamics experiments
- Unity: AR/HRI prototyping

## Scenarios
- Docking under wind; unit loss; reconfiguration; landfill hazards

## Running
- Gazebo: `ros2 launch simulations/gazebo mosaic_swarm.launch.py world:=indoor_arena`
- Scenario param: `wind:=2.0 loss_rate:=0.01`

## KPIs
- Dock success rate and time; formation pose error; energy per minute; CPU load

## Pass/Fail thresholds
- Docking ≥ 95% success; pose error ≤ 30 mm RMS; all tests < 80% CPU
