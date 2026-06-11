# Database Schema

## PostgreSQL

```sql
CREATE TABLE users (
  id UUID PRIMARY KEY,
  email TEXT UNIQUE NOT NULL,
  password_hash TEXT NOT NULL,
  role TEXT NOT NULL DEFAULT 'student',
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE submissions (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  name TEXT NOT NULL,
  language TEXT NOT NULL,
  sha256 TEXT NOT NULL,
  storage_uri TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE reports (
  id UUID PRIMARY KEY,
  left_submission_id UUID REFERENCES submissions(id),
  right_submission_id UUID REFERENCES submissions(id),
  overall_similarity NUMERIC(5, 4) NOT NULL,
  risk_level TEXT NOT NULL,
  created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE report_scores (
  report_id UUID REFERENCES reports(id),
  metric TEXT NOT NULL,
  score NUMERIC(5, 4) NOT NULL,
  PRIMARY KEY (report_id, metric)
);
```

## MongoDB

Collections:

- `analysis_artifacts` - AST, CFG, PDG, IR, highlight spans, and parser diagnostics.
- `batch_jobs` - queued classroom or institution-level scans.
- `audit_events` - security and administrative activity.

## Redis

Keys:

- `scan:{job_id}:progress`
- `fingerprint:{submission_hash}`
- `embedding:{submission_hash}`

## Elasticsearch

Indexes:

- `submissions` - searchable metadata and extracted text.
- `fingerprints` - token and document shingles.
- `reports` - report archive search.

