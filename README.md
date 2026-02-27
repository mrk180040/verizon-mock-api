# Verizon Backend API + Assistant JSON Samples

This repository contains only:

- Flask backend API in `mock_api.py`
- JSON samples used for Watsonx Assistant action design

## Run backend API

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python mock_api.py
```

Optional custom port:

```bash
MOCK_API_PORT=8080 python mock_api.py
```

## API endpoints

- `GET /api/health`
- `POST /api/auth`
- `GET /api/billing/<account_id>`
- `GET /api/plan/current`
- `GET /api/plan/eligible`
- `POST /api/network/diagnostics`

## JSON samples

The repository includes assistant/action JSON samples (for example `assistant.json`, `assistant.local.json`, `assistant.generated.cloud.json`, `verizon_assistant.json`, `action-skill.json`, `verizon-api.json`).

Use them as reference payloads/templates when creating actions in Watsonx Assistant.
