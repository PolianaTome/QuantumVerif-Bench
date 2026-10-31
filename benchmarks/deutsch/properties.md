# Deutsch's algorithm — properties checked

This benchmark simulates the full H-Uf-H circuit of Deutsch's algorithm on one
input qubit and one ancilla qubit, with `nondet_bool()` used to make ESBMC
explore both a constant oracle (f(x) = 0) and a balanced oracle (f(x) = x) as two
separate verification branches of the same program.

1. **Determinism of the measurement outcome**: for the branch actually simulated,
   the probability mass on the *other* outcome of qubit q0 must be (numerically)
   zero — i.e. the algorithm never leaves any amplitude on the wrong answer. This
   is the property that makes Deutsch's algorithm interesting: a single oracle
   query fully resolves constant-vs-balanced with certainty, unlike any classical
   single-query strategy.
2. **Output bit matches the simulated case**: the measured bit (0 for the
   constant oracle, 1 for the balanced oracle) must equal what the actual
   simulated amplitudes predict, for whichever branch `nondet_bool()` selected.
   Because ESBMC explores both branches, this is really two properties checked
   in one program — one per oracle type — not a single hard-coded case.
