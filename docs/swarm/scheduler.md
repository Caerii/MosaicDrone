# Scheduler and Logistics Spec

## Objectives
- Maximize utility (yield, stability) with energy and safety constraints

## Model
- Task: id, type, utility function, deadline, duration estimate
- Resources: agents with SOC, health, link quality; docks and cells availability
- Constraints: collision envelopes, geofences, deadlines, redundancy slots

## Policies
- Recharge rotation: threshold SOC with hysteresis; substitution before departure
- Failure handling: reassign tasks; degrade gracefully; notify operator
- Priority: critical safety and control > recharge > formation aesthetics > logging

## KPIs
- Uptime (% of coverage); mean plan latency; task success rate; energy per minute
- Dock success rate; formation pose error; scheduler CPU load

## Versioning
- v0.2 detailed spec
