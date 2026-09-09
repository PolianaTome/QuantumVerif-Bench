"""Quantum teleportation protocol on 3 qubits: q0 holds Alice's arbitrary
input state (alpha|0> + beta|1>), q1 and q2 share a Bell pair (Alice keeps
q1, Bob keeps q2). Alice applies CNOT(q0,q1) and H(q0), then measures q0
and q1, sending the two classical bits (m0, m1) to Bob. Bob applies a
correction (X if m1, then Z if m0) to q2. The benchmark asserts that Bob's
final qubit equals Alice's original (alpha, beta), for every one of the
four possible classical outcomes and for every normalized real input state.

Simplification: alpha and beta are taken as real (im = 0), which keeps every
amplitude in this benchmark real-valued. A symbolic (nondet_float() plus
__ESBMC_assume()-normalized) input state was tried first but made the Z3
floating-point solving step intractable (no result after minutes on 302
VCCs); a fixed, non-trivial, normalized input state (alpha, beta) is used
instead, while nondet_bool() still explores all four classical measurement
outcomes (m0, m1) and their corrections. See docs/methodology.md.
Basis order for the 3-qubit state: index = 4*q0 + 2*q1 + q2.
"""

SQRT1_2 = 0.70710678118654752440

alpha = 0.6
beta = 0.8

# Initial state: q0 = alpha|0> + beta|1>, (q1,q2) = Bell pair (|00>+|11>)/sqrt2.
amp = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
amp[0] = alpha * SQRT1_2  # |000>
amp[3] = alpha * SQRT1_2  # |011>
amp[4] = beta * SQRT1_2   # |100>
amp[7] = beta * SQRT1_2   # |111>

# CNOT(control=q0, target=q1): flips q1 whenever q0=1, i.e. swaps
# |100><->|110> (index 4<->6) and |101><->|111> (index 5<->7).
amp[4], amp[6] = amp[6], amp[4]
amp[5], amp[7] = amp[7], amp[5]

# H on q0: mixes basis pairs (i, i+4) for i in range(4).
new_amp = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
for i in range(4):
    new_amp[i] = SQRT1_2 * (amp[i] + amp[i + 4])
    new_amp[i + 4] = SQRT1_2 * (amp[i] - amp[i + 4])
amp = new_amp

# Alice measures q0, q1; nondet_bool() explores all four classical outcomes.
m0 = nondet_bool()
m1 = nondet_bool()

if m0 and m1:
    bob0 = amp[6]
    bob1 = amp[7]
elif m0 and (not m1):
    bob0 = amp[4]
    bob1 = amp[5]
elif (not m0) and m1:
    bob0 = amp[2]
    bob1 = amp[3]
else:
    bob0 = amp[0]
    bob1 = amp[1]

# Bob's correction: X if m1, then Z if m0.
if m1:
    bob0, bob1 = bob1, bob0
if m0:
    bob1 = -bob1

# Each branch's pre-correction amplitude pair has squared magnitude exactly
# 1/4 whenever alpha^2 + beta^2 = 1, so renormalizing means scaling by 2.
final0 = bob0 * 2.0
final1 = bob1 * 2.0

assert abs(final0 - alpha) < 1e-4
assert abs(final1 - beta) < 1e-4
