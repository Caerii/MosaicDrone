# Swarm Telemetry Spec

## Data
- Pose, twist, accel; health (temps, voltages, currents); SOC/SoH; dock state; task state; link metrics

## Transport
- Topics: `/agent/<id>/telemetry`; QoS BEST_EFFORT; 10–30 Hz
- Reliability for critical health alerts: RELIABLE with latched last state

## Storage
- Rolling logs with compression; aggregation to timeseries DB; retention per policy
- Indices by agent id, time, scenario

## Versioning
- v0.2 detailed spec
