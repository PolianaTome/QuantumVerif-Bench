"""Bell state circuit: H on qubit 0 followed by CNOT(control=q0, target=q1),
starting from |00>. Verifies state normalization and the expected Bell-pair
amplitudes.

State vector is represented as two parallel float lists (real and imaginary
parts), basis-ordered as index 0=|00>, 1=|01>, 2=|10>, 3=|11> (see
docs/methodology.md for why complex/numpy types are not used).
"""

SQRT1_2 = 0.70710678118654752440

re = [1.0, 0.0, 0.0, 0.0]
im = [0.0, 0.0, 0.0, 0.0]

# H on qubit 0 acts independently on the (|00>,|10>) and (|01>,|11>) pairs.
new_re0 = SQRT1_2 * (re[0] + re[2])
new_re2 = SQRT1_2 * (re[0] - re[2])
new_im0 = SQRT1_2 * (im[0] + im[2])
new_im2 = SQRT1_2 * (im[0] - im[2])
new_re1 = SQRT1_2 * (re[1] + re[3])
new_re3 = SQRT1_2 * (re[1] - re[3])
new_im1 = SQRT1_2 * (im[1] + im[3])
new_im3 = SQRT1_2 * (im[1] - im[3])

re = [new_re0, new_re1, new_re2, new_re3]
im = [new_im0, new_im1, new_im2, new_im3]

# CNOT(control=q0, target=q1): swap the amplitudes of |10> and |11>.
re[2], re[3] = re[3], re[2]
im[2], im[3] = im[3], im[2]

norm_sq = 0.0
for i in range(4):
    norm_sq = norm_sq + re[i] * re[i] + im[i] * im[i]
assert abs(norm_sq - 1.0) < 1e-6

# Expected Bell state (|00> + |11>) / sqrt(2): zero amplitude on |01>, |10>.
assert abs(re[0] - SQRT1_2) < 1e-6
assert abs(im[0]) < 1e-6
assert abs(re[1]) < 1e-6
assert abs(im[1]) < 1e-6
assert abs(re[2]) < 1e-6
assert abs(im[2]) < 1e-6
assert abs(re[3] - SQRT1_2) < 1e-6
assert abs(im[3]) < 1e-6
