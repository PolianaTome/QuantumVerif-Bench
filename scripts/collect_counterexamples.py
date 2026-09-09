#!/usr/bin/env python3
"""Parse ESBMC verification logs under results/ and produce a structured
JSON summary of counterexamples (objective 2 of the QuantumVerif-Bench
project): which benchmark failed, which property was violated, and what
values the counterexample assigned to each variable along the trace.
"""

import argparse
import json
import re
from pathlib import Path

STATE_HEADER_RE = re.compile(r"^State \d+ file (\S+) line (\d+) column (\d+) thread \d+$")
ASSIGNMENT_RE = re.compile(r"^\s{2}(?P<name>[A-Za-z_][A-Za-z0-9_\[\]]*)\s*=\s*(?P<value>.+?)\s*(\([01 ]+\))?$")
VIOLATED_PROPERTY_HEADER_RE = re.compile(r"^Violated property:$")
PROPERTY_LOCATION_RE = re.compile(r"^\s*file (?P<file>\S+) line (?P<line>\d+) column (?P<column>\d+)$")
ASSERTION_RE = re.compile(r"^\s*assertion (?P<expr>.+)$")


def parse_log(path: Path) -> dict:
    text = path.read_text(encoding="utf-8", errors="replace")
    summary = {"log_file": str(path), "benchmark": path.stem}

    if "VERIFICATION SUCCESSFUL" in text:
        summary["status"] = "SUCCESSFUL"
        return summary

    if "[Counterexample]" not in text or "VERIFICATION FAILED" not in text:
        summary["status"] = "UNKNOWN"
        return summary

    summary["status"] = "FAILED"
    violated_property = {}
    counterexample_values = {}

    in_violated_block = False
    for line in text.splitlines():
        if VIOLATED_PROPERTY_HEADER_RE.match(line.strip()):
            in_violated_block = True
            continue

        if in_violated_block:
            match = PROPERTY_LOCATION_RE.match(line)
            if match:
                violated_property["file"] = match.group("file")
                violated_property["line"] = int(match.group("line"))
                continue
            match = ASSERTION_RE.match(line)
            if match and "assertion" not in violated_property:
                violated_property["assertion"] = match.group("expr").strip()
                continue
            if line.strip() == "":
                in_violated_block = False
            continue

        match = ASSIGNMENT_RE.match(line)
        if match:
            counterexample_values[match.group("name")] = match.group("value").strip()

    summary["violated_property"] = violated_property
    summary["counterexample_values"] = counterexample_values
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--results-dir", default=Path("results"), type=Path,
                         help="Directory containing ESBMC .log files (default: results/)")
    parser.add_argument("--output", default=Path("results/counterexamples.json"), type=Path,
                         help="Where to write the JSON summary (default: results/counterexamples.json)")
    args = parser.parse_args()

    summaries = [parse_log(log_file) for log_file in sorted(args.results_dir.glob("*.log"))]

    args.output.write_text(json.dumps(summaries, indent=2), encoding="utf-8")
    print(f"Wrote {len(summaries)} log summaries to {args.output}")


if __name__ == "__main__":
    main()
