import json


def save_json(data, filepath="data/result.json"):
    with open(filepath, "w") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
