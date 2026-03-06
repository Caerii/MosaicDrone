# MosaicDrone documentation

Technical specs, subsystem status, and design docs. **Start here** for anything beyond the [main README](../README.md).

---

## Start here

| Purpose | Link |
|--------|------|
| **Subsystem status and gaps** (have / missing / next) | [Subsystems index](subsystems/INDEX.md) |
| **Safety and operations** | [Safety case](safety/safety_case.md), [Ops](safety/ops.md) |

---

## Docs folder layout

```text
docs/
├── README.md           ← you are here
├── writing-specs.md    How to flesh out and improve specs
├── subsystems/        Status per subsystem (INDEX + docking, power, compute, …)
├── acoustics/          Noise, blades, ESC tuning
├── airframe/           Rotating arm, propulsion
├── compute/            Platform, networking, ROS 2, DDS, msgs
├── control/            SQP allocator, outer loops, dynamic allocation
├── data/               Schemas, retention
├── docking/            Mechanical/electrical/data interface
├── hri/                Operator station, interaction, privacy
├── perception/         Localization, docking perception, multi-modal
├── power/              Battery, bus, sharing
├── safety/             Safety case, ops, landfill operations
└── swarm/              Behaviors, scheduler, telemetry
```

---

## Specs by area

| Area | Specs |
|------|--------|
| **Docking** | [Interface](docking/interface.md) |
| **Airframe** | [Rotating arm](airframe/rotating_arm.md), [Propulsion](airframe/propulsion.md) |
| **Power** | [Battery module](power/battery_module.md), [Bus & sharing](power/bus_and_sharing.md) |
| **Compute / ROS 2** | [Platform](compute/platform.md), [Networking](compute/networking.md), [ROS 2 conventions](compute/ros2_conventions.md), [DDS QoS](compute/dds_qos_profiles.md), [Msgs](compute/ros2_msgs.md) |
| **Perception** | [Localization](perception/localization.md), [Docking](perception/docking.md), [Multi-modal](perception/multi_modal_architecture.md) |
| **Control** | [SQP allocator](control/sqp_allocator.md), [Outer loops](control/outer_loops.md), [Dynamic allocation](control/dynamic_allocation.md) |
| **Swarm** | [Behaviors](swarm/behaviors.md), [Scheduler](swarm/scheduler.md), [Telemetry](swarm/telemetry.md) |
| **Safety** | [Safety case](safety/safety_case.md), [Ops](safety/ops.md), [Landfill operations safety](safety/landfill_operations_safety_case.md) |
| **Acoustics** | [Noise package](acoustics/noise_package.md) |
| **HRI** | [Interaction](hri/interaction.md), [Operator station](hri/operator_station.md), [Privacy](hri/privacy.md) |
| **Data** | [Schemas](data/schemas.md), [Retention](data/retention.md) |

---

## Proposals and research

Long-form proposals and theses live at the repo root:

- [Recyclofacturing proposal](../Recyclofacturing-Proposal.md)
- [Landfill mining README](../README.landfill-mining.md)
- [Landfill mining thesis](../THESIS.landfill-mining.md)
- [Strategic upgrade roadmap](../STRATEGIC_UPGRADE_ROADMAP.md)

---

## Documentation elsewhere in the repo

| Topic | Location |
|-------|----------|
| **Simulation** | [simulations/README.md](../simulations/README.md) |
| **Manufacturing / CAD** | [hardware/CAD/README.md](../hardware/CAD/README.md) |
| **BOM and sourcing** | [hardware/BOM/README.md](../hardware/BOM/README.md) |
| **Process and QC** | [process/README.md](../process/README.md) |
| **Cells (toolheads, recipes)** | [cells/toolheads.md](../cells/toolheads.md), [cells/mobile_cells.md](../cells/mobile_cells.md), [cells/recipes/README.md](../cells/recipes/README.md) |
| **LCA** | [lca/model.md](../lca/model.md) |
| **Economics** | [economics/unit_model.md](../economics/unit_model.md) (and other files in `economics/`) |

---

## How to write specs

- **[Writing specs](writing-specs.md)** — Checklist and template for fleshing out specs (scope, requirements tables, thresholds, recovery, cross-links, tests, changelog). Example: [docking/interface.md](docking/interface.md).

---

## Contributing to docs

- Add or update specs in the appropriate `docs/` subfolder.
- Update [subsystems/INDEX.md](subsystems/INDEX.md) when closing gaps or adding new subsystems.
- Optionally add at the top of a spec: `↑ [Docs index](../README.md)` (or the path back to this README) so readers can jump to the index.
- For flight-critical or safety-related changes, coordinate in issues and reference [safety/safety_case.md](safety/safety_case.md) and [safety/ops.md](safety/ops.md).
