# QuantumVerif-Bench

QuantumVerif-Bench is a PIBITI (UFAM) undergraduate research project that applies
[ESBMC](https://github.com/esbmc/esbmc) — a general-purpose, SV-COMP/Test-COMP
competitive SMT-based bounded model checker — directly to Python quantum
programs, checking a small suite of textbook quantum algorithms (Bell state,
Deutsch's algorithm, quantum teleportation, a Hadamard/CNOT sequence, and a
simplified Grover search) for state normalization, unitary consistency, and
measurement validity, using ESBMC's Python front-end instead of a purpose-built
quantum-circuit DSL.

## Requirements

- Linux (or WSL2) with [ESBMC](https://github.com/esbmc/esbmc) >= 8.2 installed
  and on `PATH` (`esbmc --version`); versions before 8.2 do not support the
  Python front-end features this project relies on.
- Python 3.
- A virtual environment with the packages in `requirements.txt`:
  ```bash
  python3 -m venv .venv
  source .venv/bin/activate
  pip install -r requirements.txt
  ```

## Quickstart

```bash
bash scripts/run_esbmc.sh benchmarks/bell/bell.py
```

Run every benchmark and save each verification log under `results/`:

```bash
bash scripts/run_esbmc.sh
```

Summarize any counterexamples found across `results/*.log` into a structured
JSON report:

```bash
python3 scripts/collect_counterexamples.py
```

## Benchmarks and properties verified

| Benchmark | Properties verified |
|---|---|
| `bell` | State normalization; expected ±1/√2 entangled amplitudes on \|00⟩ and \|11⟩, zero elsewhere |
| `deutsch` | Deterministic measurement outcome (no amplitude leaks to the wrong answer); measured bit matches the simulated oracle (constant vs. balanced) |
| `teleportation` | Bob's final qubit, after his conditional correction, exactly equals Alice's original qubit, for all four classical measurement outcomes |
| `hadamard_cnot` | State normalization preserved after *every* individual gate in the sequence, not just at the end |
| `grover_simplified` | Marked item's amplitude strictly grows after each Grover iteration; state stays normalized; amplitude matches the exact closed-form value after 2 iterations |

See each benchmark's `properties.md` for the full prose explanation, and
`docs/methodology.md` for how quantum state vectors are represented and which
front-end limitations were found while building these benchmarks.

## Related work

Automated formal verification of quantum programs via SMT already exists
(symQV, AutoQ 2.0), so that alone is not this project's contribution. What sets
QuantumVerif-Bench apart is using a mature, general-purpose verifier — ESBMC,
competitive in SV-COMP/Test-COMP — that verifies Python source directly instead
of a purpose-built circuit DSL, which means the same verification run also
catches conventional software bugs (division by zero, out-of-bounds indexing,
type errors) alongside quantum state properties. See `docs/related-work.md` for
the full comparison table and discussion, including two author-name
corrections to the original PIBITI proposal's references.

## License

MIT — see [LICENSE](LICENSE).

## Citation

See [CITATION.cff](CITATION.cff). Some fields (DOI, release date, ORCID iDs) are
left as placeholders pending information not yet available.
