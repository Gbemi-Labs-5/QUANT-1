from __future__ import annotations

import argparse
import json
from pathlib import Path

from .data_pipeline import SyntheticMarketDataProvider, validate_market_frame
from .features import compute_feature_frame
from .research import run_research, save_report


def _validate_data_command() -> None:
    provider = SyntheticMarketDataProvider(symbols=["BTCUSD"], rows=80, seed=7)
    frame = provider.load()
    report = validate_market_frame(frame)
    print(json.dumps(report.__dict__, indent=2))


def _backtest_command() -> None:
    results = run_research()
    print(json.dumps(results["results"], indent=2))


def _research_command() -> None:
    results = run_research()
    output_dir = Path("artifacts/research")
    save_report(results, output_dir)
    print(json.dumps(results["results"], indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(description="QUANT-1 CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("validate-data", help="Validate a synthetic market-data frame")
    subparsers.add_parser("backtest", help="Run a synthetic backtest across candidate strategies")
    subparsers.add_parser("research", help="Run a research experiment and save reports")

    args = parser.parse_args()

    if args.command == "validate-data":
        _validate_data_command()
    elif args.command == "backtest":
        _backtest_command()
    elif args.command == "research":
        _research_command()
    else:
        parser.error(f"Unsupported command: {args.command}")


if __name__ == "__main__":
    main()
