"""Run the two review stages against OpenRouter with the app's normal provider settings."""

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import json
from pathlib import Path
import subprocess
import sys

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from radar import ReviewError, confirmed_requirements, evaluate, extract


def review(case):
    """Save only synthetic fixtures' results and the app's safe provider metadata."""
    result = {"id": case["id"]}
    stage = "extraction"
    try:
        originals, result["extraction"] = extract(case["instructions"], case["draft"])
        result["requirements"] = originals
        stage = "confirmation"
        confirmed = confirmed_requirements("\n".join(item["text"] for item in originals), originals)
        result["confirmed"] = confirmed
        stage = "review"
        result["report"], result["review"] = evaluate(case["instructions"], case["draft"], confirmed)
    except ReviewError as exc:
        result["error"] = {"stage": stage, "message": str(exc), "diagnostics": exc.diagnostics}
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path, help="New JSON evidence file")
    args = parser.parse_args()
    load_dotenv(ROOT / ".env")
    fixture_bytes = Path(__file__).with_name("cases.json").read_bytes()
    cases = json.loads(fixture_bytes)
    evidence = {
        "head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "radar_sha256": hashlib.sha256((ROOT / "radar.py").read_bytes()).hexdigest(),
        "cases_sha256": hashlib.sha256(fixture_bytes).hexdigest(),
        "results": [],
    }
    with args.output.open("x", encoding="utf-8") as output, ThreadPoolExecutor(max_workers=2) as pool:
        futures = [pool.submit(review, case) for case in cases]
        for future in as_completed(futures):
            result = future.result()
            evidence["results"].append(result)
            print(result["id"], result.get("error", {}).get("message", "complete"), flush=True)
        evidence["results"].sort(key=lambda result: result["id"])
        json.dump(evidence, output, indent=2, ensure_ascii=False)
        output.write("\n")


if __name__ == "__main__":
    main()
