# Control and Autonomy

## Have
- SQP allocation overview and per-agent control stack diagram
- Reconfiguration idea for aggregates and mixer updates

## Missing
- SQP objective/constraint formal spec; timing budgets; singularity handling details
- Outer-loop control design; mode switching; limit enforcement; disturbance rejection
- Formation and reconfiguration spec with stability margins and aggregate limits

## Next
- Write `docs/control/sqp_allocator.md` and `docs/control/outer_loops.md`
- Define `docs/swarm/reconfiguration.md` and test scenarios in `simulations/`
- Add fail-injection tests for loss of unit and docking events
