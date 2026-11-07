
import os
from dotenv import load_dotenv

load_dotenv()

# Gemini configuration (retained as a backup)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
GEMINI_MODEL = "gemini-3.5-flash-lite"

# OpenRouter configuration (OpenAI-compatible API)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()

OPENAI_BASE_URL = os.getenv(
    "OPENAI_BASE_URL",
    "https://openrouter.ai/api/v1"
).strip()

OPENAI_MODEL = os.getenv(
    "OPENAI_MODEL",
    "openrouter/free"
).strip()

# Kivviq customer configuration
KIVVIQ_API_KEY = os.getenv("KIVVIQ_API_KEY", "").strip()

KIVVIQ_BACKEND_URL = os.getenv(
    "KIVVIQ_BACKEND_URL",
    "https://kivviq.ethiodeploy.app"
).strip()


def validate_settings():
    missing = []

    if not OPENAI_API_KEY:
        missing.append("OPENAI_API_KEY")

    if not KIVVIQ_API_KEY:
        missing.append("KIVVIQ_API_KEY")

    if missing:
        raise ValueError(
            "Missing environment variables: " + ", ".join(missing)
        )
