#!/usr/bin/env python3
"""Fill the README's LATEST section from public GitHub data (stdlib only).

Shows: latest public releases across the owner's repos, and merged pull requests
to other people's projects (open-source contributions). Nothing private is read.
Env: GH_TOKEN (workflow token), GH_USER (profile owner).
"""
import json
import os
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

USER = os.environ.get("GH_USER", "Raviteja2k2k")
TOKEN = os.environ.get("GH_TOKEN", "")
README = Path(__file__).resolve().parent.parent / "README.md"
START, END = "<!-- LATEST:START -->", "<!-- LATEST:END -->"


def api(path: str):
    req = urllib.request.Request(f"https://api.github.com{path}",
                                 headers={"Accept": "application/vnd.github+json",
                                          "X-GitHub-Api-Version": "2022-11-28",
                                          **({"Authorization": f"Bearer {TOKEN}"} if TOKEN else {})})
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def releases(limit: int = 5):
    rows = []
    for repo in api(f"/users/{USER}/repos?type=owner&sort=pushed&per_page=50"):
        if repo.get("private") or repo.get("fork"):
            continue
        for rel in api(f"/repos/{repo['full_name']}/releases?per_page=3"):
            if rel.get("draft"):
                continue
            rows.append((rel["published_at"], f"[{repo['name']} {rel['tag_name']}]({rel['html_url']})"))
    return [f"- 🚀 {text} · {when[:10]}" for when, text in sorted(rows, reverse=True)[:limit]]


def contributions(limit: int = 5):
    q = urllib.parse.quote(f"is:pr author:{USER} is:merged -user:{USER}")
    items = api(f"/search/issues?q={q}&sort=updated&order=desc&per_page={limit}").get("items", [])
    out = []
    for it in items:
        repo = it["repository_url"].split("/repos/")[1]
        out.append(f"- 🤝 [{it['title']}]({it['html_url']}) in **{repo}** · {it['closed_at'][:10]}")
    return out


def main():
    try:
        rel, prs = releases(), contributions()
    except Exception as exc:  # network or rate limit: keep the current section untouched
        print(f"skip refresh: {exc}", file=sys.stderr)
        return
    lines = []
    if rel:
        lines += ["**Latest releases**", "", *rel, ""]
    if prs:
        lines += ["**Recent open-source contributions**", "", *prs, ""]
    if not lines:
        lines = ["_First public showcases and open-source contributions land here as they ship (Oct–Nov 2026)._", ""]
    body = "\n".join([START, *lines, "<sub>Updated automatically by GitHub Actions.</sub>", END])
    text = README.read_text(encoding="utf-8")
    new = re.sub(re.escape(START) + r".*?" + re.escape(END), body, text, flags=re.S)
    if new != text:
        README.write_text(new, encoding="utf-8")
        print("README latest section updated")
    else:
        print("no change")


if __name__ == "__main__":
    main()
