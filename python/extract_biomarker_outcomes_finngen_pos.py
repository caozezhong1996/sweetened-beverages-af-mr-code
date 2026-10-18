# -*- coding: utf-8 -*-
"""extract_biomarker_outcomes_finngen_pos.py — FinnGen R13 match by rsid AND by GRCh38 chr:pos fallback."""
import gzip, csv, os

ROOT = r"C:\Users\64915\Documents\kimi\workspace\奶茶房颤MR_迁移包_20260822\06_升级分析_v4"
tags = ["caffeine", "paraxanthine", "theobromine"]
rs2pos, rsid_set = {}, set()
for tag in tags:
    with open(os.path.join(ROOT, "results", f"biomarker_tophits_{tag}.tsv")) as f:
        for r in csv.DictReader(f, delimiter="\t"):
            rsid_set.add(r["rsid"])
            rs2pos[r["rsid"]] = (r["chr"].replace("chr", ""), int(r["pos"]))

found = {}
with gzip.open(os.path.join(ROOT, "finngen_R13_I9_AF.gz"), "rt") as fh:
    rd = csv.DictReader(fh, delimiter="\t")
    for r in rd:
        key = (r["#chrom"], int(r["pos"]))
        rsset = set(r["rsids"].split(",")) if r["rsids"] else set()
        hits = (rsset & rsid_set)
        if not hits:
            for rs, (c, p) in rs2pos.items():
                if rs in found:
                    continue
                if (c, p) == key:
                    hits = {rs}
                    break
        for rs in hits:
            if rs not in found:
                found[rs] = r

with open(os.path.join(ROOT, "results", "biomarker_outcome_finngen.tsv"), "w", newline="") as o:
    w = csv.writer(o, delimiter="\t")
    w.writerow(["rsid","chr","pos","ea","oa","eaf","beta","se","p"])
    for rs, r in found.items():
        w.writerow([rs, r["#chrom"], r["pos"], r["alt"], r["ref"],
                    r["af_alt"], r["beta"], r["sebeta"], r["pval"]])
print("FinnGen matched (rsid+pos):", len(found), "/", len(rsid_set))
missing = rsid_set - set(found)
print("missing:", sorted(missing))
