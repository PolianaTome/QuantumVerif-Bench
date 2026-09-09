"""Risk spike: check nondet_float() and __ESBMC_assume() support, needed to
verify teleportation for an arbitrary (symbolic) input qubit state."""

a = nondet_float()
b = nondet_float()

__ESBMC_assume(a * a + b * b > 1.0 - 1e-6)
__ESBMC_assume(a * a + b * b < 1.0 + 1e-6)

norm_sq = a * a + b * b
assert abs(norm_sq - 1.0) < 1e-5
