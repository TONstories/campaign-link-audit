import json
import subprocess
import sys
import tempfile
from pathlib import Path

command = ['audit.py', 'examples/plan.csv']
def check(arguments, code):
    result = subprocess.run([sys.executable, *arguments, "--json"], capture_output=True, text=True)
    assert result.returncode == code, result.stderr
    return json.loads(result.stdout)["findings"]

assert check(command, 1) == ["plan.csv:3: standardize utm_source spelling to 'telegram'", 'plan.csv:3: remove duplicate utm_campaign', 'plan.csv:3: add utm_medium']
with tempfile.TemporaryDirectory() as folder:
    target = Path(folder) / "plan.csv"
    target.write_text('url\nhttps://example.org/?utm_source=x&utm_medium=y&utm_campaign=z\n')
    command[1] = str(target)
    assert check(command, 0) == []

with tempfile.TemporaryDirectory() as folder:
    target = Path(folder) / "ports.csv"
    target.write_text("url\nhttps://example.org:bad/\n")
    assert check(["audit.py", str(target)], 1) == ["ports.csv:2: expected absolute HTTP(S) URL"]
