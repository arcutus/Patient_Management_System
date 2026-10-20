# Tutorials
for practice 

## FastAPI patient data

Patient endpoints use PostgreSQL as the source of truth. To import records from
`patients.json` once, run:

```powershell
.\myenv\Scripts\python.exe .\migrate_patients_json.py
```

The importer skips patient IDs that already exist in PostgreSQL, so it can be
run again safely. After importing, start the API with:

```powershell
.\myenv\Scripts\python.exe -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```
