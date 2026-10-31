re = [nondet_float(), nondet_float(), nondet_float(), nondet_float(), nondet_float(), nondet_float(), nondet_float(), nondet_float()]
im = [nondet_float(), nondet_float(), nondet_float(), nondet_float(), nondet_float(), nondet_float(), nondet_float(), nondet_float()]
for i in range(8):
    __ESBMC_assume(re[i] >= -1.0 and re[i] <= 1.0)
    __ESBMC_assume(im[i] >= -1.0 and im[i] <= 1.0)
n0 = 0.0
for i in range(8):
    n0 = n0 + re[i] * re[i] + im[i] * im[i]
__ESBMC_assume(n0 > 1.0 - 1e-6 and n0 < 1.0 + 1e-6)
nre = [re[0], re[1], re[2], re[3], re[4], re[5], re[7], re[6]]
nim = [im[0], im[1], im[2], im[3], im[4], im[5], im[7], im[6]]
re = nre
im = nim
n1 = 0.0
for i in range(8):
    n1 = n1 + re[i] * re[i] + im[i] * im[i]
assert abs(n1 - 1.0) < 1e-5
