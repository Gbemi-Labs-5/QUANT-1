# Upstream provenance

This repository is built on top of a selected upstream foundation and intentionally documents provenance and scope.

## Foundation selected

- Repository: QuantConnect/Lean
- URL: https://github.com/QuantConnect/Lean
- Commit selected: 58dd54065a7b582f197ec373ae23cf4da647270f
- Commit date: 2026-10-06 13:50:36 -0300
- License: See upstream repository license file
- Selected on: 2026-10-06

## Runner-up reviewed

- Repository: NautilusTrader
- URL: https://github.com/nautechsystems/nautilus_trader
- Commit reviewed: 4f021bafc2e99c5490cee204b0fc2bd2c83baab4
- Commit date: 2026-10-06 16:24:52 +0800
- License: See upstream repository license file

## Experimental AI research stack reviewed

- Repository: AI4Finance-Foundation/FinRL
- URL: https://github.com/AI4Finance-Foundation/FinRL
- Commit reviewed: e60e26e4870f00fbc704c6297edfd9d81816b3d3
- Commit date: 2026-09-28 11:59:35 +0800
- Positioning: RL research and educational research framework, not the direct engine foundation

## Modifications made in this repo

- Reduced the architecture to a Pipster-specific digital twin and risk-first research shell
- Added explicit timestamp controls
- Added data quality gates
- Added a structured AI event schema
- Added competition-rules configuration and provenance docs
- Added a reusable local AI installation script
- Added regression tests for data quality, risk logic, and time semantics

## License handling

This repository preserves upstream attribution and does not copy third-party code directly. Any future upstream integration should preserve the upstream repository license requirements and attribution obligations.
