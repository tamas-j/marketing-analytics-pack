# Project — Marketing Analytics Pack

**Codename:** MAP / Pack
**Linear:** URB-182 (parent URB-181, project Experiments, team Urbsai)
**Repo:** https://github.com/tamas-j/marketing-analytics-pack
**Status:** 0.1.0 scaffold complete; next is the shared visual style system.

## What it is
A coherent Claude plugin packaging 25 marketing/analytics skills across 7 clusters. Reframes the original "ship 3 portfolio projects" plan (URB-181) into a single product-shaped deliverable.

## Why this reframe
- Repositions Tamas from "person who built some skills" to "person who shipped an analytics product" — meaningfully more senior CV signal.
- One coherent product story with a front door, user journey, and install path beats a pile of disconnected skills.
- Public installable artefact with discovery beyond GitHub.
- Built incrementally — ship core skills, start applying for jobs while filling the pack.
- Marketplace listing (especially Anthropic-official) is a credentialing event in its own right.

## Target user
Non-technical marketing/analytics person who wants to do real analytical work but doesn't know how to start. The plugin's entry point is the Main analysis planner; the Data readiness checker validates input before any work begins.

## Architecture
- Tiered skills: most are **core** (prompt + matplotlib); three are **advanced runners** with heavier deps declared on first use.
- Shared visual style system: `lib/visualize.py` + `lib/styles/*.yaml`, three bundled styles (`default`, `executive`, `custom`), plus a Style picker front-door skill.
- File-only input for v1 (CSV / Excel / paste). Warehouse access deferred and documented.

## Build order
1. Scaffold + style system + KPI tree generator (proves the pattern)
2. Remaining front-door skills (Main analysis planner, Data readiness checker)
3. Metrics + Diagnosis + Marketing ops clusters
4. Experimentation cluster (includes MMM stack)
5. Segmentation + Forecasting clusters
6. Advanced runners — RFM, Forecast (Prophet), MMM (Meridian)
7. README polish + screenshots + sample data
8. GitHub publish
9. Marketplace submissions (Anthropic + 1–2 third-party)
10. Add GitHub URL to CV

## Success criteria
- 25 skills, consistent visual style, non-technical-friendly SKILL.md each
- Installable end-to-end on a fresh Claude install
- Working example flow on sample data
- Polished README on GitHub
- Submitted to Anthropic marketplace
- Listed on at least one third-party marketplace
- GitHub URL on Tamas's CV
- *(Stretch)* first external install / star / feedback

## Notes
- This ticket supersedes the "Claude analytics skill" project (#2) in URB-181 and consolidates with the broader skills approach. Project #1 (dbt Privizee pipeline) remains separately tracked. Project #3 (A/B testing / MMM) is absorbed here as the experimentation cluster + MMM runner.
- Visual style consistency is treated as **core infrastructure, not decoration** — mirrors Tamas's CV line at RAPP ("Established data visualisation standards adopted by a 5-person BI team").
