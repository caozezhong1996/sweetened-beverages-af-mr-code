# -*- coding: utf-8 -*-
"""stage_s16_s18.py — build supplement TSVs for v4.5.3 tables S16-S18."""
import csv
from pathlib import Path

BASE = Path(r"C:\Users\64915\Documents\kimi\workspace\奶茶房颤MR_迁移包_20260822\06_升级分析_v4")
RES = BASE / "results"
TBL = BASE / "supplement_tables"
TBL.mkdir(exist_ok=True)

# ---------- S16: two-step mediation ----------
sc = {}
with open(RES / "tmp_mediation_scalars_v46.csv", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        sc[row["item"]] = float(row["value"])

med = {}
with open(RES / "mediation_bmi_v46.tsv", encoding="utf-8") as f:
    for row in csv.DictReader(f, delimiter="\t"):
        med[row["quantity"]] = float(row["estimate"])

def fmt_p(p):
    if p < 1e-3:
        m, e = f"{p:.1e}".split("e")
        return f"{m}e{int(e)}"
    return f"{p:.4f}".rstrip("0").rstrip(".")

rows = [
    ["Total effect", "Coffee intake -> AF (Nielsen 2018)", "IVW (random effects)", "34",
     f"{sc['b_total']:.4f}", f"{sc['se_total']:.4f}", fmt_p(sc["p_total"])],
    ["Step 1 (X->M)", "Coffee intake -> BMI (Yengo 2018, GCST006900)", "IVW", "17",
     f"{sc['b_XM']:.4f}", f"{sc['se_XM']:.4f}", fmt_p(sc["p_XM"])],
    ["Step 2 (M->Y)", "BMI -> AF (Nielsen 2018)", "IVW", "701",
     f"{med['beta_MY_BMI_to_AF']:.4f}", f"{med['se_MY']:.4f}", fmt_p(med["p_MY"])],
    ["Indirect effect", "product beta_XM x beta_MY (log OR per intake category)", "delta method", "-",
     f"{med['indirect_effect']:.4f}", f"{med['se_indirect']:.4f}", "-"],
    ["Proportion mediated", "indirect / total (95% CI -0.231 to 2.627)", "delta method", "-",
     f"{med['proportion_mediated']:.3f}", f"{med['se_proportion']:.3f}", fmt_p(med["p_proportion"])],
    ["Direct effect", "total - indirect", "-", "-",
     f"{sc['b_total'] - med['indirect_effect']:.4f}", "-", "-"],
]
with open(TBL / "S16_mediation.tsv", "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f, delimiter="\t", lineterminator="\n")
    w.writerow(["Component", "Analysis", "Method", "No. SNPs", "Beta", "SE", "P"])
    w.writerows(rows)

# ---------- S17: MRlap ----------
rows17 = [
    ["Observed IVW effect (per SD)", "0.0279", "0.0183", "0.128"],
    ["Corrected effect (per SD)", "0.0371", "0.0233", "0.111"],
    ["Test of difference (corrected - observed)", "-1.8118", "-", "0.070"],
    ["MR-Egger intercept P", "-", "-", "0.703"],
    ["Instruments used by MRlap", "25 (523 candidates P < 5e-8, 500-kb distance pruning)", "-", "-"],
    ["LDSC SNP heritability, exposure (coffee)", "0.0501", "0.0040", "-"],
    ["LDSC intercept, exposure", "1.0056", "-", "-"],
    ["LDSC SNP heritability, outcome (AF)", "0.0240", "0.0020", "-"],
    ["LDSC intercept, outcome", "1.0453", "-", "-"],
    ["Cross-trait genetic covariance", "0.0012", "0.0010", "-"],
    ["Cross-trait rg", "0.0351", "-", "-"],
    ["Cross-trait LDSC intercept (overlap metric)", "-0.0104", "0.0057", "-"],
    ["Estimated polygenicity (exposure)", "0.0040", "-", "-"],
    ["Per-SNP heritability (exposure)", "1.1e-05", "-", "-"],
]
with open(TBL / "S17_mrlap.tsv", "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f, delimiter="\t", lineterminator="\n")
    w.writerow(["Quantity", "Estimate", "SE", "P"])
    w.writerows(rows17)

# ---------- S18: AV block negative control ----------
keep = {"Inverse variance weighted", "Weighted median", "MR Egger"}
order = ["Coffee_intake", "Tea_intake", "Sugar_added_to_tea", "Sugar_added_to_coffee",
         "Fizzy_drink_intake_SSB", "Low_calorie_drink_intake_ASB",
         "Artificial_sweetener_added_to_tea", "Alcohol_intake_frequency",
         "Alcoholic_drinks_per_week_GSCAN"]
label = {
    "Coffee_intake": "Coffee intake", "Tea_intake": "Tea intake",
    "Sugar_added_to_tea": "Sugar added to tea", "Sugar_added_to_coffee": "Sugar added to coffee",
    "Fizzy_drink_intake_SSB": "Fizzy drink intake (SSB)",
    "Low_calorie_drink_intake_ASB": "Low-calorie drink intake (ASB)",
    "Artificial_sweetener_added_to_tea": "Artificial sweetener added to tea",
    "Alcohol_intake_frequency": "Alcohol intake frequency (control)",
    "Alcoholic_drinks_per_week_GSCAN": "Alcoholic drinks per week (control)",
}
rows18 = []
with open(RES / "mr_avblock_v46.csv", encoding="utf-8") as f:
    data = [r for r in csv.DictReader(f) if r["method"] in keep]
for ex in order:
    sub = [r for r in data if r["exposure"] == ex]
    for meth in ("Inverse variance weighted", "Weighted median", "MR Egger"):
        r = next((x for x in sub if x["method"] == meth), None)
        if r is None:
            continue
        rows18.append([label[ex], meth, r["nsnp"], f"{float(r['b']):+.4f}",
                       f"{float(r['se']):.4f}", fmt_p(float(r["pval"]))])
with open(TBL / "S18_avblock.tsv", "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f, delimiter="\t", lineterminator="\n")
    w.writerow(["Exposure", "Method", "No. SNPs", "Beta", "SE", "P"])
    w.writerows(rows18)

print("staged:", (TBL / "S16_mediation.tsv").exists(),
      (TBL / "S17_mrlap.tsv").exists(), (TBL / "S18_avblock.tsv").exists())
print("S16 rows:", len(rows), "S17 rows:", len(rows17), "S18 rows:", len(rows18))
