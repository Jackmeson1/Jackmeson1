"""Refresh assets/ledger.json from GitHub: every merged PR by AUTHOR in other people's repositories.

Incremental: PRs already in the ledger keep their area and flags (edit those by hand), and new ones get their size
from the PR's changed lines and an area from RULES. Nothing is removed. Then run build.py to redraw the cards.

    GITHUB_TOKEN=... python assets/update.py

A daily GitHub Actions job (.github/workflows/refresh.yml) runs both and commits only when something changed.
"""
import json
import os
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

AUTHOR = "Jackmeson1"
QUERY = f"author:{AUTHOR} is:pr is:merged -user:{AUTHOR} -repo:The-Last-Math-Competition/The-Last-Math-Competition"
MEDIUM_LINES = 100  # "M" = 100+ changed lines (additions + deletions), "S" = fewer
LEDGER = Path(__file__).with_name("ledger.json")

# (repository, title pattern or None, area). The first match wins; only new PRs are classified.
RULES = [
    (r"sqlfluff/|lballabio/|vllm-project/guidellm|morluto/rea", None, "tooling & libraries"),
    (r"vllm-project/semantic-router", None, "gateway & routing"),
    (r"gpustack/", None, "deployment config"),
    (r"vladmandic/sdnext|huggingface/diffusers|hao-ai-lab/FastVideo|python-pillow/Pillow|Comfy-Org/", None,
     "image & video"),
    (r"vllm-project/aibrix", r"(?i)download|artifact|\b(S3|TOS|GCS)\b|storage|files metadata", "storage & downloads"),
    (r"vllm-project/aibrix", r"(?i)\bbatch", "batch API"),
    (r"vllm-project/aibrix", r"(?i)\b(APA|KPA|HPA)\b|autoscal|scaling|queue totals", "autoscaling"),
    (r"vllm-project/aibrix", r"(?i)\bchart\b|helm|kustomize", "deployment config"),
    (r"vllm-project/aibrix", r"(?i)roleset|raycluster|stormservice|podset|modelclaim('s)? kv|kv (limit|ceiling)",
     "orchestration"),
    (r"vllm-project/aibrix", None, "gateway & routing"),
    (r"xorbitsai/inference", r"(?i)virtualenv|\bpin|diffusers \d", "deployment config"),
    (r"xorbitsai/inference", r"(?i)omni|-vl\b|vision|audio|whisper|image|multimodal|gemma|minicpm|ovis", "multimodal models"),
    (r"xorbitsai/inference", r"(?i)supervisor|shard|worker", "orchestration"),
    (r"xorbitsai/inference", r"(?i)stream|disconnect|metrics|thinking|router", "streaming & requests"),
    (r"xorbitsai/inference", None, "inference engines"),
    (r".*", None, "tooling & libraries"),
]


def api(url):
    headers = {"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28"}
    if os.environ.get("GITHUB_TOKEN"):
        headers["Authorization"] = f"Bearer {os.environ['GITHUB_TOKEN']}"
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=60) as resp:
        return json.load(resp)


def merged_prs():
    items, page = [], 1
    while True:
        query = urllib.parse.urlencode({"q": QUERY, "per_page": 100, "page": page})
        batch = api(f"https://api.github.com/search/issues?{query}")
        items += batch["items"]
        if len(batch["items"]) < 100:
            return items
        page += 1


def classify(repo, title):
    for repo_pattern, title_pattern, area in RULES:
        if re.search(repo_pattern, repo) and (title_pattern is None or re.search(title_pattern, title)):
            return area


def main():
    data = json.loads(LEDGER.read_text(encoding="utf-8")) if LEDGER.exists() else {"prs": []}
    known = {(p["repo"], p["number"]) for p in data["prs"]}
    added = []
    for item in merged_prs():
        repo = item["repository_url"].split("/repos/", 1)[1]
        if (repo, item["number"]) in known:
            continue
        pr = api(f"https://api.github.com/repos/{repo}/pulls/{item['number']}")
        if not pr.get("merged_at"):
            continue
        lines = pr["additions"] + pr["deletions"]
        added.append({
            "repo": repo, "number": item["number"], "merged": pr["merged_at"][:10], "title": item["title"],
            "lines": lines, "size": "M" if lines >= MEDIUM_LINES else "S",
            "area": classify(repo, item["title"]), "regression": False,
        })
    if not added:
        print("ledger unchanged:", len(data["prs"]), "PRs")
        return 0
    data["prs"] = sorted(data["prs"] + added, key=lambda p: (p["merged"], p["repo"], p["number"]))
    with open(LEDGER, "w", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(data, indent=1, ensure_ascii=False) + "\n")
    for p in added:
        print(f"added {p['repo']}#{p['number']} {p['size']} [{p['area']}] {p['title']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
