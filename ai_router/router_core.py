from .key_resolver import resolve_api_key_for_call, key_source_for_call
from .model_resolver import resolve_model
from .provider_client import call_gemini
import json


def extract_text(provider_body: str) -> str:
    try:
        j = json.loads(provider_body)
        return j["candidates"][0]["content"]["parts"][0]["text"]
    except Exception:
        return provider_body


def handle_translate(req: dict) -> dict:
    text = req.get("text", "")
    caller_id = req.get("caller_id", "prod")

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
