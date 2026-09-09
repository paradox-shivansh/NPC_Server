import os
from pathlib import Path

from dotenv import load_dotenv


# NPC_Server/.env
PROJECT_ROOT = Path(__file__).resolve().parents[2]

load_dotenv(PROJECT_ROOT / ".env")


GROQ_API_KEY = os.getenv("GROQ_API_KEY")

MODEL_NAME = os.getenv(
    "MODEL_NAME",
    "openai/gpt-oss-120b"
)

TEMPERATURE = float(
    os.getenv("TEMPERATURE", "0.7")
)

DAY_DURATION = int(
    os.getenv("DAY_DURATION", "300")
)

SIMULATION_STEP = int(
    os.getenv("SIMULATION_STEP", "5")
)


if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY not found in NPC_Server/.env"
    )