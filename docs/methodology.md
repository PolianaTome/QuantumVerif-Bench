# Methodology

## Environment confirmation (Step 0)

- ESBMC version: 8.4.0 (64-bit, x86_64-linux) — confirmed with `esbmc --version`.
- Python version: 3.12.3 — confirmed with `python3 --version`.
- ESBMC's Python front-end options were confirmed with `esbmc --help` (`--python`,
  `--override-return-annotation`, `--strict-types`, `--python-no-fold`,
  `--nondet-str-length`, `--python-list-compare-depth`) instead of assumed from
  memory.
- ESBMC 8.4.0 satisfies the >= 8.2 requirement for complex-number support in the
  Python front-end, so the project could proceed past Step 0.
- A local virtual environment (`.venv/`, created with `python3 -m venv`) is used to
  provide `numpy` to the Python interpreter that ESBMC's front-end shells out to
  (`--python .venv/bin/python`), since the system Python is externally managed
  (PEP 668) and does not allow direct `pip install` of third-party packages.

## Risk spike: representing complex quantum amplitudes (Step 1)

This is the central technical risk of the project: quantum state vectors are
naturally complex-valued, but it was not known in advance whether ESBMC's Python
front-end could verify code that manipulates complex numbers, and if not, what the
best workaround would be. Four spikes were run, in order, under
`benchmarks/_spike/`.

### Spike 1 — `spike_complex_numpy.py`: numpy `complex128` array

```python
state = np.array([0.70710678, 0.70710678], dtype=np.complex128)
```

Result: **failed to parse.**

- With a non-literal expression (`1 / np.sqrt(2)`) as an array element:
  `ERROR: TypeError: np.array(..., dtype=...) requires literal numeric elements`.
- Even with literal float elements, the complex dtype itself is rejected:
  `ERROR: TypeError: complex dtype is not supported in NumPy constructors yet`.

Conclusion: numpy arrays with a complex dtype are not usable with ESBMC 8.4.0's
Python front-end, regardless of whether the elements are literals.

### Spike 2 — `spike_native_complex.py`: native Python `complex` type

```python
a = complex(0.70710678, 0.0)
norm_squared = abs(a) ** 2 + abs(b) ** 2
```

Result: **parses, but is impractical to verify.**

`complex(...)` construction is accepted, but calling `abs()` on a complex value
routes through ESBMC's internal libm model for `abs`/`hypot`, which in turn calls
into an `exp`/`expm1` implementation (`c2goto/library/libm/exp.c`) containing a loop
that ESBMC unwinds without ever reaching a fixed point in a reasonable amount of
time — the run was left unwinding past 200+ iterations of that internal loop with
no sign of terminating. This is a bounded model checker's classic failure mode for
an unbounded/ill-suited internal loop, not a hang in the surrounding tooling (a
plain WSL/ESBMC liveness check run concurrently returned normally).

Conclusion: the native `complex` type is parseable but **not viable** for this
project, because any property that needs `abs()` of a complex amplitude
(normalization, in particular) cannot be checked in practical time.

### Spike 3 — `spike_float_pair.py`: manual (real, imaginary) float pair

```python
a_re = 0.70710678
a_im = 0.0
norm_squared = (a_re * a_re + a_im * a_im) + (b_re * b_re + b_im * b_im)
assert abs(norm_squared - 1.0) < 1e-4
```

Result: **works.** `VERIFICATION SUCCESSFUL` in ~2.5s, 1 real VCC generated (not
trivially discharged). A second run with a deliberately unnormalized state
(`spike_float_pair_violation.py`) correctly produced `VERIFICATION FAILED` with a
`[Counterexample]` block and a `Violated property:` line — confirming that ESBMC's
Python front-end both verifies and falsifies this representation correctly, and
that the counterexample output has the structure `scripts/collect_counterexamples.py`
(objective 2 of the project) needs to parse.

### Spike 4 — `spike_float_list.py`: parallel Python lists of floats, indexed with `range()`

```python
state_re = [0.5, 0.5, 0.5, 0.5]
state_im = [0.0, 0.0, 0.0, 0.0]
for i in range(4):
    norm_squared = norm_squared + state_re[i] * state_re[i] + state_im[i] * state_im[i]
```

Result: **works.** `VERIFICATION SUCCESSFUL`, loop over `range(4)` unwound cleanly
(4 iterations, no manual `--unwind` bound needed for this bound), list indexing
worked. This confirms multi-amplitude state vectors (2+ qubits) are representable
as plain Python lists of floats, driven by `for i in range(N)` loops.

### Decision

Quantum state vectors in all 5 benchmarks are represented as **two parallel plain
Python lists of floats** — one for the real part, one for the imaginary part of each
amplitude — indexed with `for _ in range(N)` loops. Neither numpy complex arrays nor
the native Python `complex` type are used anywhere in the benchmarks. This is a
deliberate simplification of the *representation*, not of the *verification target*:
every property in this project (normalization, unitary consistency, measurement
validity) is still checked exactly, just written in terms of `re[i]`/`im[i]` pairs
instead of a `complex` value.

This finding is itself a novel-ish practical observation about ESBMC 8.4.0's Python
front-end and is worth reporting as a limitation: complex-number support exists at
the parsing level for simple arithmetic, but the standard-library path for `abs()`
of a complex number is not currently practical for bounded model checking.

## Front-end limitations observed while building the benchmarks

This section is updated as further limitations are found while building the 5
benchmarks in Step 3 (see also the spike results above):

- `numpy` arrays with `dtype=complex128` (or any complex dtype): not supported by
  ESBMC's NumPy constructor handling (see Spike 1).
- Native Python `complex` + `abs()`: parses but does not terminate in practical time
  (see Spike 2).
- `mypy` is not installed in the project venv; ESBMC's Python front-end emits a
  warning (`Warning: mypy not found on PATH; type checking will be skipped.`) and
  falls back to skipping the optional static type-checking pass. This does not
  affect verification and was left as-is rather than adding an extra dependency
  purely to silence a warning.
- `nondet_float()` + `__ESBMC_assume()` are supported and work for small examples
  (confirmed in `benchmarks/_spike/spike_nondet_float_assume.py`), but using them to
  make `benchmarks/teleportation/teleportation.py`'s input qubit fully symbolic
  (2 nondet floats, normalized via `__ESBMC_assume`) made the Z3 floating-point
  solving step intractable in practice: two separate runs did not return a verdict
  after several minutes on a 302-VCC program, whereas the same program with a fixed
  concrete input state solved in under a second. The benchmark uses a fixed,
  non-trivial, normalized input state instead, while still using `nondet_bool()` to
  exhaustively cover Bob's four possible classical-correction branches. This is a
  solver-performance limitation of this particular nonlinear floating-point problem,
  not a front-end parsing limitation.
