"""
experimento_ordenacao.py
------------------------
Roda os três algoritmos de ordenação (Insertion Sort, Merge Sort, Quick Sort)
nos vetores de 1.000, 10.000 e 100.000 elementos e exibe os resultados.

Dependências: matplotlib (pip install matplotlib)
Uso: python experimento_ordenacao.py
"""

import time
import random
import math
import sys
import signal
import matplotlib
matplotlib.use('Agg')   # troca pra 'TkAgg' se quiser janela interativa
import matplotlib.pyplot as plt
import numpy as np

# ── imports dos algoritmos (se rodar tudo junto)
from insertion_sort import insertion_sort
from merge_sort import merge_sort
from quick_sort import quick_sort

# ─────────────────────────────────────────────
# TIMEOUT
# ─────────────────────────────────────────────
LIMITE_SEGUNDOS = 300  # 5 minutos

class TimeoutError(Exception):
    pass

def _timeout_handler(signum, frame):
    raise TimeoutError()

def rodar_com_timeout(func, arr, limite=LIMITE_SEGUNDOS):
    """Executa func(arr) com limite de tempo. Retorna (tempo, moves) ou None se N/C."""
    signal.signal(signal.SIGABRT, _timeout_handler)
    signal.alarm(limite)
    try:
        t0 = time.perf_counter()
        _, moves = func(arr[:])
        elapsed = time.perf_counter() - t0
        signal.alarm(0)
        return elapsed, moves
    except TimeoutError:
        signal.alarm(0)
        return None

# ─────────────────────────────────────────────
# EXPERIMENTO
# ─────────────────────────────────────────────

TAMANHOS = [1000, 10000, 100000]
REPETICOES = 3

algoritmos = [
    ("Insertion Sort", insertion_sort),
    ("Merge Sort",     merge_sort),
    ("Quick Sort",     quick_sort),
]

# IMPORTANTE: mesmo vetor base para cada tamanho → comparação justa
resultados = {}

print("=" * 65)
print("  EXPERIMENTO: COMPARAÇÃO DE ALGORITMOS DE ORDENAÇÃO")
print("=" * 65)

for nome, func in algoritmos:
    resultados[nome] = {}
    print(f"\n>>> {nome}")
    for n in TAMANHOS:
        random.seed(n)
        vetor_base = [random.randint(1, 10 * n) for _ in range(n)]

        tempos = []
        movs   = []
        nc     = False

        for run in range(1, REPETICOES + 1):
            resultado = rodar_com_timeout(func, vetor_base)
            if resultado is None:
                print(f"  n={n:>7}  run{run}: N/C (> {LIMITE_SEGUNDOS}s)")
                nc = True
                break
            t, m = resultado
            tempos.append(t)
            movs.append(m)
            print(f"  n={n:>7}  run{run}: {t:.6f}s  operações={m:,}")

        if nc:
            resultados[nome][n] = {"nc": True}
        else:
            avg = sum(tempos) / REPETICOES
            std = math.sqrt(sum((t - avg)**2 for t in tempos) / (REPETICOES - 1))
            avg_mov = int(sum(movs) / REPETICOES)
            resultados[nome][n] = {
                "nc":     False,
                "tempos": tempos,
                "avg":    avg,
                "std":    std,
                "moves":  avg_mov,
            }
            print(f"         → média={avg:.6f}s  dp={std:.8f}s  ops_médias={avg_mov:,}")

# ─────────────────────────────────────────────
# RESUMO
# ─────────────────────────────────────────────
print("\n" + "=" * 65)
print("  RESUMO")
print("=" * 65)
header = f"{'Algoritmo':<18} {'n':>8}  {'Média (s)':>12}  {'DP (s)':>12}  {'Operações':>14}"
print(header)
print("-" * 65)
for nome, _ in algoritmos:
    for n in TAMANHOS:
        d = resultados[nome][n]
        if d["nc"]:
            print(f"{nome:<18} {n:>8}  {'N/C':>12}  {'N/C':>12}  {'N/C':>14}")
        else:
            print(f"{nome:<18} {n:>8}  {d['avg']:>12.6f}  {d['std']:>12.8f}  {d['moves']:>14,}")

# ─────────────────────────────────────────────
# GRÁFICO
# ─────────────────────────────────────────────
CORES = {
    "Insertion Sort": "#ff5c8a",
    "Merge Sort":     "#6ee7f7",
    "Quick Sort":     "#b5f0a5",
}

fig, axes = plt.subplots(1, 2, figsize=(15, 6))
fig.patch.set_facecolor('#0f0f11')

for ax in axes:
    ax.set_facecolor('#1a1a24')
    ax.tick_params(colors='#cccccc')
    ax.xaxis.label.set_color('#cccccc')
    ax.yaxis.label.set_color('#cccccc')
    ax.title.set_color('#eeeeee')
    for spine in ax.spines.values():
        spine.set_edgecolor('#333344')
    ax.grid(True, color='#2a2a3a', linewidth=0.5)

# — Gráfico 1: tempo médio (log-log)
ax1 = axes[0]
for nome, _ in algoritmos:
    xs_v, ys_v, es_v = [], [], []
    for n in TAMANHOS:
        d = resultados[nome][n]
        if not d["nc"]:
            xs_v.append(n); ys_v.append(d["avg"]); es_v.append(d["std"])
    if xs_v:
        ax1.errorbar(xs_v, ys_v, yerr=es_v, fmt='o-', color=CORES[nome],
                     linewidth=2, markersize=6, capsize=4, label=nome)
    # Marca N/C
    for n in TAMANHOS:
        if resultados[nome][n]["nc"]:
            ax1.annotate("N/C", xy=(n, ax1.get_ylim()[0] if ax1.get_ylim()[0] > 0 else 0.001),
                         ha='center', fontsize=8, color=CORES[nome], style='italic')

ax1.set_xscale('log'); ax1.set_yscale('log')
ax1.set_title('Tempo Médio de Execução\n(escala log-log)', fontsize=12, pad=10)
ax1.set_xlabel('Tamanho do vetor (n)')
ax1.set_ylabel('Tempo médio (s)')
ax1.set_xticks(TAMANHOS)
ax1.set_xticklabels(['1.000', '10.000', '100.000'])
ax1.legend(facecolor='#1a1a24', edgecolor='#444455', labelcolor='#cccccc', fontsize=9)

# — Gráfico 2: trocas/movimentações
ax2 = axes[1]
x = np.arange(len(TAMANHOS))
width = 0.28
for i, (nome, _) in enumerate(algoritmos):
    mvs = [resultados[nome][n].get("moves", 0) if not resultados[nome][n]["nc"] else 0
           for n in TAMANHOS]
    bars = ax2.bar(x + i * width, mvs, width, label=nome, color=CORES[nome], alpha=0.85)
    for bar, m, n in zip(bars, mvs, TAMANHOS):
        if not resultados[nome][n]["nc"] and m > 0:
            ax2.text(bar.get_x() + bar.get_width() / 2, bar.get_height() * 1.02,
                     f'{m:,.0f}', ha='center', va='bottom', fontsize=7,
                     color='#cccccc', rotation=90)

ax2.set_title('Trocas / Movimentações por Algoritmo', fontsize=12, pad=10)
ax2.set_xlabel('Tamanho do vetor (n)')
ax2.set_ylabel('Número de operações')
ax2.set_xticks(x + width)
ax2.set_xticklabels(['1.000', '10.000', '100.000'])
ax2.legend(facecolor='#1a1a24', edgecolor='#444455', labelcolor='#cccccc', fontsize=9)
ax2.tick_params(colors='#cccccc')

plt.suptitle('Comparação de Algoritmos de Ordenação', color='#ffffff',
             fontsize=14, fontweight='bold', y=1.01)
plt.tight_layout()
plt.savefig('grafico_ordenacao.png', dpi=150, bbox_inches='tight', facecolor='#0f0f11')
print("\nGráfico salvo em: grafico_ordenacao.png")
plt.show()
