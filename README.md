# QUANT-1

A Pipster-focused quantitative research and execution foundation built around a conservative, evidence-backed design. The repository is deliberately structured to model event-driven market logic, AI-informed signal ingestion, and risk-aware strategy validation without inventing contest-specific numbers that are not officially published.

## What is in the project

- Time and session handling for UTC-normalized market windows
- Data quality validation for bids, asks, spreads, and duplicate timestamps
- AI event schema validation for market-impact signals and text-based event ingestion
- Risk engine guardrails for drawdown, exposure, and position caps
- Explicit Pipster rules provenance with a conservative default config
- Local AI smoke-test helper for CPU-only environments

## Repository layout

- `src/pipster_quant/` — quant and AI core modules
- `tests/` — regression tests for contracts and rules
- `config/` — contest configuration and provenance metadata
- `docs/` — foundation comparisons and decision records
- `scripts/` — local environment setup helpers

## Validation

Run the project tests with:

```bash
cd /workspaces/QUANT-1
python3 -m pytest -q
```

## Notes on the foundation

The project intentionally favors the most mature, reproducible foundation under the current environment constraints. In practice, this means leaning toward event-driven backtesting practices and research discipline inspired by QuantConnect LEAN, while keeping the Pipster contest rules explicit and conservative rather than assuming unsupported parameters.
