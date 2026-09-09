# Contributing to QuantumVerif-Bench

Thanks for your interest in contributing! This is a small academic research
project (PIBITI, UFAM), so the process is intentionally lightweight.

## Getting started

1. Fork and clone the repository.
2. Create a virtual environment and install dependencies:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
3. Make sure ESBMC (>= 8.2) is installed and on your `PATH` (`esbmc --version`).

## Adding or changing a benchmark

- Every benchmark lives under `benchmarks/<name>/` with two files: `<name>.py`
  (the code to verify) and `properties.md` (a short prose explanation of what
  formal property is being checked and why).
- Represent quantum state vectors as two parallel plain Python lists of floats
  (real and imaginary parts) — see `docs/methodology.md` for why numpy complex
  arrays and the native Python `complex` type are not used.
- Before opening a pull request, run ESBMC on your benchmark directly and make
  sure it reports `VERIFICATION SUCCESSFUL`:
  ```bash
  bash scripts/run_esbmc.sh benchmarks/<name>/<name>.py
  ```
- If you hit a real limitation of ESBMC's Python front-end (an unsupported
  construct, a type-inference error, etc.), simplify the *code*, not the
  *property* being verified, and document the limitation in
  `docs/methodology.md`.
- Run the smoke tests to make sure the benchmark also runs cleanly under plain
  Python (no ESBMC):
  ```bash
  pytest tests/
  ```

## Reporting issues

Please open an issue describing what you expected, what happened instead, and
the ESBMC version you used (`esbmc --version`).

## Code style

- Benchmark code, scripts, and documentation (outside of `docs/weekly-logs/`)
  are written in English.
- No unnecessary comments — only comment on non-obvious *why*, not *what*.
- Keep benchmarks minimal: don't add abstractions or generality the
  verification target doesn't need.
