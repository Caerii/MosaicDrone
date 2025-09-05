# Compute Platform Spec

## Purpose
Define onboard compute, OS, real-time profile, and observability.

## Hardware
- Baseline SBC: RK3588 (Radxa Rock 5A/B) or NVIDIA Orin Nano (for vision-heavy units)
- RAM: ≥ 8 GB; Storage: ≥ 64 GB NVMe; Wi‑Fi 6 + BT; optional UWB module
- Interfaces: USB-C, CSI/CSI2 for cameras, UART/CAN, GPIO, GigE (PoE optional)
- Power: 24 V input via DC-DC; budget 10–20 W typical

## Software
- OS: Ubuntu 22.04 LTS; kernel RT-preempt optional
- ROS 2 Humble or newer; CycloneDDS; colcon workspace
- Containerization: Docker/Podman for non-RT nodes
- Watchdog: hardware (WDT) + software supervisor

## Observability
- Logging: ros2 bag; structured logs (JSON) with rotation
- Metrics: Prometheus node exporter; custom ROS 2 metrics topics
- Tracing: LTTng/ros2_tracing for timing analysis

## Security
- Secure boot where supported; signed images; least-privilege services
- Secrets: Vault/env files with rotation; SSH key-based access only

## Tests
- RT latency under load; camera throughput; DDS discovery in mesh; thermal throttling

## Versioning
- v0.2 detailed spec
