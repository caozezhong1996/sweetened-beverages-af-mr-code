# -*- coding: utf-8 -*-
"""Graphical abstract for EJPC submission — 12.5 x 18 cm at 300 dpi."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

W_CM, H_CM, DPI = 12.5, 18.0, 300
fig = plt.figure(figsize=(W_CM / 2.54, H_CM / 2.54), dpi=DPI)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, 100)
ax.set_ylim(0, 144)  # portrait coordinate space
ax.axis("off")

INK = "#1f313a"
MUT = "#5b6f79"
BLUE = "#2f6f8f"
LBLUE = "#e3eef4"
GREEN = "#2e7d5b"
LGREEN = "#e5f2ec"
AMBER = "#b3641c"
LAMBER = "#f9eee0"
GREY = "#eef3f6"


def box(x, y, w, h, fc, ec, lw=1.2, r=1.6):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}",
                                facecolor=fc, edgecolor=ec, linewidth=lw))


def txt(x, y, s, size=8.2, color=INK, weight="normal", ha="center", va="center", style="normal"):
    ax.text(x, y, s, fontsize=size, color=color, fontweight=weight, ha=ha, va=va,
            style=style, linespacing=1.35)


def arrow(x1, y1, x2, y2, color=MUT):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>", mutation_scale=14,
                                 linewidth=1.6, color=color))


# ---------------- title ----------------
txt(50, 139.0, "Sweetened Beverage Consumption and Risk of Atrial Fibrillation",
    size=9.2, weight="bold")
txt(50, 135.2, "A two-sample and multivariable Mendelian randomization study\nwith cross-ancestry replication",
    size=7.0, color=MUT, style="italic")

# ---------------- exposures ----------------
box(4, 116, 92, 15, LBLUE, BLUE)
txt(50, 128.6, "EXPOSURES — 7 beverage phenotypes\n(UK Biobank GWAS, N = 64,949–447,485)",
    size=7.6, weight="bold", color=BLUE)
txt(50, 122.6, "Sugar added to tea  ·  Sugar added to coffee  ·  Fizzy drinks (SSB)\n"
               "Low-calorie drinks (ASB)  ·  Artificial sweetener in tea\n"
               "Coffee intake  ·  Tea intake", size=8.0)

# ---------------- methods spine ----------------
arrow(50, 116, 50, 110.5)
box(4, 97.5, 92, 13, GREY, MUT)
txt(50, 108.2, "CAUSAL-INFERENCE FRAMEWORK", size=8.0, weight="bold", color=MUT)
txt(50, 102.6, "Two-sample MR (IVW + MR-Egger / weighted-median / MR-PRESSO)\n"
               "Multivariable MR with BMI  ·  Locus-level colocalization  ·  Cross-trait LDSC\n"
               "Reverse MR  ·  Alcohol positive lifestyle control",
    size=7.3)

arrow(50, 97.5, 50, 92)

# ---------------- outcome ----------------
box(4, 79, 92, 13, LBLUE, BLUE)
txt(50, 89.6, "OUTCOME — atrial fibrillation, four GWAS sources", size=8.0, weight="bold", color=BLUE)
txt(50, 84.2, "Nielsen 2018 (60,620 cases; primary)  ·  FinnGen R13 (67,783)\n"
              "AFGen 2018 (55,114; sensitivity)  ·  BioBank Japan (8,180; East Asian replication)",
    size=7.8)

# ---------------- findings ----------------
txt(50, 74.5, "KEY FINDINGS", size=8.6, weight="bold")

box(4, 55.5, 44, 16, LGREEN, GREEN)
txt(26, 69.0, "Sweetened beverages", size=7.9, weight="bold", color=GREEN)
txt(26, 66.3, "→ NO causal association with AF", size=7.9, weight="bold", color=GREEN)
txt(26, 61.2, "Meta-analytic OR 0.82–0.97\nall P ≥ 0.06; null across cohorts,\nestimators and ancestries",
    size=7.4)

box(52, 55.5, 44, 16, LAMBER, AMBER)
txt(74, 69.0, "Coffee nominal signal (OR 1.34)", size=7.9, weight="bold", color=AMBER)
txt(74, 66.3, "→ fails every consistency test", size=7.9, weight="bold", color=AMBER)
txt(74, 61.2, "Attenuated by BMI (OR 0.82);\ncolocalizes with AF only at FTO\n(adiposity), not CYP1A1–CYP1A2 / AHR",
    size=7.4)

box(4, 40.5, 92, 12, LGREEN, GREEN)
txt(50, 50.0, "Genetic correlation ≠ causation", size=7.9, weight="bold", color=GREEN)
txt(50, 45.0, "SSB / ASB share genetic architecture with AF (rg = 0.24–0.31, FDR q < 0.05)\n"
              "despite robustly null MR estimates — adiposity-related pleiotropy;\n"
              "cross-trait intercepts ≈ 0 exclude sample-overlap bias", size=7.2)

# ---------------- conclusion ----------------
arrow(50, 40.5, 50, 35.5)
box(4, 22.5, 92, 13, INK, INK)
txt(50, 32.4, "CONCLUSION", size=8.0, weight="bold", color="#bcd3de")
txt(50, 27.2, "Sweetened-beverage intake is not causally associated with atrial fibrillation.\n"
              "Observational associations are best explained by adiposity-related confounding;\n"
              "prevention should target established cardiometabolic risk factors.",
    size=7.8, color="white")

txt(50, 18.5, "Direct measurement of milk-tea consumption in prospective East Asian cohorts remains needed.",
    size=7.2, color=MUT, style="italic")

import pathlib
out = pathlib.Path(r"C:\Users\64915\Documents\kimi\workspace\奶茶房颤MR_迁移包_20260822\06_升级分析_v4\figures\Graphical_Abstract_v45_300dpi.png")
out.parent.mkdir(parents=True, exist_ok=True)
fig.savefig(out, dpi=DPI)
print("written:", out)

from PIL import Image
im = Image.open(out)
print("pixel size:", im.size, "expected:", (round(W_CM / 2.54 * DPI), round(H_CM / 2.54 * DPI)))
