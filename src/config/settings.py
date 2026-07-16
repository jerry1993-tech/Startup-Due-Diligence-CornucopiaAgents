
"""Configuration settings for the due diligence workflow."""

import os
from dotenv import load_dotenv


# Load .env 
load_dotenv(override=True)


# ​​Load configuration​​
AUTH_TOKEN = os.getenv("ANTHROPIC_AUTH_TOKEN")
BASE_URL = os.getenv("ANTHROPIC_BASE_URL", "https://api.anthropic.com")


# Model name mappings - short names to full IDs
MODEL_MAPPING = {
    "haiku": "deepseek-v4-flash",
    "sonnet": "deepseek-v4-flash",
    "opus": "deepseek-v4-pro",
    "deepseek-v4-flash": "deepseek-v4-flash",
    "deepseek-v4-pro": "deepseek-v4-pro",
}


def get_model_id(model_name: str) -> str:
    """Get the full model ID from a short name.
    
    Args:
        model_name: Short name like 'haiku', 'sonnet', 'opus' or full ID
    
    Returns:
        Full model ID string
    """
    return MODEL_MAPPING.get(model_name, model_name)