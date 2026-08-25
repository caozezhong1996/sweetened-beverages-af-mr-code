# -*- coding: utf-8 -*-
# v4 forest plot: v3.1 (AFGen primary) vs v4 (Nielsen 2018 primary) + alcohol positive control
from pathlib import Path
import sys, re
sys.path.insert(0, str(Path(sys.executable).parent.parent.parent))
from daimon_runtime import setup_plot
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

setup_plot()

ROOT = Path(r"C:\Users\64915\Documents\kimi\workspace\奶茶房颤MR_迁移包_20260822")
RES  = ROOT / "06_升级分析_v4" / "results"
OUT  = ROOT / "06_升级分析_v4" / "figures"
OUT.mkdir(parents=True, exist_ok=True)

def parse_orci(s):
    m = re.match(r"([\d.]+) \(([\d.]+)-([\d.]+)\)", str(s))
    return tuple(float(x) for x in m.groups()) if m else (np.nan, np.nan, np.nan)

master = pd.read_csv(RES / "MASTER_v4_compare.csv")
alc    = pd.read_csv(RES / "SUMMARY_v4_alcohol_control.csv")

# ---------- Panel A rows ----------
series_A = [
    ("AFGen 2018 (v3.1 primary, N=537k)",  "AFGen_OR",      "AFGen_P",      "#8c8c8c"),
    ("Nielsen 2018 (v4 new, N=1.03M)",     "Nielsen_OR",    "Nielsen_P",    "#c0392b"),
    ("EUR meta v3.1 (AFGen+FinnGen)",      "EURmeta_v31_OR","EURmeta_v31_P","#8c8c8c"),
    ("EUR meta v4 (Nielsen+FinnGen)",      "EURmeta_v4_OR", "EURmeta_v4_P", "#1a5276"),
]

rowsA = []  # (y, orr, lo, hi, label_line2, color, sig)
ylabelsA, yposA = [], []
y = 0.0
for _, r in master.iterrows():
    y += 1.6
    ylabelsA.append((y + 0.9, r["exposure"]))
    for name, orc, pc, color in series_A:
        orr, lo, hi = parse_orci(r[orc])
        p = float(r[pc])
        rowsA.append((y, orr, lo, hi, f"{orr:.2f} ({lo:.2f}\u2013{hi:.2f}), P={p:.3f}", color, p < 0.05))
        yposA.append((y, name))
        y += 1.0

# ---------- Panel B rows ----------
rowsB = []
ylabelsB, yposB = [], []
yb = 0.0
order = [("Alcoholic drinks per week (GSCAN)", "GSCAN drinks/week", "#1a5276"),
         ("Alcohol intake frequency (UKB)",   "UKB intake frequency", "#7d3c98")]
oc_names = {"ebi_a_GCST006414": "Nielsen 2018", "ebi_a_GCST006061": "AFGen 2018",
            "finn_b_I9_AF": "FinnGen R5", "bbj_a_71": "BBJ (EAS)", "EUR_meta_v4": "EUR meta v4"}
for expo, short, color in order:
    sub = alc[alc["exposure"] == expo]
    yb += 1.6
    ylabelsB.append((yb + 1.5, short))
    for oc in ["ebi_a_GCST006414", "ebi_a_GCST006061", "finn_b_I9_AF", "bbj_a_71", "EUR_meta_v4"]:
        rr = sub[sub["outcome"] == oc]
        if rr.empty:
            continue
        rr = rr.iloc[0]
        orr, lo, hi = parse_orci(rr["OR"])
        p = float(rr["P"])
        c = "#c0392b" if oc == "EUR_meta_v4" else color
        rowsB.append((yb, orr, lo, hi, f"{orr:.2f} ({lo:.2f}\u2013{hi:.2f}), P={p:.3f}", c, p < 0.05))
        yposB.append((yb, oc_names[oc]))
        yb += 1.0

fig, (axA, axB) = plt.subplots(
    2, 1, figsize=(11.5, 13.5),
    gridspec_kw={"height_ratios": [y, yb]}, constrained_layout=True)

for ax in (axA, axB):
    ax.axvline(1.0, ls="--", lw=1, color="0.4", zorder=1)
    ax.set_xscale("log")
    ax.set_xlim(0.3, 5.5)
    ax.set_xticks([0.5, 0.67, 1.0, 1.5, 2.0, 3.0, 5.0])
    ax.set_xticklabels(["0.5", "0.67", "1.0", "1.5", "2.0", "3.0", "5.0"])

def draw(ax, rows, ylabels, ypos):
    for yy, orr, lo, hi, txt, color, sig in rows:
        ax.plot([lo, hi], [yy, yy], "-", color=color, lw=2.2, zorder=2)
        ax.plot(orr, yy, "s", ms=9 if sig else 6.5, color=color,
                mfc=color if sig else "white", mec=color, zorder=3)
        ax.annotate(txt, (5.65, yy), xycoords=("data", "data"),
                    va="center", ha="left", fontsize=9,
                    fontweight="bold" if sig else "normal", color=color)
    for yy, lab in ylabels:
        ax.annotate(lab, (0.28, yy), xycoords=("data", "data"),
                    va="center", ha="right", fontsize=10.5, fontweight="bold")
    for yy, lab in ypos:
        ax.annotate(lab, (0.30, yy), xycoords=("data", "data"),
                    va="center", ha="left", fontsize=8, color="0.45")
    ax.set_yticks([])
    for sp in ["top", "right", "left"]:
        ax.spines[sp].set_visible(False)

draw(axA, rowsA, ylabelsA, yposA)
draw(axB, rowsB, ylabelsB, yposB)
axA.set_title("A. Beverage exposures \u2192 atrial fibrillation: v3.1 vs v4 outcome upgrade",
              fontsize=13, fontweight="bold", loc="left")
axB.set_title("B. Positive lifestyle control: alcohol \u2192 atrial fibrillation",
              fontsize=13, fontweight="bold", loc="left")
axB.set_xlabel("Odds ratio per exposure increment (log scale, IVW)")
axA.set_xlabel("Odds ratio per exposure increment (log scale, IVW)")

out_png = OUT / "Figure_v4_forest_comparison_300dpi.png"
fig.savefig(out_png, dpi=300, bbox_inches="tight")
print("saved:", out_png)
