from .key_resolver import resolve_api_key_for_call, key_source_for_call
from .model_resolver import resolve_model
from .provider_client import call_gemini
from .cost_optimizer import local_translate
import json


def extract_text(provider_body: str) -> str:
    try:
        j = json.loads(provider_body)
        return j["candidates"][0]["content"]["parts"][0]["text"]
    except Exception:
        return provider_body


def handle_translate(req: dict) -> dict:
    text = req.get("text", "")
    target = req.get("target", "")
    caller_id = req.get("caller_id", "prod")
    profile = req.get("translation_profile", "") or req.get("profile", "")

    # --- Cost Optimizer (API bypass) ---
    cached = local_translate(text, target)
    if cached:
        return {
            "ok": True,
            "model": "local-cache",
            "key_source": "LOCAL_CACHE",
            "provider_status": 200,
            "translatedText": cached,
            "optimizer": "local_cache",
        }

    # --- MT-only profile: NEVER call Gemini / LLM ---
    if profile == "core_mt_no_ai":
        return {
            "ok": False,
            "model": "mt-only",
            "key_source": "MT_ONLY",
            "provider_status": 503,
            "translatedText": "",
        }

    api_key = resolve_api_key_for_call(caller_id)
    model = resolve_model()

    result = call_gemini(api_key, model, text)

    translated = extract_text(result["body"])

    return {
        "ok": result["status"] == 200,
        "model": model,
        "key_source": key_source_for_call(caller_id),
        "provider_status": result["status"],
        "translatedText": translated,
    }
