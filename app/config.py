import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")
ENBEDDING_MODEL = "text-embedding-3-small"
ENBEDDING_DIMENSIONS = 1536