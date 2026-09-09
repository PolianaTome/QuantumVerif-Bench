"""Risk spike: check whether ESBMC's Python frontend supports the native
Python complex type as a representation for quantum amplitudes."""

a = complex(0.70710678, 0.0)
b = complex(0.70710678, 0.0)

norm_squared = abs(a) ** 2 + abs(b) ** 2

assert abs(norm_squared - 1.0) < 1e-4
