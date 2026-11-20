"""Audit campaign URLs without making network requests."""
import csv
from urllib.parse import parse_qsl, urlsplit


def inspect(path):
    findings = []
    spellings = {}
    with path.open(encoding="utf-8-sig", newline="") as stream:
        rows = csv.DictReader(stream, strict=True)
        if not rows.fieldnames or rows.fieldnames.count("url") != 1:
            raise ValueError("CSV needs one url column")
        for row in rows:
            line = rows.line_num
            def warn(message):
                findings.append(f"{path.name}:{line}: {message}")
            try:
                url = urlsplit(row["url"] or "")
                if url.scheme not in ("http", "https") or not url.hostname:
                    raise ValueError()
            except ValueError:
                warn("expected absolute HTTP(S) URL")
                continue
            params = {}
            for key, value in parse_qsl(url.query, keep_blank_values=True):
                if key.startswith("utm_"):
                    if key in params:
                        warn(f"remove duplicate {key}")
                    params[key] = value
                    if value:
                        canonical = spellings.setdefault((key, value.strip().casefold()), value.strip())
                        if canonical != value:
                            warn(f"standardize {key} spelling to {canonical!r}")
            for key in ("utm_source", "utm_medium", "utm_campaign"):
                if not params.get(key, "").strip():
                    warn(f"add {key}")
    return findings

if __name__ == "__main__":
    import argparse
    import json
    import sys
    from pathlib import Path

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    try:
        findings = inspect(args.path)
    except (ValueError, OSError, csv.Error) as error:
        parser.exit(2, f"{error}\n")
    result = {"findings": findings}
    print(json.dumps(result, ensure_ascii=False) if args.json else "\n".join(findings) or "OK: checked rules passed")
    sys.exit(bool(findings))
