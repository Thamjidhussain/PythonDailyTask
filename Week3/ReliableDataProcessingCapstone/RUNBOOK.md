# Failure and Recovery Runbook

1. API failure: inspect URL, network, timeout and log. Retry is bounded.
2. 4xx: verify endpoint/config; no retry is attempted.
3. Invalid row: inspect `rejected_records` and correct upstream schema/data.
4. No new report after API retrieval failure is intentional; prior report is not overwritten.
5. Write error: check output directory permissions and disk space.
6. Repeat from a clean environment: create venv, install requirements, run pytest, then run `python main.py`.
7. Re-run replaces the output report atomically; it does not append duplicate records.
