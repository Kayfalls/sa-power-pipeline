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
- [x]  Iteration 9: First unit tests (pytest, mocked responses, no live API calls)
- [ ] Iteration 10: TBD

## Setup
1. Copy `.env.example` to `.env` and add your EskomSePush API token
2. `pip install -r requirements.txt`
3. `python fetch_status.py`

## Running tests
1. 'pip install -r requirements-dev.txt'
2. 'pytest -v'

Note to self:
remember to activate the environment: 
        'source .venv/bin/activate'