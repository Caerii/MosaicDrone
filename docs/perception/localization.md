# Localization Spec

## Modes
- Indoor: MoCap or UWB fused with VIO for IMU bias stabilization
- Outdoor: RTK GNSS + VIO; fallback to GNSS-only with drift limits

## Fusion
- UKF/IEKF with IMU propagation; camera updates; UWB/MoCap absolute fixes
- Error budgets: position < 20 mm indoor, < 50 mm outdoor RTK; orientation < 1.5°

## Relocalization
- Loss detection via innovation spikes; switch to hold mode; perform visual relocalization
- Cooperative: request neighbor pose graph snippets

## Time sync
- All sensors timestamped; PTP with < 1 ms skew target

## Versioning
- v0.2 detailed spec
