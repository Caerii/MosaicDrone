# Data Schemas

## Telemetry (ROS 2 msg schema draft)
- Pose: position (x,y,z), orientation (quaternion), covariance
- Health: temps, voltages, currents, CPU load
- Power: SOC, SoH, pack V/I, bus V/I, sharing role
- Dock: state enum, latch status, contact metrics
- Task: id, status, progress
- Link: RSSI, PER, channel

## QC and process
- Weld params: current, voltage, wire speed, gas, travel speed
- WAAM logs: layer idx, path id, temp, deposition rate
- Extrusion: nozzle temp, bed temp, speed, material code
- Inspection: dimensions, tolerance deviations, pass/fail

## Maps
- 3D: point cloud frames with timestamps; material classes; hazards (gas/heat)
- Compression: Draco or Zstd; chunked storage with index

## Versioning
- v0.2 detailed spec
