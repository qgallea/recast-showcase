# RECAST showcase website

### 🌐 Live site: **https://qgallea.github.io/recast-showcase/**

A [Quarto](https://quarto.org) website that showcases the RECAST project
(Replication and Extension with Causal AI Statistical Toolkit) and its results on
six econometrics papers — spanning PLR, IRM + generic ML, PLIV, and
difference-in-differences — plus a candidate-scouting page.

> 🚧 **Under active development & testing.** Results have not been independently
> verified. Do not cite or rely on any output without manual review.

## Layout
- `index.qmd` — landing (method-first)
- `methodology.qmd` + `methodology/` — how it works (incl. a pipeline diagram), the
  2-referee review, honest method-path coverage, the Phase-1 walkthrough
- `papers.qmd` + `papers/<slug>/` — the gallery and the six paper pages
- `candidates.qmd` — the candidate-scouting list (from the AEA Replication Tracker)
- `theme/custom.scss` — clean-academic theme (cosmo base)
- `tools/build_pages.py`, `tools/build_candidates.py`, `tools/make_*figure*.py` —
  one-time author tools that (re)generate the static pages/figures from the project
  artifacts; they are author-side only and not needed to render the committed site.

The site uses Quarto's **markdown engine** — no code runs at build time, so any
machine with Quarto can render it (`quarto render` / `quarto preview`).

## Publishing
This public repo (`recast-showcase`) is a clean subtree of the private project repo
(`recast_v2`) containing **only** the website — no code, data, or PDFs. Its
[`.github/workflows/publish.yml`](.github/workflows/publish.yml) renders the Quarto
project and deploys it to GitHub Pages on every push to `main` (Settings → Pages →
Source = GitHub Actions).
