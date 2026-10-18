# -*- coding: utf-8 -*-
"""patch_v51_nmcd_compress4.py — heading-level trims for safety margin."""
import re
import shutil
from pathlib import Path

BASE = Path(r"C:\Users\64915\Documents\kimi\workspace\奶茶房颤MR_迁移包_20260822")
BLD = BASE / "04_docx构建脚本"


def sub_literal(text, anchor, new_inner):
    pat = re.compile(r"T`[^`]*" + re.escape(anchor) + r"[^`]*`", re.S)
    n = len(pat.findall(text))
    if n != 1:
        raise SystemExit(f"ANCHOR NOT UNIQUE ({n}): {anchor[:70]}")
    return pat.sub(lambda m: "T`" + new_inner + "`", text, count=1)


REPL = [
    # methods h2
    ("Study design and reporting", "Study design"),
    ("Genetic correlation and overlap diagnostics", "Genetic correlation"),
    ("Pre-specified analyses and deviations", "Deviations"),
    # results h2
    ("Sweetened beverages and AF in European populations",
     "Sweetened beverages and AF"),
    ("Nominal associations that were not robust", "Non-robust nominal associations"),
    ("Multivariable MR: attenuation of the coffee signal by adiposity",
     "Multivariable MR"),
    ("Directionality, radial MR, reverse MR and statistical power",
     "Directionality, reverse MR and power"),
    ("Positive lifestyle control: alcohol consumption", "Positive control: alcohol"),
    ("Negative outcome control: atrioventricular block",
     "Negative control: atrioventricular block"),
    # discussion h2
    ("Potential mechanisms and the role of adiposity", "Mechanisms: the role of adiposity"),
    ("Clinical and public-health implications", "Implications"),
    # paragraph trims
    ("Most fundamentally",
     "Most fundamentally, the component-proxy design estimates the marginal, "
     "lifelong effects of individual ingredients rather than the composite "
     "beverage: a null for sugar, caffeine and tea does not entail a null "
     "for milk tea, which additionally entails possible sugar–caffeine "
     "interaction, non-instrumented constituents and an acute per-serving "
     "character outside the lifelong estimand. The acute window and "
     "dose–response shape are questions for randomized ambulatory-monitoring "
     "designs [30]."),
    ("Exposure data.",
     "Exposure data. Instruments for seven beverage phenotypes were obtained "
     "from UK Biobank GWAS (identifiers in Table 1): sugar added to tea, "
     "sugar added to coffee, fizzy drink intake (sugar-sweetened beverages, "
     "SSBs), low-calorie drink intake (artificially sweetened beverages, "
     "ASBs) and artificial sweetener added to tea (each N = 64,949), coffee "
     "intake (N = 428,860) and tea intake (N = 447,485), all "
     "European-ancestry. Sugar added to tea or coffee is conceptually the "
     "closest proxy for milk-tea-type composite beverages."),
    ("Coffee intake was nominally associated with higher AF odds",
     "Coffee intake was nominally associated with higher AF odds (Nielsen "
     "2018 OR 1.26; P = 0.036; AFGen 2018 OR 1.26, P = 0.031; FinnGen R13 "
     "OR 1.58; P = 0.016; European meta-analysis OR 1.34, 1.11–1.62; P = "
     "0.002, surviving Benjamini–Hochberg correction). It failed every "
     "pre-specified consistency criterion: significant heterogeneity "
     "(Cochran's Q P = 9 × 10⁻⁴ and 4 × 10⁻¹⁰), null weighted-median and "
     "MR-Egger estimates, and significant MR-PRESSO global tests, with "
     "outlier correction resolving to the null in Nielsen 2018 (P = 0.20) "
     "but not FinnGen R13 (β = 0.345; P = 0.007). The contamination-mixture "
     "estimator gave the same source-dependent pattern (Nielsen 2018 β = "
     "0.068, −0.136 to 0.564; FinnGen R13 β = 0.689, 0.257–0.958; Table "
     "S14), and genome-wide CAUSE (1,081,418 shared variants) found "
     "correlated pleiotropy explained the overlap as well as a causal model "
     "(P = 0.53; causal effect γ = 0.01, −0.01 to 0.04; Table S15). A small "
     "genuine effect cannot be excluded."),
]


def main():
    mp = BLD / "build_manuscript_v51.js"
    shutil.copy(mp, str(mp) + ".bak_nmcd4")
    src = mp.read_text(encoding="utf-8")
    for anchor, new in REPL:
        src = sub_literal(src, anchor, new)
    mp.write_text(src, encoding="utf-8")
    print(f"pass-4 applied: {len(REPL)} replacements")


if __name__ == "__main__":
    main()
