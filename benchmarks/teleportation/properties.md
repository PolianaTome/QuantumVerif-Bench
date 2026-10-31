# Quantum teleportation — properties checked

This benchmark simulates the 3-qubit teleportation protocol end to end: Alice's
CNOT and H gates, her two classical measurement bits, and Bob's conditional
correction. `nondet_bool()` is used twice (for m0 and m1) so ESBMC checks all four
possible classical outcomes of Alice's measurement in a single run, rather than
one hard-coded outcome.

1. **Teleportation correctness**: for every one of the four classical outcomes
   (m0, m1), after Bob applies his correction (X if m1, then Z if m0) and
   renormalizes, his qubit's amplitudes must equal Alice's original (alpha, beta)
   within a small floating-point tolerance. This is the entire point of the
   protocol — the classical bits alone carry no information about (alpha, beta),
   yet the corrected qubit always recovers it exactly.

The input state (alpha, beta) is a fixed, non-trivial, normalized real qubit
rather than a fully symbolic one; see docs/methodology.md for why a symbolic input
made the SMT solving step intractable in practice for this benchmark.
