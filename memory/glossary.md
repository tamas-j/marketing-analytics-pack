# Glossary

Shorthand and internal language for the Marketing Analytics Pack build.

## Acronyms / terms
| Term | Meaning |
|------|---------|
| MAP | Marketing Analytics Pack (this plugin) |
| Pack | Same — the plugin as a whole |
| Core skill | Light-dep skill: prompt + matplotlib, installs instantly |
| Advanced runner | Heavier-dep skill (RFM, Forecast, MMM) that pip-installs deps on first use |
| Style system | `lib/visualize.py` + `lib/styles/*.yaml` — shared visual layer used by every skill that draws |
| Front door | The three entry-point skills: Style picker, Main analysis planner, Data readiness checker |
| KPI tree | First skill to be built — proof-of-pattern for the whole pack |
| MMM | Marketing Mix Modelling — built on Google Meridian (chosen over PyMC-Marketing) |
| Meridian | Google's open-source MMM library — the MMM runner uses this |
| Prophet | Facebook/Meta's open-source forecasting library — the Forecast runner uses this |
| RFM | Recency / Frequency / Monetary segmentation |
| CLV | Customer Lifetime Value |
| NBA | Next Best Action |
| URB-182 | Linear ticket for this build (parent: URB-181) |
| URB-181 | Parent Linear ticket — the broader "ship portfolio" initiative this reframes |

## Distribution targets
| Target | Notes |
|--------|-------|
| GitHub | `github.com/tamas-j/marketing-analytics-pack` — primary |
| Anthropic marketplace | `claude.ai/settings/plugins/submit` |
| claudepluginhub | Third-party marketplace (open submission verified May 2026) |
| claudemarketplaces | Third-party marketplace (open submission verified May 2026) |

## Bundled visual styles
| Style | When to use |
|-------|-------------|
| `default` | General-purpose, clean, balanced |
| `executive` | Higher-contrast, fewer gridlines, headline-friendly |
| `custom` | User-tunable via the Style picker skill |
