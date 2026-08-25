# -*- coding: utf-8 -*-
"""polish_v455.py — native-English language polish of the v4.5.4 manuscript.

Scope: grammar fixes, de-AI-flavored phrasing, smoother argumentation.
Hard constraints: every numeric string, citation marker and verified key string
is preserved verbatim; body word count must stay <= 5,100 (word-neutral edits);
abstract <= 250 words. Supplement untouched (stays v4.5.4).
"""
import io, sys

MS = r"C:\Users\64915\Documents\kimi\workspace\奶茶房颤MR_迁移包_20260822\04_docx构建脚本\build_manuscript_v45.js"
ms = io.open(MS, encoding="utf-8").read()


def sub_once(old, new, tag):
    global ms
    n = ms.count(old)
    if n != 1:
        print(f"FAIL  anchor not unique ({n}x): {tag}")
        sys.exit(1)
    ms = ms.replace(old, new, 1)
    print(f"  ok  {tag}")


# ---- version bump ----
sub_once("Manuscript version: v4.5.4", "Manuscript version: v4.5.5", "version bump")
sub_once("and a full-coverage BMI mediation sensitivity (25 August 2026)",
         "and a full-coverage BMI mediation sensitivity; v4.5.5: native-English language polish (25 August 2026)",
         "version note")

# ---- Abstract (word-neutral: +3 / -4) ----
sub_once("has never been prospectively studied for atrial fibrillation (AF)",
         "has never been prospectively studied in relation to atrial fibrillation (AF)",
         "abstract aim: collocation")
sub_once("multivariable MR with body mass index, locus-level colocalization, cross-trait linkage disequilibrium score (LDSC) regression, two-step mediation MR, and positive and negative controls",
         "multivariable MR, locus-level colocalization, cross-trait linkage disequilibrium score (LDSC) regression, mediation MR, and positive and negative controls",
         "abstract methods: tighten list")
sub_once("The alcohol control behaved as expected (P = 0.035).",
         "The alcohol control detected its established effect (P = 0.035).",
         "abstract results: precise verb")

# ---- Introduction: comma-splice chain -> semicolons ----
sub_once("Milk tea itself has never been studied as an exposure, the SSB–AF association lacks causal evidence, virtually all evidence derives from middle-aged European populations, and sugar and caffeine have rarely been evaluated within a single causal framework.",
         "Milk tea itself has never been studied as an exposure; the SSB–AF association lacks causal evidence; virtually all evidence derives from middle-aged European populations; and sugar and caffeine have rarely been examined within a single causal framework.",
         "intro: splice chain")

# ---- Methods ----
sub_once("instruments for these exposures were selected at a relaxed threshold (P < 5 × 10⁻⁶), which is addressed as a limitation.",
         "instruments for these exposures were selected at a relaxed threshold (P < 5 × 10⁻⁶), a choice revisited in the Limitations.",
         "methods: relaxed threshold phrasing")
sub_once("Locus-level colocalization. To interrogate the nominal coffee signal, Bayesian colocalization (coloc.abf, default priors) was performed in 500-kb windows",
         "Finally, to interrogate the nominal coffee signal, locus-level Bayesian colocalization (coloc.abf, default priors) was performed in 500-kb windows",
         "methods: orphan heading integrated")

# ---- Results ----
sub_once("One isolated exception emerged:", "One exception emerged:", "results: drop filler")
sub_once("This signal was unsupported by the weighted median (P = 0.061)",
         "This signal was not supported by the weighted median (P = 0.061)",
         "results: natural negation")
sub_once("significant in FinnGen R13 (OR 1.58, 1.09–2.29; P = 0.016), and a European meta-analytic OR of 1.34 (1.11–1.62; P = 0.002) that survived",
         "significant in FinnGen R13 (OR 1.58, 1.09–2.29; P = 0.016), with a European meta-analytic OR of 1.34 (1.11–1.62; P = 0.002) that survived",
         "results: broken parallel fixed")
sub_once("null weighted-median estimates (OR 1.16, P = 0.26 and OR 1.29, P = 0.14) and MR-Egger (OR 1.12; P = 0.60);",
         "null weighted-median (OR 1.16, P = 0.26 and OR 1.29, P = 0.14) and MR-Egger (OR 1.12; P = 0.60) estimates;",
         "results: parallel estimates")
sub_once("estimates, mirroring the European pattern of a fragile IVW-only signal. Given European-ancestry instruments, these are supportive context rather than independent evidence.",
         "estimates, mirroring the fragile IVW-only pattern seen in Europe. Given the European-ancestry instruments, these estimates are supportive context rather than independent evidence.",
         "results: BBJ closing sentence")
sub_once("the larger outcome GWAS resolved previously split support into strong evidence of a shared causal variant",
         "the larger outcome GWAS turned previously split support into strong evidence for a shared causal variant",
         "results: smoother verb")
sub_once("Because genetic correlation also captures non-causal pleiotropy, the positive rg values for SSBs and ASBs alongside robustly null MR estimates reinforce the interpretation that shared genetic architecture—for example, adiposity-related biology—rather than a causal effect links sweetened-drink intake to AF.",
         "Because genetic correlation captures non-causal pleiotropy, the positive rg values for SSBs and ASBs alongside robustly null MR estimates reinforce the interpretation that what links sweetened-drink intake to AF is shared genetic architecture—for example, adiposity-related biology—rather than a causal effect.",
         "results: untangle LDSC sentence")

# ---- Discussion ----
sub_once("The null was consistent across five conceptually distinct exposures—including sugar added to tea or coffee, the closest available genetic proxy for milk-tea-type composite beverages—across three European outcome sources, and across all complementary estimators.",
         "This null finding was consistent across five conceptually distinct exposures—including sugar added to tea or coffee, the closest available genetic proxy for milk-tea-type composite beverages—across three European outcome sources and all complementary estimators.",
         "discussion: 'The null' nominalization")
sub_once("argue against a causal interpretation of a signal of this size",
         "argue against a causal interpretation for a signal of this size",
         "discussion: preposition")
sub_once("displayed substantial heterogeneity whose outlier correction resolved to the null in Nielsen 2018 but not in FinnGen R13",
         "displayed substantial heterogeneity, with outlier correction resolving to the null in Nielsen 2018 but not FinnGen R13",
         "discussion: 'whose' misuse")

io.open(MS, "w", encoding="utf-8", newline="").write(ms)
print("\nPOLISH v4.5.5 COMPLETE")
