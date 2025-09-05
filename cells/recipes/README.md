# Process Recipes for Recyclofacturing

Detailed process parameters, quality control thresholds, and optimization guidelines for converting sorted waste streams into products via mobile cells.

---

## Metal Processes

### Wire Arc Additive Manufacturing (WAAM)

#### Steel (Low Carbon, Recycled Wire)
```yaml
material: ER70S-6_recycled
wire_diameter: 1.2mm
process_params:
  current: 180-220A
  voltage: 24-28V
  wire_feed_speed: 8-12 m/min
  travel_speed: 6-10 mm/s
  standoff: 15-20mm
  shielding_gas: 75%Ar/25%CO2 @ 15-20 L/min
thermal_management:
  inter_pass_temp: <150°C
  max_layer_temp: 800°C
  cooling_time: 2-5 min between layers
quality_targets:
  layer_height: 2.5-3.5mm
  bead_width: 8-12mm
  porosity: <2%
  hardness: 150-200 HV
energy_consumption: 3.2-4.1 kWh/kg
```

#### Aluminum (6061 Equivalent from Sorted Cans)
```yaml
material: ER4043_recycled
wire_diameter: 1.2mm
process_params:
  current: 120-160A
  voltage: 20-24V
  wire_feed_speed: 10-15 m/min
  travel_speed: 8-12 mm/s
  standoff: 12-18mm
  shielding_gas: 100%Ar @ 20-25 L/min
thermal_management:
  preheat_temp: 100-150°C
  inter_pass_temp: <200°C
  post_weld_cooling: forced air
quality_targets:
  tensile_strength: >200 MPa
  porosity: <1%
  oxide_inclusion: <0.5%
contamination_tolerance:
  paint_residue: <0.1% by weight
  oil_contamination: <50 ppm
energy_consumption: 4.8-6.2 kWh/kg
```

### Conventional Welding

#### MIG Welding Schedule (Structural Joints)
```yaml
joint_types:
  fillet_3mm:
    current: 90-120A
    voltage: 18-22V
    travel_speed: 4-6 mm/s
    prep: grind to bare metal
    pass_sequence: single_pass
  butt_6mm:
    root_pass: {current: 80A, voltage: 19V, speed: 3mm/s}
    fill_passes: {current: 140A, voltage: 24V, speed: 5mm/s}
    cap_pass: {current: 120A, voltage: 22V, speed: 4mm/s}
quality_requirements:
  penetration: 80% minimum
  undercut: <0.5mm
  spatter: minimal
  visual: smooth, uniform bead
ndt_requirements:
  structural: ultrasonic @ 100% coverage
  non_critical: visual + dye penetrant @ 10% sample
```

---

## Polymer Processes

### Large Format FFF (Recycled HDPE)

#### Standard Profile (Pallets, Enclosures)
```yaml
material: rHDPE_clean
contamination_limits:
  moisture: <0.02%
  paper_labels: <0.5%
  adhesive_residue: <0.1%
print_settings:
  nozzle_temp: 210-230°C
  bed_temp: 80-100°C
  chamber_temp: 40-60°C
  layer_height: 0.4-0.8mm
  print_speed: 30-50 mm/s
  infill: 20-40% (application dependent)
post_processing:
  annealing: 120°C for 2h (stress relief)
  surface_finish: sanding if required
quality_targets:
  layer_adhesion: >80% of virgin strength
  dimensional_accuracy: ±0.5mm
  surface_roughness: Ra <50μm
energy_consumption: 2.1-2.8 kWh/kg
```

#### High Performance (Structural Components)
```yaml
material: rHDPE_reinforced
additives:
  glass_fiber: 10-20% by weight
  compatibilizer: 2-5% maleated PE
  uv_stabilizer: 0.5% hindered amine
process_modifications:
  nozzle_temp: 220-240°C
  print_speed: 20-35 mm/s (reduced for fiber)
  nozzle_wear: monitor hourly, replace at 500kg
mechanical_properties:
  tensile_strength: >25 MPa
  flexural_modulus: >1200 MPa
  impact_strength: >15 kJ/m²
```

### Pellet Extrusion (Sheet and Profile)

#### Sheet Production (2-10mm thickness)
```yaml
extruder_config:
  screw_speed: 40-80 rpm
  barrel_temps: [180, 200, 220, 230]°C
  die_temp: 225°C
  line_speed: 2-8 m/min
cooling:
  chill_roll_temp: 25-40°C
  air_knife: 15-25 m/s
quality_control:
  thickness_tolerance: ±5%
  gauge_variation: <2%
  optical_clarity: >85% (clear grades)
contamination_response:
  black_specks: stop, purge, restart
  gels: reduce temp 10°C, increase screw speed
```

---

## Quality Control Gates

### Dimensional Metrology

#### 3D Scanning Protocol
```yaml
equipment: structured_light_scanner
accuracy: ±0.05mm
coverage: >95% of critical surfaces
frequency:
  setup_parts: 100% inspection
  production: statistical sampling (n=5 per 100)
acceptance_criteria:
  critical_dimensions: ±0.2mm
  general_dimensions: ±0.5mm
  surface_finish: Ra <25μm
data_storage: point_cloud + deviation_map
```

#### Mechanical Testing

##### Tensile Testing (Welded Joints)
```yaml
standard: AWS_D1.1_modified
specimen_prep: machine to standard coupon
test_conditions:
  crosshead_speed: 2mm/min
  temperature: 20±2°C
  humidity: 50±10% RH
acceptance_criteria:
  yield_strength: >80% base metal
  ultimate_strength: >90% base metal
  elongation: >15%
  failure_location: base_metal_preferred
sample_size: n=3 per joint type per shift
```

##### Impact Testing (Polymer Parts)
```yaml
standard: ASTM_D256
specimen: 12.7mm thick, notched
test_temp: 23°C and -40°C
acceptance_criteria:
  room_temp: >12 kJ/m²
  cold_temp: >8 kJ/m²
frequency: daily validation batch
```

### Non-Destructive Testing

#### Ultrasonic (Critical Welds)
```yaml
method: pulse_echo
frequency: 2-5 MHz
probe_angle: 45° and 70°
calibration: IIW reference blocks
scan_coverage: 100% weld length
acceptance: AWS_D1.1 Class_B
documentation: digital archive + plots
```

#### Thermal Imaging (Process Monitoring)
```yaml
camera_spec: FLIR_A655sc or equivalent
temperature_range: 0-1200°C
accuracy: ±2°C or 2%
monitoring:
  waam_melt_pool: continuous
  weld_cooling_rate: record
  polymer_nozzle_temp: real-time
alerts:
  over_temp: immediate stop
  under_temp: process deviation flag
```

---

## Process Optimization

### Energy Efficiency Targets
```yaml
waam_steel: 3.5 kWh/kg (target)
waam_aluminum: 5.2 kWh/kg (target)
polymer_extrusion: 2.4 kWh/kg (target)
total_cell_efficiency: >75% (process energy / total energy)
```

### Contamination Management

#### Pre-Process Cleaning
```yaml
metal_preparation:
  degreasing: alkaline_wash + rinse
  paint_removal: abrasive_blast (80-120 grit)
  oxide_removal: wire_brush + solvent_wipe
polymer_preparation:
  wash_temp: 60-80°C
  detergent: biodegradable_surfactant
  rinse_cycles: 3x clean_water
  drying: hot_air @ 80°C, <0.1% moisture
```

#### In-Process Monitoring
```yaml
spectroscopic_analysis:
  frequency: every_10kg_processed
  elements: C, Si, Mn, P, S (steel)
  action_limits: AWS_A5.18_Grade_ER70S-6
optical_sorting_feedback:
  purity_target: >98%
  false_positive_rate: <2%
  throughput: maintain_>500kg/h
```

---

## Failure Modes and Recovery

### Common Issues and Solutions

#### WAAM Defects
```yaml
porosity:
  causes: [contamination, incorrect_gas_flow, moisture]
  detection: ultrasonic_inspection
  mitigation: increase_cleaning, verify_gas_purity
  rework: grind_out + reweld
lack_of_fusion:
  causes: [low_heat_input, fast_travel, poor_prep]
  detection: visual + UT
  mitigation: increase_current, reduce_speed
  rework: complete_joint_removal
```

#### Polymer Processing Issues
```yaml
layer_delamination:
  causes: [low_temp, contamination, moisture]
  detection: visual + peel_test
  mitigation: increase_nozzle_temp, improve_drying
  rework: reprocess_material
dimensional_drift:
  causes: [thermal_expansion, warping, bed_adhesion]
  detection: continuous_measurement
  mitigation: chamber_temp_control, better_fixturing
  rework: machine_to_tolerance
```

### Statistical Process Control

#### Control Charts (X-bar and R)
```yaml
parameters_monitored:
  - weld_penetration_depth
  - layer_height_polymer
  - dimensional_accuracy
  - energy_consumption_per_kg
sample_size: n=5
frequency: hourly
control_limits: ±3σ from process_mean
action_rules:
  single_point_beyond_limits: stop_investigate
  seven_consecutive_same_side: adjust_process
  trending: predictive_maintenance_alert
```

---

## Versioning and Updates

- v0.3 detailed recipes with statistical validation
- Next: adaptive parameter optimization based on feedstock analysis
- Future: ML-driven process optimization and quality prediction
