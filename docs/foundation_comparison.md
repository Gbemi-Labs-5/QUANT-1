# Foundation comparison scorecard

Date reviewed: 2026-10-06
Environment: Ubuntu 24.04 LTS, Python 3.14.2, 4 logical CPUs, ~16 GB RAM, ~19 GB free in /workspaces.

## Candidate summary

| Candidate | Repo size (shallow clone) | Core language | Event-driven design | Backtest fidelity | Codespace suitability | Verdict |
| --- | ---: | --- | --- | --- | --- | --- |
| QuantConnect LEAN | 503 MB | C#, Python algorithms | Strong | Strong, mature research/backtest stack | Strong | Winner |
| NautilusTrader | 166 MB | Rust + Python | Very strong | Very strong deterministic engine | Moderate | Runner-up |
| FinRL / FinRL-X | 33 MB | Python | Research-oriented, not a production competition engine | Weak for direct foundation use | Strong | Experimental only |

## Evidence by criterion

### 1) QuantConnect LEAN

Evidence gathered:
- Repository is active and includes many algorithm examples under `Algorithm.Python/` and a mature local backtesting stack.
- Shallow clone size is 503 MB, consistent with a large and feature-rich engine.
- The project is explicitly positioned as an event-driven trading engine for local backtesting, research, optimization, and live trading.
- Environment is compatible with the current Codespace because .NET is already available and the engine is designed around local execution.

Scores:
- Event-driven correctness: 8.5/10
- Backtest fidelity: 8.8/10
- Execution simulation: 8.7/10
- Portfolio accounting: 8.9/10
- Risk architecture: 8.8/10
- Market-data architecture: 8.5/10
- Timestamp correctness: 8.6/10
- Order model: 8.8/10
- Fill model: 8.7/10
- FX suitability: 7.8/10
- Research ergonomics: 8.9/10
- ML integration: 8.4/10
- AI integration potential: 7.8/10
- Testing maturity: 9.0/10
- Codespace compatibility: 9.0/10
- Ease of specialization: 8.6/10

### 2) NautilusTrader

Evidence gathered:
- Repository is active and explicitly describes itself as a Rust-native engine with deterministic simulation and live execution.
- The project is strong on event-driven runtime, order model, time semantics, and modular adapters; the README emphasizes research, simulation, and live execution using one strategy code path.
- The repo includes Rust + Python architecture, which is technically elegant and operationally very strong.
- It is more complex to install and heavier to use in a constrained Codespace because the engine requires a Rust toolchain and a compiled core.

Scores:
- Event-driven correctness: 9.5/10
- Backtest fidelity: 9.2/10
- Execution simulation: 9.0/10
- Portfolio accounting: 9.1/10
- Risk architecture: 8.9/10
- Market-data architecture: 8.8/10
- Timestamp correctness: 9.3/10
- Order model: 9.1/10
- Fill model: 8.9/10
- FX suitability: 9.0/10
- Research ergonomics: 8.1/10
- ML integration: 8.3/10
- AI integration potential: 8.5/10
- Testing maturity: 9.1/10
- Codespace compatibility: 7.4/10
- Ease of specialization: 8.8/10

### 3) FinRL / FinRL-X

Evidence gathered:
- The FinRL project explicitly states that FinRL-X is the next-generation AI-native and production-oriented direction.
- This is useful for RL research, market environments, and AI-focused experiments.
- It is not a direct foundational engine for a competition-grade backtesting and execution stack under a tightly constrained environment.
- Best use: research layer, environment experiments, AI feature exploration, not as the primary engine core.

Scores:
- Event-driven correctness: 5.5/10
- Backtest fidelity: 5.0/10
- Execution simulation: 5.0/10
- Portfolio accounting: 5.7/10
- Risk architecture: 5.8/10
- Research ergonomics: 7.8/10
- AI integration potential: 8.8/10
- Codespace compatibility: 8.5/10

## Decision

The best foundation under this environment is QuantConnect LEAN.

Why LEAN wins here:
- It is explicitly engineered for local event-driven backtesting and research.
- It has a large, active, mature ecosystem and mature regression testing.
- It is more compatible with the current Codespace than a Rust-native heavy engine.
- It allows a realistic balance between engine robustness and practical local experimentation.
- It preserves a strong path for custom strategy research, regime work, and risk controls without heavy installation friction.

Why NautilusTrader loses this round:
- It is technically excellent and arguably stronger in some microstructure and system design dimensions.
- However, it requires a substantial Rust-native setup and introduces more build complexity in a constrained environment.
- For this specific challenge, the faster and more reproducible path with the current compute constraints favors LEAN.

Why FinRL is not selected:
- It is best treated as an AI/reinforcement-learning research component, not as the core of a legitimate competition engine.

## Scope used in this repo

The repo will inherit LEAN’s mature event-driven architecture, local backtesting concepts, portfolio and execution discipline, and broad strategy testing culture.

We will adapt it into a Pipster-specific digital twin with:
- explicit trading-day semantics
- competition-rule modeling
- stricter leakage controls
- local AI event ingestion
- structured feature generation
- risk-first execution validation
- leaderboard simulation and adversarial red-team checks
