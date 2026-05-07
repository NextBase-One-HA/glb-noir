import requests
from requests.exceptions import Timeout, RequestException


def call_gemini(api_key: str, model: str, text: str) -> dict:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"

    headers = {"Content-Type": "application/json"}
    params = {"key": api_key}

    body = {
        "contents": [
            {
                "parts": [{"text": text}]
            }
        ]
    }

    try:
        r = requests.post(url, headers=headers, params=params, json=body, timeout=10)
        return {"status": r.status_code, "body": r.text}
    except Timeout:
        return {"status": 504, "body": "provider_timeout"}
    except RequestException as e:
        return {"status": 502, "body": str(e)[:200]}
