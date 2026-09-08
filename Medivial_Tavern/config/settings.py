import os

from dotenv import load_dotenv

load_dotenv()


GROQ_API_KEY = os.getenv("GROQ_API_KEY")


MODEL_NAME = "openai/gpt-oss-120b"

TEMPERATURE = 0.7


DAY_DURATION = int(
    os.getenv("DAY_DURATION", 300)
)


SIMULATION_STEP = int(
    os.getenv("SIMULATION_STEP", 5)
)