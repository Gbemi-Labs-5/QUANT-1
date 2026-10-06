# Foundation Decision

This repository adopts a lightweight, evidence-first architecture designed for a constrained Codespace and a competition-style workflow.

## Adopted pattern

The system borrows the strengths of mature research frameworks without importing their full complexity:

- event-driven research patterns
- deterministic, time-aware data handling
- strategy and regime separation
- explicit risk checks
- synthetic-data validation clearly labeled as such
- walk-forward evaluation emphasis
- reproducible reports and CLI workflows

## Rejected patterns

The following are intentionally excluded or minimized:

- unbounded AI trading decisions inside the production loop
- naive random train/test splitting on time series
- future-looking execution based on non-timestamped data
- fake backtests labeled as live or competition results
- large GPU-dependent model stacks that do not fit the environment

## Practical outcome

The current system is intentionally compact enough to operate reliably in the current environment while still being serious enough to support research-grade signal generation, event-driven execution checks, and synthetic strategy evaluation.

It is not a complete live trading platform, and it is not pretending to be one.
