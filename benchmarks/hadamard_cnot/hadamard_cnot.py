"""Sequence of H and CNOT gates on 2 qubits, starting from |00>, checking
that the state stays normalized (unitary consistency) after every single
operation, not just at the end.

State vector: two parallel float lists (real, imaginary parts), basis order
index 0=|00>, 1=|01>, 2=|10>, 3=|11> (first digit q0, second digit q1). See
docs/methodology.md for why this representation was chosen over numpy/complex.
"""

SQRT1_2 = 0.70710678118654752440


def check_norm(re, im):
    norm_sq = 0.0
    for i in range(4):
        norm_sq = norm_sq + re[i] * re[i] + im[i] * im[i]
    assert abs(norm_sq - 1.0) < 1e-6


re = [1.0, 0.0, 0.0, 0.0]
im = [0.0, 0.0, 0.0, 0.0]
check_norm(re, im)

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
check_norm(re, im)

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
check_norm(re, im)

# CNOT(control=q0, target=q1): swap amplitudes of |10> and |11> (index 2,3).
re[2], re[3] = re[3], re[2]
im[2], im[3] = im[3], im[2]
check_norm(re, im)

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
check_norm(re, im)

# CNOT(control=q1, target=q0): swap amplitudes of |01> and |11> (index 1,3).
re[1], re[3] = re[3], re[1]
im[1], im[3] = im[3], im[1]
check_norm(re, im)
