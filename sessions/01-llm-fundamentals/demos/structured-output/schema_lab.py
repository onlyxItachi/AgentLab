"""Compare JSON validity, the demo schema and the meaning of a claim offline."""

import argparse
import json
from pathlib import Path

from demo import validate_result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--language", choices=("tr", "en"), default="tr")
    args = parser.parse_args()
    schema = json.loads(
        Path(__file__).with_name("schema.json").read_text(encoding="utf-8")
    )
    false_claim = (
        "Token her zaman bir kelimedir."
        if args.language == "tr"
        else "A token is always a word."
    )
    examples = {
        "A": {"term": "token", "found": True, "explanation": false_claim},
        "B": {"term": "token", "found": "true", "explanation": false_claim},
    }
    for name, example in examples.items():
        encoded = json.dumps(example, ensure_ascii=False)
        parsed = json.loads(encoded)
        try:
            validate_result(parsed, schema)
        except ValueError:
            status = "ŞEMAYA UYGUN DEĞİL" if args.language == "tr" else "SCHEMA FAIL"
        else:
            status = "ŞEMAYA UYGUN" if args.language == "tr" else "SCHEMA PASS"
        print(f"{name}: {encoded}")
        print(f"JSON: OK | {status}")
    print(
        "Not: İki örnekteki açıklama bilerek yanlıştır; şema gerçekleri kontrol etmez."
        if args.language == "tr"
        else "Note: Both explanations are intentionally false; the schema does not check facts."
    )


if __name__ == "__main__":
    import sys

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    main()
