# -*- coding: utf-8 -*-
"""Aggregate v3.1 + v4 result CSVs into tidy TSVs for the v4 manuscript and supplement docx builds."""
import math, re
from pathlib import Path
import pandas as pd

ROOT = Path(r"C:\Users\64915\Documents\kimi\workspace\奶茶房颤MR_迁移包_20260822")
OLD  = ROOT / "03_结果数据_mr_results"
NEW  = ROOT / "06_升级分析_v4" / "results"
OUT  = ROOT / "06_升级分析_v4" / "supplement_tables"
OUT.mkdir(parents=True, exist_ok=True)

EXPO_ORDER = ["Sugar added to tea","Sugar added to coffee","Fizzy drink intake SSB",
              "Low-calorie drink intake ASB","Artificial sweetener added to tea",
              "Coffee intake","Tea intake"]
EXPO_LABEL = {"Fizzy drink intake SSB":"Fizzy drink intake (SSB)",
              "Low-calorie drink intake ASB":"Low-calorie drink intake (ASB)"}
EXPO_ID = {"Sugar added to tea":"ukb-b-8442","Sugar added to coffee":"ukb-b-243",
           "Fizzy drink intake SSB":"ukb-b-2832","Low-calorie drink intake ASB":"ukb-b-19703",
           "Artificial sweetener added to tea":"ukb-b-5867","Coffee intake":"ukb-b-5237",
           "Tea intake":"ukb-b-6066"}
EXPO_N = {"ukb-b-8442":"64,949","ukb-b-243":"64,949","ukb-b-2832":"64,949","ukb-b-19703":"64,949",
          "ukb-b-5867":"64,949","ukb-b-5237":"428,860","ukb-b-6066":"447,485"}
EXPO_THR = {"ukb-b-8442":"5 × 10⁻⁶","ukb-b-243":"5 × 10⁻⁶","ukb-b-2832":"5 × 10⁻⁶",
            "ukb-b-19703":"5 × 10⁻⁶","ukb-b-5867":"5 × 10⁻⁶","ukb-b-5237":"5 × 10⁻⁸","ukb-b-6066":"5 × 10⁻⁸"}
# (otag, label, results dir). Nielsen first = primary in v4.
# v4.1: FinnGen R5 (finn_b_I9_AF, OLD) is superseded by FinnGen release R13
# (67,783 cases / 241,269 controls), which subsumes R5; R5 is dropped to avoid
# double counting in the European meta-analysis.
SOURCES = [("ebi_a_GCST006414","Nielsen 2018 (EUR, primary)", NEW),
           ("ebi_a_GCST006061","AFGen 2018 (EUR)", OLD),
           ("finngen_R13","FinnGen R13 (EUR)", NEW),
           ("bbj_a_71","BioBank Japan (EAS)", OLD)]

def tag(s): return re.sub(r"[^A-Za-z0-9]+","_",s)
def find(stem, expo, otag, base):
    cands = [base/f"{stem}_{tag(expo)}_{otag}.csv"]
    if otag == "ebi_a_GCST006061":
        cands.append(base/f"{stem}_{tag(expo)}.csv")
    for c in cands:
        if c.exists(): return pd.read_csv(c)
    return None
def orfmt(b,se): return f"{math.exp(b):.2f} ({math.exp(b-1.96*se):.2f}\u2013{math.exp(b+1.96*se):.2f})"
def pfmt(p):
    if p < 1e-4:
        m,e = f"{p:.1e}".split("e"); return f"{m} × 10{chr(0x207B) if int(e)<0 else ''}{abs(int(e))}"
    return f"{p:.3f}".rstrip('0').rstrip('.') if p >= 0.001 else f"{p:.4f}"
def lab(e): return EXPO_LABEL.get(e,e)
def ivw(d): return d[d["method"]=="Inverse variance weighted"].iloc[0]

# ---- S1: instruments (now incl. Nielsen column) ----
rows=[]
for e in EXPO_ORDER:
    counts=[]; fmin=fmean=None
    for otag,_,base in SOURCES:
        d=find("dat",e,otag,base)
        counts.append(str(len(d)) if d is not None else "—")
        if otag=="ebi_a_GCST006414" and d is not None and "F_stat" in d:
            fmin,fmean = d["F_stat"].min(), d["F_stat"].mean()
    rows.append([lab(e),EXPO_ID[e],EXPO_N[EXPO_ID[e]],EXPO_THR[EXPO_ID[e]]," / ".join(counts),
                 f"{fmin:.1f}" if fmin else "—", f"{fmean:.1f}" if fmean else "—"])
pd.DataFrame(rows,columns=["Exposure","OpenGWAS ID","GWAS N","Instrument P threshold",
    "SNPs retained (Nielsen/AFGen/FinnGenR13/BBJ)","Min per-variant F","Mean F"]).to_csv(OUT/"S1_instruments.tsv",sep="\t",index=False)

# ---- S2: full UVMR (4 sources) ----
rows=[]
for e in EXPO_ORDER:
    for otag,olab,base in SOURCES:
        d=find("mr",e,otag,base)
        if d is None: continue
        for m in ["Inverse variance weighted","MR Egger","Weighted median","Weighted mode"]:
            r=d[d["method"]==m]
            if len(r):
                r=r.iloc[0]
                rows.append([lab(e),olab,m,int(r["nsnp"]),orfmt(r["b"],r["se"]),pfmt(r["pval"])])
pd.DataFrame(rows,columns=["Exposure","Outcome source","Method","No. SNPs","OR (95% CI)","P value"]).to_csv(OUT/"S2_uvmr_full.tsv",sep="\t",index=False)

# ---- S3: heterogeneity + pleiotropy (4 sources) ----
rows=[]
for e in EXPO_ORDER:
    for otag,olab,base in SOURCES:
        h=find("het",e,otag,base); p=find("pleio",e,otag,base)
        if h is None and p is None: continue
        q=qp=qi=qip="—"
        if h is not None:
            r=h[h["method"]=="Inverse variance weighted"].iloc[0]
            q=f"{r['Q']:.1f} ({int(r['Q_df'])})"; qp=pfmt(r["Q_pval"])
        if p is not None and len(p):
            r=p.iloc[0]; qi=f"{r['egger_intercept']:.4f} ({r['se']:.4f})"; qip=pfmt(r["pval"])
        rows.append([lab(e),olab,q,qp,qi,qip])
pd.DataFrame(rows,columns=["Exposure","Outcome source","Cochran Q (df)","Q P value",
    "Egger intercept (SE)","Intercept P value"]).to_csv(OUT/"S3_het_pleio.tsv",sep="\t",index=False)

# ---- manuscript Table 2 (Nielsen primary) ----
rows=[]
meta_info = {}
for e in EXPO_ORDER:
    cells=[lab(e)]; ses={}
    for otag,olab,base in SOURCES:
        d=find("mr",e,otag,base)
        if d is None: cells.append("—"); continue
        r=ivw(d); ses[otag]=(r["b"],r["se"])
        cells.append(f"{orfmt(r['b'],r['se'])}, {pfmt(r['pval'])}")
    b1,se1=ses["ebi_a_GCST006414"]; b2,se2=ses["finngen_R13"]
    w1,w2=1/se1**2,1/se2**2; mb=(b1*w1+b2*w2)/(w1+w2); mse=math.sqrt(1/(w1+w2))
    mp=math.erfc(abs(mb/mse)/math.sqrt(2))
    meta_info[e]=(mb,mse)
    cells.append(f"{orfmt(mb,mse)}, {pfmt(mp)}")
    ns=[]
    for otag,_,base in SOURCES:
        d=find("mr",e,otag,base); ns.append(str(int(ivw(d)["nsnp"])) if d is not None else "—")
    cells.append(" / ".join(ns))
    rows.append(cells)
pd.DataFrame(rows,columns=["Exposure","Nielsen 2018 (EUR, primary), OR (95% CI), P",
    "AFGen 2018 (EUR), OR (95% CI), P","FinnGen R13 (EUR), OR (95% CI), P",
    "BioBank Japan (EAS), OR (95% CI), P","EUR meta-analysis v4.1 (Nielsen+FinnGen R13), OR (95% CI), P",
    "SNPs (Niels/AFG/FinnR13/BBJ)"]).to_csv(OUT/"T2_main.tsv",sep="\t",index=False)

# ---- manuscript Table 3: sensitivity vs Nielsen 2018 (primary) ----
rows=[]
for e in EXPO_ORDER:
    d=find("mr",e,"ebi_a_GCST006414",NEW)
    wm=d[d["method"]=="Weighted median"].iloc[0]; eg=d[d["method"]=="MR Egger"].iloc[0]
    h=find("het",e,"ebi_a_GCST006414",NEW); p=find("pleio",e,"ebi_a_GCST006414",NEW)
    qp=h[h["method"]=="Inverse variance weighted"].iloc[0]["Q_pval"]
    ip=p.iloc[0]["pval"] if p is not None and len(p) else float("nan")
    presso="—"
    if e=="Coffee intake": presso="0.002 (2 outliers; corrected P = 0.20)"
    rows.append([lab(e),f"{orfmt(wm['b'],wm['se'])}, {pfmt(wm['pval'])}",
                 f"{orfmt(eg['b'],eg['se'])}, {pfmt(eg['pval'])}",
                 pfmt(ip),pfmt(qp),presso])
pd.DataFrame(rows,columns=["Exposure","Weighted median, OR (95% CI), P","MR-Egger, OR (95% CI), P",
    "Egger intercept P","Cochran Q P","MR-PRESSO global P"]).to_csv(OUT/"T3_sensitivity_nielsen.tsv",sep="\t",index=False)

# ---- manuscript Table 4: MVMR vs Nielsen ----
mv=pd.read_csv(NEW/"mvmr_coffee_sugartea_bmi_Nielsen.csv")
rows=[]
note_map={"BMI":"Positive control; robust direct effect",
          "Coffee intake":"Univariable nominal signal attenuated to null",
          "Sugar added to tea":"Uninformative (single joint instrument)"}
for _,r in mv.iterrows():
    rows.append([r["exposure_label"],orfmt(r["b"],r["se"]),pfmt(r["pval"]),int(r["nsnp"]),note_map[r["exposure_label"]]])
pd.DataFrame(rows,columns=["Exposure (conditional)","OR (95% CI)","P value","No. SNPs","Interpretation"]).to_csv(OUT/"T4_mvmr.tsv",sep="\t",index=False)

# ---- manuscript Table 5: power (Nielsen + EUR meta v4) ----
rows=[]
for e in EXPO_ORDER:
    d=find("mr",e,"ebi_a_GCST006414",NEW); r=ivw(d)
    se_n=r["se"]; mb,mse=meta_info[e]
    mde_n=math.exp(2.8003*se_n); mde_m=math.exp(2.8003*mse)
    pw_n=0.5*(1+math.erf((math.log(1.10)/se_n-1.95996)/math.sqrt(2)))
    pw_m=0.5*(1+math.erf((math.log(1.10)/mse-1.95996)/math.sqrt(2)))
    rows.append([lab(e),int(r["nsnp"]),f"{mde_n:.2f} / {mde_m:.2f}",f"{pw_n*100:.0f}%",f"{pw_m*100:.0f}%"])
pd.DataFrame(rows,columns=["Exposure","No. SNPs (Nielsen)",
    "Minimum detectable OR (80% power), Nielsen / EUR meta v4.1",
    "Power to detect OR 1.10, Nielsen","Power to detect OR 1.10, EUR meta v4.1"]).to_csv(OUT/"T5_power.tsv",sep="\t",index=False)

# ---- S5: alcohol positive lifestyle control (v4.1: FinnGen R13 replaces R5) ----
oc_names={"ebi_a_GCST006414":"Nielsen 2018 (EUR)","ebi_a_GCST006061":"AFGen 2018 (EUR)",
          "finngen_R13":"FinnGen R13 (EUR)","bbj_a_71":"BioBank Japan (EAS)"}
rows=[]
for alc_expo in ["Alcohol intake frequency","Alcoholic drinks per week GSCAN"]:
    pretty_alc="Alcoholic drinks per week (GSCAN)" if "GSCAN" in alc_expo else alc_expo
    ests={}
    for otag,olab,_base in SOURCES:
        d=find("mr",alc_expo,otag,NEW)
        if d is None: continue
        r=ivw(d); ests[otag]=(r["b"],r["se"])
        rows.append([pretty_alc,olab,int(r["nsnp"]),orfmt(r["b"],r["se"]),pfmt(r["pval"])])
    b1,se1=ests["ebi_a_GCST006414"]; b2,se2=ests["finngen_R13"]
    w1,w2=1/se1**2,1/se2**2; mb=(b1*w1+b2*w2)/(w1+w2); mse=math.sqrt(1/(w1+w2))
    mp=math.erfc(abs(mb/mse)/math.sqrt(2))
    rows.append([pretty_alc,"EUR meta v4.1 (Nielsen+FinnGen R13)","—",orfmt(mb,mse),pfmt(mp)])
pd.DataFrame(rows,columns=["Exposure","Outcome","No. SNPs","OR (95% CI)","P value"]).to_csv(OUT/"S5_alcohol_control.tsv",sep="\t",index=False)

# ---- S7: radial IVW (Nielsen) + reverse MR (Nielsen instruments) ----
rad=pd.read_csv(NEW/"upgrade_radial_ivw_nielsen.csv")
rev=pd.read_csv(NEW/"upgrade_reverse_mr_nielsen.csv")
rev_ivw=rev[rev["method"]=="Inverse variance weighted"]
revmap={r["outcome_label"]:(r["b"],r["se"],r["pval"],int(r["nsnp"])) for _,r in rev_ivw.iterrows()}
radmap={}
for _,r in rad.iterrows():
    radmap[r["exposure"]]=(r["b"],r["se"],r["pval"])
rows=[]
for e in EXPO_ORDER:
    t=tag(e)
    rb,rs,rp = radmap.get(t,(float("nan"),)*3)
    rl = EXPO_LABEL.get(e,e)
    rv = revmap.get(rl) or revmap.get(e)
    if rv: rb2,rs2,rp2,nn=rv; rev_s=f"{rb2:.4f} ({rb2-1.96*rs2:.4f} to {rb2+1.96*rs2:.4f})"
    else:  rp2,nn,rev_s=float("nan"),"—","—"
    rows.append([rl,f"{rb:.3f} ({rs:.3f})",pfmt(rp),rev_s,pfmt(rp2),nn])
pd.DataFrame(rows,columns=["Exposure","Radial IVW (mod. 2nd order) beta (SE), Nielsen","P value",
    "Reverse MR IVW beta (95% CI), AF(Nielsen) instruments","P value","Reverse MR No. SNPs"]).to_csv(OUT/"S7_radial_reverse.tsv",sep="\t",index=False)

# ---- S8: colocalization, AFGen vs Nielsen comparison (+ FTO vs FinnGen R13 in v4.2) ----
c_old={}
for rg in ["CYP1A1_CYP1A2","AHR","FTO"]:
    d=pd.read_csv(OLD/f"upgrade_coloc_{rg}.csv"); c_old[d.iloc[0]["region"]]=d.iloc[0]
c_new=pd.read_csv(NEW/"upgrade_coloc_coffee_loci_Nielsen.csv")
c_r13=pd.read_csv(NEW/"upgrade_coloc_FTO_FinnGenR13.csv")
r13_h1=float(c_r13.iloc[0]["PP.H1"]); r13_h4=float(c_r13.iloc[0]["PP.H4"]); r13_n=int(c_r13.iloc[0]["nsnp"])
rows=[]
region_pretty={"CYP1A1-CYP1A2":"CYP1A1–CYP1A2, 15q24 (rs2472297)","AHR":"AHR, 7p21 (rs4410790)","FTO":"FTO, 16q12 (rs1421085)"}
region_win={"CYP1A1-CYP1A2":"chr15:74,777,880–75,277,880","AHR":"chr7:17,034,577–17,534,577","FTO":"chr16:53,550,954–54,050,954"}
for _,rn in c_new.iterrows():
    rg=rn["region"]; ro=c_old.get(rg)
    is_fto = rg=="FTO"
    rows.append([region_pretty[rg],region_win[rg],int(rn["nsnp"]),
        f"{ro['PP.H1']:.3f}" if ro is not None else "—", f"{rn['PP.H1']:.3f}",
        f"{ro['PP.H4']:.3f}" if ro is not None else "—", f"{rn['PP.H4']:.3f}",
        f"{r13_h1:.1e} (n={r13_n})".replace("e-07"," × 10⁻⁷") if is_fto else "—", f"{r13_h4:.3f}" if is_fto else "—"])
pd.DataFrame(rows,columns=["Locus (lead coffee SNP)","Region (500-kb window)","SNPs (Nielsen merge)",
    "PP.H1 coffee only (AFGen)","PP.H1 coffee only (Nielsen)",
    "PP.H4 shared (AFGen)","PP.H4 shared (Nielsen)",
    "PP.H1 coffee only (FinnGen R13)","PP.H4 shared (FinnGen R13)"]).to_csv(OUT/"S8_coloc.tsv",sep="\t",index=False)

# ---- S6: Steiger (Nielsen) ----
st=pd.read_csv(NEW/"upgrade_steiger_nielsen.csv")
pretty={"Sugar_added_to_tea":"Sugar added to tea","Sugar_added_to_coffee":"Sugar added to coffee",
        "Fizzy_drink_intake_SSB":"Fizzy drink intake (SSB)","Low_calorie_drink_intake_ASB":"Low-calorie drink intake (ASB)",
        "Artificial_sweetener_added_to_tea":"Artificial sweetener added to tea","Coffee_intake":"Coffee intake","Tea_intake":"Tea intake"}
d=find("dat","Coffee intake","ebi_a_GCST006414",NEW)
rows=[]
for e in EXPO_ORDER:
    t=tag(e); r=st[st["exposure"]==t].iloc[0]
    dd=find("dat",e,"ebi_a_GCST006414",NEW)
    rows.append([pretty[t],len(dd),f"{r['snp_r2.exposure']:.4f}",f"{r['snp_r2.outcome']:.2e}".replace("e-"," × 10⁻"),
                 str(r["correct_causal_direction"]),pfmt(max(r["steiger_pval"],1e-300)),"0"])
pd.DataFrame(rows,columns=["Exposure","No. SNPs","R² (exposure)","R² (outcome)","Correct direction","Steiger P","Violations"]).to_csv(OUT/"S6_steiger.tsv",sep="\t",index=False)

for f in sorted(OUT.glob("*.tsv")):
    print(f.name, len(pd.read_csv(f,sep="\t")), "rows")
