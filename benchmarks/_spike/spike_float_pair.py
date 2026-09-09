"""Risk spike: represent a quantum amplitude as a manual (real, imaginary)
float pair instead of numpy complex128 or native Python complex."""

a_re = 0.70710678
a_im = 0.0
b_re = 0.70710678
b_im = 0.0

norm_squared = (a_re * a_re + a_im * a_im) + (b_re * b_re + b_im * b_im)

assert abs(norm_squared - 1.0) < 1e-4
