LOCAL_TRANSLATIONS = {
    ("hello", "ja"): "こんにちは",
    ("hi", "ja"): "こんにちは",
    ("thank you", "ja"): "ありがとう",
    ("thanks", "ja"): "ありがとう",
    ("where is the toilet?", "ja"): "トイレはどこですか？",
    ("how much is this?", "ja"): "これはいくらですか？",
    ("i need a doctor.", "ja"): "医者が必要です。",
    ("please call the police.", "ja"): "警察を呼んでください。",
    ("do you speak english?", "ja"): "英語を話せますか？",
    ("please help me.", "ja"): "助けてください。",
    ("where is the hotel?", "ja"): "ホテルはどこですか？",
}


def local_translate(text: str, target: str):
    clean = (text or "").strip().lower()
    target = (target or "").strip().lower()

    if not clean:
        return None

    if len(clean) <= 1 or clean.isdigit():
        return text

    return LOCAL_TRANSLATIONS.get((clean, target))
