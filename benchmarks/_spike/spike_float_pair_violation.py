"""Risk spike: sanity check that ESBMC reports a counterexample when the
normalization assertion is actually violated (unnormalized state)."""

a_re = 0.9
a_im = 0.0
b_re = 0.9
b_im = 0.0

norm_squared = (a_re * a_re + a_im * a_im) + (b_re * b_re + b_im * b_im)

assert abs(norm_squared - 1.0) < 1e-4
