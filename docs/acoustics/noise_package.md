# Noise Reduction Package Spec

## Purpose
Reduce acoustic footprint for indoor/public operation while maintaining performance.

## Targets
- Hover SPL at 1 m: ≤ 62 dBA (indoor class), ≤ 68 dBA (outdoor class)
- Maneuver SPL at 1 m: ≤ 70 dBA (indoor), ≤ 75 dBA (outdoor)
- Psychoacoustic: tonality index ≤ 0.1; roughness ≤ 0.05 asper

## Techniques
- Prop selection: larger/slower RPM; serrated/toroidal blades; balance and tracking
- ESC control: 48–96 kHz PWM; slew rate limits; spread-spectrum if available
- Structural damping: motor isolators; foam-lined panels; brace placement to move modes
- Control smoothing: allocator penalties for throttle/arm velocity; trajectory smoothers

## Measurement setup
- Mic array at 1 m, 45° increments; room qualification or outdoor baseline
- Weighting: A-weighted primary; 1/3 octave band capture
- Profiles: hover, step, sinusoidal sweep, trajectory
- Data schema: timestamp, SPL bands, RPM, thrust, position

## Acceptance criteria
- Meet targets across profiles; no dominant tones > 6 dB above adjacent bands

## Risks
- Efficiency tradeoffs; mass increase; heat

## Versioning
- v0.2 detailed spec
