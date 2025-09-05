# Interaction and Intent Grammar

## Gestures and intents
- Attract (pull voxel/patch)
- Repel (push away)
- Lock (freeze local shape)
- Rotate (roll/pitch/yaw patch)
- Draw (trace path or surface)
- Approve (confirm plan) / Halt (pause)

## Latency budgets
- Gesture to intent parse: ≤ 30 ms; intent to actuation: ≤ 50 ms
- Total loop: ≤ 80 ms

## Safety
- Dynamic exclusion zone around humans with margin; immediate freeze on violation
- Consent prompts for close-range operation; supervised modes
- Manual override: hardware and software E-stop

## Feedback
- AR: outline, vectors, confidence shading; audio cues; optional haptics

## Privacy
- No biometric storage; on-device inference where possible; redaction in recordings

## Versioning
- v0.2 detailed spec
