# Power and Energy

## Have
- Recharge rotation flow and infrastructure ideas (perches/inductive/swaps)
- High-level power sharing concept via dock

## Missing
- Battery module spec: pack format, BMS, telemetry, connectors, thermal and crash safety
- Power bus spec: DC voltage/current, protection, pre-charge, soft-start, efficiency
- Power sharing protocol: source/sink negotiation, limits, brownout protection, handover
- Charger hardware and charging profile spec; occupancy arbitration

## Next
- Write `docs/power/battery_module.md` and `docs/power/bus_and_sharing.md`
- Define charging handshake messages and test procedures
- Model energy budgets and SOC thresholds in `swarm/logistics/`
