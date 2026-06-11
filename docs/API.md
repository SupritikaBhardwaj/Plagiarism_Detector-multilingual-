# API Documentation

## Health

`GET /health`

Returns service status.

## Authentication

`POST /api/auth/login`

```json
{
  "username": "student@example.com",
  "password": "secret"
}
```

Returns a JWT bearer token. The current scaffold uses demo authentication; production deployments should connect `backend/auth` to PostgreSQL users and role tables.

## Code and Document Comparison

`POST /api/analysis/compare`

```json
 {
   "left": {
     "name": "left.py",
     "language": "python", // Optional: If not provided, language will be auto-detected.
     "content": "def add(a, b): return a + b"
   },
   "right": {
     "name": "right.py",
     "language": "python", // Optional: If not provided, language will be auto-detected.
     "content": "def sum(x, y): return x + y"
   },
   "enable_ai": true
 }
```

Response fields:

- `overall_similarity` - weighted ensemble score.
- `breakdown` - text, token, AST, graph, semantic, stylometry, and AI-generation scores.
- `evidence` - explainable reasons for the score.
- `ast`, `cfg`, `pdg` - visualization payloads.
- `highlighted_regions` - copied or highly similar regions.

## Upload Comparison

`POST /api/analysis/upload-compare`

Multipart fields: `left`, `right`, and optional `language`.

## Live Analysis

`WS /api/analysis/live`

Sends progress events and final report payloads for real-time scanning.

## Report Export

- `POST /api/reports/json`
- `POST /api/reports/csv`
