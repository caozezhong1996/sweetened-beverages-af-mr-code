# -*- coding: utf-8 -*-
"""Figure 2 (v4.1). Forest plot — Nielsen 2018 primary, AFGen sensitivity, FinnGen R13, EUR meta v4.1, BBJ."""
from pathlib import Path
import sys, re, math

sys.path.insert(0, str(Path(sys.executable).parent.parent.parent))
from daimon_runtime import setup_plot
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

setup_plot()

ROOT = Path(r"C:/Users/64915/Documents/kimi/workspace/奶茶房颤MR_迁移包_20260822")
OLD  = ROOT / "03_结果数据_mr_results"
NEW  = ROOT / "06_升级分析_v4" / "results"
OUTDIR = ROOT / "06_升级分析_v4" / "figures"
OUTDIR.mkdir(parents=True, exist_ok=True)

def tag_of(s):
    return re.sub(r"[^A-Za-z0-9]+", "_", s)

def ivw_row(path):
    d = pd.read_csv(path)
    return d[d["method"] == "Inverse variance weighted"].iloc[0]

exposures = [
    "Sugar added to tea", "Sugar added to coffee", "Fizzy drink intake SSB",
    "Low-calorie drink intake ASB", "Artificial sweetener added to tea",
    "Coffee intake", "Tea intake",
]
label_map = {"Fizzy drink intake SSB": "Fizzy drink intake (SSB)",
             "Low-calorie drink intake ASB": "Low-calorie drink intake (ASB)"}

sources = [
    ("Nielsen 2018 (EUR, primary)", NEW, "mr_{t}_ebi_a_GCST006414.csv", "#B33A3A"),
    ("AFGen 2018 (EUR, sensitivity)", OLD, None, "#8c8c8c"),   # special: two candidate filenames
    ("FinnGen R13 (EUR)", NEW, "mr_{t}_finngen_R13.csv", "#C08329"),
    ("BioBank Japan (EAS)", OLD, "mr_{t}_bbj_a_71.csv", "#7A4E7E"),
]

records = []
for expo in exposures:
    t = tag_of(expo)
    per = {}
    est = {}
    for src, base, pat, color in sources:
        f = None
        if src.startswith("AFGen"):
            for cand in [base / f"mr_{t}_ebi_a_GCST006061.csv", base / f"mr_{t}.csv"]:
                if cand.exists():
                    f = cand; break
        else:
            f = base / pat.format(t=t)
            if not f.exists():
                f = None
        if f is None:
            continue
        r = ivw_row(f)
        est[src] = (r["b"], r["se"])
        per[src] = (math.exp(r["b"]), math.exp(r["b"] - 1.96 * r["se"]),
                    math.exp(r["b"] + 1.96 * r["se"]), r["pval"], int(r["nsnp"]), color)
    # EUR fixed-effect meta: Nielsen + FinnGen R13
    k1, k2 = "Nielsen 2018 (EUR, primary)", "FinnGen R13 (EUR)"
    if k1 in est and k2 in est:
        b1, se1 = est[k1]; b2, se2 = est[k2]
        w1, w2 = 1 / se1 ** 2, 1 / se2 ** 2
        b = (b1 * w1 + b2 * w2) / (w1 + w2)
        se = math.sqrt(1 / (w1 + w2))
        p = math.erfc(abs(b / se) / math.sqrt(2))
        per["EUR meta v4.1 (Nielsen+FinnGen R13)"] = (math.exp(b), math.exp(b - 1.96 * se),
                                                math.exp(b + 1.96 * se), p, 0, "#1A5276")
    for src, vals in per.items():
        records.append({"exposure": label_map.get(expo, expo), "source": src, "OR": vals[0],
                        "lo": vals[1], "hi": vals[2], "p": vals[3], "nsnp": vals[4], "color": vals[5]})

df = pd.DataFrame(records)
source_order = ["Nielsen 2018 (EUR, primary)", "AFGen 2018 (EUR, sensitivity)",
                "FinnGen R13 (EUR)", "EUR meta v4.1 (Nielsen+FinnGen R13)", "BioBank Japan (EAS)"]
offsets = {s: o for s, o in zip(source_order, [0.44, 0.22, 0.0, -0.22, -0.44])}

fig, ax = plt.subplots(figsize=(11.0, 8.4))
yticks, ylabels = [], []
for i, expo in enumerate(reversed([label_map.get(e, e) for e in exposures])):
    base = i * 1.75
    yticks.append(base)
    ylabels.append(expo)
    sub = df[df["exposure"] == expo]
    for _, r in sub.iterrows():
        y = base + offsets[r["source"]]
        sig = r["p"] < 0.05
        ax.plot([r["lo"], r["hi"]], [y, y], color=r["color"], lw=1.8 if sig else 1.4, zorder=2)
        ax.scatter(r["OR"], y, color=r["color"], s=58 if r["source"].startswith("EUR meta") else 44,
                   zorder=3, marker="D" if r["source"].startswith("EUR meta") else "o",
                   facecolors=r["color"] if sig else "white", edgecolors=r["color"])
        star = "*" if sig else ""
        ax.text(5.0, y, f'{r["OR"]:.2f} ({r["lo"]:.2f}\u2013{r["hi"]:.2f}){star}',
                va="center", fontsize=8.2, color=r["color"],
                fontweight="bold" if sig else "normal")

ax.axvline(1.0, color="#666666", lw=1, ls="--")
ax.set_xscale("log")
ax.set_xlim(0.15, 5.6)
ax.set_xticks([0.2, 0.3, 0.5, 0.75, 1, 1.5, 2, 3, 5])
ax.set_xticklabels(["0.2", "0.3", "0.5", "0.75", "1", "1.5", "2", "3", "5"])
ax.set_yticks(yticks)
ax.set_yticklabels(ylabels, fontsize=10)
ax.set_xlabel("Odds ratio for atrial fibrillation per instrumented intake (log scale, IVW)")
ax.set_title("Mendelian randomization: beverage exposures and atrial fibrillation\n"
             "Primary outcome Nielsen 2018 (N = 1.03 M); FinnGen release R13; * P < 0.05 (nominal)", fontsize=11)

handles = [plt.Line2D([], [], marker="o", ls="", color=c, label=s) for s, _, _, c in sources]
handles.append(plt.Line2D([], [], marker="D", ls="", color="#1A5276", label="EUR meta v4.1 (Nielsen+FinnGen R13)"))
ax.legend(handles=handles, loc="lower left", fontsize=8.6, frameon=True)
sns.despine(ax=ax, left=True)
fig.subplots_adjust(left=0.235, right=0.855, top=0.90, bottom=0.09)

out = OUTDIR / "Figure2_Forest_v41_300dpi.png"
fig.savefig(out, dpi=300)
print("saved:", out)
