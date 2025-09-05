# Docking Perception Spec

## Sensors
- Fiducial markers (AprilTag) or active beacons (IR/LED)
- Short-range depth (stereo or ToF)
- IMU for contact detection

## Performance
- Pose accuracy: < 5 mm, < 2° within 0.3 m range
- Latency: < 30 ms end-to-end for corrections
- Lighting: 50–10,000 lux; flicker and glare rejection

## Algorithms
- Marker detection/tracking; PnP solve; Kalman smoothing
- Confidence thresholds; outlier rejection; fallback to brute-force proximity alignment

## Versioning
- v0.2 detailed spec
