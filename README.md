# sa-power-pipeline

A batch ELT pipeline tracking South African load shedding data — from raw API script to an orchestrated, tested, cloud-warehoused pipeline.

**Status:** 🚧 Iteration 1 — project scaffolding

## Roadmap
- [x] Iteration 1: Repo setup
- [x] Iteration 2: First API call
- [x] Iteration 3: Timestamped raw dumps, quota tracking
- [x] Iteration 4: Basic error handling (401, 429, unexpected codes)
- [x] Iteration 5: TBD

## Setup
1. Copy `.env.example` to `.env` and add your EskomSePush API token
2. `pip install -r requirements.txt`
3. `python fetch_status.py`