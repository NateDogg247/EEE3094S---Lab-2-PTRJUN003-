"""Run all Lab 2 analysis stages from the project root or any directory."""

from pathlib import Path
import json
from modules.pipeline import run_all

if __name__ == "__main__":
    results = run_all(Path(__file__).resolve().parents[1])
    print(json.dumps(results, indent=2))
