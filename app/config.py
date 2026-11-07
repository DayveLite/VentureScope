import os

import streamlit as st
from dotenv import load_dotenv

load_dotenv()


def get_setting(name: str, default: str = "") -> str:
    """Read Streamlit Cloud secrets or local environment variables."""

    try:
        value = st.secrets.get(name)
        if value is not None:
            return str(value).strip()
    except Exception:
        pass

    return os.getenv(name, default).strip()


# Gemini configuration
GEMINI_API_KEY = get_setting("GEMINI_API_KEY")
GEMINI_MODEL = "gemini-3.5-flash-lite"

# OpenRouter configuration
OPENAI_API_KEY = get_setting("OPENAI_API_KEY")
OPENAI_BASE_URL = get_setting(
    "OPENAI_BASE_URL",
    "https://openrouter.ai/api/v1"
)
OPENAI_MODEL = get_setting("OPENAI_MODEL", "openrouter/free")

# Kivviq configuration
KIVVIQ_API_KEY = get_setting("KIVVIQ_API_KEY")
KIVVIQ_BACKEND_URL = get_setting(
    "KIVVIQ_BACKEND_URL",
    "https://kivviq.ethiodeploy.app"
)

# Tavily configuration
TAVILY_API_KEY = get_setting("TAVILY_API_KEY")


def validate_settings():
    missing = []

    required = {
        "OPENAI_API_KEY": OPENAI_API_KEY,
        "KIVVIQ_API_KEY": KIVVIQ_API_KEY,
        "TAVILY_API_KEY": TAVILY_API_KEY,
    }

    for name, value in required.items():
        if not value:
            missing.append(name)

    if missing:
        raise ValueError(
            "Missing configuration: " + ", ".join(missing)
        )
