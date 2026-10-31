re = [nondet_float(), nondet_float(), nondet_float(), nondet_float(), nondet_float(), nondet_float(), nondet_float(), nondet_float()]
im = [nondet_float(), nondet_float(), nondet_float(), nondet_float(), nondet_float(), nondet_float(), nondet_float(), nondet_float()]
for i in range(8):
    __ESBMC_assume(re[i] >= -1.0 and re[i] <= 1.0)
    __ESBMC_assume(im[i] >= -1.0 and im[i] <= 1.0)
r0 = re
i0 = im
nre = [re[0], re[1], re[2], re[3], re[4], re[5], re[7], re[6]]
nim = [im[0], im[1], im[2], im[3], im[4], im[5], im[7], im[6]]
re = nre
im = nim
nre = [re[0], re[1], re[2], re[3], re[4], re[5], re[7], re[6]]
nim = [im[0], im[1], im[2], im[3], im[4], im[5], im[7], im[6]]
re = nre
im = nim
for i in range(8):
    assert abs(re[i] - r0[i]) < 1e-9
    assert abs(im[i] - i0[i]) < 1e-9
