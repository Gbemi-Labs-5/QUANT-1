# Phase 3 gap audit

Date: 2026-10-06
Repository SHA: b67e61e4dd234664400b830480182ee986727849

## 1. What is genuinely implemented

The repository currently contains the following materialized components:

- a synthetic data generator and a CSV-based provider abstraction in `src/pipster_quant/data_pipeline.py`
- a basic feature engine with trend, momentum, volatility, mean-reversion, and breakout features in `src/pipster_quant/features.py`
- a regime detector in `src/pipster_quant/regime.py`
- several strategy families in `src/pipster_quant/strategies.py`
- a simple event-driven execution layer in `src/pipster_quant/execution.py`
- a logging-level risk guardrail in `src/pipster_quant/risk.py`
- a basic ML direction model in `src/pipster_quant/ml.py`
- a research runner and artifact writer in `src/pipster_quant/research.py`
- CLI entry points in `src/pipster_quant/cli.py`
- a rule loader and YAML rule contract in `src/pipster_quant/config.py`
- contract tests in `tests/test_phase2_engine.py` and earlier tests

## 2. What is simplified

The following are materially simplified relative to a true competition-grade engine:

- the execution model does not model realistic latency, slippage curves, partial fills in detail, or full order lifecycle stages
- the risk engine is basic rather than a full portfolio-level rule engine
- the regime detector is heuristic and not validated against real market regimes
- the ML layer is lightweight and not a true walk-forward research pipeline
- the research runner is synthetic-data-centric and is not yet a serious historical-data evaluation stack
- the current rules contract is conservative and honest about unknowns, but it still lacks a complete official contest contract

## 3. What is synthetic-only

These parts remain synthetic-only unless real market data is explicitly loaded:

- the main strategy evaluation stack in `src/pipster_quant/research.py`
- the default backtesting path in the CLI
- the parameterized results in the generated research artifact
- the regime labels derived from synthetic generated time series
- the majority of the output metrics in the generated JSON report

## 4. What has no real data support

The project supports a CSV route and synthetic data generation, but it does not yet contain a full live or historical-market ingestion pipeline with production-quality source adapters, time-zone normalization, and official instrument metadata for Pipster-relevant markets.

This lacks:

- a complete real-data source abstraction with metadata and licensing documentation
- a dataset registry
- source-specific validation beyond CSV columns
- explicit support for bid/ask spreads from real exchange data
- real multi-instrument ingestion and normalization
- rule-specific historical data filters

## 5. What lacks out-of-sample validation

The current Phase 2 runner is still primarily evaluated on a single synthetic frame or a small set of synthetic scenarios.

There is no serious walk-forward validation across multiple non-overlapping periods and no test that prevents validation leakage from affecting strategy selection.

## 6. What lacks realistic execution

The execution layer is not enough for realistic simulation because it does not model:

- stop and limit orders end-to-end
- partial fills and queue priority
- commission and fee models by venue
- spread widening and slippage by volatility regime
- latency assumptions tied to order type and venue
- mark-to-market and unrealized P&L across positions
- portfolio-level turnover and exposure constraints

## 7. What lacks transaction-cost modeling

The current implementation does not model:

- commission or spread cost as a function of instrument and venue
- market impact
- slippage by order size and liquidity regime
- market-open/market-close execution cost changes
- partial-fill costs and queue delay

## 8. What lacks portfolio-level risk

The existing risk model is a narrow exposure guardrail. It does not yet quantify:

- gross and net exposure over the full portfolio
- concentration per symbol
- turnover and transaction cost burden
- daily and cumulative drawdown history
- rule violation accounting over a full run
- position sizing by volatility or regime

## 9. What lacks Pipster-specific optimization

The repository has a conservative rules scaffold, but it does not yet take the actual competitive objective seriously enough. Specifically missing:

- measurable competition score model
- probability-of-rule-violation scoring
- leaderboard-oriented optimization objective
- regime-adjusted sizing under contest constraints
- daily contribution cap analysis
- explicit trade rejection before execution when rule thresholds would be violated

## 10. Hidden TODOs or placeholders

The repo still contains logic that is a placeholder in spirit, even when it is run successfully:

- rule values remain mostly `UNVERIFIED` or conservative placeholders
- real Pipster contest values are not loaded from a public official machine-readable rules file
- real historical data is not yet integrated into the main evaluation path
- modern portfolio and execution realism remain future work
- strategy family output is valid but not yet competition-grade

## 11. Tests that are too trivial

The current tests validate basic contracts and some synthetic behavior, but they do not yet cover:

- future leakage behavior
- time-split validation leakage
- rule violation logic pre-trade
- multi-instrument portfolio constraints
- walk-forward strategy selection contamination
- parameter perturbation robustness
- drawdown invariants across a full run
- leaderboard scoring under competition constraints

## 12. Documentation claims that exceed actual evidence

The Phase 2 documentation was intentionally more positive than the code quality justified. The repository is now more honest, but the following claims still require caution:

- no claim that a strategy is competition-ready
- no claim that a strategy is profitable without out-of-sample evidence
- no claim that the engine is a production competition engine
- no claim that all rules are official or final unless publicly verified and recorded

## Phase 3 priority order

1. convert the rules contract into an honest, official-source-aware system
2. add real-data provider support and validation reporting
3. improve the execution engine with realistic cost/slippage checks and order lifecycle modeling
4. build true walk-forward and optimization logic
5. add competition-aware risk modeling with pre-trade rejection
6. improve the leaderboard and experiment reproducibility
7. keep synthetic data for unit tests and controlled experiments, but stop using it as the main evidence base

## Bottom line

The repository has advanced from a contract scaffold to a legitimate research prototype, but it is not yet a real competition-grade engine. The Phase 3 objective is to replace the remaining shallow assumptions with evidence-backed machinery and explicit real-data support.
