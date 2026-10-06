# QUANT-1

QUANT-1 is a CPU-friendly quantitative research and backtesting foundation for the Pipster Halloween 2026 contest. It is designed to be scientifically defensible, time-aware, and reproducible without pretending to be a live trading platform or a profitable strategy engine.

This repository is deliberately honest about the current maturity level. It contains a real research pipeline for synthetic market data and a structured foundation for further extension with competition-grade data and rules.

## What is implemented

- data validation and synthetic market-data generation
- technical feature engineering for trend, momentum, volatility, mean-reversion, and breakout logic
- regime detection for market states such as trend, range, high-volatility, and transition
- multiple strategy families with deterministic signal output
- event-driven execution simulation with market orders and anti-duplicate protection
- a lightweight ML direction model using classical statistical learning
- a reproducible research CLI that saves machine-readable and Markdown outputs
- explicit audit and provenance documentation for the project’s design decisions

## Architecture

The implemented stack is intentionally small but realistic:

- Data provider and validation layer
- Feature engineering layer
- Strategy families and regime detection
- Ensemble and ML signal filtering
- Event-driven execution simulation
- Walk-forward-style research evaluation and reporting

This is not a giant framework; it is a lean but serious research stack built to operate in this Codespace.

## Repository layout

- `src/pipster_quant/` — core quant engine and research modules
- `tests/` — contract and regression tests
- `config/` — contest configuration and provenance metadata
- `docs/` — architecture audit, foundation comparison, and decisions
- `scripts/` — local environment tooling
- `artifacts/research/` — generated experiment outputs

## Installation

```bash
cd /workspaces/QUANT-1
python3 -m pip install -e .
```

## Data format

The synthetic provider produces a market-data frame with the following columns:

- `timestamp`
- `symbol`
- `open`
- `high`
- `low`
- `close`
- `volume`
- `bid`
- `ask`

The project expects time-ordered data and rejects invalid rows with zero or negative spread inconsistencies.

## Commands

Run the validation check:

```bash
cd /workspaces/QUANT-1
python3 -m pipster_quant.cli validate-data
```

Run a synthetic backtest across strategies:

```bash
cd /workspaces/QUANT-1
python3 -m pipster_quant.cli backtest
```

Run the research pipeline and save reports:

```bash
cd /workspaces/QUANT-1
python3 -m pipster_quant.cli research
```

## Research workflow

The current research flow is:

1. generate synthetic or structured market data
2. validate ordering and data quality
3. build feature frames
4. detect regime states
5. evaluate multiple strategy families
6. produce a ranking and report

This is a practical, time-aware research workflow rather than a fake live-pipeline promise.

## Strategy system

The project currently includes multiple strategy families:

- trend following
- momentum
- mean reversion
- breakout
- ensemble weighting

Each strategy emits a deterministic signal with a direction, confidence, expected edge, stop distance, and take-profit distance.

## ML / statistical model

The project includes a lightweight classical ML layer using a logistic-regression direction model fitted on time-aware features. This model is intentionally kept outside the live-trading loop and used as a research aid rather than as a black-box trading decision system.

## Risk and Pipster semantics

The system preserves a conservative rules-first posture:

- explicit contest rules metadata remains separate from strategy logic
- execution happens in a time-aware, deterministic pathway
- future data cannot be used to justify earlier fills in the event engine
- synthetic results are clearly labeled as synthetic rather than live or competition results

## Reproducibility

The project is designed for reproducible research:

- deterministic synthetic generators with configurable seeds
- test coverage for the core data-to-signal-to-execution path
- saved JSON and Markdown reports under `artifacts/research/`

## Limitations

This project is not a complete live competition engine and should not be presented as one. It is a serious foundation for future extension, but the current data and execution environment remain synthetic and research-oriented unless real Pipster market data and official rule parameters are provided.

## Validation

Run the test suite with:

```bash
cd /workspaces/QUANT-1
python3 -m pytest -q
```

## Current status

The repository now contains a functioning end-to-end research pipeline covering data validation, feature creation, regime detection, multiple strategies, execution simulation, and reproducible reporting. The remaining work is primarily domain expansion and competition-specific calibration when more authoritative Pipster data and rules become available.
