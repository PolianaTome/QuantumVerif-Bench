"""Risk spike: check whether a plain Python list of floats (used to hold
the real/imaginary parts of a multi-amplitude state vector) is supported
by ESBMC's Python front-end."""

state_re = [0.5, 0.5, 0.5, 0.5]
state_im = [0.0, 0.0, 0.0, 0.0]

norm_squared = 0.0
for i in range(4):
    norm_squared = norm_squared + state_re[i] * state_re[i] + state_im[i] * state_im[i]

assert abs(norm_squared - 1.0) < 1e-4
