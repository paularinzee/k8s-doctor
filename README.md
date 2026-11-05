# K8s Diagnose & Remediate Agent  

An AI agent that diagnoses Kubernetes problems and fixes them, with a human approving every change.

## Structure

```
ai-agent/
  agent-backend/    Python/FastAPI agent
  frontend/  Next.js chat UI
```

## Local development

```sh
cd agent-backend
cp .env.example .env
pip install -r requirements.txt
uvicorn app.main:app          # backend on http://127.0.0.1:8000

cd ../frontend
npm install
npm run dev              # frontend on http://localhost:3000
```

Requires a working `kubectl` context (`~/.kube/config`) pointing at the cluster you want the agent
to diagnose/remediate, and an OpenAI API key (`OPENAI_API_KEY`) in `agent-backend/.env`, along with
the two model IDs (`DIAGNOSTICS_MODEL_ID` and `REMEDIATION_MODEL_ID`, e.g. `gpt-5.4-mini`).
The key is read from the environment or `.env` and is never baked into the Docker image.


## API endpoints

All served by the FastAPI backend (`agent-backend/app/main.py`):

| Method | Path | Purpose |
|---|---|---|
| GET | `/api/health` | Basic health check |
| GET | `/healthz` | Liveness probe (also reports `require_approval`) |
| GET | `/readyz` | Readiness probe - checks Kubernetes API and Bedrock client connectivity |
| GET | `/api/usage` | Token usage/cost tracking |
| POST | `/api/query` | Submit a diagnosis request; starts a new agent session |
| POST | `/api/decision` | Approve or reject a proposed fix |
| POST | `/api/retry` | Retry remediation after a failed verification |
| POST | `/api/select-issues` | Choose which of the diagnosed issues to remediate |
| POST | `/api/guidance` | Give the agent human guidance before its next attempt |
| GET | `/metrics` | Prometheus metrics (mounted sub-app) |

## Key files

| File | Purpose |
|---|---|
| `agent-backend/app/agent/` | LangGraph state machine - the diagnose/propose/apply/verify/retry loop |
| `agent-backend/app/tools/` | Kubernetes API tools the agent calls (read-only diagnostics + write remediation) |
| `agent-backend/app/main.py` | FastAPI backend - `/api/query`, `/api/decision`, `/api/retry`, `/healthz`, `/readyz`, `/metrics` |
| `agent-backend/app/infra/openai_client.py` | AWS Bedrock model client factory |
| `agent-backend/app/infra/checkpointer.py` | LangGraph checkpoint storage - Postgres (connection pool) if `DATABASE_URL` is set, in-memory otherwise |
| `agent-backend/app/infra/usage_tracker.py` | Token usage/cost tracking |
| `agent-backend/Dockerfile` | Backend container image |
| `agent-interface/` | Next.js chat UI (own `Dockerfile`) |
