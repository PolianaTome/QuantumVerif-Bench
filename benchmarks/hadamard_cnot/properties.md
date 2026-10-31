# Hadamard/CNOT sequence — properties checked

This benchmark applies a sequence of six gates (H, H, CNOT, H, CNOT) to a 2-qubit
state starting from |00>, and checks state normalization after *every single gate*,
not only at the end of the circuit.

1. **Unitary consistency at each step**: after each of the six operations, the sum
   of squared amplitude magnitudes must equal 1 within tolerance. Checking this
   after every gate — rather than once at the end — is what actually pins down
   *which* operation in a sequence broke unitarity if a bug is introduced (e.g. an
   incorrect gate matrix, a wrong basis-pair index, or a missing 1/sqrt(2) factor),
   instead of only knowing that *some* gate in the whole sequence did.
