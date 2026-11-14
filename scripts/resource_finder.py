#!/usr/bin/env python3
"""Find, inspect, and render the 66 persuasion patterns and 75 templates.

Read-only Python standard library. Exports and templates go only to stdout.
Search is literal word matching, not semantic judgment or a recommendation.
"""

import argparse
from collections import Counter
from pathlib import Path
import re
import sys
sys.dont_write_bytecode = True

from _sales_common import emit, loads, read_json, safe_path

ROOT = Path(__file__).resolve().parents[1]
PATTERN_FIELDS = {"id", "family", "title", "when", "application", "example", "mechanism", "check", "measure", "evidence", "source_ids", "related_tactics"}
TEMPLATE_FIELDS = {"id", "title", "category", "path", "purpose", "inputs", "related_tactics"}
ORIGINAL_TEMPLATES = (
    "assets/conversion-brief.md", "assets/experiment-brief.md",
    "assets/event-contract.json", "assets/review-checklist.md",
    "assets/pricing-audit.md", "assets/tactic-decisions.md",
)


def tokens(value):
    return re.findall(r"[a-z0-9]+", value.casefold())


def load_resources(root=ROOT):
    root = Path(root)
    patterns = []
    for number, line in enumerate((root / "references/persuasion-catalog.jsonl").read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue
        try:
            patterns.append(loads(line))
        except ValueError as exc:
            raise ValueError(f"Persuasion catalog line {number}: {exc}") from exc
    manifest = read_json(root / "references/template-catalog.json")
    if not isinstance(manifest, dict) or type(manifest.get("version")) is not int or manifest["version"] != 1 or not isinstance(manifest.get("templates"), list):
        raise ValueError("Template catalog must contain version: 1 and a templates array")
    return patterns, manifest["templates"]


def validate(root=ROOT):
    root = Path(root)
    patterns, templates = load_resources(root)
    errors = []
    tactic_ids = set()
    for path in (root / "references").glob("tactics-*.jsonl"):
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                tactic_ids.add(loads(line)["id"])
    source_text = (root / "references/persuasion-evidence.md").read_text(encoding="utf-8")
    for kind, records, fields, prefix, count in (
        ("pattern", patterns, PATTERN_FIELDS, "PAT", 66),
        ("template", templates, TEMPLATE_FIELDS, "TMP", 75),
    ):
        seen = {"id": set(), "title": set(), "application" if kind == "pattern" else "path": set()}
        found_ids = set()
        if len(records) != count:
            errors.append(f"Expected {count} {kind}s; found {len(records)}")
        for pos, row in enumerate(records, 1):
            label = f"{kind} {pos}"
            if not isinstance(row, dict):
                errors.append(f"{label}: must be an object")
                continue
            label = row.get("id", label)
            if set(row) != fields:
                errors.append(f"{label}: fields differ from the documented schema")
            arrays = {"source_ids", "related_tactics"} if kind == "pattern" else {"inputs", "related_tactics"}
            valid = True
            for field in fields - arrays:
                if not isinstance(row.get(field), str) or not row[field].strip():
                    errors.append(f"{label}: {field} must be nonempty text")
                    valid = False
            for field in arrays:
                value = row.get(field)
                if not isinstance(value, list) or any(not isinstance(v, str) or not v.strip() for v in value):
                    errors.append(f"{label}: {field} must be an array of nonempty strings")
                    valid = False
                elif len(value) != len(set(value)):
                    errors.append(f"{label}: repeated {field} entry")
            if not valid:
                continue
            found_ids.add(row["id"])
            for field, values in seen.items():
                key = " ".join(tokens(row[field]))
                if key in values:
                    errors.append(f"{label}: duplicate {field}")
                values.add(key)
            if not re.fullmatch(prefix + r"-\d{3}", row["id"]):
                errors.append(f"{label}: invalid ID format")
            for related in row["related_tactics"]:
                if related not in tactic_ids:
                    errors.append(f"{label}: unknown tactic {related}")
            if kind == "pattern":
                for source in row["source_ids"]:
                    if source not in source_text:
                        errors.append(f"{label}: source {source} absent from evidence register")
            else:
                try:
                    path = safe_path(root, row["path"])
                    if not path.is_file():
                        errors.append(f"{label}: template file is missing")
                    if not row["path"].startswith("assets/"):
                        errors.append(f"{label}: templates must be in assets/")
                except ValueError as exc:
                    errors.append(f"{label}: {exc}")
        expected = {f"{prefix}-{i:03d}" for i in range(1, count + 1)}
        if found_ids != expected:
            errors.append(f"{kind} IDs must cover {prefix}-001 through {prefix}-{count:03d}")
    by_id = {r.get("id"): r for r in templates if isinstance(r, dict)}
    for i, path in enumerate(ORIGINAL_TEMPLATES, 1):
        if by_id.get(f"TMP-{i:03d}", {}).get("path") != path:
            errors.append(f"TMP-{i:03d}: original template path changed")
    listed = {r.get("path") for r in templates if isinstance(r, dict)}
    actual = {str(p.relative_to(root)) for p in (root / "assets/templates").glob("*.md")}
    new = {p for p in listed if isinstance(p, str) and p.startswith("assets/templates/")}
    if len(new) != 69 or actual != new:
        errors.append("Expected exactly 69 new template files, each listed once")
    return {"patterns": len(patterns), "templates": len(templates), "new_patterns": len(patterns) - 22,
            "new_templates": len(new), "errors": errors, "valid": not errors,
            "limits": "Structural validation does not establish semantic uniqueness or business effectiveness."}


def combine(patterns, templates):
    return [dict(row, kind="pattern", category=row["family"]) for row in patterns] + [dict(row, kind="template") for row in templates]


def select(records, kind=None, category=None):
    if category and category not in {row["category"] for row in records if not kind or row["kind"] == kind}:
        raise ValueError(f"Unknown category: {category}")
    return [r for r in records if (not kind or r["kind"] == kind) and (not category or r["category"] == category)]


def search(records, query, limit):
    terms = set(tokens(query))
    if not terms:
        raise ValueError("Search query must contain letters or digits")
    ranked = []
    for row in records:
        title = set(tokens(row["title"] + " " + row["id"]))
        body = set(tokens(" ".join(str(value) for value in row.values())))
        score = 4 * len(terms & title) + len(terms & body)
        if score:
            ranked.append((score, row))
    ranked.sort(key=lambda pair: (-pair[0], pair[1]["id"]))
    return [dict(row, search_score=score) for score, row in ranked[:limit]]


def export_markdown(records, kind):
    if kind == "pattern":
        lines = [f"# {len(records)} persuasion patterns", "", "The original 22 mechanisms plus 44 additional applied patterns. Select by the buyer's observed obstacle; these are application hypotheses, not guaranteed effects.", "", "Read the [selection playbook](references/persuasion-patterns.md) and [primary-source register](references/persuasion-evidence.md).", ""]
        for row in records:
            lines.extend([f"## {row['id']} — {row['title']}", "", f"**Family:** {row['category']}", ""])
            for key, label in (("when", "Use when"), ("application", "Apply"), ("example", "Example"), ("mechanism", "Mechanism"), ("check", "Check"), ("measure", "Measure"), ("evidence", "Evidence")):
                lines.extend([f"**{label}:** {row[key]}", ""])
            lines.extend([f"**Sources:** {', '.join(row['source_ids']) or 'Application hypothesis; no direct source assigned.'}", "", f"**Related tactics:** {', '.join(row['related_tactics'])}", ""])
    else:
        lines = [f"# {len(records)} reusable sales and conversion templates", "", "Six existing templates plus 69 additional task-specific templates. Open a linked file, replace placeholders with verified facts, and use the relevant scaffold. Select only the outputs needed for the task.", "", "See the [template selector](references/template-library.md) and [Python tools](references/python-tools.md).", ""]
        for row in records:
            lines.extend([f"## {row['id']} — [{row['title']}]({row['path']})", "", f"**Category:** {row['category']}", "", row["purpose"], "", "**Inputs:** " + "; ".join(row["inputs"]), "", "**Related tactics:** " + ", ".join(row["related_tactics"]), ""])
    return "\n".join(lines)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("list", "search", "categories"):
        command = sub.add_parser(name)
        command.add_argument("--kind", choices=("pattern", "template"))
        if name != "categories":
            command.add_argument("--category")
        if name == "search":
            command.add_argument("query")
            command.add_argument("--limit", type=int, default=8)
    show = sub.add_parser("show")
    show.add_argument("ids", nargs="+")
    render = sub.add_parser("render", help="Print the exact template to stdout without filling or executing it")
    render.add_argument("id")
    sub.add_parser("validate")
    export = sub.add_parser("export")
    export.add_argument("--kind", required=True, choices=("pattern", "template"))
    args = parser.parse_args(argv)
    try:
        if args.command == "validate":
            result = validate()
            emit(result)
            return 0 if result["valid"] else 1
        records = combine(*load_resources())
        if args.command in ("show", "render"):
            wanted = args.ids if args.command == "show" else [args.id]
            by_id = {r["id"]: r for r in records}
            missing = [key for key in wanted if key not in by_id]
            if missing:
                raise ValueError("Unknown resource ID: " + ", ".join(missing))
            if args.command == "show":
                emit([by_id[key] for key in wanted])
            else:
                row = by_id[args.id]
                if row["kind"] != "template":
                    raise ValueError("render requires a TMP template ID")
                print(safe_path(ROOT, row["path"]).read_text(encoding="utf-8"), end="")
        else:
            rows = select(records, args.kind, getattr(args, "category", None))
            if args.command == "export":
                print(export_markdown(rows, args.kind))
            elif args.command == "search":
                if not 1 <= args.limit <= 141:
                    raise ValueError("limit must be between 1 and 141")
                emit({"matches": search(rows, args.query, args.limit), "method": "Literal word overlap; inspect the category list when vocabulary differs."})
            elif args.command == "categories":
                counts = Counter((r["kind"], r["category"]) for r in rows)
                emit([{"kind": key[0], "category": key[1], "count": count} for key, count in sorted(counts.items())])
            else:
                emit([{key: r[key] for key in ("id", "kind", "category", "title")} for r in rows])
        return 0
    except (ValueError, OSError, KeyError, TypeError) as exc:
        parser.exit(2, f"error: {exc}\n")


if __name__ == "__main__":
    sys.exit(main())
