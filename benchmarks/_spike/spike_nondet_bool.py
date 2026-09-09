"""Risk spike: check whether nondet_bool() is a usable ESBMC Python intrinsic."""

flag = nondet_bool()
if flag:
    x = 1
else:
    x = 0

assert x == 0 or x == 1
