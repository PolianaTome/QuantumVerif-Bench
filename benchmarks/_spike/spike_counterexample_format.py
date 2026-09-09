"""Risk spike: inspect the full [Counterexample] trace format ESBMC produces
when a nondet variable is involved, to design collect_counterexamples.py."""

x = nondet_int()
__ESBMC_assume(x > 0)
__ESBMC_assume(x < 10)

assert x > 100
