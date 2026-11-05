"""
config.py - all settings for the project, in one place.

Why it exists: other files import their settings from here, so no setting
is typed in two places. Secrets come from the .env file, never from Git.
"""
import os
from pathlib import Path

from dotenv import load_dotenv

# Read the .env file and put its lines into the environment.
# LangSmith also reads its own settings from there automatically.
load_dotenv()

# ---------- Secrets (from .env) ----------
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
DATABASE_URL = os.getenv("DATABASE_URL", "")
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY", "")
# ---------- Models ----------
# Check the current free model names in Google AI Studio and change them here.
LLM_MODEL = os.getenv("LLM_MODEL", "gemini-3.6-flash")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "gemini-embedding-001")
EMBEDDING_DIMENSIONS = 768  # must match the vector size in the database

# ---------- Search ----------
RETRIEVAL_MODE = "vector"  # "vector", "hybrid", or "hybrid_rerank"
CANDIDATES = 10            # chunks returned by the first search
TOP_K = 3                  # chunks the agent finally receives

# ---------- Agent limits ----------
MAX_AGENT_STEPS = 6        # after this many tool calls the agent escalates
MAX_TICKET_LENGTH = 1000   # longer tickets are rejected

# ---------- Folders ----------
ROOT_DIR = Path(__file__).resolve().parent.parent
POLICY_DIR = ROOT_DIR / "data" / "policies"
CACHE_DIR = ROOT_DIR / ".cache"
RESULTS_DIR = ROOT_DIR / "evals" / "results"


def check_required_settings():
    """Stop early with a clear message if a secret is missing."""
    missing = []
    if not GOOGLE_API_KEY:
        missing.append("GOOGLE_API_KEY")
    if not DATABASE_URL:
        missing.append("DATABASE_URL")
    if missing:
        raise RuntimeError("Missing in .env: " + ", ".join(missing))