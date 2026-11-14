#!/usr/bin/env python3
"""Find concrete SaaS conversion tactics without loading the whole catalog.

Python standard library only. Read-only: no network, telemetry, file writes,
site changes, customer messages, billing changes, or automatic rollout decisions.
Export writes Markdown to stdout; redirect it only to a destination you intend.
"""

import argparse
from collections import Counter
import json
import math
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
CATEGORIES = {
    "intent": ("INT", "Acquisition intent, entry paths, and message match"),
    "positioning": ("POS", "Customer fit, outcomes, differentiation, and alternatives"),
    "copy": ("CPY", "Specific wording, framing, comprehension, and reading effort"),
    "proof": ("PRF", "Customer evidence, social proof, authority, and credibility"),
    "demo": ("DEM", "Product previews, samples, demonstrations, and evaluation"),
    "objections": ("OBJ", "Fit, risk, compatibility, privacy, and adoption concerns"),
    "pricing": ("PRI", "Price framing, actual costs, units, and value calculations"),
    "packaging": ("PKG", "Plan structure, differences, limits, and choice of tier"),
    "offers": ("OFR", "Trials, guarantees, promotions, discounts, and bundles"),
    "decisions": ("DEC", "Decision aids, behavioral mechanisms, and choice architecture"),
    "cta": ("CTA", "Action wording, placement, sequencing, and expectations"),
    "visual": ("VIS", "Color, salience, hierarchy, typography, and visual attention"),
    "signup": ("SIG", "Registration, forms, authentication, and verification"),
    "checkout": ("PAY", "Payment, commitments, errors, and purchase completion"),
    "activation": ("ACT", "Onboarding, first value, setup, and useful progress"),
    "upgrades": ("UPG", "Contextual paywalls, expansion, and upgrade timing"),
    "retention": ("RET", "Continuing value, recovery, cancellation, and winback"),
    "sales": ("SLS", "Sales-assisted evaluation, procurement, and stakeholder approval"),
}
FIELDS = ("id", "category", "title", "trigger", "action", "mechanism", "guardrail", "measure", "scope")
SCOPES = ("presentation", "journey", "commercial", "outreach")
PER_CATEGORY = 20
EXPECTED_TOTAL = PER_CATEGORY * len(CATEGORIES)
STOP_WORDS = set("a an and are as at be before by can do does for from has have if in into is it its may of on or that the their them then these they this to use users visitor visitors when where which with your".split())


def words(value):
    return re.findall(r"[a-z0-9]+", value.casefold())


def normalized(value):
    return " ".join(words(value))


def load_catalog(root=ROOT):
    records = []
    for category in CATEGORIES:
        path = Path(root) / "references" / f"tactics-{category}.jsonl"
        if not path.is_file():
            raise ValueError(f"Missing catalog file: {path}")
        for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            try:
                item = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path.name}:{number}: invalid JSON: {exc.msg}") from exc
            records.append(item)
    return records


def validate_records(records, require_counts=True):
    errors = []
    seen = {field: {} for field in ("id", "title", "action")}
    counts = Counter()
    for index, record in enumerate(records, 1):
        if not isinstance(record, dict):
            errors.append(f"Record {index}: expected a JSON object")
            continue
        label = record.get("id", f"record {index}")
        if set(record) != set(FIELDS):
            errors.append(f"{label}: expected exactly these fields: {', '.join(FIELDS)}")
        for field in FIELDS:
            if not isinstance(record.get(field), str) or not record[field].strip():
                errors.append(f"{label}: {field} must be a nonempty string")
        if any(not isinstance(record.get(field), str) for field in FIELDS):
            continue
        category = record["category"]
        if category not in CATEGORIES:
            errors.append(f"{label}: unknown category {category!r}")
        else:
            counts[category] += 1
            prefix = CATEGORIES[category][0]
            if not re.fullmatch(re.escape(prefix) + r"-\d{3}", record["id"]):
                errors.append(f"{label}: ID must match category prefix {prefix}")
        if record["scope"] not in SCOPES:
            errors.append(f"{label}: unknown action scope {record['scope']!r}")
        for field in seen:
            value = normalized(record[field])
            if value in seen[field]:
                errors.append(f"{label}: duplicate {field} with {seen[field][value]}")
            else:
                seen[field][value] = label
        if len(words(record["action"])) < 8:
            errors.append(f"{label}: action is too short to describe a concrete intervention")
    if require_counts:
        if len(records) != EXPECTED_TOTAL:
            errors.append(f"Expected {EXPECTED_TOTAL} tactics; found {len(records)}")
        ids = {r.get("id") for r in records if isinstance(r, dict) and isinstance(r.get("id"), str)}
        for category, (prefix, _) in CATEGORIES.items():
            if counts[category] != PER_CATEGORY:
                errors.append(f"{category}: expected {PER_CATEGORY}; found {counts[category]}")
            expected = {f"{prefix}-{number:03d}" for number in range(1, PER_CATEGORY + 1)}
            missing = sorted(expected - ids)
            if missing:
                errors.append(f"{category}: missing IDs {', '.join(missing)}")
    return errors


def filter_records(records, categories=None, scopes=None):
    return [record for record in records
            if (not categories or record["category"] in categories)
            and (not scopes or record["scope"] in scopes)]


def find_records(records, query, limit=8):
    terms = set(words(query)) - STOP_WORDS
    if not terms:
        raise ValueError("Search needs at least one meaningful word")
    weighted_fields = (("id", 8), ("title", 5), ("trigger", 3), ("action", 3),
                       ("mechanism", 2), ("guardrail", 1), ("measure", 1))
    scores = []
    for record in records:
        score = sum(weight * len(terms.intersection(words(record[field])))
                    for field, weight in weighted_fields)
        if normalized(query) == normalized(record["id"]):
            score += 100
        if score:
            scores.append((score, record))
    scores.sort(key=lambda pair: (-pair[0], pair[1]["id"]))
    return [record for _, record in scores[:limit]]


def similar_pairs(records, limit=25):
    """Lexical overlap candidates for human review, not semantic proof of duplication."""
    documents = [Counter(token for token in words(r["title"] + " " + r["trigger"] + " " + r["action"])
                         if token not in STOP_WORDS) for r in records]
    frequency = Counter(token for document in documents for token in document)
    vectors = []
    for document in documents:
        vector = {token: (1 + math.log(count)) * math.log(1 + len(documents) / frequency[token])
                  for token, count in document.items()}
        norm = math.sqrt(sum(weight * weight for weight in vector.values())) or 1
        vectors.append({token: weight / norm for token, weight in vector.items()})
    candidates = []
    for first, vector in enumerate(vectors):
        for second in range(first + 1, len(vectors)):
            other = vectors[second]
            score = sum(weight * other.get(token, 0) for token, weight in vector.items())
            if score >= 0.30:
                candidates.append({"first": records[first]["id"], "second": records[second]["id"],
                                   "similarity": round(score, 3),
                                   "titles": [records[first]["title"], records[second]["title"]]})
    return sorted(candidates, key=lambda pair: (-pair["similarity"], pair["first"], pair["second"]))[:limit]


def render_record(record):
    lines = [f"### {record['id']} — {record['title']}", "",
             f"**Use when:** {record['trigger']}", "",
             f"**Change:** {record['action']}", "",
             f"**Why it may help:** {record['mechanism']}", "",
             f"**Check:** {record['guardrail']}", "",
             f"**Measure:** {record['measure']}", "",
             f"**Action scope:** {record['scope']}"]
    return "\n".join(lines)


def markdown_export(records):
    lines = ["# 360 practical SaaS conversion tactics", "",
             "These are concrete implementation hypotheses, selected by an observed buyer obstacle. "
             "They are additional to the skill's existing annual-first and annual monthly-equivalent "
             "baseline checks. They are not 360 guaranteed effects or instructions to apply every tactic.", "",
             "Each entry identifies a trigger, exact change, proposed mechanism, check, measure, and action scope. "
             "A commercial change alters an offer or its economics; an outreach action involves contacting people. "
             "Use the user's actual authorization and verified product facts.", "",
             "See [the selection workflow](references/tactic-library.md), "
             "[behavioral evidence](references/behavioral-evidence.md), and [the main skill](SKILL.md).", "",
             "## Categories", "",
             "| Category | Entries | Focus |", "| --- | ---: | --- |"]
    for category, (_, description) in CATEGORIES.items():
        count = sum(record["category"] == category for record in records)
        lines.append(f"| [{category.title()}](#{category}) | {count} | {description} |")
    for category in CATEGORIES:
        selected = [record for record in records if record["category"] == category]
        if selected:
            lines.extend(["", f"## {category.title()}", ""])
            for record in selected:
                lines.extend([render_record(record), ""])
    return "\n".join(lines).rstrip() + "\n"


def positive_int(value):
    try:
        result = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("must be a positive integer") from exc
    if result < 1:
        raise argparse.ArgumentTypeError("must be a positive integer")
    return result


def parser():
    cli = argparse.ArgumentParser(description=__doc__)
    commands = cli.add_subparsers(dest="command", required=True)
    categories = commands.add_parser("categories", help="List the 18 tactic families")
    categories.add_argument("--json", action="store_true")
    for command, help_text in (("list", "Scan titles and triggers in a family"),
                                ("search", "Retrieve relevant entries by literal words")):
        child = commands.add_parser(command, help=help_text)
        if command == "search":
            child.add_argument("query")
        child.add_argument("--category", action="append", choices=CATEGORIES)
        child.add_argument("--scope", action="append", choices=SCOPES)
        child.add_argument("--limit", type=positive_int, default=40 if command == "list" else 8)
        child.add_argument("--json", action="store_true")
    show = commands.add_parser("show", help="Read complete entries by stable ID")
    show.add_argument("ids", nargs="+")
    show.add_argument("--json", action="store_true")
    validate = commands.add_parser("validate", help="Check count, schema, IDs, and exact duplicates")
    validate.add_argument("--similar", action="store_true", help="Also report lexical overlap candidates for human review")
    validate.add_argument("--limit", type=positive_int, default=25)
    commands.add_parser("export", help="Write the complete human-readable Markdown catalog to stdout")
    return cli


def main():
    cli = parser()
    args = cli.parse_args()
    try:
        records = load_catalog()
        errors = validate_records(records)
        if args.command == "validate":
            result = {"valid": not errors, "count": len(records), "expected": EXPECTED_TOTAL,
                      "categories": dict(Counter(r.get("category", "invalid") for r in records if isinstance(r, dict))),
                      "errors": errors}
            if args.similar and not errors:
                result["overlap_candidates"] = similar_pairs(records, args.limit)
                result["overlap_note"] = "Review the actual interventions; lexical similarity is not a duplicate verdict."
            print(json.dumps(result, indent=2, ensure_ascii=False))
            return 1 if errors else 0
        if errors:
            raise ValueError("Catalog validation failed: " + "; ".join(errors[:5]))
        if args.command == "export":
            print(markdown_export(records), end="")
            return 0
        if args.command == "categories":
            rows = [{"category": name, "prefix": prefix, "count": PER_CATEGORY, "focus": description,
                     "file": f"references/tactics-{name}.jsonl"}
                    for name, (prefix, description) in CATEGORIES.items()]
            if args.json:
                print(json.dumps(rows, indent=2))
            else:
                for row in rows:
                    print(f"{row['category']:12} {row['prefix']}  {row['count']:2}  {row['focus']}")
            return 0
        if args.command == "show":
            by_id = {record["id"]: record for record in records}
            missing = [identifier for identifier in args.ids if identifier not in by_id]
            if missing:
                raise ValueError("Unknown tactic IDs: " + ", ".join(missing))
            selected = [by_id[identifier] for identifier in args.ids]
        else:
            pool = filter_records(records, args.category, args.scope)
            selected = (find_records(pool, args.query, args.limit) if args.command == "search"
                        else pool[:args.limit])
        if args.json:
            print(json.dumps(selected, indent=2, ensure_ascii=False))
        elif args.command == "list":
            for record in selected:
                print(f"{record['id']} [{record['scope']}] {record['title']}\n  When: {record['trigger']}\n")
            print(f"Showing {len(selected)} of {len(pool)} matching entries.")
        elif selected:
            print("\n\n".join(render_record(record) for record in selected))
        else:
            print("No matching tactics. Try the family list or simpler words; this is lexical search.")
        return 0
    except (OSError, ValueError) as exc:
        cli.error(str(exc))


if __name__ == "__main__":
    sys.exit(main())
