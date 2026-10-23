# Reliable Data-Processing Utility with API Adapter

## Setup
Python 3.10+ recommended.

```powershell
python -m venv .venv
.venv\\Scripts\\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

## Run and test
```powershell
python main.py
python -m pytest -v
```
The live run uses JSONPlaceholder `/users` and needs internet access. Tests mock HTTP calls and run offline.

## Architecture
`main.py` orchestrates `api_client.py` -> `processor.py` -> `report_generator.py`.
The report contains a UTC timestamp, counts, normalized valid records, and rejected records.

## Recovery behavior
- Timeout/connection/HTTP 5xx: bounded retries, then controlled error and exit code 1.
- HTTP 4xx: no retry; inspect URL/request configuration.
- Invalid individual record or duplicate ID: reject the row and continue.
- Non-list API payload: controlled processing error.
- Report write error: logged and exit code 2.
- Empty list: valid empty report.
- Output uses a temporary file and atomic replacement.
Do not commit `.env`, secrets, generated reports, or sensitive client data.

## CI
GitHub Actions runs pytest on pushes and pull requests. Check the repository Actions tab for actual CI evidence; the local test result is not proof that remote CI passed.

## Git delivery
```powershell
git status
git add .
git diff --cached
git commit -m "Complete reliable data-processing capstone"
git push
```

## Limitations
This is a CLI training project. Its schema expects `id`, `name`, and `email`; the public demo API can be unavailable. HTTP behavior is tested with mocks rather than a live provider.
