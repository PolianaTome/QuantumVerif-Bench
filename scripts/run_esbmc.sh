#!/usr/bin/env bash
# Roda o ESBMC nos benchmarks do QuantumVerif-Bench e salva cada log de
# verificação em results/<nome-do-benchmark>.log.
#
# Uso:
#   scripts/run_esbmc.sh                       # roda todos os benchmarks/*/*.py (exceto _spike)
#   scripts/run_esbmc.sh benchmarks/bell/bell.py [mais arquivos...]

# -e: encerra no primeiro erro, -u: erro em variáveis não definidas,
# -o pipefail: um comando que falha dentro de um pipe faz o pipe inteiro
# falhar (não só o último estágio).
set -euo pipefail

# Resolve os caminhos relativos à localização deste próprio script, para que
# ele funcione não importa de qual diretório seja chamado.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Prefere o Python do venv do projeto (que tem numpy instalado) para que o
# front-end Python do ESBMC -- que invoca o interpretador apontado -- consiga
# de fato importar os pacotes que os benchmarks usam; usa o python3 do
# sistema como alternativa caso o venv ainda não tenha sido criado.
PYTHON_BIN="$PROJECT_ROOT/.venv/bin/python"
if [ ! -x "$PYTHON_BIN" ]; then
    PYTHON_BIN="python3"
fi

mkdir -p "$PROJECT_ROOT/results"

# Continue through the full suite, but let callers detect any failed run.
overall_status=0

# Teto de memória do ESBMC (sobrescreva com MEM_MAX=4G, por exemplo). Ele
# roda num cgroup próprio via systemd-run: se estourar, o OOM killer mata só
# o ESBMC (exit 137) em vez de atingir o init.scope e derrubar o WSL inteiro.
MEM_MAX="${MEM_MAX:-2500M}"

# Roda o ESBMC em um único arquivo de benchmark, nomeando o log de saída
# a partir do diretório que contém o benchmark (ex.:
# benchmarks/bell/bell.py -> results/bell.log).
run_one() {
    local file="$1"
    local name
    name="$(basename "$(dirname "$file")")"
    local log="$PROJECT_ROOT/results/${name}.log"

    echo "==> Verifying $file"
    # Redireciona stdout e stderr para o arquivo de log; reporta
    # sucesso/falha no console com base no código de saída do ESBMC, sem
    # deixar uma verificação falha abortar o script inteiro (senão o
    # set -e pararia o loop após o primeiro benchmark que falhasse).
    # OOMPolicy=continue: sem ele o systemd derruba o scope inteiro com
    # SIGTERM e mata também este script. O OOM é detectado pelo journal da
    # unidade, porque o processo morto pode ser o filho Python do front-end e
    # o ESBMC sai com um código próprio, não 137.
    local rc=0 unit="esbmc-$$-$RANDOM"
    systemd-run --user --scope -q --unit="$unit" -p MemoryMax="$MEM_MAX" \
        -p MemorySwapMax=0 -p OOMPolicy=continue \
        esbmc --python "$PYTHON_BIN" "$file" > "$log" 2>&1 || rc=$?
    if journalctl --user -u "$unit.scope" -o cat --no-pager 2>/dev/null | grep -q "OOM killer"; then
        rc=137
    fi
    if [ "$rc" -eq 0 ] && grep -q "VERIFICATION SUCCESSFUL" "$log"; then
        echo "    VERIFICATION SUCCESSFUL -> $log"
    elif [ "$rc" -eq 137 ]; then
        echo "    OUT OF MEMORY (limite $MEM_MAX) -> $log"
    else
        echo "    VERIFICATION FAILED or ERROR -> $log"
        overall_status=1
    fi
}

if [ "$#" -ge 1 ]; then
    # Arquivo(s) explícito(s) passado(s) na linha de comando: verifica só esses.
    for file in "$@"; do
        run_one "$file"
    done
else
    # Sem argumentos: descobre todo benchmarks/<nome>/<nome>.py, pulando o
    # diretório _spike/ (são sondagens pontuais de viabilidade, não fazem
    # parte da suíte de benchmarks propriamente dita).
    for file in "$PROJECT_ROOT"/benchmarks/*/*.py; do
        dir_name="$(basename "$(dirname "$file")")"
        if [ "$dir_name" = "_spike" ]; then
            continue
        fi
        run_one "$file"
    done
fi

exit "$overall_status"
