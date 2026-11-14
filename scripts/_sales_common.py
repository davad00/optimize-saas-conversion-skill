"""Shared local-input helpers; not a standalone tool."""

import json
from pathlib import Path


def _constant(value):
    raise ValueError(f"Non-finite JSON number is not allowed: {value}")


def _pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"Duplicate JSON key: {key}")
        result[key] = value
    return result


def loads(text):
    return json.loads(text, parse_constant=_constant, object_pairs_hook=_pairs)


def read_json(path):
    return loads(Path(path).read_text(encoding="utf-8"))


def emit(value):
    print(json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False))


def text(value, label):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} must be a nonempty string")
    return value


def integer(value, label, minimum=0):
    if isinstance(value, bool) or not isinstance(value, int) or value < minimum:
        raise ValueError(f"{label} must be an integer >= {minimum}")
    return value


def safe_path(root, relative):
    text(relative, "path")
    path = (Path(root) / relative).resolve()
    if Path(relative).is_absolute() or not path.is_relative_to(Path(root).resolve()):
        raise ValueError("Catalog path must stay inside the skill directory")
    return path
