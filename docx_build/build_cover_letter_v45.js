import fs from "node:fs";
import path from "node:path";
import {
  AlignmentType, Document, Footer, HeadingLevel, Packer, PageNumber,
  Paragraph, ShadingType, Table, TableCell, TableRow, TextRun, WidthType,
} from "docx";

const out1 = process.argv[2];
if (!out1) throw new Error("Usage: node build_cover_letter.js cover.docx");
const out2 = path.join(path.dirname(out1), "Target_Journal_Shortlist.docx");
for (const o of [out1, out2]) fs.mkdirSync(path.dirname(o), { recursive: true });

const font = { ascii: "Times New Roman", hAnsi: "Times New Roman", cs: "Times New Roman", eastAsia: "SimSun" };
const palette = { dark: "263238", primary: "37474F", light: "78909C", fill: "EEF3F6", ph: "9C3D3D" };
const run = (text, o = {}) => new TextRun({ text, font, size: 24, ...o });
const para = (children, o = {}) =>
  new Paragraph({ spacing: { after: 140, line: 340 }, ...o, children: Array.isArray(children) ? children : [children] });
const h1 = (t) => para(run(t, { bold: true, size: 28, color: palette.dark }), { heading: HeadingLevel.HEADING_1, spacing: { before: 240, after: 120 } });
const ph = (t) => new TextRun({ text: t, font, size: 24, italics: true, color: palette.ph });

// ============ FILE 1: COVER LETTER ============
const L = [];
L.push(
  para(run("Cover Letter", { bold: true, size: 30, color: palette.dark }), { alignment: AlignmentType.CENTER, spacing: { after: 300 } }),
  para([run("Date: "), run("25 August 2026")]),
  para([run("To: "), run("The Editor-in-Chief, European Journal of Preventive Cardiology", { bold: true })]),
  para([run("Re: "), run("Submission of original research manuscript — “Sweetened Beverage Consumption and Risk of Atrial Fibrillation: A Two-Sample and Multivariable Mendelian Randomization Study With Cross-Ancestry Replication”", { bold: true })]),
  para(run("Dear Editor-in-Chief,")),
  para(run("We are pleased to submit the above original research manuscript for consideration by the European Journal of Preventive Cardiology. The journal’s focus on the causes and prevention of cardiovascular disease makes it a natural home for this work, which addresses whether a ubiquitous and rapidly growing dietary exposure—sweetened beverages, and in particular milk-tea-type composite beverages—is a causal determinant of atrial fibrillation (AF), the commonest sustained arrhythmia.")),
  para(run("We analysed publicly available GWAS summary statistics: seven beverage exposures instrumented in UK Biobank, with AF outcomes from the Nielsen 2018 meta-analysis (60,620 cases; primary source), FinnGen release R13 (67,783 cases) and AFGen 2018 (European supporting sources), and BioBank Japan (East Asian replication). Genetically proxied intake of sugar added to tea or coffee, sugar-sweetened beverages, artificially sweetened beverages and artificial sweetener added to tea was not causally associated with AF, with consistent null estimates across cohorts, estimators and ancestries.")),
  para(run("Three nominal IVW signals emerged—an inverse association for sugar added to coffee (AFGen 2018 only), an inverse association for sugar added to tea (FinnGen R13 only), and a positive association for coffee intake (European meta-analysis OR 1.34, 95% CI 1.11–1.62; P = 0.002, surviving Benjamini–Hochberg correction)—but none satisfied pre-specified consistency criteria. The coffee signal showed null weighted-median estimates, source-dependent robustness to MR-PRESSO outlier correction, attenuation to the null after adjustment for body mass index (multivariable MR OR 0.82, 0.65–1.04; P = 0.099), and colocalization with AF only at the adiposity locus FTO (PP.H4 = 0.894; independently replicated in FinnGen R13 at 0.906), not at caffeine-metabolism loci (PP.H4 ≤ 0.008); instruments restricted to those caffeine-metabolism loci were null in both European sources, whereas body mass index itself showed a robust direct effect (OR 1.47, 1.37–1.57; P = 2.0 × 10⁻²⁷). Two analyses added during revision reinforced this reading: an independent coffee-exposure GWAS (Neale lab UK Biobank field 1498) gave a directionally concordant estimate (cross-GWAS meta-analytic OR 1.23, 1.04–1.44; P = 0.013), and two-step mediation MR attributed the nominal association in full to the adiposity pathway, concordantly across two independent BMI data sources.")),
  para(run("A positive lifestyle control (alcoholic drinks per week) detected the established causal effect (European meta-analysis P = 0.035), confirming analytical sensitivity. Cross-trait LD score regression showed that SSB and ASB intake share genetic architecture with AF (rg up to 0.31; FDR q < 0.05 in FinnGen R13) despite null causal estimates—directly illustrating the pleiotropy-versus-causation distinction—while cross-trait intercepts (all |intercept| ≤ 0.018) quantitatively excluded material sample-overlap bias.")),
  para(run("We believe these findings matter for three reasons. First, they provide, to our knowledge, the first genetic causal assessment of sweetened tea/coffee consumption—the closest available proxy for milk-tea-type beverages, which are consumed daily by hundreds of millions of predominantly young people in East Asia and have never been studied prospectively. Second, they indicate that the modest observational association between sweetened beverages and incident AF reported in UK Biobank cohorts is more consistent with residual confounding, including adiposity, than with a direct causal effect of beverage sugar, refining the evidence base for arrhythmia-specific dietary guidance. Third, the study demonstrates a transparent, pre-specified analytic pipeline (STROBE-MR compliant, with multiplicity control, MR-PRESSO and a positive-control multivariable design) that readers can audit in full from the accompanying supplementary tables and analysis code. The timeliness of the question is underscored by the 2026 American Heart Association scientific statement on caffeine and cardiovascular disease (Marcus et al., Circulation, 20 July 2026), which concluded that habitual caffeinated coffee does not increase AF risk—concordant with our genetic evidence—and identified both the separation of caffeine from accompanying beverage components and effect modification by caffeine-metabolism variants as open questions; our component-resolved design and locus-level colocalization at CYP1A1–CYP1A2 and AHR address exactly these gaps.")),
  para(run("This manuscript is original, has not been published previously and is not under consideration by any other journal. All analyses used publicly available, de-identified summary statistics; no individual-level data were accessed. The authors declare no conflicts of interest and received no specific funding for this work. Both authors have read and approved the submitted version and agree to its submission to the European Journal of Preventive Cardiology. GWAS dataset identifiers are listed in the manuscript, the complete analysis code is publicly archived with a DOI (https://doi.org/10.5281/zenodo.22099675), and complete result files accompany the submission as Supplementary Data Files. In accordance with journal policy, we disclose that portions of the analysis workflow and drafting were assisted by an artificial-intelligence tool (Kimi, Moonshot AI); all content was independently verified and approved by the authors, who take full responsibility for the integrity of the work.")),
  para(run("We hope you find the manuscript suitable for peer review, and we look forward to the editors’ and reviewers’ comments.")),
  para(run("Yours faithfully,"), { spacing: { after: 240 } }),
  para([run("Cao Zezhong, on behalf of both authors", { bold: true })]),
  para([run("The Affiliated Hospital of Yangzhou University, Yangzhou, Jiangsu, China")]),
  para([run("Email: caozezhong1996@163.com")]),
  para([run("Co-author: Chen Rongrong, The Affiliated Hospital of Yangzhou University, Yangzhou, Jiangsu, China (chenrrxh@126.com)")]),
  para(run("Note: if another journal is selected, the addressee line and journal name can be adapted; the body text is journal-agnostic except the first paragraph.", { size: 18, color: palette.light, italics: true }), { spacing: { before: 240 } })
);
const doc1 = new Document({
  sections: [{ properties: { page: { margin: { top: 1440, bottom: 1440, left: 1440, right: 1440 } } },
    footers: { default: new Footer({ children: [para(new TextRun({ children: [PageNumber.CURRENT] }), { alignment: AlignmentType.CENTER })] }) },
    children: L }],
});
fs.writeFileSync(out1, await Packer.toBuffer(doc1));
console.log("written:", out1);

// ============ FILE 2: JOURNAL SHORTLIST ============
const cell = (t, w, o = {}) =>
  new TableCell({ children: [new Paragraph({ spacing: { after: 10, line: 250 }, children: [typeof t === "string" ? run(t, { size: 20 }) : t] })],
    margins: { top: 70, bottom: 70, left: 90, right: 90 }, width: { size: w, type: WidthType.DXA }, ...o });
const table = (widths, head, rows) =>
  new Table({ width: { size: 100, type: WidthType.PERCENTAGE }, columnWidths: widths,
    rows: [new TableRow({ tableHeader: true, children: head.map((t, i) => cell(t, widths[i], { shading: { type: ShadingType.CLEAR, fill: palette.fill } })) }),
      ...rows.map((r) => new TableRow({ children: r.map((t, i) => cell(t, widths[i])) }))] });

const S = [];
S.push(
  para(run("Target Journal Shortlist — Sweetened Beverages and Atrial Fibrillation (MR study)", { bold: true, size: 30, color: palette.dark }), { alignment: AlignmentType.CENTER, spacing: { after: 160 } }),
  para(run("Journal metrics and CAS warning-list status verified online on 16–17 August 2026 (sources below); confirm against the journal homepage at submission.", { size: 20, color: palette.light, italics: true }), { spacing: { after: 240 } }),
  h1("Tier 1 — Ambitious (higher visibility)"),
  table([2200, 1500, 1600, 2100, 2800],
    ["Journal", "Impact Factor", "Speed", "Acceptance", "Fit"],
    [
      ["European Journal of Preventive Cardiology (EJPC)", "10.0 per ESC/OUP page (2025); third-party aggregators list 7.5 for the 2025 JCR — verify in JCR", "—", "Selective; Q1, rank 18/237", "Scope match: causes and prevention of CVD; ambitious first choice."],
      ["Journal of the American Heart Association (JAHA)", "Q1 — rank 41/230 (2024 IF basis)", "Mean 22 days to first decision (2025)", "~18% (original research)", "Publishes MR regularly; fast decisions."],
      ["Nutrition, Metabolism & Cardiovascular Diseases (NMCD)", "3.9 (2025)", "—", "Moderate", "Most topical fit; published the prior coffee–AF MR (Yuan 2019); friendly to null results."],
    ]),
  h1("Tier 2 — Fast and higher acceptance (non-warning-list)"),
  table([2200, 1500, 1600, 2100, 2800],
    ["Journal", "Impact Factor", "Speed", "Acceptance", "Fit"],
    [
      ["Open Heart (BMJ; official journal of the British Cardiovascular Society)", "3.1 (2025)", "Median 3 days desk-screen; 45 days with review; 22 days acceptance→publication", "32% (2025)", "OA cardiology journal covering all study designs including genetic epidemiology; highest acceptance rate on this list."],
      ["BMC Cardiovascular Disorders (Springer Nature)", "3.1 (2025)", "Median 16 days to first decision; ~108 days submission→acceptance (PubMed median)", "High volume (~700 articles/yr)", "MR-friendly, publishes TwoSampleMR studies routinely; OA (APC ≈ US$2,690, verify)."],
      ["Annals of Medicine (Taylor & Francis)", "4.9 (2025), Q1", "Fast desk screening (days)", "Moderate; MR-friendly", "General medical journal that publishes many Mendelian randomization studies; highest IF of the fast tier."],
    ]),
  h1("CAS Early-Warning List check (中国科学院《国际期刊预警名单》)"),
  para(run("Checked against the 2025, 2024, 2023, 2021 and 2020 lists (Chinese Academy of Sciences, National Science Library). The 2025 list contains only 5 journals, all in engineering/computer science; no medical journal is currently listed. None of the six journals above appears on any edition of the list.")),
  para(run("Caution by publisher family: several MDPI medical journals (Journal of Clinical Medicine, Journal of Personalized Medicine, Diagnostics, Cancers) were on the 2024 list, and Frontiers in Medicine / Frontiers in Surgery appeared on earlier editions — we therefore recommend avoiding MDPI and Frontiers titles even when individual titles are not currently listed, and checking your institution’s internal journal policy before submission.")),
  h1("Suggested strategy"),
  para(run("Fast-track route: Open Heart or BMC Cardiovascular Disorders first — decision within roughly 2–7 weeks, acceptance odds favourable, both non-warning-list; if aiming higher, try EJPC or JAHA first (decision in ~3 weeks) and fall back to Tier 2.")),
  para(run("Balanced route: JAHA first (22-day mean first decision limits time loss), then Open Heart or BMC Cardiovascular Disorders, then NMCD.")),
  h1("Sources (accessed 16–17 August 2026)"),
  para(run("EJPC: Oxford Academic “Why publish” page and ESC journal page (accessed 26 August 2026) — “Impact Factor 10 (2025)”, Q1, rank 18/237; two third-party aggregators (journalsimpactfactors.com, askbisht.com; accessed 26 August 2026) list the 2025 JCR value as 7.5 (Q1, 23/230) — verify against Clarivate JCR before citing a number anywhere.", { size: 20 })),
  para(run("JAHA: Editor-in-Chief year-in-review (Ovbiagele, J Am Heart Assoc 2026) — 22-day mean to first decision (2025); 18% acceptance for original research; 41st of 230 by 2024 IF.", { size: 20 })),
  para(run("NMCD: journalmetrics.org (2025 IF 3.9, June 2026 release); Italian Society of Human Nutrition journal page.", { size: 20 })),
  para(run("Open Heart: BMJ official journal statistics page (2025) — IF 3.1; acceptance 32%; median 3 days desk / 45 days with review / 22 days acceptance→publication.", { size: 20 })),
  para(run("BMC Cardiovascular Disorders: Springer Nature official journal page — 2025 IF 3.1; median 16 days to first decision; journalmetrics.org — ~108 days median submission-to-acceptance; indicative APC US$2,690 (OpenAlex, verify).", { size: 20 })),
  para(run("Annals of Medicine: Taylor & Francis official journal page — 2025 IF 4.9, Q1.", { size: 20 })),
  para(run("CAS Early-Warning Lists 2020–2025: Chinese Academy of Sciences National Science Library, as republished by university research offices (e.g., ynctv.edu.cn, csu.edu.cn, fjut.edu.cn).", { size: 20 })),
  para(run("Note: impact factors are journal-level averages and do not predict individual article citations; speed/acceptance figures are journal aggregates, not guarantees for a specific manuscript.", { size: 18, color: palette.light, italics: true }), { spacing: { before: 160 } })
);
const doc2 = new Document({
  sections: [{ properties: { page: { margin: { top: 1200, bottom: 1200, left: 1200, right: 1200 } } },
    footers: { default: new Footer({ children: [para(new TextRun({ children: [PageNumber.CURRENT] }), { alignment: AlignmentType.CENTER })] }) },
    children: S }],
});
fs.writeFileSync(out2, await Packer.toBuffer(doc2));
console.log("written:", out2);
