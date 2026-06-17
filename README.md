# RECAST showcase website

A [Quarto](https://quarto.org) website that showcases the RECAST project
(Replication and Extension with Causal AI Statistical Toolkit) and its validated
results on four econometrics papers.

## Layout
- `index.qmd` — landing (method-first)
- `methodology.qmd` + `methodology/` — how it works, the 2-referee review, honest coverage, the Phase-1 walkthrough
- `papers.qmd` + `papers/<slug>/` — the gallery and the four paper pages
- `theme/custom.scss` — clean-academic theme (cosmo base)
- `tools/build_pages.py` — one-time author tool that generates the four paper
  pages from the Phase-2 artifacts under `../phase2/projects/<slug>/`
- `tools/make_ag_figure.py` — generates the Ashraf–Galor dose-response figure

The site uses Quarto's **markdown engine** — no code runs at build time, so any
machine with Quarto can render it. The Python tools above are author-side only.

## Build locally
```bash
# (re)generate paper pages + the AG figure  (run from this folder)
../phase1/.venv/Scripts/python.exe tools/make_ag_figure.py
../phase1/.venv/Scripts/python.exe tools/build_pages.py
# render / preview
quarto render
quarto preview
```

## Deploy to GitHub Pages
This folder is part of the `recast_v2` repo. The deploy workflow is already
written at `../.github/workflows/publish.yml` (Quarto's official Pages action:
checkout → setup → render `website/` → upload `website/_site` → deploy; runs on
push to `main`). No Python step is needed — the pages and the AG figure are
pre-generated and committed. To go live:
1. Repo **Settings → Pages → Source = GitHub Actions**.
2. Confirm `site-url` / `repo-url` in `_quarto.yml` match the repo, then push to
   `main`. The workflow renders and publishes automatically.
