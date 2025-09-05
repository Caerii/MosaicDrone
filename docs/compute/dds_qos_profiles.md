# DDS QoS Profiles (CycloneDDS focus) v0.1

## Topic classes
- Control (wrench, mode): RELIABLE, KEEP_LAST depth=5, deadline=20 ms, history=KEEP_LAST, liveliness=AUTOMATIC lease=200 ms
- Telemetry (health, power): BEST_EFFORT, KEEP_LAST depth=50, deadline=500 ms
- State (dock_state, task_status): RELIABLE, TRANSIENT_LOCAL, depth=1
- Video/vision: BEST_EFFORT, KEEP_LAST depth=10

## CycloneDDS XML mapping
See sample `cyclonedds.xml` for concrete profile names:
- `Profile.ControlLowLatency`
- `Profile.Telemetry`
- `Profile.StateLatched`
- `Profile.Vision`

## Network
- Disable multicast where required; prefer unicast peers on outdoor pilots
- Fine-tune `Transport/Builtin/UDP/RecvBufferSize` for video streams
- Time sync via PTP; monitor drift; avoid clock jumps

## Notes
- Assign profiles per-topic in launch files via `RMW_QOS_PROFILE` or programmatic QoS
- Validate end-to-end latency with `ros2_tracing` sessions under expected load


