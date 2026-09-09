"""Simplified Grover search on 3 qubits (N=8 basis states), searching for a
single marked item with 2 Grover iterations (close to the optimal
round(pi/4 * sqrt(8)) = 2 iterations for N=8). Checks that the marked item's
amplitude strictly grows after each iteration, that the state stays
normalized, and that the amplitude after 2 iterations matches the exact
closed-form value for this case.

State amplitudes are a single plain float list (all real-valued here, since
the oracle phase-flip and diffusion operator used are real; see
docs/methodology.md for the representation decision). Basis order is the
plain index 0..7 of the 3-qubit computational basis state.
"""

SQRT1_8 = 0.35355339059327376220  # 1 / sqrt(8)

N = 8
# Marked item is index 3 (a literal index; see docs/methodology.md for a
# separate front-end limitation this benchmark ran into with `amp[i] = -amp[i]`).

amp = [SQRT1_8, SQRT1_8, SQRT1_8, SQRT1_8, SQRT1_8, SQRT1_8, SQRT1_8, SQRT1_8]

initial_marked_amp = amp[3]

# --- Grover iteration 1: oracle (phase flip on the marked item) then
# diffusion (inversion about the mean). ---
# `amp[3] = -amp[3]` fails ESBMC's type inference for negating a list
# element in place; `0.0 - amp[3]` is used instead (see docs/methodology.md).
amp[3] = 0.0 - amp[3]

mean = 0.0
for i in range(N):
    mean = mean + amp[i]
mean = mean / N

new_amp = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
for i in range(N):
    new_amp[i] = 2.0 * mean - amp[i]
amp = new_amp

amp_after_iter1 = amp[3]
assert amp_after_iter1 > initial_marked_amp

# --- Grover iteration 2 ---
amp[3] = 0.0 - amp[3]

mean = 0.0
for i in range(N):
    mean = mean + amp[i]
mean = mean / N

new_amp = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
for i in range(N):
    new_amp[i] = 2.0 * mean - amp[i]
amp = new_amp

amp_after_iter2 = amp[3]
assert amp_after_iter2 > amp_after_iter1

# Grover's operator is unitary: normalization must still hold.
norm_sq = 0.0
for i in range(N):
    norm_sq = norm_sq + amp[i] * amp[i]
assert abs(norm_sq - 1.0) < 1e-6

# Exact closed-form amplitude of the marked item after 2 iterations for N=8.
expected = 11.0 * SQRT1_8 / 4.0
assert abs(amp_after_iter2 - expected) < 1e-6
