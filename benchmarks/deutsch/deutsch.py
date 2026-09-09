"""Deutsch's algorithm on a single input qubit (q0, "x") and one ancilla
qubit (q1, "y"), using the standard H - Uf - H circuit. nondet_bool() picks
between a constant oracle (f(x) = 0) and a balanced oracle (f(x) = x), and
the benchmark checks that the algorithm deterministically measures q0 = 0
for the constant case and q0 = 1 for the balanced case, in a single query.

State vector: two parallel float lists (real, imaginary parts), basis order
index 0=|00>, 1=|01>, 2=|10>, 3=|11> (first digit q0, second digit q1). See
docs/methodology.md for why this representation was chosen over numpy/complex.
"""

SQRT1_2 = 0.70710678118654752440

is_balanced = nondet_bool()

# Initial state |0>_x |1>_y = |01> = index 1.
re = [0.0, 1.0, 0.0, 0.0]
im = [0.0, 0.0, 0.0, 0.0]

# H on q0 (mixes basis pairs (0,2) and (1,3)).
r0 = SQRT1_2 * (re[0] + re[2])
r2 = SQRT1_2 * (re[0] - re[2])
r1 = SQRT1_2 * (re[1] + re[3])
r3 = SQRT1_2 * (re[1] - re[3])
i0 = SQRT1_2 * (im[0] + im[2])
i2 = SQRT1_2 * (im[0] - im[2])
i1 = SQRT1_2 * (im[1] + im[3])
i3 = SQRT1_2 * (im[1] - im[3])
re = [r0, r1, r2, r3]
im = [i0, i1, i2, i3]

# H on q1 (mixes basis pairs (0,1) and (2,3)).
r0 = SQRT1_2 * (re[0] + re[1])
r1 = SQRT1_2 * (re[0] - re[1])
r2 = SQRT1_2 * (re[2] + re[3])
r3 = SQRT1_2 * (re[2] - re[3])
i0 = SQRT1_2 * (im[0] + im[1])
i1 = SQRT1_2 * (im[0] - im[1])
i2 = SQRT1_2 * (im[2] + im[3])
i3 = SQRT1_2 * (im[2] - im[3])
re = [r0, r1, r2, r3]
im = [i0, i1, i2, i3]

# Oracle Uf: |x,y> -> |x, y XOR f(x)>.
# Constant oracle f(x) = 0: identity, no change.
# Balanced oracle f(x) = x: flips y only when x = 1, i.e. swaps |10> and |11>
# (index 2 and index 3).
if is_balanced:
    re[2], re[3] = re[3], re[2]
    im[2], im[3] = im[3], im[2]

# H on q0 again (mixes basis pairs (0,2) and (1,3)).
r0 = SQRT1_2 * (re[0] + re[2])
r2 = SQRT1_2 * (re[0] - re[2])
r1 = SQRT1_2 * (re[1] + re[3])
r3 = SQRT1_2 * (re[1] - re[3])
i0 = SQRT1_2 * (im[0] + im[2])
i2 = SQRT1_2 * (im[0] - im[2])
i1 = SQRT1_2 * (im[1] + im[3])
i3 = SQRT1_2 * (im[1] - im[3])
re = [r0, r1, r2, r3]
im = [i0, i1, i2, i3]

# Probability mass on q0 = 0 (indices 0,1) versus q0 = 1 (indices 2,3).
prob_q0_0 = re[0] * re[0] + im[0] * im[0] + re[1] * re[1] + im[1] * im[1]
prob_q0_1 = re[2] * re[2] + im[2] * im[2] + re[3] * re[3] + im[3] * im[3]

if is_balanced:
    expected_bit = 1
    assert prob_q0_0 < 1e-6
else:
    expected_bit = 0
    assert prob_q0_1 < 1e-6

if prob_q0_1 > 0.5:
    measured_bit = 1
else:
    measured_bit = 0

assert measured_bit == expected_bit
