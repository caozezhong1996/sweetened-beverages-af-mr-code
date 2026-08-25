# -*- coding: utf-8 -*-
"""check_refs_pubmed.py — verify all 28 manuscript references against PubMed (v4).

v3 fixes: stopword-filtered distinctive-word + "Lastname I[Author]" queries;
correction/erratum records deprioritized; journal-match scoring; elocation handling.
v4: 28 refs (AHA 2026 scientific statement inserted as ref 7); supports
epub-ahead-of-print citations of the form "Journal. Year. doi:..." (DOI check).
"""
import io, json, re, sys, time, urllib.parse, urllib.request

MS = r"C:\Users\64915\Documents\kimi\workspace\奶茶房颤MR_迁移包_20260822\04_docx构建脚本\build_manuscript_v45.js"
EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
STOP = set("""between from with without within among amongst across after before under over into onto upon about above below
their there these those which where while whilst using used use based via per and the for are was were has have had not but all
can may might its his her our their who how what when than then thus also such this that each both neither either one two six
among along against during through toward towards""".split())

src = io.open(MS, encoding="utf-8").read()
refs = re.findall(r"T`(\d{1,2})\.\s+([^`]+?)`,\n", src)
refs = [(int(n), t) for n, t in refs if 1 <= int(n) <= 28][-28:]
assert len(refs) == 28


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "ref-check/3.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "replace")


def esearch(term):
    url = f"{EUTILS}/esearch.fcgi?db=pubmed&retmode=json&term={urllib.parse.quote(term)}"
    res = json.loads(get(url))["esearchresult"]
    time.sleep(0.45)
    return res.get("idlist", [])


def esummary(pmid):
    s = json.loads(get(f"{EUTILS}/esummary.fcgi?db=pubmed&retmode=json&id={pmid}"))["result"][pmid]
    time.sleep(0.45)
    return s


def norm_pages(p):
    m = re.match(r"^(\d+)-(\d+)$", p or "")
    if not m:
        return p or ""
    a, b = m.group(1), m.group(2)
    if len(b) < len(a):
        b = a[: len(a) - len(b)] + b
    return f"{a}-{b}"


def sim(a, b):
    aw = set(re.findall(r"[a-z]{3,}", a.lower())); bw = set(re.findall(r"[a-z]{3,}", b.lower()))
    return len(aw & bw) / max(1, len(aw))


print(f"{'#':>2} {'verdict':<7} {'PMID':<9} detail")
problems = []
for n, full in refs:
    parts = full.split(". ")
    first_author_cited = parts[0].split(",")[0].strip()          # e.g. "Van Gelder IC"
    claimed_title = parts[1].rstrip(".")
    rest = ". ".join(parts[2:])
    m = re.match(r"(.+?)\. (\d{4});(\d+)?(?:\(([^)]+)\))?:(\S+?)\.?(?: |$)", rest)
    if m:
        claimed_journal, claimed_year = m.group(1), m.group(2)
        claimed_vol = m.group(3) or ""
        claimed_issue = m.group(4) or ""
        claimed_pages = m.group(5).rstrip(".")
        claimed_doi = ""
    else:
        m2 = re.match(r"(.+?)\. (\d{4})\. doi:(\S+?)\.?$", rest)
        assert m2, f"ref {n}: unparseable citation tail: {rest}"
        claimed_journal, claimed_year = m2.group(1), m2.group(2)
        claimed_vol = claimed_issue = claimed_pages = ""
        claimed_doi = m2.group(3).rstrip(".")

    words = [w for w in re.findall(r"[A-Za-z]{4,}", claimed_title) if w.lower() not in STOP][:4]
    queries = [
        " AND ".join(f"{w}[Title]" for w in words) + f" AND {first_author_cited}[Author]",
        " AND ".join(f"{w}[Title]" for w in words[:3]) + f" AND {first_author_cited}[Author]",
        f"{first_author_cited}[Author] AND {claimed_journal}[Journal] AND {claimed_year}[Date - Publication]",
    ]
    ids = []
    for q in queries:
        ids = esearch(q)
        if ids:
            break
    if not ids:
        print(f"{n:>2} MISS    no PubMed hit: {claimed_title[:70]}")
        problems.append(n)
        continue

    best = None
    for pmid in ids[:6]:
        s = esummary(pmid)
        pt = " ".join(s.get("pubtype", []))
        t_sim = sim(claimed_title, s.get("title", ""))
        cj = re.sub(r"[. ]", "", claimed_journal).lower()
        aj = re.sub(r"[. ]", "", s.get("source", "")).lower()
        j_bonus = 0.3 if cj == aj else 0.0
        corr_pen = -0.5 if ("Correction" in pt or "Erratum" in pt or "Letter" in pt or "Comment" in pt) else 0.0
        score = t_sim + j_bonus + corr_pen
        if best is None or score > best[0]:
            best = (score, t_sim, pmid, s)
    _, t_sim, pmid, s = best
    if t_sim < 0.6:
        print(f"{n:>2} MISS    best title sim={t_sim:.2f}: '{s.get('title','')[:70]}' (PMID {pmid})")
        problems.append(n)
        continue

    authors = s.get("authors") or []
    actual_first = authors[0]["name"] if authors else ""
    actual_journal = s.get("source", "")
    actual_year = s.get("pubdate", "")[:4]
    actual_vol = s.get("volume", "") or ""
    actual_issue = s.get("issue", "") or ""
    actual_pages = norm_pages(s.get("pages", ""))
    if not actual_pages:
        elo = s.get("elocationid", "") or ""
        mm = re.search(r"(\w*?\d[\w\d]*)$", elo)
        actual_pages = ("e" + mm.group(1)) if mm else elo

    diffs = []
    ln_c = re.sub(r"\s+[A-Z]{1,3}$", "", first_author_cited).lower()
    ln_a = re.sub(r"\s+[A-Z]{1,3}$", "", actual_first).lower()
    if ln_a and ln_c != ln_a:
        diffs.append(f"first-author claimed='{first_author_cited}' actual='{actual_first}'")
    cj = re.sub(r"[. ]", "", claimed_journal).lower()
    aj = re.sub(r"[. ]", "", actual_journal).lower()
    if cj != aj:
        diffs.append(f"journal claimed='{claimed_journal}' actual='{actual_journal}'")
    if actual_year != claimed_year:
        diffs.append(f"year claimed={claimed_year} actual={actual_year}")
    if claimed_doi:
        doi_actual = next((a.get("value", "") for a in s.get("articleids", [])
                           if a.get("idtype") == "doi"), "")
        if doi_actual.lower() != claimed_doi.lower():
            diffs.append(f"doi claimed={claimed_doi} actual={doi_actual}")
    else:
        if actual_vol != claimed_vol:
            diffs.append(f"volume claimed={claimed_vol} actual={actual_vol}")
        if actual_issue != claimed_issue:
            diffs.append(f"issue claimed={claimed_issue} actual={actual_issue}")
        cp = claimed_pages.replace("–", "-").lower()
        if actual_pages.lower() != cp:
            diffs.append(f"pages claimed={claimed_pages} actual={actual_pages}")

    verdict = "OK" if not diffs else "DIFF"
    if diffs:
        problems.append(n)
    print(f"{n:>2} {verdict:<7} {pmid:<9} " + ("; ".join(diffs) if diffs else
          f"{actual_journal} {actual_year};{actual_vol}({actual_issue}):{actual_pages}"))

print()
print("PROBLEM REFS:", problems if problems else "none — all 28 verified against PubMed")
sys.exit(1 if problems else 0)
