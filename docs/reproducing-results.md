# Reproducing the results

This guide describes how to rerun the five formal-verification benchmarks in
this repository. Run the commands from the repository root.

## Tested environment

The documented baseline is Linux x86_64 with Python 3.12.3 and ESBMC 8.4.0.
The benchmark suite requires ESBMC 8.2 or newer; solver versions, runtimes,
and diagnostic details may differ between environments.

The verification runner uses `systemd-run --user --scope` to limit ESBMC's
memory use. On WSL2, enable systemd for the distribution and restart it before
running the suite. Check that the user systemd manager is available with:

```bash
systemd-run --user --scope -q true
```

Install ESBMC using the
[official ESBMC installation instructions](https://github.com/esbmc/esbmc#installation),
then confirm that it is available:

```bash
esbmc --version
```

Create a Python virtual environment and install the project dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python --version
```

The runner automatically uses `.venv/bin/python` when it exists. This lets
ESBMC's Python front-end import the project's NumPy dependency.

## Run the checks

First, run the smoke tests. These check that each benchmark executes under
CPython, but they do not prove the benchmark properties:

```bash
python -m pytest tests/
```

Run one formal verification:

```bash
bash scripts/run_esbmc.sh benchmarks/bell/bell.py
```

Run the complete formal-verification suite:

```bash
bash scripts/run_esbmc.sh
```

The full suite covers `bell`, `deutsch`, `grover_simplified`,
`hadamard_cnot`, and `teleportation`. Each run writes its ESBMC output to
`results/<benchmark>.log`. A successful run prints
`VERIFICATION SUCCESSFUL` for every benchmark and exits with status 0. If any
benchmark fails or ESBMC cannot produce a verdict, the runner continues with
the remaining benchmarks, reports the affected log, and exits with a
non-zero status.

Summarize the logs into JSON:

```bash
python scripts/collect_counterexamples.py
```

By default, the report is written to `results/counterexamples.json`. It records
each log's `SUCCESSFUL`, `FAILED`, or `UNKNOWN` status; failed logs also include
the violated property and counterexample values when those can be parsed.
To choose different paths, use `--results-dir` and `--output`.

## Expected results and scope

For the repository's five primary benchmarks, the expected status is
`VERIFICATION SUCCESSFUL` for each one. The committed methodology and each
benchmark's `properties.md` describe the verified claims and the modeling
choices behind them.

The exploratory programs under `benchmarks/_spike/` are not part of the
default suite. They investigate ESBMC front-end behavior and are not included
in the five-benchmark expected result above.

GitHub Actions runs the CPython smoke tests on pushes and pull requests. The
formal ESBMC job is currently disabled; therefore, a passing GitHub Actions
run alone does not reproduce or certify the formal-verification results.
