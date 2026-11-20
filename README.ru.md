# Campaign Link Audit

[English](README.md)

Ищет ошибки разметки в CSV-медиаплане до запуска рекламы.

![Campaign Link Audit](banner.webp)

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

Передайте CSV в UTF-8 с колонкой url. Первая запись задает написание метки. В примере нужно добавить utm_medium, убрать повтор utm_campaign и привести Telegram к telegram.

Требуется Python 3.9+. Флаг --json выводит список findings. Код 0 означает успешную проверку, 1 — замечания, 2 — ошибка входа или запуска.

0.049 s · macOS · Python · bundled example · single local run.

Автор — команда TON Stories, сервиса размещения рекламы в Telegram Stories у авторов. [TON Stories](https://tonstories.com/?utm_source=github&utm_medium=referral&utm_campaign=open_source&utm_content=campaign-link-audit_ru) · [Telegram](https://t.me/TON_Storiesbot?start=gh_campaign_link_audit_ru)
