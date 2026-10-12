# Build log

This project was built one small step at a time, and each step is a commit. The early code is deliberately rough: it was refactored later, not written well on day one. This log keeps the honest version, including what broke.

## Phase 1: Get data moving

| Step | What changed | What went wrong or what I learned |
| --- | --- | --- |
| 1 | Repo, `.gitignore`, MIT license | The API token stays in an untracked `.env` from the first commit. |
| 2 | First call to the EskomSePush status endpoint | The first run that worked was a flat script printing JSON. |
| 3 | Timestamped snapshots and quota logging | Overwriting one file per run would have thrown away history. The API reports remaining quota in response headers. |
| 4 | Handling for 401, 429 and unexpected status codes | A script that only handles success is not finished. |
| 5 | Area endpoint, with a hardcoded area | The API needs three chained calls: area, then its schedules, then a schedule. |
| 6 | Schedule endpoint | The schedule ID has to come from the area response. A DNS failure on my machine looked like a code bug until I read the error. |

## Phase 2: Add discipline

| Step | What changed | What went wrong or what I learned |
| --- | --- | --- |
| 7 | API calls moved into functions with a `main()` | Same behaviour, but each call can now be tested on its own. |
| 8 | `print` replaced by structured logging | Unattended code needs timestamps and log levels. |
| 9 | First unit tests, with mocked API responses | Tests should never depend on the network or burn API quota. |
| 10 | `src/` package layout and `pyproject.toml` | Installing the package in editable mode fixed the imports. |
| 11 | First GitHub Actions workflow | It listened for pushes to `main` while my branch was `master`, so it silently never ran. I only found out in step 31. |
| 12 | Config module, type hints, docstrings | Settings now live in one place. |

## Phase 3: A real warehouse

| Step | What changed | What went wrong or what I learned |
| --- | --- | --- |
| 13 | GCP project, service account, first BigQuery load | The service account got only the roles it needs, not project owner. |
| 14 | Raw files written as newline-delimited JSON, one loader for all endpoints | BigQuery wants one JSON object per line. Old pretty-printed files left in the folder broke the load until I cleared them. |
| 15 | One `run_pipeline` entrypoint for extract and load | One command and one log stream. |
| 16 | dbt project connected to BigQuery | I interrupted `dbt init` halfway, so no profile was written. I wrote `profiles.yml` by hand. |
| 17 | `stg_status` staging model | BigQuery had turned the nested response into structs. A one-letter typo in a field name was the only error. |
| 18 | `extracted_at` added to every raw payload | Rows from different pulls could not be told apart. Fixing it at the source, not in dbt, also meant handling schema changes in the load. |
| 19 | `mart_current_status` and the dbt docs lineage graph | The first model built for a consumer: one row per region, always the latest. |

## Phase 4: Orchestrate and containerise

| Step | What changed | What went wrong or what I learned |
| --- | --- | --- |
| 20 | First Airflow DAG | dbt and Airflow need conflicting versions of the same libraries. Separate environments were the answer. |
| 21 | Extract and load split into two tasks | A failure now shows which half broke, and the API is not called again to retry a load. |
| 22 | Retries and a failure callback | The callback only fires if a task actually fails, which mattered in step 30. |
| 23 | The pipeline in a Docker image | A placeholder path in my run command mounted a folder where a key file belonged. |
| 24 | Airflow in Docker Compose | Installing the package against a mounted folder failed on file permissions. Building a custom image with the right file ownership fixed it. A leftover local Airflow was also holding port 8080. |
| 25 | dbt inside the Airflow image, in its own environment | `pip` timed out on a weak connection, `git` was missing from the image, and dbt's leftover starter models failed their tests in the container. |
| 26 | `dbt run` and `dbt test` as DAG tasks | The full chain now runs from one schedule. |
| 27 | Raw files archived after a successful load | Every run had been re-loading old files, so raw filled up with duplicates. |

## Phase 5: Scale and polish

| Step | What changed | What went wrong or what I learned |
| --- | --- | --- |
| 28 | Incremental `fct_status_history` model | Its uniqueness test failed on 20 keys. The duplicates came from the loads before step 27, and 106 rows became 30 once the model deduplicated. A dependency conflict between dbt and other libraries in my local environment also surfaced here. |
| 29 | Freshness gate and stricter dbt tests | Tests that check the shape of data say nothing about whether data is still arriving. |
| 30 | Extraction raises on failure, alerts go to Discord | The extract step logged API errors and carried on, so tasks stayed green and the failure alert could never fire. |
| 31 | CI split into lint and tests, dbt parse and Docker build | CI had never run because of the `main` and `master` mismatch from step 11. After renaming the branch, the install commands had collapsed onto one line, and `pip` tried to install a package called `install`. Re-running an old run reuses the old workflow file, so only a new run tests a fix. |
| 32 | A real `dbt build` in CI with keyless login | Workload Identity Federation replaced a stored key. The CI account reads `raw` and writes only to its own dataset. A typo in an API name was the only snag. |
| 33 | This README, the diagram and this log | Written last, for someone who has never seen the project. |

## Decisions along the way

- **A second data source was dropped.** Property24 has no public API, only scrapers, so I kept to documented sources.
- **No second area yet.** The pipeline tracks one area while the foundations are solid.