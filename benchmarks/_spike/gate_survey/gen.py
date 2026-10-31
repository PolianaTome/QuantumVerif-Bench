"""Gera um arquivo ESBMC por (porta, propriedade) para o levantamento de portas
unitárias suportadas. P1: U^dagger U = I com matriz concreta. P2: U^dagger(U psi) = psi
com psi simbólico. P3: norma preservada com psi simbólico normalizado."""
S = "0.70710678118654752440"
def perm(n, p):
    return lambda: [(f"re[{p.get(k,k)}]", f"im[{p.get(k,k)}]") for k in range(2**n)]
def neg(n, idx):
    return lambda: [((f"0.0 - re[{k}]", f"0.0 - im[{k}]") if k in idx else (f"re[{k}]", f"im[{k}]")) for k in range(2**n)]
Hact = lambda: [(f"{S} * (re[0] + re[1])",f"{S} * (im[0] + im[1])"),(f"{S} * (re[0] - re[1])",f"{S} * (im[0] - im[1])")]
Yact = lambda: [("im[1]","0.0 - re[1]"),("0.0 - im[0]","re[0]")]
G = {
 "I":   (1, perm(1,{}), perm(1,{})),
 "X":   (1, perm(1,{0:1,1:0}), perm(1,{0:1,1:0})),
 "Y":   (1, Yact, Yact),
 "Z":   (1, neg(1,{1}), neg(1,{1})),
 "H":   (1, Hact, Hact),
 "S":   (1, lambda: [("re[0]","im[0]"),("0.0 - im[1]","re[1]")], lambda: [("re[0]","im[0]"),("im[1]","0.0 - re[1]")]),
 "T":   (1, lambda: [("re[0]","im[0]"),(f"{S} * (re[1] - im[1])",f"{S} * (re[1] + im[1])")],
            lambda: [("re[0]","im[0]"),(f"{S} * (re[1] + im[1])",f"{S} * (im[1] - re[1])")]),
 "CNOT":(2, perm(2,{2:3,3:2}), perm(2,{2:3,3:2})),
 "CZ":  (2, neg(2,{3}), neg(2,{3})),
 "SWAP":(2, perm(2,{1:2,2:1}), perm(2,{1:2,2:1})),
 "TOFFOLI":(3, perm(3,{6:7,7:6}), perm(3,{6:7,7:6})),
 "FREDKIN":(3, perm(3,{5:6,6:5}), perm(3,{5:6,6:5})),
 "H_BUG":(1, lambda: [("re[0] + re[1]","im[0] + im[1]"),("re[0] - re[1]","im[0] - im[1]")], None),
}
def apply(L, act):
    ex = act()
    L += ["nre = [" + ", ".join(e[0] for e in ex) + "]", "nim = [" + ", ".join(e[1] for e in ex) + "]", "re = nre", "im = nim"]
def sym(L, N):
    L += ["re = [" + ", ".join(["nondet_float()"]*N) + "]", "im = [" + ", ".join(["nondet_float()"]*N) + "]",
          f"for i in range({N}):", "    __ESBMC_assume(re[i] >= -1.0 and re[i] <= 1.0)", "    __ESBMC_assume(im[i] >= -1.0 and im[i] <= 1.0)"]
def norm(L, N, v):
    L += [f"{v} = 0.0", f"for i in range({N}):", f"    {v} = {v} + re[i] * re[i] + im[i] * im[i]"]
for name,(n,act,adj) in G.items():
    N = 2**n
    if adj is not None:
        L = []
        for b in range(N):
            L += ["re = [" + ", ".join("1.0" if k==b else "0.0" for k in range(N)) + "]", "im = [" + ", ".join(["0.0"]*N) + "]"]
            apply(L, act); L += [f"c{b}r = re", f"c{b}i = im"]
        for a in range(N):
            for b in range(N):
                L += ["dr = 0.0", "di = 0.0", f"for k in range({N}):",
                      f"    dr = dr + c{a}r[k] * c{b}r[k] + c{a}i[k] * c{b}i[k]",
                      f"    di = di + c{a}r[k] * c{b}i[k] - c{a}i[k] * c{b}r[k]",
                      f"assert abs(dr - {1.0 if a==b else 0.0}) < 1e-9", "assert abs(di) < 1e-9"]
        open(f"{name}__P1_unitary_concrete.py","w").write("\n".join(L)+"\n")
        L = []; sym(L, N); L += ["r0 = re", "i0 = im"]; apply(L, act); apply(L, adj)
        L += [f"for i in range({N}):", "    assert abs(re[i] - r0[i]) < 1e-9", "    assert abs(im[i] - i0[i]) < 1e-9"]
        open(f"{name}__P2_inverse_symbolic.py","w").write("\n".join(L)+"\n")
    L = []; sym(L, N); norm(L, N, "n0")
    L.append("__ESBMC_assume(n0 > 1.0 - 1e-6 and n0 < 1.0 + 1e-6)")
    apply(L, act); norm(L, N, "n1"); L.append("assert abs(n1 - 1.0) < 1e-5")
    open(f"{name}__P3_norm_symbolic.py","w").write("\n".join(L)+"\n")
