# -*- coding: utf-8 -*-
"""Figure 1 (v4). Study design flowchart — Nielsen 2018 primary outcome, alcohol positive control."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(sys.executable).parent.parent.parent))
from daimon_runtime import setup_plot
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

setup_plot()

OUTDIR = Path(r"C:/Users/64915/Documents/kimi/workspace/奶茶房颤MR_迁移包_20260822/06_升级分析_v4/figures")
OUTDIR.mkdir(parents=True, exist_ok=True)

C_DATA = "#2A6F7F"   # teal   - data sources
C_INST = "#C08329"   # amber  - instrument selection
C_ANA  = "#4A6FA5"   # blue   - analyses
C_ROB  = "#7A4E7E"   # purple - robustness
C_NOTE = "#8A8A8A"   # gray   - note

fig, ax = plt.subplots(figsize=(11.5, 8.6))
ax.set_xlim(0, 100)
ax.set_ylim(0, 100)
ax.axis("off")

def box(x, y, w, h, title, body, color, title_fs=10.5, body_fs=9.2):
    p = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.4,rounding_size=1.2",
                       linewidth=1.4, edgecolor=color, facecolor="white", zorder=2)
    ax.add_patch(p)
    ax.add_patch(FancyBboxPatch((x, y + h - 5.2), w, 5.2,
                 boxstyle="round,pad=0.4,rounding_size=1.2",
                 linewidth=0, facecolor=color, alpha=0.14, zorder=2))
    ax.text(x + w / 2, y + h - 2.6, title, ha="center", va="center",
            fontsize=title_fs, fontweight="bold", color=color, zorder=3)
    ax.text(x + w / 2, y + (h - 5.2) / 2, body, ha="center", va="center",
            fontsize=body_fs, color="#263238", zorder=3, linespacing=1.45)

def arrow(x1, y1, x2, y2, color="#666666"):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>",
                 mutation_scale=13, linewidth=1.3, color=color, zorder=1))

# ---------------- Band 1: data sources ----------------
y1, h1 = 74, 22
box(2, y1, 30, h1, "Exposure GWAS",
    "UK Biobank, MRC IEU pipeline\n(OpenGWAS; European ancestry)\n"
    "7 beverage phenotypes\nN = 64,949\u2013447,485",
    C_DATA)
box(35, y1, 30, h1, "Outcome GWAS: atrial fibrillation",
    "Nielsen 2018 (EUR, primary):\n60,620 / 970,216\n"
    "AFGen 2018 (EUR, sensitivity):\n55,114 / 482,295\n"
    "FinnGen (EUR): 22,068 / 116,926\n"
    "BioBank Japan (EAS): 8,180 / 28,612",
    C_DATA, body_fs=8.4)
box(68, y1, 30, h1, "Covariate & positive-control GWAS",
    "BMI: GIANT (EUR), N = 681,275\n(MVMR positive control)\n"
    "Alcohol: GSCAN drinks/week\nN = 335,394; UKB intake frequency\nN = 462,346 (lifestyle control)",
    C_DATA, body_fs=8.4)

# ---------------- Band 2: instrument selection ----------------
y2, h2 = 52, 15
box(17, y2, 66, h2, "Instrument selection and harmonization",
    "Independent SNPs (r\u00b2 < 0.001, 10,000 kb); P < $5 \\times 10^{-8}$ for coffee/tea intake,\n"
    "P < $5 \\times 10^{-6}$ for five beverage sub-phenotypes (pre-specified relaxed threshold)\n"
    "Palindromic-SNP exclusion; all per-variant F > 20  \u2192  8\u201334 SNPs per exposure,\n"
    "identical instrument lists across outcome sources",
    C_INST)

# ---------------- Band 3: analyses ----------------
y3, h3 = 25, 19
box(2, y3, 23, h3, "Univariable MR",
    "Random-effects IVW\n(primary)\nMR-Egger, weighted\nmedian, weighted mode\n(sensitivity)",
    C_ANA, title_fs=10, body_fs=8.8)
box(27.3, y3, 23, h3, "European meta-analysis",
    "Fixed-effect pooling of\nNielsen 2018 + FinnGen\nBenjamini\u2013Hochberg\nFDR across 7 primary\ntests",
    C_ANA, title_fs=10, body_fs=8.8)
box(52.6, y3, 23, h3, "Cross-ancestry replication",
    "BioBank Japan\n(East Asian)\nIVW estimates with\nsensitivity methods",
    C_ANA, title_fs=10, body_fs=8.8)
box(77.9, y3, 20.1, h3, "Multivariable MR",
    "Coffee intake + sugar\nadded to tea + BMI\nconditional direct\neffects",
    C_ANA, title_fs=10, body_fs=8.8)

# ---------------- Band 4: robustness ----------------
y4, h4 = 6, 12
box(2, y4, 47, h4, "Robustness and pleiotropy assessment",
    "Cochran's Q \u00b7 MR-Egger intercept \u00b7 MR-PRESSO \u00b7 radial IVW\n"
    "Steiger directionality \u00b7 reverse MR (111 AF instruments)\n"
    "Alcohol positive lifestyle control",
    C_ROB, body_fs=8.6)
box(52, y4, 46, h4, "Pre-specified conditional analyses",
    "Colocalization performed as mechanistic probe of the nominal\n"
    "coffee signal (CYP1A1\u2013CYP1A2, AHR, FTO loci); mediation MR\n"
    "not pursued \u2014 no robust total causal effect detected",
    C_NOTE, title_fs=9.5, body_fs=8.4)

# ---------------- arrows ----------------
for xc in (17, 50, 83):            # band1 -> band2
    arrow(xc, y1 - 0.6, 50, y2 + h2 + 0.6)
for xc in (13.5, 38.8, 64.1, 88):  # band2 -> band3
    arrow(50, y2 - 0.6, xc, y3 + h3 + 0.6)
for xc in (13.5, 38.8, 64.1, 88):  # band3 -> band4
    arrow(xc, y3 - 0.6, 42, y4 + h4 + 0.6, color="#888888")

ax.text(50, 98.6, "Study design: sweetened beverage consumption and atrial fibrillation (Mendelian randomization)",
        ha="center", va="top", fontsize=12, fontweight="bold", color="#263238")

fig.subplots_adjust(left=0.01, right=0.99, top=0.97, bottom=0.02)
out = OUTDIR / "Figure1_Study_Design_v4_300dpi.png"
fig.savefig(out, dpi=300)
print("saved:", out)
