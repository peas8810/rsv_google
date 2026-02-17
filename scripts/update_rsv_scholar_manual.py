from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

OUT = Path("rsv-scholar.json")

def parse_series(text: str):
    series = []
    for raw in (text or "").splitlines():
        raw = raw.strip()
        if not raw or "=" not in raw:
            continue
        y, v = raw.split("=", 1)
        y = y.strip()
        v = v.strip().replace(",", ".")
        try:
            series.append({"year": str(int(y)), "value": float(v) if "." in v else int(v)})
        except Exception:
            pass
    series.sort(key=lambda x: int(x["year"]))
    return series

def to_int(s: str | None, default=0) -> int:
    s = (s or "").strip()
    if not s:
        return default
    s = s.replace(".", "").replace(",", ".")
    try:
        return int(float(s))
    except Exception:
        return default

def main():
    import os
    payload = {
        "source": os.getenv("SOURCE", "https://scholar.google.com/"),
        "profile_name": os.getenv("PROFILE_NAME", "RSV (Google Scholar)"),
        "updated_at": datetime.now(timezone.utc).date().isoformat(),
        "metrics": {
            "citations_all": to_int(os.getenv("CITATIONS_ALL")),
            "citations_5y": to_int(os.getenv("CITATIONS_5Y"), 0),
            "h_index_all": to_int(os.getenv("H_INDEX_ALL")),
            "h_index_5y": to_int(os.getenv("H_INDEX_5Y"), 0),
            "i10_index_all": to_int(os.getenv("I10_INDEX_ALL")),
            "i10_index_5y": to_int(os.getenv("I10_INDEX_5Y"), 0),
        },
        "citations_by_year": parse_series(os.getenv("CITATIONS_BY_YEAR", "")),
    }
    OUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print("OK: rsv-scholar.json atualizado via workflow manual.")

if __name__ == "__main__":
    main()

