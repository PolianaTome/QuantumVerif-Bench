"""Risk spike: check whether ESBMC's Python front-end supports negating a
list element in place. Direct unary negation (amp[i] = -amp[i]) failed with
a type-inference error; this tests the 0.0 - amp[i] workaround instead."""

amp = [1.0, 2.0, 3.0]
amp[0] = 0.0 - amp[0]

assert amp[0] == -1.0
