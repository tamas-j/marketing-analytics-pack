# Sample datasets

Small synthetic datasets the worked examples can reference. None of
them are real customer data; everything is generated with a fixed seed.

| File | Rows | Use it for |
|---|---|---|
| `orders.csv` | 400 transactions | RFM segmentation, CLV scenarios, repeat-purchase analysis, suppression waterfall |
| `sessions.csv` | 800 sessions | KPI tree, customer journey, conversion rate analysis, attribution |
| `campaigns.csv` | 8 campaigns | Campaign post-mortem, attribution, frequency / fatigue, marketing taxonomy audit |
| `mmm-weekly.csv` | 96 weeks | MMM readiness check, MMM runner spec, MMM result interpretation, forecast method selection |
| `churn.csv` | 250 customers | Churn driver narrative, root cause investigation, retention KPI tree |

Sizes are deliberately small so the files load instantly in Claude and
fit in a single screen. For real analysis bring your own data; these
just let the example flows run end-to-end without you uploading
anything.
