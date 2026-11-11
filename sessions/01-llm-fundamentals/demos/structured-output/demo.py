"""Call a deterministic local tool and check its output against a simple schema."""

import argparse
import json
import sys
from pathlib import Path

CONCEPTS = {
    "token": {
        "tr": "Modelin işlediği metin parçasıdır; her zaman bir kelime değildir.",
        "en": "A piece of text processed by a model; it is not always a word.",
    },
    "tool": {
        "tr": "Bir sistemin modele kontrollü biçimde kullanıma açtığı işlevdir.",
        "en": "A function a host system makes available to a model in a controlled way.",
    },
    "schema": {
        "tr": "Bir çıktının beklenen yapısını ve kurallarını tarif eder.",
        "en": "A description of the expected structure and constraints of an output.",
    },
}


def lookup_concept(term: str, language: str) -> dict:
    """A local stand-in for an externally exposed tool; no model is involved."""
    name = term.strip().lower()
    entry = CONCEPTS.get(name)
    missing = {"tr": "Kavram bulunamadı.", "en": "Concept not found."}
    return {
        "term": name,
        "found": entry is not None,
        "explanation": entry[language] if entry else missing[language],
    }


def validate_result(result: object, schema: dict) -> None:
    """Check the small JSON Schema subset used here, not arbitrary schemas."""
    if not isinstance(result, dict):
        raise ValueError("Result must be an object")
    required = set(schema["required"])
    if not required.issubset(result):
        raise ValueError("A required field is missing")
    if schema.get("additionalProperties") is False and set(result) - set(schema["properties"]):
        raise ValueError("Unexpected field")
    types = {"string": str, "boolean": bool}
    for name, value in result.items():
        if name in schema["properties"]:
            expected = types[schema["properties"][name]["type"]]
            if type(value) is not expected:
                raise ValueError(f"Invalid type for {name}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--term", default="token")
    parser.add_argument("--language", choices=("tr", "en"), default="tr")
    args = parser.parse_args()
    schema = json.loads((Path(__file__).parent / "schema.json").read_text(encoding="utf-8"))
    result = lookup_concept(args.term, args.language)
    validate_result(result, schema)
    sys.stdout.reconfigure(encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
