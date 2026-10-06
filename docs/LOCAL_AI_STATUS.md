# Local AI status

This project does not require an LLM in the live trading decision loop.

The earlier Qwen/local-AI experiments are not used as production trading logic. They are treated as a separate research convenience only.

## Current position

- local AI is not required for the strategy engine
- local AI is not part of the deterministic risk engine
- live execution decisions remain a function of deterministic rule checks, strategy logic, and risk constraints
- any future local model must be used only as a research aid or a structured signal filter, never as the sole source of action

## Reasoning

The environment is CPU-only and resource constrained. Large models are not necessary to build a disciplined quantitative framework. The project prioritizes transparent statistical and event-driven logic over black-box LLM actioning.

## Practical status

The repo treats local AI as optional and non-critical. The live decision loop remains deterministic and explainable.
