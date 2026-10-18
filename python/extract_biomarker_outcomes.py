# -*- coding: utf-8 -*-
"""extract_biomarker_outcomes.py — pull Nielsen2018 + FinnGenR13 rows for biomarker tophit rsids."""
import gzip, csv, os

ROOT = r"C:\Users\64915\Documents\kimi\workspace\奶茶房颤MR_迁移包_20260822\06_升级分析_v4"
tags = ["caffeine", "paraxanthine", "theobromine"]
rsid_set = set()
for tag in tags:
    with open(os.path.join(ROOT, "results", f"biomarker_tophits_{tag}.tsv")) as f:
        for r in csv.DictReader(f, delimiter="\t"):
            rsid_set.add(r["rsid"])
print("rsids to find:", len(rsid_set))

# ---- Nielsen 2018 (GWAS Catalog harmonised; rs in variant_id) ----
found_n = {}
with gzip.open(os.path.join(ROOT, "nielsen2018_AF_full.tsv.gz"), "rt") as fh:
    rd = csv.DictReader(fh, delimiter="\t")
    for r in rd:
        v = r["variant_id"]
        if v in rsid_set:
            found_n[v] = r
with open(os.path.join(ROOT, "results", "biomarker_outcome_nielsen.tsv"), "w", newline="") as o:
    w = csv.writer(o, delimiter="\t")
    w.writerow(["rsid","chr","pos","ea","oa","eaf","beta","se","p"])
    for rs, r in found_n.items():
        w.writerow([rs, r["chromosome"], r["base_pair_location"], r["effect_allele"],
                    r["other_allele"], r["effect_allele_frequency"], r["beta"],
                    r["standard_error"], r["p_value"]])
print("Nielsen matched:", len(found_n))

# ---- FinnGen R13 I9_AF (rsids comma-separated) ----
found_f = {}
with gzip.open(os.path.join(ROOT, "finngen_R13_I9_AF.gz"), "rt") as fh:
    rd = csv.DictReader(fh, delimiter="\t")
    for r in rd:
        for rs in r["rsids"].split(","):
            if rs in rsid_set:
                found_f[rs] = r
                break
with open(os.path.join(ROOT, "results", "biomarker_outcome_finngen.tsv"), "w", newline="") as o:
    w = csv.writer(o, delimiter="\t")
    w.writerow(["rsid","chr","pos","ea","oa","eaf","beta","se","p"])
    for rs, r in found_f.items():
        w.writerow([rs, r["#chrom"], r["pos"], r["alt"], r["ref"],
                    r["af_alt"], r["beta"], r["sebeta"], r["pval"]])
print("FinnGen matched:", len(found_f))

missing = rsid_set - set(found_n) - set(found_f)
print("missing in both:", sorted(missing))
