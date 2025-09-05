# Networking and Time Sync Spec

## Radios and links
- Primary: Wi‑Fi 6 (5 GHz, 80 MHz) for high-throughput; backup: 2.4 GHz
- Optional: UWB for ranging indoors; LTE/5G backhaul for ops
- Mesh: 802.11s or batman-adv for ad-hoc in field tests

## Channel plan
- Assign non-overlapping channels per area; detect interference and auto-shift
- Tx power management to limit interference and save power

## QoS
- Control topics: reliable, low latency; depth=5
- Telemetry: best effort; depth=50
- Video/vision: best effort; adaptive bitrate

## Time sync
- PTP (gPTP) via boundary clock on a master node; fall back to Chrony NTP
- Drift monitoring; alarms if > 1 ms offset

## Failover
- Link health (RSSI, PER) triggers switch to backup SSID or 2.4 GHz
- Degraded mode reduces video/telemetry rates; keeps control reliable

## Security
- WPA3/Enterprise where possible; per-node certs; rotating keys

## Versioning
- v0.2 detailed spec
