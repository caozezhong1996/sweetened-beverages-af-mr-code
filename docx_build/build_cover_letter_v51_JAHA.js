import fs from "node:fs";
import path from "node:path";
import {
  AlignmentType, Document, Footer, Packer, PageNumber, Paragraph, TextRun,
} from "docx";

const out1 = process.argv[2];
if (!out1) throw new Error("Usage: node build_cover_letter_v51_JAHA.js cover.docx");
fs.mkdirSync(path.dirname(out1), { recursive: true });

const font = { ascii: "Times New Roman", hAnsi: "Times New Roman", cs: "Times New Roman", eastAsia: "SimSun" };
const palette = { dark: "263238", light: "78909C" };
const run = (text, o = {}) => new TextRun({ text, font, size: 24, ...o });
const para = (children, o = {}) =>
  new Paragraph({ spacing: { after: 140, line: 340 }, ...o, children: Array.isArray(children) ? children : [children] });

const L = [];
L.push(
  para(run("Cover Letter", { bold: true, size: 30, color: palette.dark }), { alignment: AlignmentType.CENTER, spacing: { after: 300 } }),
  para([run("Date: "), run("13 October 2026")]),
  para([run("To: "), run("The Editor-in-Chief, Journal of the American Heart Association", { bold: true })]),
  para([run("Re: "), run("Submission of original research manuscript — “Sweetened Beverage Consumption and Risk of Atrial Fibrillation: A Two-Sample and Multivariable Mendelian Randomization Study With East Asian Contextual Analysis”", { bold: true })]),
  para(run("Dear Editor-in-Chief,")),
  para(run("We are pleased to submit the above original research manuscript for consideration by the Journal of the American Heart Association. JAHA’s broad cardiovascular remit—spanning epidemiology, nutrition and preventive cardiology—is where this study sits, and the work speaks directly to a priority identified in the American Heart Association’s 2026 scientific statement on caffeine and cardiovascular disease (Marcus et al., Circulation 2026): the need to distinguish caffeine itself from the components co-consumed with it in modern beverages. We ask whether genetically proxied consumption of sweetened beverages—including the sugar and caffeine components that define milk-tea-type beverages, a dietary exposure now ubiquitous among young East Asians—is causally associated with atrial fibrillation (AF).")),
  para(run("Using public genome-wide association study (GWAS) summary statistics, we instrumented seven beverage phenotypes in UK Biobank (N = 64,949–447,485) and estimated their effects on AF in the largest available European-ancestry GWAS (Nielsen 2018; 60,620 cases; primary), in FinnGen release R13 (67,783 cases), which shares no participants with UK Biobank and served as a co-primary, overlap-free outcome, in AFGen 2018 (sensitivity), and in BioBank Japan (East Asian contextual arm). No sweetened-beverage exposure showed evidence of a causal association with AF, and the null estimates exclude moderate-to-large effects of the magnitude reported observationally. The single nominal signal—for coffee intake (European meta-analytic OR 1.34, 1.11–1.62; P = 0.002)—failed every pre-specified robustness criterion and was dissected mechanistically: it attenuated after multivariable adjustment for body mass index (OR 0.82; P = 0.099), colocalized with AF only at the adiposity locus FTO and not at caffeine-metabolism loci, and was compatible with correlated pleiotropy in genome-wide CAUSE analysis. Biomarker-level MR of plasma caffeine, paraxanthine and theobromine—whose instruments are anchored in caffeine-metabolism biology rather than self-reported behavior—likewise returned null estimates; this arm extends the two-variant plasma-caffeine analysis of Larsson et al. (BMJ Med 2023), which reported null cardiovascular associations including atrial fibrillation, with independent multi-locus instruments and adds the first MR tests of paraxanthine and theobromine. Cross-trait LD score regression showed that sweetened-beverage traits share genetic architecture with AF (rg = 0.24–0.31) despite null causal estimates—an instructive pleiotropy-versus-causation contrast—while a positive lifestyle control (alcoholic drinks per week) detected its established effect, confirming analytical sensitivity.")),
  para(run("To our knowledge this is the first study to bring the full sweetened-beverage spectrum into a single, uniformly analyzed Mendelian randomization framework, at roughly sixteen times the outcome case count of prior beverage–AF MR work, and the first to combine multivariable adiposity modelling, locus-level colocalization, biomarker-level MR of plasma caffeine metabolites, robust profile-score (MR-RAPS) and weak-instrument (conditional F) diagnostics for these exposures, with an East Asian contextual arm that cohort studies have not yet been able to field directly. In total, the analysis spans ten exposures (seven behavioral beverage phenotypes and three plasma metabolites) plus cis estimation, four outcome sources including an overlap-free co-primary and an East Asian contextual arm, twenty-five supplementary tables, and fully archived code and harmonized datasets—a workload that distinguishes this study from its single-exposure predecessors. The work was strengthened through two rounds of external peer review received during earlier submissions elsewhere, which added the weak-instrument-robust estimators, the conditional F analysis, the biomarker-MR arm and the East Asian contextual arm.")),
  para(run("This manuscript is original, has not been published previously and is not under consideration by any other journal. All analyses used publicly available, de-identified summary statistics; no individual-level data were accessed. The authors declare no conflicts of interest and received no specific funding for this work. Both authors have read and approved the submitted version and agree to its submission to the Journal of the American Heart Association. Dataset identifiers are listed in the manuscript, and complete analysis code, harmonized datasets and result tables are publicly archived with a DOI (https://doi.org/10.5281/zenodo.22099675). In accordance with journal policy on generative AI, we disclose that portions of the analysis workflow and drafting were assisted by an artificial-intelligence tool (Kimi, Moonshot AI); all content was independently verified and approved by the authors, who take full responsibility for the integrity of the work.")),
  para(run("We hope you find the manuscript suitable for peer review, and we look forward to the editors’ and reviewers’ comments.")),
  para(run("Yours faithfully,"), { spacing: { after: 240 } }),
  para([run("Cao Zezhong, on behalf of both authors", { bold: true })]),
  para([run("The Affiliated Hospital of Yangzhou University, Yangzhou, Jiangsu, China")]),
  para([run("Email: caozezhong1996@163.com; ORCID: 0000-0002-8949-6078")]),
  para([run("Co-author: Chen Rongrong, The Affiliated Hospital of Yangzhou University, Yangzhou, Jiangsu, China (chenrrxh@126.com)")])
);
const doc1 = new Document({
  sections: [{ properties: { page: { margin: { top: 1440, bottom: 1440, left: 1440, right: 1440 } } },
    footers: { default: new Footer({ children: [para(new TextRun({ children: [PageNumber.CURRENT] }), { alignment: AlignmentType.CENTER })] }) },
    children: L }],
});
fs.writeFileSync(out1, await Packer.toBuffer(doc1));
console.log("written:", out1);
