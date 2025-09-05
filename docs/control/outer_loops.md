# Outer Loop Control Spec

## Purpose
Stabilize position and orientation, manage modes, and enforce limits.

## Signals
- Inputs: desired pose/velocity/accel; wind estimate; load estimate
- Outputs: desired wrench (F, M); mode transitions; safety flags

## Controllers
- Position: PID+feedforward on xyz; jerk-limited setpoint generator
- Orientation: PID on yaw/pitch/roll or quaternion error; rate feedforward
- Anti-windup and integrator clamping; bias estimation for steady errors

## Modes
- Hover; Trajectory; Formation Attach/Detach; Docking; Fault Safe (land/perch)
- Transitions: guarded by velocity and proximity thresholds

## Limits
- Vel/acc/jerk caps; workspace bounds; geofence; tilt limits for non-omni fallback

## Safety
- Watchdogs; link loss behavior; E-stop path (zero wrench or guided land)

## Parameters and tuning
- Gain tables by mass/inertia estimates; autotune procedure; logging for system ID

## Tests
- Step/ramp/trajectory tracking; wind disturbance; mass change; sensor dropout

## Versioning
- v0.2 detailed spec
