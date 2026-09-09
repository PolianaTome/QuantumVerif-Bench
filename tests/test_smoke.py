"""Smoke tests: run every benchmark with plain python3 (no ESBMC) to catch
basic execution errors (syntax errors, typos, wrong indexing, etc.) quickly,
without needing to invoke the SMT solver.

ESBMC's Python front-end recognizes nondet_bool(), nondet_int(),
nondet_float() and __ESBMC_assume() as intrinsics without any import (see
docs/methodology.md); plain CPython does not know them, so this module
provides minimal stand-ins and injects them into the executed benchmark's
namespace. Since ESBMC has already proven every assertion holds for every
nondet_bool() branch, a random True/False choice here cannot make a
benchmark fail for the "wrong" branch.
"""

import glob
import os
import random

import pytest

BENCHMARKS_DIR = os.path.join(os.path.dirname(__file__), "..", "benchmarks")


def nondet_bool():
    return random.choice([True, False])


def nondet_int():
    return random.randint(-10, 10)


def nondet_float():
    return random.uniform(-10.0, 10.0)


def __esbmc_assume_stub(condition):
    pass


def _discover_benchmark_files():
    pattern = os.path.join(BENCHMARKS_DIR, "*", "*.py")
    files = sorted(glob.glob(pattern))
    return [f for f in files if os.path.basename(os.path.dirname(f)) != "_spike"]


@pytest.mark.parametrize("path", _discover_benchmark_files())
def test_benchmark_runs_without_error(path):
    with open(path, "r", encoding="utf-8") as f:
        source = f.read()

    namespace = {
        "__name__": "__main__",
        "nondet_bool": nondet_bool,
        "nondet_int": nondet_int,
        "nondet_float": nondet_float,
        "__ESBMC_assume": __esbmc_assume_stub,
    }
    exec(compile(source, path, "exec"), namespace)
