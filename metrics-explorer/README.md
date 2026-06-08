# GBLS Metrics Explorer

A dependency-free JavaScript dashboard for exploring the coded-summary feature files.

## Open it

Double-click `metrics-explorer/index.html`. The data is bundled in
`../2-outputs/metrics/metrics-explorer-synthesized-data.js`, so the dashboard does not require npm,
internet access, or a web server.

If a browser restricts local JavaScript files, run a local server from this folder:

```bash
python3 -m http.server 8765
```

Then visit `http://localhost:8765`.

## Files

- `metrics-explorer/index.html`: dashboard page
- `metrics-explorer/metrics-explorer.js`: filters, SVG charts, and article table
- `metrics-explorer/metrics-explorer.css`: responsive visual design
- `2-outputs/metrics/metrics-explorer-synthesized-data.js`: generated data bundle from the CSV
  feature files
- `2-outputs/metrics/`: all generated CSV, workbook, documentation, and validation artifacts
