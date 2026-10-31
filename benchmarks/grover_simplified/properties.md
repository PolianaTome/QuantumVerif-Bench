# Simplified Grover search — properties checked

This benchmark runs 2 Grover iterations (oracle phase-flip + diffusion) over an
8-item search space (3 qubits) with a single marked item, and checks how the
marked item's amplitude evolves.

1. **Amplitude growth per iteration**: the marked item's amplitude must be
   strictly larger after iteration 1 than before it, and strictly larger again
   after iteration 2 than after iteration 1. This directly checks Grover's
   amplitude-amplification behavior step by step, not just "the final answer is
   probably right" — a broken diffusion operator that still happened to leave the
   final probability high would still be caught if it violated monotonic growth
   along the way.
2. **Unitary consistency**: the state stays normalized after both iterations,
   since the combined oracle + diffusion operator is unitary.
3. **Exact closed-form match**: the amplitude after 2 iterations equals the known
   closed-form value for N=8, 1 marked item, 2 iterations — a stronger check than
   growth alone, since it pins down the exact expected amplitude rather than just
   its direction of change.
