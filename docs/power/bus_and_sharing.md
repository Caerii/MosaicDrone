# Power Bus and Sharing Spec

## Purpose
Enable safe power distribution and source/sink sharing across docked units.

## Bus
- Nominal bus: 24 V DC (compatible with 6S packs); optional 48 V for aggregates
- Max continuous current per segment: 40 A; peak 80 A for 3 s
- Cabling: silicone wire AWG 12–14 for units; AWG 8–10 for rails; derating per temp
- Protection: polyfuse or fuse links per unit; ideal diode ORing at each source
- Grounding: single-point reference on aggregate; shield drains to chassis at one end

## Sharing protocol
- Physical: sense line and direction pins; ADC read of bus voltage and current
- Discovery: announce source capability (Vset, Imax), sink demand (Ireq)
- Arbitration: single master per aggregate (orchestrator); tie-break by ID
- Negotiation: 
  - Sources expose droop (mΩ) and Imax; sinks request Ireq
  - Master assigns current budgets; sources limit via DC-DC or ESC supply
- Brownout protection: cut-in at 23.0 V; cut-out at 22.0 V with hysteresis
- Pre-charge: resistor path enabled when |Vpack−Vbus| > 0.3 V; main connect below 0.1 V delta

## Detection
- Presence detect: GPIO pulled by mating; debounce 10–50 ms
- Direction: pin strap indicates source/sink/bidirectional capability
- Fault: overcurrent, undervoltage, reverse polarity, isolation fault

## Tests
- Inrush timing and voltage overshoot
- Short-circuit clearing time and fault reporting
- Load steps 0→Imax and Imax→0; voltage droop/overshoot
- Efficiency vs load; thermal steady-state on rails

## Risks
- Ground loops; oscillations among multiple sources; EMI from switching regulators

## Open questions
- 48 V aggregate bus option; DC-DC topology choice; galvanic isolation needs

## Versioning
- v0.2 detailed spec
