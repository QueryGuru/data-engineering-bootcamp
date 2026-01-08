# Data Engineering Bootcamp – Pipeline Architecture

## 1. Problem Statement
Ingest CRM ticket data from an API, store raw data safely,
transform it into analytics-ready models, and support both
batch and near-real-time use cases.

## 2. Data Sources

### Source: CRM API
- Type: REST API
- Data: Tickets, Users
- Update Pattern: Incremental (updated_at)
- Expected Volume: Low to medium (100s–1000s rows/day)

### Data Contract Assumptions
- `id` is immutable
- `updated_at` is monotonic per record
- Deleted records are rare or soft-deleted

## 3. Pipeline Layers

### Bronze (Raw)
Purpose:
- Store data exactly as received
- Enable reprocessing and audits

Characteristics:
- JSON or lightly structured tables
- Append-only
- Partitioned by ingestion_date

Failure Tolerance:
- High (bad data allowed)

---

### Silver (Validated)
Purpose:
- Enforce schema
- Clean and standardize fields

Characteristics:
- Typed columns
- Invalid records rejected
- One row per business entity

Failure Tolerance:
- Medium (bad rows rejected, pipeline continues)

---

### Gold (Analytics)
Purpose:
- Serve BI and analytics use cases

Characteristics:
- Star schema
- Business metrics
- Incremental updates

Failure Tolerance:
- Low (must be correct)

## 4. Incremental Processing Strategy

- Watermark column: `updated_at`
- State storage: metadata table (last_successful_run)

Ingestion logic:
- Fetch records where updated_at > last_run
- Write to bronze with ingestion timestamp
- Deduplicate on (id, updated_at)

Idempotency guarantee:
- Re-running the same date produces the same result

## 5. Failure Scenarios & Handling

### Scenario 1: API timeout
- Impact: Partial data ingestion
- Handling:
  - Retry with backoff
  - Resume from last successful page

### Scenario 2: Schema change in API
- Impact: Silver layer failure
- Handling:
  - Bronze still stores raw data
  - Schema validation fails loudly
  - Alert triggered

### Scenario 3: Pipeline crashes mid-run
- Impact: Incomplete batch
- Handling:
  - Idempotent writes
  - Safe rerun using watermark

### Scenario 4: Bad data (nulls, invalid enums)
- Impact: Analytics corruption
- Handling:
  - Reject rows in silver
  - Log rejection metrics

## 6. Orchestration

Tool: Apache Airflow (local)

DAG Structure:
- Task 1: Ingest API → Bronze
- Task 2: Validate → Silver
- Task 3: Transform → Gold
- Task 4: Data quality checks

Schedule:
- Daily batch
- Manual backfills supported

Retry Strategy:
- Task-level retries
- No DAG-level blind retries

## 7. Cost & Performance Considerations

- Partitioned BigQuery tables
- Incremental queries only
- Avoid SELECT *
- Limit streaming usage
- Use batch where latency allows
