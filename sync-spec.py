#!/usr/bin/env python3
"""Keep fred-schema.json in step with fred-schema.yaml.

fred-schema.yaml is the source of truth. Edit it, then run this script to
validate the document and regenerate the JSON copy:

    pip install pyyaml openapi-spec-validator
    python sync-spec.py

Use --check to verify without writing, which is what CI should run:

    python sync-spec.py --check
"""

import argparse
import json
import sys
from pathlib import Path

import yaml
from openapi_spec_validator import validate
from openapi_spec_validator.validation.exceptions import OpenAPIValidationError

HERE = Path(__file__).resolve().parent
YAML_PATH = HERE / "fred-schema.yaml"
JSON_PATH = HERE / "fred-schema.json"


def render(spec):
    """Serialise the spec exactly as fred-schema.json is expected to look."""
    return json.dumps(spec, indent=2, ensure_ascii=False) + "\n"


class SpecError(Exception):
    """A problem worth reporting on one line instead of as a traceback."""


def check_operation_ids(spec):
    """operationIds must be unique; duplicates silently break code generators."""
    seen = {}
    for path, item in spec["paths"].items():
        for operation in item.values():
            op_id = operation.get("operationId")
            if not op_id:
                raise SpecError(f"{path} has no operationId")
            if op_id in seen:
                raise SpecError(
                    f"duplicate operationId {op_id!r}: {seen[op_id]} and {path}"
                )
            seen[op_id] = path
    return len(seen)


def main():
    """Validate the YAML and sync or check the JSON; returns an exit code."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check", action="store_true",
        help="fail if the JSON copy is out of date instead of rewriting it",
    )
    args = parser.parse_args()

    try:
        spec = yaml.safe_load(YAML_PATH.read_text(encoding="utf-8"))
        count = check_operation_ids(spec)
        validate(spec)
    except yaml.YAMLError as exc:
        print(f"{YAML_PATH.name} is not valid YAML: {exc}")
        return 1
    except SpecError as exc:
        print(f"{YAML_PATH.name}: {exc}")
        return 1
    except OpenAPIValidationError as exc:
        location = "/".join(str(part) for part in exc.absolute_path) or "(document root)"
        print(f"{YAML_PATH.name} is not valid OpenAPI at {location}: {exc.message}")
        return 1

    rendered = render(spec)

    current = JSON_PATH.read_text(encoding="utf-8") if JSON_PATH.exists() else None
    if args.check:
        if current != rendered:
            print(f"{JSON_PATH.name} is out of date; run: python {Path(__file__).name}")
            return 1
        print(f"OK: {len(spec['paths'])} paths, {count} operations, JSON in sync")
        return 0

    if current == rendered:
        print(f"OK: {len(spec['paths'])} paths, {count} operations, JSON already in sync")
        return 0

    JSON_PATH.write_text(rendered, encoding="utf-8", newline="\n")
    print(f"wrote {JSON_PATH.name}: {len(spec['paths'])} paths, {count} operations")
    return 0


if __name__ == "__main__":
    sys.exit(main())
