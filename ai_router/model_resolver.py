import os


def resolve_model() -> str:
    return os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
