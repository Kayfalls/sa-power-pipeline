# sa-power-pipeline

A batch ELT pipeline tracking South African load shedding data — from raw API script to an orchestrated, tested, cloud-warehoused pipeline.

**Status:** 🚧 Iteration 21 — split extract and load into separate Airflow tasks

## Roadmap
### Phase 1: Get data moving
- [x] Iteration 1: Repo setup
- [x] Iteration 2: First API call
- [x] Iteration 3: Timestamped raw dumps, quota tracking
- [x] Iteration 4: Basic error handling (401, 429, unexpected codes)
- [x] Iteration 5: Area Information endpoint (hardcoded area)
- [x] Iteration 6: Schedule Information endpoint

### Phase 2: Add discipline
- [x] Iteration 7: Refactored into functions ('fetch_status', 'fetch_area', 'fetch_schedule', 'main')
- [x] Iteration 8: Structured logging (INFO/WARNING/ERROR levels, timestamps)
- [x] Iteration 9: First unit tests (pytest, mocked responses, no live API calls)
- [x] Iteration 10: Proper src/ package layout, installable via pyproject.toml
- [x] Iteration 11: GitHub Actions CI (ruff lint + pytest on every push)
- [x] Iteration 12: Externalized config module, type hints, docstrings

### Phase 3: Real warehouse (BigQuery + dbt)
- [x] Iteration 13: GCP project  service account setup, first raw JSON load into BigQuery
- [x] Iteration 14: NDJSON format, generalized loader for status/area/schedule tables
- [x] Iteration 15: Combined extract + load into one 'run_pipeline.py' entrypoint
- [x] Iteration 16: dbt project initialized, connected to BigQuery
- [x] Iteration 17: stg_status staging model + schema tests
- [x] Iteration 18: extracted_at metadata, schema evolution handling
- [x] Iteration 19: mart_current_status model, unique/not_null tests, dbt docs

### Phase 4: Orchestrate + containerize
- [x] Iteration 20: First Airflow DAG, running in isolated venv, daily schedule, manual trigger verified
- [x] Iteration 21: Split into extract_from_eskomsepush and load_to_bigquery tasks
- [ ] Iteration 22: TBD

![CI](https://github.com/Kayfalls/sa-power-pipeline/actions/workflows/ci.yml/badge.svg)

## Data flow
EskomSePush API → raw JSON (NDJSON) → BigQuery `raw` dataset → dbt staging (`stg_status`) → dbt mart (`mart_current_status`)

## Airflow
1. 'export AIRFLOW_HOME=~/airflow'
2. 'airflow webserver --port 8080' and 'airflow scheduler' (separate terminals)
3. DAG: 'sa_power_pipeline', scheduled daiy

## Environments
This project uses two separate virtual environments due to dependency conflicts between Airflow and dbt:
- `.venv` — pipeline code, dbt, testing, linting
- `.venv-airflow` — Airflow only (also has the pipeline package installed via `pip install -e .` so DAGs can import it)

## Setup
1. Copy `.env.example` to `.env` and add your EskomSePush API token, GCP project ID, and path to your GCP service account key.
2. `pip install -r requirements.txt`
3. 'pip install -e .'
4. 'python src/sa_power_pipeline/fetch_status.py'


## Running tests
1. 'pip install -r requirements-dev.txt'
2. 'pytest -v'

Note to self:
remember to activate the environment: 
        'source .venv/bin/activate'

Verification code: WTC-QNYTS8NT
