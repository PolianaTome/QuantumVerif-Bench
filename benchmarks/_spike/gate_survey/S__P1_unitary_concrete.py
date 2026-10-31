re = [1.0, 0.0]
im = [0.0, 0.0]
nre = [re[0], 0.0 - im[1]]
nim = [im[0], re[1]]
re = nre
im = nim
c0r = re
c0i = im
re = [0.0, 1.0]
im = [0.0, 0.0]
nre = [re[0], 0.0 - im[1]]
nim = [im[0], re[1]]
re = nre
im = nim
c1r = re
c1i = im
dr = 0.0
di = 0.0
for k in range(2):
    dr = dr + c0r[k] * c0r[k] + c0i[k] * c0i[k]
    di = di + c0r[k] * c0i[k] - c0i[k] * c0r[k]
assert abs(dr - 1.0) < 1e-9
assert abs(di) < 1e-9
dr = 0.0
di = 0.0
for k in range(2):
    dr = dr + c0r[k] * c1r[k] + c0i[k] * c1i[k]
    di = di + c0r[k] * c1i[k] - c0i[k] * c1r[k]
assert abs(dr - 0.0) < 1e-9
assert abs(di) < 1e-9
dr = 0.0
di = 0.0
for k in range(2):
    dr = dr + c1r[k] * c0r[k] + c1i[k] * c0i[k]
    di = di + c1r[k] * c0i[k] - c1i[k] * c0r[k]
assert abs(dr - 0.0) < 1e-9
assert abs(di) < 1e-9
dr = 0.0
di = 0.0
for k in range(2):
    dr = dr + c1r[k] * c1r[k] + c1i[k] * c1i[k]
    di = di + c1r[k] * c1i[k] - c1i[k] * c1r[k]
assert abs(dr - 1.0) < 1e-9
assert abs(di) < 1e-9
