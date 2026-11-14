#!/usr/bin/env python3
"""Flag form and action obstacles in a supplied HTML snapshot.

Static, local, standard-library heuristics. Does not render CSS, run JavaScript,
compute the full accessibility tree, crawl links or verify purchase completion.
"""

import argparse
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
import sys
sys.dont_write_bytecode = True

from _sales_common import emit

VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}
NONCONTENT = {"script", "style", "template", "noscript"}


class Snapshot(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.nodes = []
        self.stack = []

    def handle_starttag(self, tag, attrs):
        node = {"tag": tag, "attrs": dict(attrs), "line": self.getpos()[0],
                "parent": self.stack[-1] if self.stack else None, "parts": []}
        index = len(self.nodes)
        self.nodes.append(node)
        if self.stack:
            self.nodes[self.stack[-1]]["parts"].append(index)
        if tag not in VOID:
            self.stack.append(index)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag):
        for position in range(len(self.stack) - 1, -1, -1):
            if self.nodes[self.stack[position]]["tag"] == tag:
                self.stack = self.stack[:position]
                break

    def handle_data(self, data):
        if self.stack:
            self.nodes[self.stack[-1]]["parts"].append(data)

    def ancestors(self, index):
        while self.nodes[index]["parent"] is not None:
            index = self.nodes[index]["parent"]
            yield index

    def content(self, index, include_hidden=False):
        node = self.nodes[index]
        if node["tag"] in NONCONTENT:
            return ""
        attrs = node["attrs"]
        if not include_hidden and ("hidden" in attrs or "inert" in attrs or attrs.get("aria-hidden") == "true"):
            return ""
        if node["tag"] == "img":
            return node["attrs"].get("alt") or ""
        parts = [self.content(part, include_hidden=include_hidden) if isinstance(part, int) else part for part in node["parts"]]
        return " ".join(" ".join(parts).split())


def lint(source, required_field_review=5):
    if not isinstance(source, str) or not source.strip():
        raise ValueError("HTML snapshot is empty")
    if required_field_review < 1:
        raise ValueError("required-field-review must be at least 1")
    doc = Snapshot()
    doc.feed(source)
    nodes = doc.nodes
    if not nodes:
        raise ValueError("No HTML elements found; provide rendered HTML, not a URL or component source")
    ids = {}
    issues = []
    renderable = [i for i in range(len(nodes)) if not any(nodes[j]["tag"] in NONCONTENT for j in [i] + list(doc.ancestors(i)))]
    def add(index, level, code, message):
        node = nodes[index] if index is not None else {"line": 1, "tag": "document"}
        issues.append({"line": node["line"], "tag": node["tag"], "level": level, "code": code, "message": message})
    for i in renderable:
        node = nodes[i]
        identifier = node["attrs"].get("id")
        if identifier:
            if identifier in ids:
                add(i, "review", "duplicate_id", "Repeated HTML id can make label and control associations ambiguous")
            else:
                ids[identifier] = i
    labels = {}
    for i in renderable:
        node = nodes[i]
        if node["tag"] == "label" and node["attrs"].get("for"):
            labels.setdefault(node["attrs"]["for"], []).append(i)

    def excluded(i):
        for j in [i] + list(doc.ancestors(i)):
            attrs = nodes[j]["attrs"]
            if nodes[j]["tag"] in NONCONTENT or "hidden" in attrs or "inert" in attrs:
                return True
        return False

    def name(i, visited=None):
        visited = set() if visited is None else set(visited)
        if i in visited:
            return ""
        visited.add(i)
        node = nodes[i]
        attrs = node["attrs"]
        labelledby = (attrs.get("aria-labelledby") or "").split()
        if labelledby:
            content = " ".join(doc.content(ids[key], include_hidden=True) for key in labelledby if key in ids)
            if content.strip():
                return content.strip()
        if (attrs.get("aria-label") or "").strip():
            return attrs["aria-label"].strip()
        if node["tag"] in ("input", "select", "textarea"):
            associated = list(labels.get(attrs.get("id"), []))
            associated += [j for j in doc.ancestors(i) if nodes[j]["tag"] == "label"]
            result = " ".join(doc.content(j) for j in associated).strip()
            if result:
                return result
            if node["tag"] == "input":
                kind = (attrs.get("type") or "text").lower()
                if kind == "image":
                    return (attrs.get("alt") or "").strip()
                if kind in ("submit", "reset"):
                    return (attrs.get("value") or ("Submit" if kind == "submit" else "Reset")).strip()
                if kind == "button":
                    return (attrs.get("value") or "").strip()
        if node["tag"] in ("button", "a") or attrs.get("role") in ("button", "link"):
            content = doc.content(i)
            if content:
                return content
        return (attrs.get("title") or "").strip()

    controls = []
    actions = []
    required_by_form = {}
    for i, node in enumerate(nodes):
        if excluded(i):
            continue
        tag, attrs = node["tag"], node["attrs"]
        kind = (attrs.get("type") or "text").lower()
        if tag == "input" and kind == "hidden":
            continue
        if tag in ("input", "select", "textarea"):
            controls.append(i)
            if not name(i):
                add(i, "review", "control_name_unresolved", "No usable native/ARIA/title name found by the static checker; inspect the rendered accessible name and visible label")
            if "placeholder" in attrs and not name(i):
                add(i, "review", "placeholder_only", "A placeholder disappears during entry; supply a persistent visible label")
            if kind in ("email", "password") and not attrs.get("autocomplete"):
                add(i, "review", "autocomplete_missing", "Consider the correct autocomplete token for this email or password task")
            form = ids.get(attrs.get("form")) if attrs.get("form") else next((j for j in doc.ancestors(i) if nodes[j]["tag"] == "form"), None)
            if form is not None and nodes[form]["tag"] != "form":
                form = None
            if form is not None and "required" in attrs and "disabled" not in attrs:
                key = (kind, attrs.get("name")) if kind == "radio" and attrs.get("name") else ("control", i)
                required_by_form.setdefault(form, set()).add(key)
            if form is not None and kind == "password" and (nodes[form]["attrs"].get("method") or "get").lower() == "get":
                add(i, "review", "password_get_form", "Native form submission would put fields in a GET request; verify secure submission behavior and prevent password exposure")
        action = tag == "button" or (tag == "a" and "href" in attrs) or attrs.get("role") in ("button", "link") or (tag == "input" and kind in ("button", "submit", "reset", "image"))
        if action:
            actions.append(i)
            if not name(i):
                add(i, "review", "action_name_unresolved", "Action has no name resolved by this static checker; inspect its accessible and visible labels")
        if tag == "button" and "type" not in attrs:
            form = ids.get(attrs.get("form")) if attrs.get("form") else next((j for j in doc.ancestors(i) if nodes[j]["tag"] == "form"), None)
            if form is not None:
                add(i, "review", "implicit_submit", "This form button defaults to submit; set an explicit type and verify auxiliary actions do not submit")
        if tag == "a" and "href" in attrs:
            href = (attrs.get("href") or "").strip()
            if href in ("", "#") or href.lower().startswith("javascript:"):
                add(i, "review", "placeholder_destination", "Link has no meaningful native destination; verify the intended action and fallback")
        refs = (attrs.get("aria-labelledby") or "").split()
        if refs and any(key not in ids for key in refs):
            add(i, "review", "missing_label_reference", "aria-labelledby references an id absent from this snapshot")
    for form, required in required_by_form.items():
        if len(required) >= required_field_review:
            add(form, "review", "required_field_burden", f"Form has {len(required)} required field groups; justify each before first value (threshold is a configurable review cue)")
    if not any(nodes[i]["tag"] == "meta" and (nodes[i]["attrs"].get("name") or "").lower() == "viewport" for i in renderable):
        add(None, "review", "viewport_unobserved", "No viewport declaration in this snapshot; verify narrow-screen rendering in the complete document")
    return {"elements": len(nodes), "controls_checked": len(controls), "actions_checked": len(actions),
            "finding_count": len(issues), "counts_by_code": dict(Counter(item["code"] for item in issues)), "findings": issues,
            "limits": ["All findings are review cues. This is not WCAG conformance or a conversion score.",
                       "Does not compute CSS visibility, browser error recovery, shadow DOM, complete accessible names, custom widgets or JavaScript behavior.",
                       "Supply a complete rendered HTML snapshot where possible. A fragment can omit labels, metadata and form owners.",
                       "Verify keyboard use, labels, mobile rendering, pricing states, validation, payment and fulfillment in a real browser."]}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--html", required=True, help="Local UTF-8 HTML snapshot; no URL fetching")
    parser.add_argument("--required-field-review", type=int, default=5)
    args = parser.parse_args(argv)
    try:
        emit(lint(Path(args.html).read_text(encoding="utf-8"), args.required_field_review))
        return 0
    except (ValueError, OSError, TypeError) as exc:
        parser.exit(2, f"error: {exc}\n")


if __name__ == "__main__":
    sys.exit(main())
