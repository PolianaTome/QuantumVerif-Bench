re = [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
im = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
nre = [re[0], re[1], re[2], re[3], re[4], re[6], re[5], re[7]]
nim = [im[0], im[1], im[2], im[3], im[4], im[6], im[5], im[7]]
re = nre
im = nim
c0r = re
c0i = im
re = [0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
im = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
nre = [re[0], re[1], re[2], re[3], re[4], re[6], re[5], re[7]]
nim = [im[0], im[1], im[2], im[3], im[4], im[6], im[5], im[7]]
re = nre
im = nim
c1r = re
c1i = im
re = [0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0]
im = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
nre = [re[0], re[1], re[2], re[3], re[4], re[6], re[5], re[7]]
nim = [im[0], im[1], im[2], im[3], im[4], im[6], im[5], im[7]]
re = nre
im = nim
c2r = re
c2i = im
re = [0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0]
im = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
nre = [re[0], re[1], re[2], re[3], re[4], re[6], re[5], re[7]]
nim = [im[0], im[1], im[2], im[3], im[4], im[6], im[5], im[7]]
re = nre
im = nim
c3r = re
c3i = im
re = [0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0]
im = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
nre = [re[0], re[1], re[2], re[3], re[4], re[6], re[5], re[7]]
nim = [im[0], im[1], im[2], im[3], im[4], im[6], im[5], im[7]]
re = nre
im = nim
c4r = re
c4i = im
re = [0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0]
im = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
nre = [re[0], re[1], re[2], re[3], re[4], re[6], re[5], re[7]]
nim = [im[0], im[1], im[2], im[3], im[4], im[6], im[5], im[7]]
re = nre
im = nim
c5r = re
c5i = im
re = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0]
im = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
nre = [re[0], re[1], re[2], re[3], re[4], re[6], re[5], re[7]]
nim = [im[0], im[1], im[2], im[3], im[4], im[6], im[5], im[7]]
re = nre
im = nim
c6r = re
c6i = im
re = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0]
im = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
nre = [re[0], re[1], re[2], re[3], re[4], re[6], re[5], re[7]]
nim = [im[0], im[1], im[2], im[3], im[4], im[6], im[5], im[7]]
re = nre
im = nim
c7r = re
c7i = im
dr = 0.0
di = 0.0
for k in range(8):
    dr = dr + c0r[k] * c0r[k] + c0i[k] * c0i[k]
    di = di + c0r[k] * c0i[k] - c0i[k] * c0r[k]
assert abs(dr - 1.0) < 1e-9
assert abs(di) < 1e-9
dr = 0.0
di = 0.0
for k in range(8):
    dr = dr + c0r[k] * c1r[k] + c0i[k] * c1i[k]
    di = di + c0r[k] * c1i[k] - c0i[k] * c1r[k]
assert abs(dr - 0.0) < 1e-9
assert abs(di) < 1e-9
dr = 0.0
di = 0.0
for k in range(8):
    dr = dr + c0r[k] * c2r[k] + c0i[k] * c2i[k]
    di = di + c0r[k] * c2i[k] - c0i[k] * c2r[k]
assert abs(dr - 0.0) < 1e-9
assert abs(di) < 1e-9
dr = 0.0
di = 0.0
for k in range(8):
    dr = dr + c0r[k] * c3r[k] + c0i[k] * c3i[k]
    di = di + c0r[k] * c3i[k] - c0i[k] * c3r[k]
assert abs(dr - 0.0) < 1e-9
assert abs(di) < 1e-9
dr = 0.0
di = 0.0
for k in range(8):
    dr = dr + c0r[k] * c4r[k] + c0i[k] * c4i[k]
    di = di + c0r[k] * c4i[k] - c0i[k] * c4r[k]
assert abs(dr - 0.0) < 1e-9
assert abs(di) < 1e-9
dr = 0.0
di = 0.0
for k in range(8):
    dr = dr + c0r[k] * c5r[k] + c0i[k] * c5i[k]
    di = di + c0r[k] * c5i[k] - c0i[k] * c5r[k]
assert abs(dr - 0.0) < 1e-9
assert abs(di) < 1e-9
dr = 0.0
di = 0.0
for k in range(8):
    dr = dr + c0r[k] * c6r[k] + c0i[k] * c6i[k]
    di = di + c0r[k] * c6i[k] - c0i[k] * c6r[k]
assert abs(dr - 0.0) < 1e-9
assert abs(di) < 1e-9
dr = 0.0
di = 0.0
for k in range(8):
    dr = dr + c0r[k] * c7r[k] + c0i[k] * c7i[k]
    di = di + c0r[k] * c7i[k] - c0i[k] * c7r[k]
assert abs(dr - 0.0) < 1e-9
assert abs(di) < 1e-9
dr = 0.0
di = 0.0
for k in range(8):
    dr = dr + c1r[k] * c0r[k] + c1i[k] * c0i[k]
    di = di + c1r[k] * c0i[k] - c1i[k] * c0r[k]
assert abs(dr - 0.0) < 1e-9
assert abs(di) < 1e-9
dr = 0.0
di = 0.0
for k in range(8):
    dr = dr + c1r[k] * c1r[k] + c1i[k] * c1i[k]
    di = di + c1r[k] * c1i[k] - c1i[k] * c1r[k]
assert abs(dr - 1.0) < 1e-9
assert abs(di) < 1e-9
dr = 0.0
di = 0.0
for k in range(8):
    dr = dr + c1r[k] * c2r[k] + c1i[k] * c2i[k]
    di = di + c1r[k] * c2i[k] - c1i[k] * c2r[k]
assert abs(dr - 0.0) < 1e-9
assert abs(di) < 1e-9
dr = 0.0
di = 0.0
for k in range(8):
    dr = dr + c1r[k] * c3r[k] + c1i[k] * c3i[k]
    di = di + c1r[k] * c3i[k] - c1i[k] * c3r[k]
assert abs(dr - 0.0) < 1e-9
assert abs(di) < 1e-9
dr = 0.0
di = 0.0
for k in range(8):
    dr = dr + c1r[k] * c4r[k] + c1i[k] * c4i[k]
    di = di + c1r[k] * c4i[k] - c1i[k] * c4r[k]
assert abs(dr - 0.0) < 1e-9
assert abs(di) < 1e-9
dr = 0.0
di = 0.0
for k in range(8):
    dr = dr + c1r[k] * c5r[k] + c1i[k] * c5i[k]
    di = di + c1r[k] * c5i[k] - c1i[k] * c5r[k]
assert abs(dr - 0.0) < 1e-9
assert abs(di) < 1e-9
dr = 0.0
di = 0.0
for k in range(8):
    dr = dr + c1r[k] * c6r[k] + c1i[k] * c6i[k]
    di = di + c1r[k] * c6i[k] - c1i[k] * c6r[k]
assert abs(dr - 0.0) < 1e-9
assert abs(di) < 1e-9
dr = 0.0
di = 0.0
for k in range(8):
    dr = dr + c1r[k] * c7r[k] + c1i[k] * c7i[k]
    di = di + c1r[k] * c7i[k] - c1i[k] * c7r[k]
assert abs(dr - 0.0) < 1e-9
assert abs(di) < 1e-9
dr = 0.0
di = 0.0
for k in range(8):
    dr = dr + c2r[k] * c0r[k] + c2i[k] * c0i[k]
    di = di + c2r[k] * c0i[k] - c2i[k] * c0r[k]
assert abs(dr - 0.0) < 1e-9
assert abs(di) < 1e-9
dr = 0.0
di = 0.0
for k in range(8):
    dr = dr + c2r[k] * c1r[k] + c2i[k] * c1i[k]
    di = di + c2r[k] * c1i[k] - c2i[k] * c1r[k]
assert abs(dr - 0.0) < 1e-9
assert abs(di) < 1e-9
dr = 0.0
di = 0.0
for k in range(8):
    dr = dr + c2r[k] * c2r[k] + c2i[k] * c2i[k]
    di = di + c2r[k] * c2i[k] - c2i[k] * c2r[k]
assert abs(dr - 1.0) < 1e-9
assert abs(di) < 1e-9
dr = 0.0
di = 0.0
for k in range(8):
    dr = dr + c2r[k] * c3r[k] + c2i[k] * c3i[k]
    di = di + c2r[k] * c3i[k] - c2i[k] * c3r[k]
assert abs(dr - 0.0) < 1e-9
assert abs(di) < 1e-9
dr = 0.0
di = 0.0
for k in range(8):
    dr = dr + c2r[k] * c4r[k] + c2i[k] * c4i[k]
    di = di + c2r[k] * c4i[k] - c2i[k] * c4r[k]
assert abs(dr - 0.0) < 1e-9
assert abs(di) < 1e-9
dr = 0.0
di = 0.0
for k in range(8):
    dr = dr + c2r[k] * c5r[k] + c2i[k] * c5i[k]
    di = di + c2r[k] * c5i[k] - c2i[k] * c5r[k]
assert abs(dr - 0.0) < 1e-9
assert abs(di) < 1e-9
dr = 0.0
di = 0.0
for k in range(8):
    dr = dr + c2r[k] * c6r[k] + c2i[k] * c6i[k]
    di = di + c2r[k] * c6i[k] - c2i[k] * c6r[k]
assert abs(dr - 0.0) < 1e-9
assert abs(di) < 1e-9
dr = 0.0
di = 0.0
for k in range(8):
    dr = dr + c2r[k] * c7r[k] + c2i[k] * c7i[k]
    di = di + c2r[k] * c7i[k] - c2i[k] * c7r[k]
assert abs(dr - 0.0) < 1e-9
assert abs(di) < 1e-9
dr = 0.0
di = 0.0
for k in range(8):
    dr = dr + c3r[k] * c0r[k] + c3i[k] * c0i[k]
    di = di + c3r[k] * c0i[k] - c3i[k] * c0r[k]
assert abs(dr - 0.0) < 1e-9
assert abs(di) < 1e-9
dr = 0.0
di = 0.0
for k in range(8):
    dr = dr + c3r[k] * c1r[k] + c3i[k] * c1i[k]
    di = di + c3r[k] * c1i[k] - c3i[k] * c1r[k]
assert abs(dr - 0.0) < 1e-9
assert abs(di) < 1e-9
dr = 0.0
di = 0.0
for k in range(8):
    dr = dr + c3r[k] * c2r[k] + c3i[k] * c2i[k]
    di = di + c3r[k] * c2i[k] - c3i[k] * c2r[k]
assert abs(dr - 0.0) < 1e-9
assert abs(di) < 1e-9
dr = 0.0
di = 0.0
for k in range(8):
    dr = dr + c3r[k] * c3r[k] + c3i[k] * c3i[k]
    di = di + c3r[k] * c3i[k] - c3i[k] * c3r[k]
assert abs(dr - 1.0) < 1e-9
assert abs(di) < 1e-9
dr = 0.0
di = 0.0
for k in range(8):
    dr = dr + c3r[k] * c4r[k] + c3i[k] * c4i[k]
    di = di + c3r[k] * c4i[k] - c3i[k] * c4r[k]
assert abs(dr - 0.0) < 1e-9
assert abs(di) < 1e-9
dr = 0.0
di = 0.0
for k in range(8):
    dr = dr + c3r[k] * c5r[k] + c3i[k] * c5i[k]
    di = di + c3r[k] * c5i[k] - c3i[k] * c5r[k]
assert abs(dr - 0.0) < 1e-9
assert abs(di) < 1e-9
dr = 0.0
di = 0.0
for k in range(8):
    dr = dr + c3r[k] * c6r[k] + c3i[k] * c6i[k]
    di = di + c3r[k] * c6i[k] - c3i[k] * c6r[k]
assert abs(dr - 0.0) < 1e-9
assert abs(di) < 1e-9
dr = 0.0
di = 0.0
for k in range(8):
    dr = dr + c3r[k] * c7r[k] + c3i[k] * c7i[k]
    di = di + c3r[k] * c7i[k] - c3i[k] * c7r[k]
assert abs(dr - 0.0) < 1e-9
assert abs(di) < 1e-9
dr = 0.0
di = 0.0
for k in range(8):
    dr = dr + c4r[k] * c0r[k] + c4i[k] * c0i[k]
    di = di + c4r[k] * c0i[k] - c4i[k] * c0r[k]
assert abs(dr - 0.0) < 1e-9
assert abs(di) < 1e-9
dr = 0.0
di = 0.0
for k in range(8):
    dr = dr + c4r[k] * c1r[k] + c4i[k] * c1i[k]
    di = di + c4r[k] * c1i[k] - c4i[k] * c1r[k]
assert abs(dr - 0.0) < 1e-9
assert abs(di) < 1e-9
dr = 0.0
di = 0.0
for k in range(8):
    dr = dr + c4r[k] * c2r[k] + c4i[k] * c2i[k]
    di = di + c4r[k] * c2i[k] - c4i[k] * c2r[k]
assert abs(dr - 0.0) < 1e-9
assert abs(di) < 1e-9
dr = 0.0
di = 0.0
for k in range(8):
    dr = dr + c4r[k] * c3r[k] + c4i[k] * c3i[k]
    di = di + c4r[k] * c3i[k] - c4i[k] * c3r[k]
assert abs(dr - 0.0) < 1e-9
assert abs(di) < 1e-9
dr = 0.0
di = 0.0
for k in range(8):
    dr = dr + c4r[k] * c4r[k] + c4i[k] * c4i[k]
    di = di + c4r[k] * c4i[k] - c4i[k] * c4r[k]
assert abs(dr - 1.0) < 1e-9
assert abs(di) < 1e-9
dr = 0.0
di = 0.0
for k in range(8):
    dr = dr + c4r[k] * c5r[k] + c4i[k] * c5i[k]
    di = di + c4r[k] * c5i[k] - c4i[k] * c5r[k]
assert abs(dr - 0.0) < 1e-9
assert abs(di) < 1e-9
dr = 0.0
di = 0.0
for k in range(8):
    dr = dr + c4r[k] * c6r[k] + c4i[k] * c6i[k]
    di = di + c4r[k] * c6i[k] - c4i[k] * c6r[k]
assert abs(dr - 0.0) < 1e-9
assert abs(di) < 1e-9
dr = 0.0
di = 0.0
for k in range(8):
    dr = dr + c4r[k] * c7r[k] + c4i[k] * c7i[k]
    di = di + c4r[k] * c7i[k] - c4i[k] * c7r[k]
assert abs(dr - 0.0) < 1e-9
assert abs(di) < 1e-9
dr = 0.0
di = 0.0
for k in range(8):
    dr = dr + c5r[k] * c0r[k] + c5i[k] * c0i[k]
    di = di + c5r[k] * c0i[k] - c5i[k] * c0r[k]
assert abs(dr - 0.0) < 1e-9
assert abs(di) < 1e-9
dr = 0.0
di = 0.0
for k in range(8):
    dr = dr + c5r[k] * c1r[k] + c5i[k] * c1i[k]
    di = di + c5r[k] * c1i[k] - c5i[k] * c1r[k]
assert abs(dr - 0.0) < 1e-9
assert abs(di) < 1e-9
dr = 0.0
di = 0.0
for k in range(8):
    dr = dr + c5r[k] * c2r[k] + c5i[k] * c2i[k]
    di = di + c5r[k] * c2i[k] - c5i[k] * c2r[k]
assert abs(dr - 0.0) < 1e-9
assert abs(di) < 1e-9
dr = 0.0
di = 0.0
for k in range(8):
    dr = dr + c5r[k] * c3r[k] + c5i[k] * c3i[k]
    di = di + c5r[k] * c3i[k] - c5i[k] * c3r[k]
assert abs(dr - 0.0) < 1e-9
assert abs(di) < 1e-9
dr = 0.0
di = 0.0
for k in range(8):
    dr = dr + c5r[k] * c4r[k] + c5i[k] * c4i[k]
    di = di + c5r[k] * c4i[k] - c5i[k] * c4r[k]
assert abs(dr - 0.0) < 1e-9
assert abs(di) < 1e-9
dr = 0.0
di = 0.0
for k in range(8):
    dr = dr + c5r[k] * c5r[k] + c5i[k] * c5i[k]
    di = di + c5r[k] * c5i[k] - c5i[k] * c5r[k]
assert abs(dr - 1.0) < 1e-9
assert abs(di) < 1e-9
dr = 0.0
di = 0.0
for k in range(8):
    dr = dr + c5r[k] * c6r[k] + c5i[k] * c6i[k]
    di = di + c5r[k] * c6i[k] - c5i[k] * c6r[k]
assert abs(dr - 0.0) < 1e-9
assert abs(di) < 1e-9
dr = 0.0
di = 0.0
for k in range(8):
    dr = dr + c5r[k] * c7r[k] + c5i[k] * c7i[k]
    di = di + c5r[k] * c7i[k] - c5i[k] * c7r[k]
assert abs(dr - 0.0) < 1e-9
assert abs(di) < 1e-9
dr = 0.0
di = 0.0
for k in range(8):
    dr = dr + c6r[k] * c0r[k] + c6i[k] * c0i[k]
    di = di + c6r[k] * c0i[k] - c6i[k] * c0r[k]
assert abs(dr - 0.0) < 1e-9
assert abs(di) < 1e-9
dr = 0.0
di = 0.0
for k in range(8):
    dr = dr + c6r[k] * c1r[k] + c6i[k] * c1i[k]
    di = di + c6r[k] * c1i[k] - c6i[k] * c1r[k]
assert abs(dr - 0.0) < 1e-9
assert abs(di) < 1e-9
dr = 0.0
di = 0.0
for k in range(8):
    dr = dr + c6r[k] * c2r[k] + c6i[k] * c2i[k]
    di = di + c6r[k] * c2i[k] - c6i[k] * c2r[k]
assert abs(dr - 0.0) < 1e-9
assert abs(di) < 1e-9
dr = 0.0
di = 0.0
for k in range(8):
    dr = dr + c6r[k] * c3r[k] + c6i[k] * c3i[k]
    di = di + c6r[k] * c3i[k] - c6i[k] * c3r[k]
assert abs(dr - 0.0) < 1e-9
assert abs(di) < 1e-9
dr = 0.0
di = 0.0
for k in range(8):
    dr = dr + c6r[k] * c4r[k] + c6i[k] * c4i[k]
    di = di + c6r[k] * c4i[k] - c6i[k] * c4r[k]
assert abs(dr - 0.0) < 1e-9
assert abs(di) < 1e-9
dr = 0.0
di = 0.0
for k in range(8):
    dr = dr + c6r[k] * c5r[k] + c6i[k] * c5i[k]
    di = di + c6r[k] * c5i[k] - c6i[k] * c5r[k]
assert abs(dr - 0.0) < 1e-9
assert abs(di) < 1e-9
dr = 0.0
di = 0.0
for k in range(8):
    dr = dr + c6r[k] * c6r[k] + c6i[k] * c6i[k]
    di = di + c6r[k] * c6i[k] - c6i[k] * c6r[k]
assert abs(dr - 1.0) < 1e-9
assert abs(di) < 1e-9
dr = 0.0
di = 0.0
for k in range(8):
    dr = dr + c6r[k] * c7r[k] + c6i[k] * c7i[k]
    di = di + c6r[k] * c7i[k] - c6i[k] * c7r[k]
assert abs(dr - 0.0) < 1e-9
assert abs(di) < 1e-9
dr = 0.0
di = 0.0
for k in range(8):
    dr = dr + c7r[k] * c0r[k] + c7i[k] * c0i[k]
    di = di + c7r[k] * c0i[k] - c7i[k] * c0r[k]
assert abs(dr - 0.0) < 1e-9
assert abs(di) < 1e-9
dr = 0.0
di = 0.0
for k in range(8):
    dr = dr + c7r[k] * c1r[k] + c7i[k] * c1i[k]
    di = di + c7r[k] * c1i[k] - c7i[k] * c1r[k]
assert abs(dr - 0.0) < 1e-9
assert abs(di) < 1e-9
dr = 0.0
di = 0.0
for k in range(8):
    dr = dr + c7r[k] * c2r[k] + c7i[k] * c2i[k]
    di = di + c7r[k] * c2i[k] - c7i[k] * c2r[k]
assert abs(dr - 0.0) < 1e-9
assert abs(di) < 1e-9
dr = 0.0
di = 0.0
for k in range(8):
    dr = dr + c7r[k] * c3r[k] + c7i[k] * c3i[k]
    di = di + c7r[k] * c3i[k] - c7i[k] * c3r[k]
assert abs(dr - 0.0) < 1e-9
assert abs(di) < 1e-9
dr = 0.0
di = 0.0
for k in range(8):
    dr = dr + c7r[k] * c4r[k] + c7i[k] * c4i[k]
    di = di + c7r[k] * c4i[k] - c7i[k] * c4r[k]
assert abs(dr - 0.0) < 1e-9
assert abs(di) < 1e-9
dr = 0.0
di = 0.0
for k in range(8):
    dr = dr + c7r[k] * c5r[k] + c7i[k] * c5i[k]
    di = di + c7r[k] * c5i[k] - c7i[k] * c5r[k]
assert abs(dr - 0.0) < 1e-9
assert abs(di) < 1e-9
dr = 0.0
di = 0.0
for k in range(8):
    dr = dr + c7r[k] * c6r[k] + c7i[k] * c6i[k]
    di = di + c7r[k] * c6i[k] - c7i[k] * c6r[k]
assert abs(dr - 0.0) < 1e-9
assert abs(di) < 1e-9
dr = 0.0
di = 0.0
for k in range(8):
    dr = dr + c7r[k] * c7r[k] + c7i[k] * c7i[k]
    di = di + c7r[k] * c7i[k] - c7i[k] * c7r[k]
assert abs(dr - 1.0) < 1e-9
assert abs(di) < 1e-9
