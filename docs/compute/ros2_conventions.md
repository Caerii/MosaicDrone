# ROS 2 Conventions

## Namespaces and topics
- Namespace per agent: `/agent/<id>/...`
- Orchestrator: `/orch/...`
- Catalog examples:
  - `/orch/formation_cmd` (geometry_msgs/WrenchStamped equiv or custom)
  - `/agent/<id>/control_cmd` (desired F,M)
  - `/agent/<id>/state` (pose, twist)
  - `/agent/<id>/telemetry` (health, power, link)
  - `/agent/<id>/dock_state` (enum, metrics)
  - `/maps/chunks` (point cloud / octomap)

## QoS defaults
- Control: RELIABLE, depth=5, deadline 20 ms
- Telemetry: BEST_EFFORT, depth=50
- Video: BEST_EFFORT, depth=10

## Node lifecycle
- Configured → Inactive → Active → ErrorProcessing → Finalized
- Health status topic with liveness

## Launch patterns
- Composition where possible; parameters via YAML; remaps per environment

## Versioning
- v0.2 detailed spec

## See also
- `docs/compute/ros2_msgs.md` — message contracts and enums
- `docs/compute/dds_qos_profiles.md` — topic classes to QoS mapping
- `docs/compute/cyclonedds.xml` — sample DDS profiles configuration