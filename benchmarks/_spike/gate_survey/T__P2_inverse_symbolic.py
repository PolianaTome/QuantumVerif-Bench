re = [nondet_float(), nondet_float()]
im = [nondet_float(), nondet_float()]
for i in range(2):
    __ESBMC_assume(re[i] >= -1.0 and re[i] <= 1.0)
    __ESBMC_assume(im[i] >= -1.0 and im[i] <= 1.0)
r0 = re
i0 = im
nre = [re[0], 0.70710678118654752440 * (re[1] - im[1])]
nim = [im[0], 0.70710678118654752440 * (re[1] + im[1])]
re = nre
im = nim
nre = [re[0], 0.70710678118654752440 * (re[1] + im[1])]
nim = [im[0], 0.70710678118654752440 * (im[1] - re[1])]
re = nre
im = nim
for i in range(2):
    assert abs(re[i] - r0[i]) < 1e-9
    assert abs(im[i] - i0[i]) < 1e-9
