import os

ROLE_ENV = {
    "prod": "NB_GATE_PROD",
    "travel": "NB_GATE_PROD",
    "glb": "NB_GATE_PROD",
    "essentials": "NB_GATE_PROD",
    "show": "NB_GATE_PROD",
    "speak": "NB_GATE_PROD",
    "dev": "NB_GATE_DEV",
    "admin": "NB_GATE_ADMIN",
    "noir": "NB_GATE_NOIR",
}

def resolve_api_key_for_call(caller_id: str = "prod") -> str:
    caller = (caller_id or "prod").strip().lower()
    env_name = ROLE_ENV.get(caller)
    if not env_name:
        raise RuntimeError(f"invalid caller_id: {caller}")

    key = os.environ.get(env_name, "").strip()
    if not key:
        raise RuntimeError(f"missing required env: {env_name}")

    return key

def key_source_for_call(caller_id: str = "prod") -> str:
    caller = (caller_id or "prod").strip().lower()
    env_name = ROLE_ENV.get(caller)
    if not env_name:
        raise RuntimeError(f"invalid caller_id: {caller}")
    return env_name
