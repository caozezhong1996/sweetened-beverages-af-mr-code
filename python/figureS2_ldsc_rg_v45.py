# -*- coding: utf-8 -*-
"""Figure S2: forest plot of cross-trait LDSC genetic correlations (rg)
between beverage intake and atrial fibrillation (v4.5.1)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(sys.executable).parent.parent.parent))
from daimon_runtime import setup_plot
setup_plot()

import pandas as pd
import matplotlib.pyplot as plt

BASE = Path(r"C:\Users\64915\Documents\kimi\workspace\奶茶房颤MR_迁移包_20260822\06_升级分析_v4")
df = pd.read_csv(BASE / "results" / "ldsc_rg_v44.csv")

EXP = {"coffee": "Coffee intake", "tea": "Tea intake", "sugarCof": "Sugar added to coffee",
       "fizzy": "Fizzy drink intake (SSB)", "lowcal": "Low-calorie drink intake (ASB)"}
OUT = {"Nielsen": "Nielsen 2018", "R13": "FinnGen R13"}

tests = df[df["exposure"].isin(EXP) & df["outcome"].isin(OUT)].copy()
tests["lab"] = tests.apply(lambda r: f"{EXP[r['exposure']]}  ×  {OUT[r['outcome']]}", axis=1)
tests["sig"] = tests["rg_fdr"] < 0.05
order = ["coffee", "tea", "sugarCof", "fizzy", "lowcal"]
tests["o1"] = tests["exposure"].map({k: i for i, k in enumerate(order)})
tests["o2"] = tests["outcome"].map({"Nielsen": 0, "R13": 1})
tests = tests.sort_values(["o1", "o2"], ascending=[False, True]).reset_index(drop=True)

ctrl = df[(df["exposure"] == "Nielsen") | (df["outcome"] == "tea")].copy()
ctrl["lab"] = ctrl.apply(
    lambda r: "Same-trait control: Nielsen 2018 × FinnGen R13"
    if r["exposure"] == "Nielsen" else "Overlap control: coffee intake × tea intake", axis=1)
ctrl = ctrl.sort_values("exposure", ascending=False).reset_index(drop=True)

fig, ax = plt.subplots(figsize=(7.6, 5.8), dpi=300)
y0 = len(ctrl) + 1.0

ax.axhspan(-0.6, len(ctrl) - 0.5, color="#EEF3F6", zorder=0)
for i, r in ctrl.iterrows():
    ax.errorbar(r["rg"], i, xerr=1.96 * r["rg_se"], fmt="s", ms=6,
                color="#78909C", ecolor="#78909C", elinewidth=1.4, capsize=3)
    ax.text(1.03, i, f"{r['rg']:+.3f}", va="center", fontsize=7.8, color="#78909C",
            transform=ax.get_yaxis_transform())
ax.text(-0.44, len(ctrl) - 0.35, "validation controls", fontsize=7.6,
        color="#78909C", style="italic", va="center")

for i, r in tests.iterrows():
    col = "#C62828" if r["sig"] else "#37474F"
    ax.errorbar(r["rg"], y0 + i, xerr=1.96 * r["rg_se"], fmt="o", ms=6,
                color=col, ecolor=col, elinewidth=1.4, capsize=3)
    ax.text(1.03, y0 + i, f"{r['rg']:+.3f} (q={r['rg_fdr']:.3f})", va="center",
            fontsize=7.6, color=col, transform=ax.get_yaxis_transform())

ax.axvline(0, color="#263238", lw=0.9, ls="--")
ax.set_yticks(list(range(len(ctrl))) + [y0 + i for i in range(len(tests))])
ax.set_yticklabels([*ctrl["lab"], *tests["lab"]], fontsize=8.6)
ax.set_xlim(-0.45, 1.08)
ax.set_ylim(-0.8, y0 + len(tests) - 0.3)
ax.set_xlabel("Cross-trait genetic correlation with atrial fibrillation, rg (95% CI)", fontsize=9.5)
ax.set_title("LD score regression: beverage intake × atrial fibrillation\n"
             "red = survives FDR q < 0.05 across the 10 beverage–AF tests",
             fontsize=10, loc="left")
for s in ("top", "right"):
    ax.spines[s].set_visible(False)

out = BASE / "figures" / "FigureS2_LDSC_rg_v45_300dpi.png"
fig.savefig(out, bbox_inches="tight")
print("written:", out)
