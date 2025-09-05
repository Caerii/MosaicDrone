# SQP Allocator Spec

## Purpose
Compute motor throttles and arm angles to realize desired wrench with objectives and constraints.

## Inputs / Outputs
- Inputs: orientation quaternion q; desired force F [N]; desired torque M [Nm]; previous a,u
- Outputs: arm angles a_i [rad]; motor throttles u_i [0..1]; diagnostic λ, residuals

## Objectives O(a,u)
- Effort: Σ w_u u_i^2
- Arm velocity penalty: Σ w_adot ((a_i − a_i_prev)/Δt)^2
- Smoothness: Σ w_Δu (u_i − u_i_prev)^2 (optional)
- Docking safety: w_dock Σ penalty near latch proximity

## Constraints G(a,u)=0
- Wrench match: Σ f_i(a,u) = q^{-1} F; Σ m_i(a,u) = q^{-1} M
- Bounds: 0 ≤ u_i ≤ 1; |(a_i − a_i_prev)/Δt| ≤ ω_max
- Actuator geometry: n_i = R(x_i, a_i) z_i; thrust f_i = μ u_i n_i; torque m_i = μ u_i (r_i × n_i) + τ s_i u_i n_i
- Aggregate updates: r_i,x_i,z_i,s_i extend when docked; loads add constraints

## Algorithm
- Newton step on KKT: H δ = −K; partial pivot LU; step scale α s.t. max Δa, Δu within limits
- Termination: |ΔO|/O < ε and ||G|| < ε; 1–8 iters target, < 3 ms on target CPU

## Parameters
- ω_max: 1 rev/s baseline; Δu_max per step; weights tuned from flight data
- Safety margins near singularities (vertical n_i) via increased w_adot

## Diagnostics
- Residual wrench; iteration count; step scales; constraint activity; per-actuator utilization

## Tests
- Singularity crossings; fast reorientation; hover in arbitrary attitude
- Docking transitions: mixer changes; solution continuity; stability margins
- Load disturbances and wind

## Versioning
- v0.2 detailed spec
