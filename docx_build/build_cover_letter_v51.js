import fs from "node:fs";
import path from "node:path";
import {
  AlignmentType, Document, Footer, Packer, PageNumber, Paragraph, TextRun,
} from "docx";

const out1 = process.argv[2];
if (!out1) throw new Error("Usage: node build_cover_letter_v51.js cover.docx");
fs.mkdirSync(path.dirname(out1), { recursive: true });

const font = { ascii: "Times New Roman", hAnsi: "Times New Roman", cs: "Times New Roman", eastAsia: "SimSun" };
const palette = { dark: "263238", light: "78909C" };
const run = (text, o = {}) => new TextRun({ text, font, size: 24, ...o });
const para = (children, o = {}) =>
  new Paragraph({ spacing: { after: 140, line: 340 }, ...o, children: Array.isArray(children) ? children : [children] });

const L = [];
L.push(
  para(run("Cover Letter", { bold: true, size: 30, color: palette.dark }), { alignment: AlignmentType.CENTER, spacing: { after: 300 } }),
  para([run("Date: "), run("11 October 2026")]),
  para([run("To: "), run("The Editor-in-Chief, Nutrition, Metabolism and Cardiovascular Diseases", { bold: true })]),
  para([run("Re: "), run("Submission of original research manuscript — “Sweetened Beverage Consumption and Atrial Fibrillation: Two-Sample and Multivariable Mendelian Randomization”", { bold: true })]),
  para(run("Dear Editor-in-Chief,")),
  para(run("We are pleased to submit the above original research manuscript for consideration by Nutrition, Metabolism and Cardiovascular Diseases. The journal’s remit at the interface of nutrition, metabolism and cardiovascular disease is precisely where this study sits: we ask whether genetically proxied consumption of sweetened beverages—including the sugar and caffeine components that define milk-tea-type beverages, a dietary exposure now ubiquitous among young East Asians—is causally associated with atrial fibrillation (AF).")),
  para(run("Using public genome-wide association study (GWAS) summary statistics, we instrumented seven beverage phenotypes in UK Biobank (N = 64,949–447,485) and estimated their effects on AF in the largest available European-ancestry GWAS (Nielsen 2018; 60,620 cases; primary), in FinnGen release R13 (67,783 cases), which shares no participants with UK Biobank and served as a co-primary, overlap-free outcome, in AFGen 2018 (sensitivity), and in BioBank Japan (East Asian contextual arm). No sweetened-beverage exposure showed evidence of a causal association with AF, and the null estimates exclude moderate-to-large effects of the magnitude reported observationally. The single nominal signal—for coffee intake (European meta-analytic OR 1.34, 1.11–1.62; P = 0.002)—failed every pre-specified robustness criterion and was dissected mechanistically: it attenuated after multivariable adjustment for body mass index (OR 0.82; P = 0.099), colocalized with AF only at the adiposity locus FTO and not at caffeine-metabolism loci, and was compatible with correlated pleiotropy in genome-wide CAUSE analysis. Cross-trait LD score regression showed that sweetened-beverage traits share genetic architecture with AF (rg = 0.24–0.31) despite null causal estimates—an instructive pleiotropy-versus-causation contrast—while a positive lifestyle control (alcoholic drinks per week) detected its established effect, confirming analytical sensitivity.")),
  para(run("The manuscript extends, and we believe will interest readers of this journal for, the question first examined in NMCD by Yuan and Larsson (2019) for coffee: it brings the same causal-inference logic to the full sweetened-beverage spectrum at roughly sixteen times the outcome case count, adds multivariable modelling of adiposity, locus-level colocalization, robust profile-score (MR-RAPS) and weak-instrument (conditional F) diagnostics, and frames the milk-tea question that cohort studies have not yet been able to ask directly. The work was strengthened through external peer review received during earlier submissions, which added the weak-instrument-robust estimators, the conditional F analysis and the East Asian contextual arm.")),
  para(run("This manuscript is original, has not been published previously and is not under consideration by any other journal. All analyses used publicly available, de-identified summary statistics; no individual-level data were accessed. The authors declare no conflicts of interest and received no specific funding for this work. Both authors have read and approved the submitted version and agree to its submission to Nutrition, Metabolism and Cardiovascular Diseases. Dataset identifiers are listed in the manuscript, and complete analysis code, harmonized datasets and result tables are publicly archived with a DOI (https://doi.org/10.5281/zenodo.22099675). In accordance with journal policy on generative AI, we disclose that portions of the analysis workflow and drafting were assisted by an artificial-intelligence tool (Kimi, Moonshot AI); all content was independently verified and approved by the authors, who take full responsibility for the integrity of the work.")),
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
