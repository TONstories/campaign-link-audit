# Campaign Link Audit

![Campaign Link Audit — Catch tracking errors before launch.](banner.webp)

[Русский](README.ru.md) · [Release notes](https://github.com/TONstories/campaign-link-audit/releases) · [0BSD license](LICENSE)

Catch tracking errors before launch. Export a UTF-8 CSV with one column named url. Keep creator, date and cost columns alongside it if useful; the checker reads the destination column only. Use absolute HTTP or HTTPS links. Quoted cells, percent-encoded parameter values and a UTF-8 byte-order mark are supported. Repeated destinations reuse parsed query fields while spelling comparisons still run for each placement.

## Try the included example

Requires Python 3.9 or later. The example intentionally includes a finding and exits with status 1.

```sh
git clone https://github.com/TONstories/campaign-link-audit.git
cd campaign-link-audit
python3 audit.py examples/plan.csv
```

```text
plan.csv:3: standardize utm_source spelling to 'telegram'
plan.csv:3: remove duplicate utm_campaign
plan.csv:3: add utm_medium
```

## Auditing a placement sheet

```sh
python3 audit.py examples/plan.csv --json
```

Start with missing source, medium or campaign fields, then resolve duplicate keys. When Telegram and telegram both appear in one field, review the first spelling before standardizing the sheet. The chosen spelling is a consistency hint, not a claim about your analytics configuration. The audit runs offline and does not test redirects or confirm receipt of events.

## CI and coding agents

Use the JSON report when consuming results programmatically. Its `findings` array contains one diagnostic per detected issue. Exit 0 means the implemented rules passed, exit 1 means review the findings, and exit 2 means the command or input could not be processed. Capture stderr separately for invocation errors. Run `python3 test_example.py` to exercise the bundled fixture and a corrected input. Agent setup is documented in [AGENTS.md](AGENTS.md).

## Performance

On a local Apple Silicon Mac, checking 40,000 CSV rows with 100 distinct destinations took **0.323 s** versus **1.109 s** with v0.1.0. Both numbers are the median of three paired CLI runs with identical local input, including interpreter startup. Timing varies with hardware, storage and input composition.

## Maintainer

Built by TON Stories, a marketplace connecting advertisers with creators for Telegram Stories campaigns. [TON Stories](https://tonstories.com/?utm_source=github&utm_medium=referral&utm_campaign=open_source&utm_content=campaign-link-audit) · [Telegram](https://t.me/TON_Storiesbot?start=gh_campaign_link_audit)
