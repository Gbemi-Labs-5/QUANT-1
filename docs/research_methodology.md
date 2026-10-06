# Research methodology

## Goal

The goal of QUANT-1 is not to claim a winning strategy. The goal is to build a strong, evidence-based research system that can support strategy development under a realistic competition-aware framework.

## Decision rules

A strategy is considered promising only if it survives the following path:

1. it is valid under real or synthetically generated data checks
2. it is free from future leakage in feature and execution logic
3. it works under a train-validation-test split
4. it survives a walk-forward period
5. it shows acceptable robustness under parameter perturbation and cost assumptions
6. it does not materially violate Pipster rule assumptions or create impossible exposure
7. it is documented with explicit caveats about the data or rule limitations

## Leakage rules

The following are forbidden:

- using future bars to calculate indicators used on a historical decision
- using test-period information to select features or model parameters
- using future regime state when deciding on a historical trade
- executing a decision using a price that would not have been available at the timestamp of the decision
- allowing generated future labels to influence model training on the same sample window

## Feature validity

Every feature must satisfy all of the following:

- it is computable from available data at the relevant timestamp
- it has a documented warmup period if needed
- it does not require future values
- it has a sensible interpretation for the strategy family
- its effect is testable under walk-forward evaluation

## Strategy validity

The implementation distinguishes between strategy families and uses a common signal format. A strategy passes to the next stage only if it demonstrates out-of-sample stability, not just in-sample performance.

## Research workflow

The repository uses a simple but disciplined flow:

- data loading and validation
- feature generation
- strategy signal generation
- regime assessment
- optional ML filtering
- risk and exposure checks
- walk-forward evaluation
- report generation

## Reporting rules

The system must separate:

- in-sample
- validation
- out-of-sample
- synthetic
- real-data

No numerical performance claim is considered valid unless the dataset and evaluation split are stated explicitly.

## When a strategy fails

A failed strategy is not a negative outcome. It is an important evidence point. The repo records failed experiments and, when appropriate, keeps the edge conditions or the failure mode in the results documentation.

## Current limitation

At present, the main evidence base is still partly synthetic. The project is intentionally moving toward real historical data support, but the larger objective is to remain scientifically honest and not to claim a winning strategy prematurely.
