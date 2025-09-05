# Docking and Interconnect

## Have
- Conceptual docking state machine and roles
- Notes on mechanical latch, pogo power, and data via pins

## Missing
- Mechanical interface spec: alignment cones, latch forces, misalignment tolerance, wear, life cycles
- Electrical interface spec: pinout, ratings, inrush/soft-start, ORing, reverse protection, EMI filters
- Data interface spec: PHY/protocol (CAN or Ethernet), CRC and retries, auto-discovery, bandwidth budget
- Full state machine with thresholds, timeouts, recovery, and fault codes
- Test jigs and acceptance tests

## Next
- Draft `docs/docking/interface.md` with mechanical, power, data sections
- Prototype latch and pogo pad layouts in `hardware/CAD/`
- Define `msgs/docking/*.msg` for state/telemetry and write unit tests
