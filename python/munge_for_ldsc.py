#!/usr/bin/env python
"""Munge Nielsen 2018 (GCST006414 harmonised, build37) and FinnGen R13 I9_AF
into LDSC-ready files (SNP A1 A2 N Z), restricted to HM3 SNPs with EUR LD scores."""
import gzip, glob, sys, os
import pandas as pd

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LDREF = os.path.join(BASE, "ld_ref", "eur_w_ld_chr")
OUT = os.path.join(BASE, "results")

# 1) HM3 rsid set from LD score files
rsids = set()
for f in sorted(glob.glob(os.path.join(LDREF, "*.l2.ldscore.gz"))):
    with gzip.open(f, "rt") as fh:
        next(fh)
        for line in fh:
            rsids.add(line.split("\t")[1])
print(f"HM3 EUR LD-score SNPs: {len(rsids)}", flush=True)

def first_hit(rsid_field):
    for r in str(rsid_field).split(";"):
        if r in rsids:
            return r
    return None

# 2) Nielsen
src = os.path.join(BASE, "nielsen2018_AF_full.tsv.gz")
dst = os.path.join(OUT, "ldsc_Nielsen2018.sumstats.gz")
N_NIELSEN = 1030836
kept = 0
with gzip.open(dst, "wt") as out:
    out.write("SNP\tA1\tA2\tN\tZ\n")
    for chunk in pd.read_csv(src, sep="\t", chunksize=2_000_000, dtype=str,
                             usecols=["variant_id","effect_allele","other_allele","beta","standard_error"]):
        chunk["rsid"] = chunk["variant_id"].map(first_hit)
        chunk = chunk[chunk["rsid"].notna()]
        beta = pd.to_numeric(chunk["beta"], errors="coerce")
        se = pd.to_numeric(chunk["standard_error"], errors="coerce")
        z = beta / se
        ok = se.notna() & (se > 0) & beta.notna()
        kept += int(ok.sum())
        sub = pd.DataFrame({"SNP": chunk.loc[ok, "rsid"],
                            "A1": chunk.loc[ok, "effect_allele"].str.upper(),
                            "A2": chunk.loc[ok, "other_allele"].str.upper(),
                            "N": N_NIELSEN, "Z": z[ok]})
        sub = sub[sub["A1"].isin(["A","C","G","T"]) & sub["A2"].isin(["A","C","G","T"])]
        sub.to_csv(out, sep="\t", index=False, header=False, float_format="%.5g")
print(f"Nielsen kept: {kept}", flush=True)

# 3) FinnGen R13 I9_AF (hg38; rsid merge)
src = os.path.join(BASE, "finngen_R13_I9_AF.gz")
dst = os.path.join(OUT, "ldsc_FinnGenR13.sumstats.gz")
if os.path.exists(dst) and os.path.getsize(dst) > 1_000_000:
    print("R13 already munged, skip", flush=True)
else:
  N_R13 = 309052  # 67,783 cases + 241,269 controls
  kept = 0
  with gzip.open(dst, "wt") as out:
    out.write("SNP\tA1\tA2\tN\tZ\n")
    for chunk in pd.read_csv(src, sep="\t", chunksize=2_000_000, dtype=str,
                             usecols=["rsids","ref","alt","beta","sebeta"]):
        chunk["rsid"] = chunk["rsids"].map(first_hit)
        chunk = chunk[chunk["rsid"].notna()]
        beta = pd.to_numeric(chunk["beta"], errors="coerce")
        se = pd.to_numeric(chunk["sebeta"], errors="coerce")
        z = beta / se
        ok = se.notna() & (se > 0) & beta.notna()
        kept += int(ok.sum())
        sub = pd.DataFrame({"SNP": chunk.loc[ok, "rsid"],
                            "A1": chunk.loc[ok, "alt"].str.upper(),
                            "A2": chunk.loc[ok, "ref"].str.upper(),
                            "N": N_R13, "Z": z[ok]})
        sub = sub[sub["A1"].isin(["A","C","G","T"]) & sub["A2"].isin(["A","C","G","T"])]
        sub.to_csv(out, sep="\t", index=False, header=False, float_format="%.5g")
  print(f"R13 kept: {kept}", flush=True)
print("DONE", flush=True)
