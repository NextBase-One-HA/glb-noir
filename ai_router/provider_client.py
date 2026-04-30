import requests


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

    r = requests.post(url, headers=headers, params=params, json=body, timeout=10)
    return {"status": r.status_code, "body": r.text}
