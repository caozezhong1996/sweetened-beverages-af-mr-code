# -*- coding: utf-8 -*-
"""trim_v453_words.py — word-budget trims for v4.5.3 (body 5268 -> <=5100)."""
import sys
from pathlib import Path

BUILD = Path(r"C:\Users\64915\Documents\kimi\workspace\奶茶房颤MR_迁移包_20260822\04_docx构建脚本")
fails = []


def check(cond, msg):
    if not cond:
        fails.append(msg)
        print("FAIL:", msg)
    return cond


def sub_once(text, old, new, label):
    n = text.count(old)
    if not check(n == 1, f"{label}: anchor x{n}"):
        return text
    print("  ok:", label)
    return text.replace(old, new, 1)


src = (BUILD / "build_manuscript_v45.js").read_text(encoding="utf-8")

src = sub_once(src,
    "Two-step mediation MR quantified this pathway for the nominal coffee signal: the BMI-mediated indirect effect statistically accounted for the entire association, leaving a null direct effect (Table S16).",
    "Two-step mediation MR quantified this pathway: the BMI-mediated indirect effect statistically accounted for the entire nominal coffee association (Table S16).",
    "Discussion mechanisms: shorten mediation sentence")

src = sub_once(src,
    "Against atrioventricular block (FinnGen R13 I9_AVBLOCK; Table S18), six of nine exposure tests were null (P ≥ 0.53); nominal positive associations for alcohol intake frequency (P = 0.043) and coffee intake (P = 0.042) did not survive Bonferroni correction across the nine tests, whereas the inverse association for sugar added to tea (P = 0.001) did. The coffee and sugar-in-tea estimates mirrored their AF associations in direction and magnitude—the behaviour expected if both track the shared adiposity-mediated pathway, BMI being an established risk factor for atrioventricular block—so the control informs pathway sharing rather than instrument specificity (Limitations).",
    "Against atrioventricular block (FinnGen R13 I9_AVBLOCK; Table S18), six of nine exposure tests were null (P ≥ 0.53); nominal associations for alcohol intake frequency (P = 0.043) and coffee intake (P = 0.042) did not survive Bonferroni correction, whereas the inverse association for sugar added to tea (P = 0.001) did. Both beverage estimates mirrored their AF associations in direction and magnitude, as expected if they track the shared adiposity-mediated pathway (Limitations).",
    "Results negative control: shorten")

src = sub_once(src,
    "Finally, mediation MR—pre-specified as conditional on a robust total effect—was performed during revision as a mechanistic probe of the sole nominal signal and carries the usual product-method assumptions (including homogeneity of the mediator–outcome effect across instrument sets); the negative outcome control was imperfect, because atrioventricular block shares adiposity-mediated aetiology with AF, so AF-specificity of the coffee and sugar-in-tea instruments cannot be formally established; the NHANES observational triangulation is deferred to future work.",
    "Finally, mediation MR—pre-specified as conditional on a robust total effect—was performed during revision as a mechanistic probe of the sole nominal signal and carries the usual product-method assumptions; the negative outcome control was imperfect (atrioventricular block shares adiposity-mediated aetiology with AF), so AF-specificity of the coffee and sugar-in-tea instruments cannot be formally established; the NHANES observational triangulation is deferred to future work.",
    "Limitations finally: shorten")

src = sub_once(src,
    "from the coffee–BMI and BMI–AF IVW estimates (product method with delta-method standard errors; Table S16).",
    "from the coffee–BMI and BMI–AF IVW estimates (product method; Table S16).",
    "Methods mediation: shorten")

src = sub_once(src,
    "The positive lifestyle control (alcoholic drinks per week) was directionally associated with AF in all four cohorts and nominally significant in the European meta-analysis, demonstrating adequate analytical sensitivity.",
    "The positive lifestyle control was directionally associated with AF in all four cohorts and nominally significant in the European meta-analysis, demonstrating adequate analytical sensitivity.",
    "Principal findings: shorten alcohol clause")

src = sub_once(src,
    "Radial IVW with modified second-order weights reproduced the primary estimates: the coffee association remained nominal (b = 0.235; P = 0.036) and all other exposures remained null (Table S7).",
    "Radial IVW with modified second-order weights reproduced the primary estimates (Table S7).",
    "Results radial: shorten")

src = sub_once(src,
    " MR-Egger intercepts were null throughout (P ≥ 0.54). The signal does not satisfy",
    " The signal does not satisfy",
    "Results coffee: drop duplicated Egger-intercept sentence")

src = sub_once(src,
    "with an almost identical estimate in AFGen 2018 (OR 1.26, 1.02–1.55; P = 0.031)",
    "with a concordant estimate in AFGen 2018 (OR 1.26; P = 0.031)",
    "Results coffee: shorten AFGen clause")

src = sub_once(src,
    "This signal was unsupported by the weighted median (P = 0.061), was absent from the other three outcome sources (all P > 0.21), displayed significant heterogeneity (Q P = 8 × 10⁻⁶) with a null MR-Egger intercept (P = 0.68), and was attenuated in the meta-analysis (P = 0.060);",
    "This signal was unsupported by the weighted median (P = 0.061), absent from the other three sources (all P > 0.21), significantly heterogeneous (Q P = 8 × 10⁻⁶) with a null MR-Egger intercept, and attenuated in the meta-analysis (P = 0.060);",
    "Results sugar-tea: shorten")

src = sub_once(src,
    "European estimates from Nielsen 2018 and FinnGen R13 were combined by fixed-effect meta-analysis, with DerSimonian–Laird random-effects meta-analysis as a sensitivity analysis;",
    "European estimates were combined by fixed-effect meta-analysis, with DerSimonian–Laird random-effects as sensitivity;",
    "Methods univariable: shorten meta clause")

src = sub_once(src,
    "Full per-variant summary statistics were obtained for coffee intake, tea intake, sugar added to coffee, fizzy drink intake and low-calorie drink intake from the Neale lab UK Biobank round-2 release (UK Biobank fields 1498, 1488, 100370, 100170 and 100160), and for AF",
    "Full per-variant summary statistics were obtained for five beverage traits from the Neale lab UK Biobank round-2 release (fields 1498, 1488, 100370, 100170, 100160) and for AF",
    "Methods LDSC: shorten source listing")

src = sub_once(src,
    "the nominal coffee association was at least as strong in the non-overlapping FinnGen R13 (OR 1.58) as in Nielsen 2018 (OR 1.26),",
    "the coffee association was at least as strong in the non-overlapping FinnGen R13 (OR 1.58 vs 1.26),",
    "Limitations sixth: shorten")

src = sub_once(src,
    "BMI retained a robust direct effect on AF (OR 1.47 per SD, 1.37–1.57; P = 2.0 × 10⁻²⁷; 467 jointly independent SNPs), serving as a positive control.",
    "BMI retained a robust direct effect on AF (OR 1.47, 1.37–1.57; P = 2.0 × 10⁻²⁷; 467 SNPs), serving as a positive control.",
    "MVMR Results: shorten (and drop ambiguous per-SD label)")

src = sub_once(src,
    "A subgroup analysis restricted to the three instruments within the caffeine-metabolism windows was likewise null in both European sources (Nielsen 2018 OR 1.03, 0.76–1.38, P = 0.86; FinnGen R13 OR 1.23, 0.73–2.07, P = 0.44), whereas the remaining 31 instruments carried the entire signal (OR 1.50, 1.12–2.01, P = 0.006 and OR 1.96, 1.18–3.24, P = 0.009):",
    "A subgroup analysis restricted to the three instruments within the caffeine-metabolism windows was likewise null in both European sources (Nielsen 2018 OR 1.03; P = 0.86; FinnGen R13 OR 1.23; P = 0.44), whereas the remaining 31 instruments carried the entire signal (OR 1.50; P = 0.006 and OR 1.96; P = 0.009):",
    "Results colocalization: drop CIs (retained in Table S4)")

if fails:
    print("\nTRIM ABORTED:", len(fails), "failure(s)")
    sys.exit(1)
(BUILD / "build_manuscript_v45.js").write_text(src, encoding="utf-8")
print("written: build_manuscript_v45.js (word-budget trims applied)")
