# Bell state — properties checked

This benchmark builds the Bell state (|00> + |11>) / sqrt(2) from |00> using an
H gate on qubit 0 followed by a CNOT(control=q0, target=q1), and checks two
properties with plain `assert` statements that ESBMC discharges as verification
conditions.

1. **State normalization**: the sum of squared magnitudes of the four amplitudes
   equals 1 within a small floating-point tolerance. This is the basic sanity
   property every valid quantum state must satisfy, and the one most likely to be
   silently broken by an implementation bug (e.g. a missing 1/sqrt(2) factor).
2. **Expected entangled amplitudes**: after the circuit, the amplitude of |00> and
   |11> must each be 1/sqrt(2), and the amplitude of |01> and |10> must be zero.
   This checks the specific entanglement structure of the Bell state, not just
   that *some* normalized state was reached — a circuit that produced a different
   but still normalized state would fail this check while passing property 1.
