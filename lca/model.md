# LCA Model

## Boundary
- Site-internal operations; avoided virgin extraction; avoided transport; end-of-life of products

## Factors (to be parameterized)
- Energy mix gCO2e/kWh; welding and printing process intensities
- Transport emissions for avoided materials; landfill methane credits if applicable

## Calculators (sketch)
- kWh/kg_processed = (E_drones + E_cells + E_balance) / mass_out
- CO2e/kg = kWh/kg * grid_factor − credits_avoided

## Reporting
- Monthly and per-project reports; confidence intervals from measurement variance

## Versioning
- v0.2 detailed spec
