# sa-power-pipeline

A batch ELT pipeline tracking South African load shedding data — from raw API script to an orchestrated, tested, cloud-warehoused pipeline.

**Status:** 🚧 Iteration 5 — Added Area Information endpoint (hardcoded area)

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
- [ ] Iteration 12: TBD

![CI](https://github.com/Kayfalls/sa-power-pipeline/actions/workflows/ci.yml/badge.svg)

## Setup
1. Copy `.env.example` to `.env` and add your EskomSePush API token
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
