"""Generate the RECAST candidates page from the scout ledger.

One-time author tool (mirrors build_pages.py): reads recast_fable/scout/ledger.json and
emits website/candidates.qmd — a static page with the scouting explanation, a summary, and
two tables (suitable candidates; screened-but-out-of-scope). Re-runnable. Not a build
dependency: the emitted .qmd is committed and renders with plain Quarto.

Run from recast_fable/website/:
    ../phase1/.venv/Scripts/python.exe tools/build_candidates.py
"""
import json
from pathlib import Path

WEB = Path(__file__).resolve().parents[1]            # recast_fable/website
LEDGER = WEB.parent / "scout" / "ledger.json"        # recast_fable/scout/ledger.json
OUT = WEB / "candidates.qmd"


def esc(s):
    return str(s if s is not None else "").replace("|", "\\|").replace("\n", " ")


def doi_link(doi):
    return f"[{esc(doi)}](https://doi.org/{esc(doi)})"


def paper_cell(rec):
    title = esc(rec.get("title") or rec.get("doi"))
    return f"[{title}](https://doi.org/{esc(rec.get('doi'))})"


def row(rec):
    sc = rec.get("screen") or {}
    dec = (rec.get("decision") or {}).get("human") or "—"
    pipe = (rec.get("pipeline") or {}).get("status") or "—"
    return (sc.get("provisional_model") or "—", paper_cell(rec),
            esc(rec.get("journal")), str(rec.get("year") or "—"),
            esc(rec.get("repo_status")), sc, dec, pipe)


def main():
    led = json.loads(LEDGER.read_text(encoding="utf-8"))
    recs = list(led.get("records", {}).values())
    crawls = led.get("meta", {}).get("crawls", [])

    evaluated = [r for r in recs if r.get("screen")]
    suitable = [r for r in evaluated if (r.get("screen") or {}).get("suitable")]
    not_suitable = [r for r in evaluated if not (r.get("screen") or {}).get("suitable")]
    backlog = [r for r in recs if not r.get("screen")]            # harvested, unscreened

    years = sorted({r.get("year") for r in recs if r.get("year")}, reverse=True)
    last_crawl = crawls[-1]["date"] if crawls else "—"

    out = []
    out.append("---")
    out.append('title: "Candidate scouting"')
    out.append('description: "Recent papers with available replication packages, '
               'screened for whether RECAST can handle their identification design."')
    out.append("toc: true")
    out.append("---\n")

    # intro
    out.append("RECAST continuously scouts recently published economics papers that it "
               "*could* process. It reads the [AEA Replication Tracker]"
               "(https://paulgp.com/replication-package-db/) "
               "(P. Goldsmith-Pinkham) to find papers whose **replication package is "
               "available**, enriches each with its abstract, and classifies the "
               "identification design to decide whether it falls in a method path RECAST "
               "supports. Every paper looked at is recorded below — accepted *and* "
               "rejected — so the coverage is auditable.\n")

    out.append("::: {.callout-note}\n## How to read this\n"
               "This is an **abstract-only screen**, not a verdict. The design is inferred "
               "from the title and abstract, so each row carries a confidence and the "
               "authoritative routing only happens at real intake. \"Suitable\" means the "
               "design maps to a supported RECAST estimand "
               "([see Coverage](methodology/coverage.qmd)); it does **not** mean the paper "
               "has been replicated. The pipeline outcome column tracks papers that have "
               "actually been run.\n:::\n")

    # how scouting works
    out.append("## How scouting works\n")
    out.append(
        "1. **Pull the index** — read the AEA Replication Tracker's data-availability "
        "lookup (DOI → package status).\n"
        "2. **Filter** to papers whose replication package is `full_data` or "
        "`partial_data`.\n"
        "3. **Enrich** each DOI with title + abstract via OpenAlex (Semantic Scholar "
        "fallback for missing abstracts).\n"
        "4. **Classify the design** (RCT / selection-on-observables / IV / panel-DiD / "
        "other) and treatment type from the abstract, and route it through the *same* "
        "estimand router the pipeline uses.\n"
        "5. **Record every paper** — accept or reject, with a reason and a confidence — "
        "in an append-only ledger (this page is generated from that ledger).\n"
        "6. **Human gate** — a suitable paper is only *suggested*; running the full "
        "replicate → extend → review pipeline is a separate, explicit step that writes "
        "the result back to the **pipeline** column below.\n")

    # summary glance
    out.append("## At a glance\n")
    out.append("::: {.glance}")
    for k, v in (("Papers crawled", len(recs)),
                 ("Screened", len(evaluated)),
                 ("Suitable", len(suitable)),
                 ("Awaiting screen", len(backlog)),
                 ("Years scouted", ", ".join(str(y) for y in years) or "—"),
                 ("Last crawl", last_crawl)):
        out.append(f'<div class="g"><span class="k">{k}</span>'
                   f'<span class="v">{v}</span></div>')
    out.append(":::\n")

    # suitable table
    out.append("## Suitable candidates\n")
    if suitable:
        out.append("Papers whose design maps to a supported RECAST path. "
                   "*Provisional model* is the estimand RECAST would route to; "
                   "*decision* is the human accept/reject; *pipeline* is the actual "
                   "replication/extension outcome once run.\n")
        out.append("| Model | Paper | Journal | Year | Data | Conf. | Decision | Pipeline |")
        out.append("|---|---|---|---|---|---|---|---|")
        for r in sorted(suitable, key=lambda r: -((r.get("screen") or {}).get("confidence") or 0)):
            m, paper, jour, yr, data, sc, dec, pipe = row(r)
            conf = sc.get("confidence")
            conf = f"{conf:.2f}" if isinstance(conf, (int, float)) else "—"
            out.append(f"| {m} | {paper} | {jour} | {yr} | {esc(data)} | {conf} "
                       f"| {esc(dec)} | {esc(pipe)} |")
    else:
        out.append("*(none yet)*\n")

    # not-suitable table
    out.append("\n## Screened — out of scope\n")
    if not_suitable:
        out.append("Papers looked at whose design RECAST does not currently handle "
                   "(or whose abstract was unavailable to screen). Recorded for "
                   "transparency.\n")
        out.append("| Paper | Journal | Year | Why not |")
        out.append("|---|---|---|---|")
        for r in not_suitable:
            sc = r.get("screen") or {}
            out.append(f"| {paper_cell(r)} | {esc(r.get('journal'))} "
                       f"| {r.get('year') or '—'} | {esc(sc.get('reason'))} |")
    else:
        out.append("*(none yet)*\n")

    # backlog note
    if backlog:
        by_year = {}
        for r in backlog:
            by_year[r.get("year")] = by_year.get(r.get("year"), 0) + 1
        yr_txt = ", ".join(f"{y}: {n}" for y, n in sorted(by_year.items(),
                                                          key=lambda x: (x[0] or 0),
                                                          reverse=True))
        out.append(f"\n[**{len(backlog)}** more data-available papers have been harvested "
                   f"and are queued for screening ({yr_txt}).]{{.text-muted-sm}}\n")

    out.append("\n---\n")
    out.append("[Replication-availability data: the AEA Replication Tracker "
               "(paulgp/replication-package-db). Paper metadata + abstracts: OpenAlex / "
               "Semantic Scholar. Designs are screened from abstracts only — see the "
               "[methodology](methodology/coverage.qmd).]{.text-muted-sm}\n")

    OUT.write_text("\n".join(out), encoding="utf-8")
    print(f"candidates.qmd written: {len(recs)} records "
          f"({len(suitable)} suitable, {len(not_suitable)} out-of-scope, "
          f"{len(backlog)} queued)")


if __name__ == "__main__":
    main()
