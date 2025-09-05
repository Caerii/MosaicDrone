# Battery Module Spec

## Purpose
Provide safe, swappable energy with telemetry and protection.

## Requirements
- Nominal voltage: 6S Li-ion/LiPo (nominal 22.2 V; max 25.2 V); option: 12S for heavy payload variants
- Capacity targets: 2.5–5.0 Ah per module (air unit); 5–10 Ah (perch-supplied buffer)
- Continuous current: ≥ 30 A (air unit); peak: ≥ 60 A for 3 s
- Swap time: ≤ 20 s with tool-less latch; hot-swap on dock supported
- Operating temp: charge 0–45 °C; discharge −10–55 °C
- IP rating target: IP54 (air unit), IP67 (perch battery enclosures)
- Compliance: UN38.3 transport; IEC 62133 (cells); relevant local regs

## BMS and protection
- Cell chemistry: 18650/21700 Li-ion; NMC or LFP variants
- Protections: OV/UV/OC/OT; short-circuit; pack imbalance
- Balancing: passive at ≥ 50 mA; active optional for high-rate packs
- Isolation: pack-side fuse; high-side FETs with ideal diode controller
- Pre-charge: 100–330 Ω, 1–2 W; bypass after < 200 ms or < 100 mV delta
- Connectors: power XT60/XT90 or SB50; signal MicroFit 3.0 or M8

## Mechanical
- Form factor: sled with guide rails and detent latch
- Mounts: vibration isolation pads; captive screws optional for service
- Latch: spring-loaded with secondary lock; wear life ≥ 5k cycles
- Enclosure: vented with flame retardant plastic; thermal pads to spread heat

## Electrical
- Power pins: mate-last/break-first for positive; ground mate-first
- Sense/comm pins: mate-after ground; ESD protection; TVS on lines
- Pre-charge path: resistor + FET controlled by dock/ECU
- Isolation resistance: ≥ 1 MΩ to chassis

## Telemetry and data
- Interface: CAN 2.0B 500 kbps (option: SMBus over I2C for bench)
- Update rate: 10–50 Hz
- Fields: SoC, SoH, pack voltage, pack current, cell min/max/avg voltages, temperatures (pack and cell), cycle count, error flags
- Identifiers: pack ID, chemistry, capacity rating, manufacture date

## Procedures
- Hot-swap on dock: orchestrator commands pre-charge, verifies Vdiff < 100 mV, enables main FETs
- Off-drone swap: system enters low-power hover or voxel substitution before removal
- Storage: 30–50% SoC; 10–25 °C; periodic top-up

## Tests
- Electrical: OC/SC response, pre-charge timing, ripple under load steps
- Environmental: drop (0.5–1 m), vibration (per IEC 60068), thermal cycle (−10↔55 °C)
- Abuse: nail/penetration surrogate tests (bench, not flight units); vent directionality validation
- Endurance: ≥ 300 cycles with ≤ 20% capacity fade

## Risks
- Thermal events; connector wear; moisture ingress; CAN bus noise

## Open questions
- Final connector selection vs mass/volume; active balancing ROI; LFP option for safety

## Versioning
- v0.2 detailed spec
