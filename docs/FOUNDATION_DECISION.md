# FOUNDATION DECISION

## Candidates considered

1. QuantConnect LEAN
2. NautilusTrader
3. FinRL / FinRL-X

## Evidence reviewed

Reviewed live upstream state on 2026-10-06 by checking the public repositories and their structure, current branch metadata, and project-level documentation.

Key evidence points:
- LEAN is structured around local backtesting, research, optimization, and execution workflows.
- NautilusTrader is highly mature as a Rust-native event-driven engine with Python strategy-control layers.
- FinRL is clearly framed as a research and RL ecosystem rather than a direct engine foundation for a competition-specific, rules-constrained trading system.

## Winner: QuantConnect LEAN

LEAN is selected as the starting foundation because it gives the best balance of:
- mature event-driven architecture
- local backtesting ergonomics
- portfolio and order simulation maturity
- reproducibility inside a modest Codespace
- lower installation friction than Rust-native alternatives
- enough extensibility to attach a Pipster-specific digital twin, leakage controls, and local AI event intelligence

## Runner-up: NautilusTrader

NautilusTrader is a very strong second-place candidate.

It wins on:
- event-driven runtime quality
- deterministic simulation qualities
- time and order model maturity
- execution architecture depth

It loses this round because:
- the Rust toolchain is heavier for this environment
- it requires a more complex installation story in a limited Codespace
- it offers less immediate ease-of-use for rapid research iteration in constrained compute

## What is inherited from the foundation

From LEAN we inherit:
- event-driven research patterns
- local backtesting discipline
- order and portfolio concepts
- strategy research workflow
- risk and execution abstractions
- broad research tooling culture

## What is removed or replaced

We remove or replace:
- generic market assumptions not aligned to Pipster rules
- any backtest assumptions that violate the competition’s explicit constraints
- all generic “AI trading” assumptions that bypass quant risk
- naive model training pipelines that ignore temporal leakage

## What will be added

We add:
- Pipster rule provenance and rule-contract validation
- explicit timezone/trading-day semantics
- data quality gates and leakage controls
- local AI structured event ingestion
- competition digital-twin simulation
- strategy domination and red-team testing
- a champion/challenger framework with adversarial attack mode

## Final assessment

This repository is not a naive LEAN clone. It is a Pipster-specialized quantitative research and execution system built on top of the strongest practical foundation under the current environment constraints.
