"""Low-level CSV parsing helpers (kept separate from validation/DB logic)."""
import csv
import io


REQUIRED_FIELDS = [
    "sport_name",
    "drill_name",
    "skill_level",
    "day_number",
    "sets",
    "reps",
    "video_url",
    "student_email",
]


def parse_csv_bytes(raw: bytes) -> list[dict]:
    text = raw.decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(text))
    return [row for row in reader]
