import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
DIAGNOSTICS_MODEL_ID = os.environ["DIAGNOSTICS_MODEL_ID"]  # e.g. gpt-4o
REMEDIATION_MODEL_ID = os.environ["REMEDIATION_MODEL_ID"]  # e.g. gpt-4o

# Optional: Azure/OpenAI-compatible gateways or proxies
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL") or None
OPENAI_TIMEOUT = float(os.getenv("OPENAI_TIMEOUT", "60"))
OPENAI_MAX_RETRIES = int(os.getenv("OPENAI_MAX_RETRIES", "2"))


def _build_model(model_id: str, temperature: float) -> ChatOpenAI:
    return ChatOpenAI(
        model=model_id,
        temperature=temperature,
        api_key=OPENAI_API_KEY,
        base_url=OPENAI_BASE_URL,
        timeout=OPENAI_TIMEOUT,
        max_retries=OPENAI_MAX_RETRIES,
        stream_usage=True,  # keeps usage_metadata populated when streaming (used by usage_tracker)
    )


def get_diagnostics_model() -> ChatOpenAI:
    return _build_model(DIAGNOSTICS_MODEL_ID, temperature=0.0)


def get_remediation_model() -> ChatOpenAI:
    return _build_model(REMEDIATION_MODEL_ID, temperature=0.2)