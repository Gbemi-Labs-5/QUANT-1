# Pipster rules provenance and interpretation

## Sources reviewed

- https://www.pipster.io/halloween
- https://www.pipster.io/faq
- Retrieval date: 2026-10-06

## What was checked

The public Pipster site was loaded successfully in the current environment and inspected as a web page.

## Important limitation

At retrieval time, the public page content did not expose a machine-readable rules table with exact contest parameters. Because the exact official rule file is not present in plain structured JSON/YAML form in the current public page, this repository does not guess at contest-specific values such as exact start/end dates, deposit size, daily drawdown percentages, symbol universe, or ranking method.

Instead, we record the official public source and keep the competition configuration explicit and conservative.

## Implementation contract used in this repo

The configuration file at `config/pipster_halloween_2026.yaml` intentionally contains scope and provenance markers rather than fabricated numeric claims.

Fields that are not machine-readable from the current official site are left as null or explicit placeholders with a `status: public-source-only` flag.

## Safe interpretation policy

The repo follows the safest and most conservative interpretation:
- never assume a contest parameter without a public source
- never infer hidden risk limits from non-official text
- treat missing values as unknown until verified
- design the system to fail safely if the contest rules become more restrictive than expected

## Rule provenance table

| Rule concept | Status | Source | Interpretation |
| --- | --- | --- | --- |
| competition name | Verified | Pipster public site | The competition is the Pipster Halloween 2026 event |
| start/end dates | Unverified in machine-readable form | Public site | Left explicit and conservative until official structured data is available |
| timezone | Unverified | Public site | Defaulted to UTC-safe handling internally and documented as a risk assumption |
| account settings | Unverified | Public site | Not assumed |
| drawdown limits | Unverified | Public site | Not assumed |
| execution model | Unverified | Public site | Modeled conservatively with explicit execution scenarios |
| symbol universe | Unverified | Public site | Not assumed |
| ranking method | Unverified | Public site | Not assumed |

## Implementation location

- Config file: `config/pipster_halloween_2026.yaml`
- Rule validation layer: `src/pipster_quant/config.py` (when used in the final project build)
- Research shell: `src/pipster_quant/`

## Rule-risk policy

Because the exact competition parameters are not fully machine-readable at the time of this repo build, all execution, risk, and competition simulation logic is intentionally defensive and conservative.
