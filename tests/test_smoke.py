"""Smoke tests: roda cada benchmark com o python3 puro (sem ESBMC) para
pegar erros básicos de execução (erros de sintaxe, digitação, indexação
errada, etc.) rapidamente, sem precisar chamar o solver SMT.

O front-end Python do ESBMC reconhece nondet_bool(), nondet_int(),
nondet_float() e __ESBMC_assume() como intrínsecos, sem nenhum import (veja
docs/methodology.md); o CPython puro não os conhece, então este módulo
fornece substitutos mínimos e os injeta no namespace do benchmark executado.
Como o ESBMC já provou que toda asserção vale para todo ramo de
nondet_bool(), uma escolha aleatória de True/False aqui não pode fazer um
benchmark falhar pelo ramo "errado".
"""

import glob
import os
import random

import pytest

# Diretório contendo benchmarks/<nome>/<nome>.py, resolvido em relação a
# este arquivo de teste para que o pytest possa ser chamado de qualquer
# diretório de trabalho.
BENCHMARKS_DIR = os.path.join(os.path.dirname(__file__), "..", "benchmarks")


def nondet_bool():
    """Substituto para o intrínseco nondet_bool() do ESBMC: sob o CPython
    puro não há execução simbólica, então isso apenas sorteia um ramo
    concreto ao acaso, em vez de explorar os dois."""
    return random.choice([True, False])


def nondet_int():
    """Substituto para o intrínseco nondet_int() do ESBMC (não usado pelos
    benchmarks atuais, fornecido para completude/benchmarks futuros)."""
    return random.randint(-10, 10)


def nondet_float():
    """Substituto para o intrínseco nondet_float() do ESBMC (não usado pelos
    benchmarks atuais, fornecido para completude/benchmarks futuros)."""
    return random.uniform(-10.0, 10.0)


def __esbmc_assume_stub(condition):
    """Substituto para o __ESBMC_assume() do ESBMC: sob o CPython puro não
    há espaço de busca simbólico para restringir, então isso é um no-op."""
    pass


def _discover_benchmark_files():
    """Retorna cada arquivo benchmarks/<nome>/<nome>.py, pulando _spike/
    (são sondagens pontuais de viabilidade, não fazem parte da suíte de
    benchmarks)."""
    pattern = os.path.join(BENCHMARKS_DIR, "*", "*.py")
    files = sorted(glob.glob(pattern))
    return [f for f in files if os.path.basename(os.path.dirname(f)) != "_spike"]


@pytest.mark.parametrize("path", _discover_benchmark_files())
def test_benchmark_runs_without_error(path):
    """Executa um arquivo de benchmark como um script Python comum, com os
    intrínsecos exclusivos do ESBMC substituídos, e deixa o pytest falhar o
    teste se rodá-lo lançar qualquer exceção."""
    with open(path, "r", encoding="utf-8") as f:
        source = f.read()

    # Namespace novo para cada benchmark, semeado apenas com os intrínsecos
    # que o código-fonte de cada benchmark espera encontrar em escopo de módulo.
    namespace = {
        "__name__": "__main__",
        "nondet_bool": nondet_bool,
        "nondet_int": nondet_int,
        "nondet_float": nondet_float,
        "__ESBMC_assume": __esbmc_assume_stub,
    }
    exec(compile(source, path, "exec"), namespace)
