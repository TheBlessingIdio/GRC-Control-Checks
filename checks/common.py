import json
from datetime import datetime, timezone
from pathlib import Path


def build_result(check_id, passed, resources_checked, failing, raw):
    return {
        "check_id": check_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "result": "PASS" if passed else "FAIL",
        "resources_checked": resources_checked,
        "failing_resources": failing,
        "raw_evidence": raw,
    }


def write_evidence(result, folder="evidence"):
    day = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    out_dir = Path(folder) / day
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"{result['check_id']}.json"
    out_file.write_text(json.dumps(result, indent=2, default=str))
    return out_file