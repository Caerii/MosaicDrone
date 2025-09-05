# Swarm Behaviors Spec

## Behavior set
- Scan: cover region; density control
- Hold: maintain positions with collision envelopes
- Aggregate: move to formation and dock
- Reconfigure: attach/detach; mixer update
- Recharge: depart/return scheduling; substitution
- Escort/Deliver: guide payloads or humans within safety limits

## Parameters
- Safety envelopes (per-unit radius, dynamic based on speed)
- Priorities and preemption rules
- Timeouts and retries; hysteresis to avoid flapping

## Interfaces
- Commands: behavior start/stop with params
- Status: state, progress, ETA, reasons for preemption
- Telemetry: per-behavior KPIs (coverage %, dock attempts)

## Examples
- Reconfigure: `{ target_topology: grid, spacing_m: 0.5 }`
- Recharge: `{ soc_min: 0.25, redundancy_slots: 2 }`

## Tests
- Multi-agent sim with injected delays and losses; ensure no deadlocks; acceptable latency and success rates

## Versioning
- v0.2 detailed spec
