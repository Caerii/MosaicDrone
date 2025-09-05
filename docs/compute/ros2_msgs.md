# ROS 2 Message Contracts (v0.1)

## Conventions
- Time: ROS `builtin_interfaces/Time` in seconds/nanoseconds
- Frames: ENU world unless noted; quaternions `(x,y,z,w)`; SI units
- IDs: `string` stable across a session; UUID where needed

## Orchestrator → Agents

### `/orch/formation_cmd`
- Type: `mosaic_msgs/FormationCommand`
- Fields:
  - `string formation_id`
  - `string type`  // e.g., "grid", "shell", "text"
  - `float32 spacing_m`
  - `geometry_msgs/Pose[] anchors`  // optional anchor poses
  - `builtin_interfaces/Time start_time`
  - `float32 duration_s`  // 0 for persistent

### `/agent/<id>/control_cmd`
- Type: `mosaic_msgs/ControlWrench`
- Fields:
  - `geometry_msgs/Vector3 force_N`  // range: ±50 N per axis
  - `geometry_msgs/Vector3 torque_Nm`  // range: ±5 Nm per axis
  - `uint8 mode`  // see MODE_* enums

## Agents → Orchestrator

### `/agent/<id>/state`
- Type: `mosaic_msgs/AgentState`
- Fields:
  - `geometry_msgs/Pose pose`
  - `geometry_msgs/Twist twist`
  - `geometry_msgs/Accel accel`
  - `float32[9] pose_cov`  // row-major 3x3 position; orientation quality in `status`
  - `uint8 status`  // 0=OK,1=Degraded,2=Fault

### `/agent/<id>/telemetry`
- Type: `mosaic_msgs/Telemetry`
- Fields:
  - `float32 cpu_load_pct`  // range: 0..100
  - `float32 ram_used_mb`  // range: 0..16384
  - `float32 temp_c`  // range: -40..85
  - `float32 bus_voltage_V`  // range: 20..26
  - `float32 bus_current_A`  // range: -80..80
  - `float32 soc_0_1`  // range: 0..1
  - `float32 soh_0_1`  // range: 0..1
  - `uint8 link_quality_pct`  // range: 0..100
  - `uint8 dock_state`  // see DOCK_* enums
  - `uint8 error_flags`  // see ERROR_* bitmask below

### `/agent/<id>/dock_state`
- Type: `mosaic_msgs/DockState`
- Fields:
  - `uint8 state`  // 0=Seeking,1=Aligning,2=SoftContact,3=Latching,4=Verify,5=Bonded,6=Unlatch,7=Separating
  - `bool power_ok`
  - `bool data_ok`
  - `float32 contact_resistance_mOhm`
  - `float32 precharge_delta_V`
  - `uint8 fault_code`  // 0=OK, >0 per table

## Scheduler Interfaces

### `/orch/task_cmd`
- Type: `mosaic_msgs/TaskCommand`
- Fields:
  - `string task_id`
  - `uint8 type`  // see TASK_* enums
  - `string[] agent_ids`
  - `geometry_msgs/Pose target_pose`
  - `builtin_interfaces/Time deadline`
  - `float32 utility_0_1`  // range: 0..1

### `/orch/task_status`
- Type: `mosaic_msgs/TaskStatus`
- Fields:
  - `string task_id`
  - `uint8 state`  // see TASK_STATE_* enums
  - `float32 progress_0_1`  // range: 0..1
  - `uint8 failure_code`  // 0=OK, see TASK_FAIL_* enums

## Perception/Docking

### `/agent/<id>/dock_target`
- Type: `mosaic_msgs/DockTarget`
- Fields:
  - `geometry_msgs/PoseStamped pose`
  - `float32 confidence_0_1`
  - `float32 range_m`

## Enums (shared)

```
# Control modes
uint8 MODE_HOVER=0
uint8 MODE_TRAJECTORY=1
uint8 MODE_DOCKING=2
uint8 MODE_FAULT=3

# Docking states
uint8 DOCK_SEEKING=0
uint8 DOCK_ALIGNING=1
uint8 DOCK_SOFT_CONTACT=2
uint8 DOCK_LATCHING=3
uint8 DOCK_VERIFY=4
uint8 DOCK_BONDED=5
uint8 DOCK_UNLATCH=6
uint8 DOCK_SEPARATING=7

# Task types
uint8 TASK_RECHARGE=0
uint8 TASK_AGGREGATE=1
uint8 TASK_SCAN=2
uint8 TASK_DELIVER=3

# Task states
uint8 TASK_STATE_QUEUED=0
uint8 TASK_STATE_ACTIVE=1
uint8 TASK_STATE_DONE=2
uint8 TASK_STATE_FAILED=3
uint8 TASK_STATE_CANCELLED=4

# Task failure codes
uint8 TASK_FAIL_NONE=0
uint8 TASK_FAIL_TIMEOUT=1
uint8 TASK_FAIL_COLLISION=2
uint8 TASK_FAIL_LOW_BATTERY=3
uint8 TASK_FAIL_LINK_LOSS=4

# Error flags bitmask
uint8 ERROR_NONE=0
uint8 ERROR_OVERTEMP=1
uint8 ERROR_UNDERVOLT=2
uint8 ERROR_OVERCURRENT=4
uint8 ERROR_IMU_FAULT=8
uint8 ERROR_DOCK_FAULT=16
uint8 ERROR_LINK_DEGRADED=32
```

## Notes
- QoS: see `docs/compute/dds_qos_profiles.md`
- Message package skeleton: `ros2_msgs/` (TBD)


