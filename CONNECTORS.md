# Connectors (placeholder — v2)

Marketing Analytics Pack v1 is **files-only**. Bring a CSV, an Excel file, or paste a table; the planner and readiness checker take it from there.

This document is a placeholder for the **v2 surface area** — direct connections to data warehouses, marketing platforms, and analytics tools via MCP. The intent is to keep the v1 boundary honest while marking what we plan to wire up next.

## Today (v1) — what works without connectors

- CSV / Excel / pasted-table input.
- Any MCP **connector the user has already installed in Claude** (BigQuery, Snowflake, Postgres, Amplitude, HubSpot, Klaviyo, etc.) can be used as a data source today — describe the table or query result to Claude, and the pack's skills will work against it. Nothing in the pack assumes the connector is present.

## Planned (v2) — first-class connector support

A v2 release will ship a `.mcp.json` that pre-declares recommended connectors per cluster, plus skill-side hints so commands can fetch directly from a warehouse or marketing platform.

Likely first connectors (subject to availability and Anthropic plugin review):

| Cluster | Connectors of interest |
|---|---|
| Metrics, Diagnosis, Forecasting | BigQuery, Snowflake, Postgres, Databricks |
| Experimentation, MMM | BigQuery / Snowflake plus campaign-platform exports |
| Marketing operations, Segmentation | HubSpot, Klaviyo, Salesforce, Iterable |
| Web / SEO context | Amplitude, GA4, Ahrefs, SimilarWeb |

## Out of scope (for now)

- Bundling vendor SDKs inside the pack — connectors stay in the user's MCP config, not in `lib/`.
- Writing data back to source systems — read-only by design in v1 and v2.
- Authentication flows — the host MCP handles auth; the pack only reads what's already authorised.

## Open questions

- Should advanced runners (RFM / Prophet / Meridian) read directly from a connector, or stay file-only with a connector-export helper?
- How do we keep skill prompts portable across warehouses (Snowflake vs. BigQuery SQL dialects)? Likely answer: lean on the `data:sql-queries` skill from the data plugin rather than hand-rolling dialect logic here.
- Where does the connector list live so it stays in sync with the marketplace catalogue? Probably a CI check against the MCP registry.

This file will be filled in properly once we start the v2 milestone. Until then it locks the v1 boundary and signals intent.
