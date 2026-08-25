#!/usr/bin/env python
"""Extract Nielsen 2018 AF rows for the FTO coloc window (rsid list from v42)
so the coloc prior-sensitivity scan can rebuild the exact v4 dataset locally."""
import gzip
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ids = set()
with open(os.path.join(BASE, "results", "coloc_FTO_rsids_v42.txt")) as fh:
    for line in fh:
        line = line.strip()
        if line:
            ids.add(line)
print(f"target rsids: {len(ids)}", flush=True)

src = os.path.join(BASE, "nielsen2018_AF_full.tsv.gz")
dst = os.path.join(BASE, "results", "coloc_FTO_Nielsen_region_v45.tsv")
kept = 0
with gzip.open(src, "rt") as f, open(dst, "w") as out:
    header = f.readline().rstrip("\n").split("\t")
    idx = {c: i for i, c in enumerate(header)}
    need = ["variant_id", "effect_allele", "other_allele", "beta", "standard_error",
            "effect_allele_frequency", "p_value"]
    have = [c for c in need if c in idx]
    out.write("\t".join(have) + "\n")
    for line in f:
        parts = line.rstrip("\n").split("\t")
        vid = parts[idx["variant_id"]]
        if any(tok in ids for tok in vid.split(";")):
            out.write("\t".join(parts[idx[c]] for c in have) + "\n")
            kept += 1
print(f"Nielsen FTO rows kept: {kept}", flush=True)
