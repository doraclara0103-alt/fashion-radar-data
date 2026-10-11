
import json
from pathlib import Path

DATA_FILE = Path("contests.json")
INBOX_FILE = Path("incoming_contests.json")

def read_json(path):
    if not path.exists():
        return []

    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, list):
        raise ValueError(f"{path} must contain a list")

    return data

def valid_contest(item):
    if not isinstance(item, dict):
        return False

    required = ["id", "title", "category", "deadline", "url"]

    return all(
        isinstance(item.get(key), str)
        for key in required
    ) and bool(item["id"].strip()) and bool(item["title"].strip())

def main():
    existing = read_json(DATA_FILE)
    incoming = read_json(INBOX_FILE)

    for item in existing + incoming:
        if not valid_contest(item):
            raise ValueError("Invalid contest data: " + repr(item))

    seen = set()
    merged = []

    for contest in existing + incoming:
        contest_id = contest["id"]

        if contest_id in seen:
            continue

        seen.add(contest_id)
        merged.append(contest)

    new_count = len(merged) - len(existing)

    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump(
            merged,
            file,
            ensure_ascii=False,
            indent=2
        )
        file.write("\n")

    print("Fashion Radar update completed!")
    print("New contests:", new_count)
    print("Total contests:", len(merged))

if __name__ == "__main__":
    main()
