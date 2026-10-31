#!/usr/bin/env bash
# Roda o ESBMC em um arquivo e acrescenta uma linha em results.tsv.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
cd "$SCRIPT_DIR"
f="$1"
if [[ "$f" != /* ]]; then
  if [[ -f "$PROJECT_ROOT/$f" ]]; then
    f="$PROJECT_ROOT/$f"
  else
    f="$SCRIPT_DIR/$f"
  fi
fi
b="$(basename "${f%.py}")"; T="${TMO:-240}"
PY="$PROJECT_ROOT/.venv/bin/python"
if [ ! -x "$PY" ]; then PY=python3; fi
grep -q "^$b	" results.tsv 2>/dev/null && exit 0
s=$(date +%s.%N)
# Teto de memória num cgroup próprio: se o ESBMC estourar, só ele morre em
# vez de o OOM atingir o init.scope e derrubar o WSL inteiro. OOMPolicy=continue
# evita que o systemd mate também este script; o OOM é lido do journal.
M="${MEM_MAX:-2500M}"; U="esbmc-$$-$RANDOM"
systemd-run --user --scope -q --unit="$U" -p MemoryMax="$M" -p MemorySwapMax=0 -p OOMPolicy=continue \
  /usr/bin/time -f "%M" -o "logs/$b.mem" timeout "$T" esbmc --python $PY "$f" > "logs/$b.log" 2>&1
oom=0; journalctl --user -u "$U.scope" -o cat --no-pager 2>/dev/null | grep -q "OOM killer" && oom=1
e=$(date +%s.%N)
v=$(grep -oE "VERIFICATION (SUCCESSFUL|FAILED)" "logs/$b.log" | tail -1 | sed 's/VERIFICATION //')
grep -q "status 124" "logs/$b.mem" && v="TIMEOUT(${T}s)"
[ "$oom" -eq 1 ] && v="OOM(${M})"
[ -z "$v" ] && v="ERROR"
vcc=$(grep -oE "[0-9]+ remaining after" "logs/$b.log" | grep -oE "^[0-9]+")
mem=$(tail -1 "logs/$b.mem" | grep -E "^[0-9]+$" || echo 0)
printf "%s\t%s\t%.1f\t%s\t%s\n" "$b" "$v" "$(echo "$e - $s" | bc)" "$vcc" "$((mem/1024))" >> results.tsv
