# Pipster Halloween 2026 rules audit

Date retrieved: 2026-10-06
Sources inspected: official Pipster public pages, including the public site homepage and the public challenge/how-it-works schema embedded in the HTML.

## Important note

The official Pipster website exposes public product-level challenge rules as structured schema on the public challenge pages. At the time of retrieval, there was no clear, public, machine-readable page explicitly labeled `Pipster Halloween 2026` with the final contest-specific rules for that event. Because of that, the repository records values as either:

- `VERIFIED` when the public site provides a specific value for a public challenge product, or
- `UNVERIFIED` when no public contest-specific value was found for the Halloween 2026 event.

This should be treated as an audit trail, not a guess.

## Official public values observed

The public HTML schema includes these challenge rule examples:

### One Phase Challenge
- profit target: 10%
- daily drawdown: 4%
- max drawdown: 8% (static)
- minimum trading days: 5
- time limit: UNVERIFIED in the schema snippet, but not explicitly shown as a fixed restriction
- source: official `https://www.pipster.io/how-it-works` public schema
- retrieval date: 2026-10-06
- enforcement in QUANT-1: recorded as a verified example case under `verified_rules.challenge_examples`

### Two Phase Challenge
- phase 1 target: 8%
- phase 1 daily drawdown: 5%
- phase 1 max drawdown: 10% (static)
- phase 1 minimum trading days: 5
- phase 2 target: 5%
- phase 2 daily drawdown: 5%
- phase 2 max drawdown: 10% (static)
- phase 2 minimum trading days: 3
- source: official `https://www.pipster.io/how-it-works` public schema
- retrieval date: 2026-10-06
- enforcement in QUANT-1: stored as a verified example and not asserted to be the Halloween 2026 final rules

### Instant Funded Account
- daily drawdown: 3%
- max drawdown: 10% (trailing)
- source: official public schema
- retrieval date: 2026-10-06
- enforcement in QUANT-1: stored as an example product rule only

### Pipster Entry
- profit target: 6%
- static maximum drawdown: 6%
- daily loss limit: none
- consistency rule: none
- time limit: none
- optional target reduction: 3%
- activation fee: 30 calendar days to pay after passing
- source: official public product schema
- retrieval date: 2026-10-06
- enforcement in QUANT-1: stored as a verified example product-level rule, not a confirmed Halloween 2026 final rule

## Contest-specific values that remain UNVERIFIED

The following values are not independently verified for the specific Halloween 2026 contest in the public official material inspected on 2026-10-06:

- official start date
- official end date
- timezone
- session start and end times
- symbol universe
- account size / starting balance
- allowed instruments
- prohibited strategies
- EA / bot restrictions
- daily trading frequency restrictions
- minimum holding period restrictions
- latency arbitrage restrictions
- news-trading restrictions
- weekend holding restrictions
- ranking metric used in the final leaderboard
- payout structure or revenue-sharing terms
- platform or broker execution assumptions
- specific position sizing constraints

These remain `UNVERIFIED` in the machine-readable YAML and rule validation code rather than being guessed.

## Machine-readable rule contract

The rule contract is stored in:

- `config/pipster_halloween_2026.yaml`
- `src/pipster_quant/config.py`

The system interprets the file as a rule contract with the following semantics:

- `VERIFIED` values are allowed to be used for baseline risk logic and product example comparison.
- `UNVERIFIED` values are not converted into numeric assumptions.
- any key absent or marked `UNVERIFIED` is treated as an explicit blocker for a hard trading decision until confirmed.

## How this is enforced by QUANT-1

The config layer exposes `validate_rule_contract()`. It marks fields as unverified and surfaces them in the generated report.

The risk engine checks pre-trade conditions based on the loaded rule contract. If a required constraint is unknown, it does not silently assume a value; it flags the rule as unverified and prevents hard optimization claims from being treated as official results.

## Authoritative source statement

The source used for the verified rule examples is the public Pipster site itself, primarily the product and challenge overview pages. That source is authoritative for the public challenge product metadata but not necessarily for a contest-specific event page that is not public or not discoverable on the date accessed.

## Conclusion

The repo now records the public challenge data honestly, separates the verified public values from the unverified contest values, and refuses to invent numbers that are not independently confirmed.
