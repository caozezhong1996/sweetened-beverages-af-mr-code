# -*- coding: utf-8 -*-
"""
Early-onset AF (Choi 2018, GCST010636, TOPMed Freeze4 WGS) sensitivity MR.
Outcome is score-test output: beta_y = Score/Var, se_y = 1/sqrt(Var), EA = alt.
Harmonise to exposure effect allele from project instrument list, then
IVW (FE + multiplicative RE), weighted median, MR-Egger, Cochran's Q.
"""
import math
import numpy as np
import pandas as pd
from scipy import stats

BASE = "C:/Users/64915/Documents/kimi/workspace/奶茶房颤MR_迁移包_20260822/06_升级分析_v4"

inst = pd.read_csv(f"{BASE}/tmp_instruments_all.csv")
out = pd.read_csv(f"{BASE}/tmp_eoaf_matched.tsv", sep="\t")
out[["chr", "pos", "ref", "alt"]] = out["varID"].str.split(":", expand=True)
out["pos"] = out["pos"].astype(int)
out["chr"] = out["chr"].astype(int)
out["beta_raw"] = out["Score"] / out["Var"]
out["se_y"] = 1.0 / np.sqrt(out["Var"])

merged = inst.merge(out, on=["chr", "pos"], how="inner")
print(f"merged rows: {len(merged)} / {len(inst)}")

def harmonise(r):
    ea, oa, alt, ref = r.ea, r.oa, r.alt, r.ref
    if alt == ea and ref == oa:
        return pd.Series({"beta_y": r.beta_raw, "flip": 0})
    if alt == oa and ref == ea:
        return pd.Series({"beta_y": -r.beta_raw, "flip": 1})
    return pd.Series({"beta_y": np.nan, "flip": -1})

merged[["beta_y", "flip"]] = merged.apply(harmonise, axis=1)
bad_allele = merged["flip"] == -1
print(f"allele mismatch dropped: {bad_allele.sum()}")
merged = merged[~bad_allele].copy()

# eAF sanity check (tolerance 0.2); drop failures
def eaf_ok(r):
    if pd.isna(r.eaf_x):
        return True
    expect = r.altFreq1 if r.flip == 0 else 1 - r.altFreq1
    return abs(expect - r.eaf_x) <= 0.2
bad_eaf = ~merged.apply(eaf_ok, axis=1)
print(f"eaf check dropped: {bad_eaf.sum()}")
merged = merged[~bad_eaf].copy()

def ivw(df):
    bx, by, sy = df.beta_x.to_numpy(), df.beta_y.to_numpy(), df.se_y.to_numpy()
    w = 1.0 / sy**2
    b = np.sum(w * bx * by) / np.sum(w * bx**2)
    se_fe = 1.0 / math.sqrt(np.sum(w * bx**2))
    q = np.sum(w * (by - b * bx) ** 2)
    k = len(df)
    phi = max(q / (k - 1), 1.0) if k > 1 else 1.0
    se_re = se_fe * math.sqrt(phi)
    return b, se_fe, se_re, q, k

def wald_ratio(df):
    return df.beta_y / df.beta_x, df.se_y / np.abs(df.beta_x)

def weighted_median(df, n_boot=1000, seed=20260827):
    r, se_r = wald_ratio(df)
    r_v, se_v = r.to_numpy(), se_r.to_numpy()

    def wmed(rv):
        w = 1.0 / se_v**2
        order = np.argsort(rv)
        rv_s, w_s = rv[order], w[order]
        cw = np.cumsum(w_s) - 0.5 * w_s
        cw /= np.sum(w_s)
        return np.interp(0.5, cw, rv_s)

    b = wmed(r_v)
    rng = np.random.default_rng(seed)
    boots = []
    for _ in range(n_boot):
        draw = rng.normal(r_v, se_v)
        boots.append(wmed(draw))
    se = float(np.std(boots, ddof=1))
    return b, max(se, 1e-8)

def egger(df):
    bx, by, sy = df.beta_x.to_numpy(), df.beta_y.to_numpy(), df.se_y.to_numpy()
    if len(df) < 3:
        return np.nan, np.nan, np.nan, np.nan
    sign = np.sign(bx)
    bx_s, by_s = bx * sign, by * sign
    w = 1.0 / sy**2
    X = np.column_stack([np.ones_like(bx_s), bx_s])
    W = np.diag(w)
    beta = np.linalg.solve(X.T @ W @ X, X.T @ W @ by_s)
    resid = by_s - X @ beta
    q = np.sum(w * resid**2)
    k = len(df)
    phi = max(q / (k - 2), 1.0)
    covb = phi * np.linalg.inv(X.T @ W @ X)
    return beta[1], math.sqrt(covb[1, 1]), beta[0], math.sqrt(covb[0, 0])

rows = []
for name, df in merged.groupby("exposure"):
    df = df.drop_duplicates(subset=["chr", "pos"])
    b, se_fe, se_re, q, k = ivw(df)
    p_re = 2 * (1 - 0.5 * (1 + math.erf(abs(b / se_re) / math.sqrt(2))))
    q_p = 1 - stats.chi2.cdf(q, k - 1)
    bm, sem = weighted_median(df)
    p_m = 2 * (1 - stats.norm.cdf(abs(bm / sem)))
    be, see, bi, sei = egger(df)
    p_e = 2 * (1 - stats.norm.cdf(abs(be / see))) if not np.isnan(be) else np.nan
    p_int = 2 * (1 - stats.norm.cdf(abs(bi / sei))) if not np.isnan(bi) else np.nan
    rows.append(dict(exposure=name, nSNP=k,
                     ivw_or=math.exp(b), ivw_lo=math.exp(b - 1.96 * se_re), ivw_hi=math.exp(b + 1.96 * se_re), ivw_p=p_re,
                     Q=q, Q_p=q_p,
                     wm_or=math.exp(bm), wm_lo=math.exp(bm - 1.96 * sem), wm_hi=math.exp(bm + 1.96 * sem), wm_p=p_m,
                     egger_or=math.exp(be) if not np.isnan(be) else np.nan, egger_p=p_e,
                     egger_int=bi, egger_int_p=p_int))

res = pd.DataFrame(rows).sort_values("exposure")
pd.set_option("display.width", 250)
pd.set_option("display.float_format", lambda v: f"{v:.4g}")
print(res[["exposure", "nSNP", "ivw_or", "ivw_lo", "ivw_hi", "ivw_p", "Q_p", "wm_or", "wm_p", "egger_or", "egger_p", "egger_int_p"]].to_string(index=False))
res.to_csv(f"{BASE}/eoaf_sensitivity_results.csv", index=False)
merged.to_csv(f"{BASE}/eoaf_harmonised_snps.csv", index=False)
print("saved: eoaf_sensitivity_results.csv, eoaf_harmonised_snps.csv")
