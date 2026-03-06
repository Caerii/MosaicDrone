# Docking and Interconnect

## Have
- [Docking interface spec](../docking/interface.md): mechanical (alignment, latch, envelope), electrical (pinout, inrush, ORing, TVS, EMI), data (CAN/Ethernet options, CRC, retries, bandwidth budget), state machine with thresholds, timeouts, recovery, fault codes, tests, related docs
- Conceptual docking state machine and roles; perception and safety cross-links

## Missing
- Test jigs and acceptance test procedures (traceable to interface spec)
- CAD: latch and pogo pad layouts in `hardware/CAD/docking/`
- ROS 2 (or equivalent) `msgs/docking/*` for state/telemetry/fault codes and unit tests

## Next
- Prototype latch and pogo pad layouts in `hardware/CAD/docking/`
- Define `msgs/docking/*.msg` (or equivalent) for state, telemetry, fault codes; add unit tests
- Add acceptance test checklist derived from [interface.md](../docking/interface.md#tests)
