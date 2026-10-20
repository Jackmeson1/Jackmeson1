"""Builds the profile SVGs (light and dark) and README.md from assets/ledger.json: python assets/build.py

The ledger is refreshed by assets/update.py (daily in GitHub Actions). Edit an entry's "area" or "regression" in
ledger.json by hand to reclassify it; update.py never overwrites existing entries.

The SVGs animate with CSS only (no script), and their resting state is the final frame, so static renderers and
prefers-reduced-motion both show the finished picture.
"""
import json
from collections import Counter
from datetime import date
from html import escape
from pathlib import Path
from urllib.parse import quote_plus

HERE = Path(__file__).parent
PRS = json.loads((HERE / "ledger.json").read_text(encoding="utf-8"))["prs"]  # merged PRs in other people's repositories
NAMES = {  # display names; any other repository shows as its name
    "vllm-project/aibrix": "AIBrix", "xorbitsai/inference": "Xinference", "gpustack/gpustack": "GPUStack",
    "vllm-project/semantic-router": "Semantic Router", "vllm-project/guidellm": "guidellm",
    "sqlfluff/sqlfluff": "SQLFluff", "morluto/rea": "REA", "lballabio/QuantLib": "QuantLib",
    "vladmandic/sdnext": "SD.Next", "huggingface/diffusers": "diffusers", "python-pillow/Pillow": "Pillow",
}
REPO_COUNTS = Counter(p["repo"] for p in PRS)


def name(repo):
    return NAMES.get(repo, repo.split("/")[1])


FACTS = {
    "merged": len(PRS),
    "projects": len(REPO_COUNTS),
    "aibrix": REPO_COUNTS["vllm-project/aibrix"],
    "xinference": REPO_COUNTS["xorbitsai/inference"],
    "as_of": date.fromisoformat(max(p["merged"] for p in PRS)).strftime("%b %Y"),  # month of the latest merge
}

PALETTES = {
    "light": dict(paper="#f4efe6", ink="#1d1b18", muted="#7a7266", rule="#dcd3c4", seal="#c2412d", grain=0.06),
    "dark": dict(paper="#15130f", ink="#ece5d8", muted="#8f8778", rule="#302b24", seal="#e4573f", grain=0.09),
}

SERIF = "'Iowan Old Style','Palatino Linotype',Palatino,Georgia,'Times New Roman',serif"
MONO = "ui-monospace,'SF Mono',SFMono-Regular,Menlo,Consolas,'Liberation Mono',monospace"

GRAIN = """
  <filter id="grain" x="0" y="0" width="100%" height="100%">
    <feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" stitchTiles="stitch"/>
    <feColorMatrix values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 {g} 0"/>
    <feComposite in2="SourceGraphic" operator="in"/>
  </filter>"""

REDUCE = "@media (prefers-reduced-motion: reduce) { * { animation: none !important; } }"


def frame(p, w, h):
    return (f'<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="16" fill="{p["paper"]}" stroke="{p["rule"]}"/>'
            f'<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="16" fill="{p["paper"]}" filter="url(#grain)"/>')


def card(p):
    """Identity and attitude."""
    lines = [
        "Agentic coding is here.",
        "Open source iterates faster than ever.",
        "I'm in — finding, fixing, getting it merged.",
    ]
    rows = []
    for i, line in enumerate(lines):
        y = 200 + i * 34
        rows.append(
            f'<g class="type" style="animation-delay:{0.9 + i * 0.8:.2f}s">'
            f'<text x="44" y="{y}" class="num">0{i + 1}</text>'
            f'<text x="80" y="{y}" class="line{" me" if i == len(lines) - 1 else ""}">{escape(line)}</text></g>'
        )
    end = 0.9 + (len(lines) - 1) * 0.8 + 0.6
    w, h = 880, 300
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img"
  aria-labelledby="t d">
  <title id="t">Jack</title>
  <desc id="d">SDET working on agentic workflows and open source. Agentic coding is here. Open source iterates faster than ever.
    I'm in: finding, fixing, getting it merged.</desc>
  <defs>{GRAIN.format(g=p['grain'])}
    <filter id="ink" x="-10%" y="-10%" width="120%" height="120%">
      <feTurbulence type="fractalNoise" baseFrequency=".75" numOctaves="2" seed="7"/>
      <feDisplacementMap in="SourceGraphic" scale="1.3"/>
    </filter>
  </defs>
  <style>
    .name {{ font: 400 54px {SERIF}; fill: {p['ink']}; letter-spacing: -.5px; }}
    .dot {{ fill: {p['seal']}; }}
    .role {{ font: 500 12px {MONO}; fill: {p['muted']}; letter-spacing: 2.6px; }}
    .num {{ font: 600 12px {MONO}; fill: {p['seal']}; letter-spacing: 1px; }}
    .line {{ font: 400 20px {SERIF}; fill: {p['muted']}; }}
    .line.me {{ fill: {p['ink']}; }}
    .rule {{ stroke: {p['rule']}; stroke-width: 1; stroke-dasharray: 792; animation: draw 1.1s cubic-bezier(.6,0,.2,1) .2s both; }}
    .fade {{ animation: fade .9s ease-out .1s both; }}
    .type {{ animation: type .7s steps(30, end) both; }}
    .seal {{ transform-box: fill-box; transform-origin: center; animation: stamp .42s cubic-bezier(.3,1.6,.5,1) {end + .3:.2f}s both; }}
    .seal text {{ fill: {p['seal']}; }}
    .seal .big {{ font: 700 17px {SERIF}; letter-spacing: 1.5px; }}
    .seal .small {{ font: 700 7.6px {MONO}; letter-spacing: .6px; }}
    @keyframes draw {{ from {{ stroke-dashoffset: 792; }} to {{ stroke-dashoffset: 0; }} }}
    @keyframes fade {{ from {{ opacity: 0; transform: translateY(6px); }} to {{ opacity: 1; transform: none; }} }}
    @keyframes type {{ from {{ clip-path: inset(0 100% 0 0); }} to {{ clip-path: inset(0 0 0 0); }} }}
    @keyframes stamp {{ 0% {{ opacity: 0; transform: rotate(-8deg) scale(1.7); }} 70% {{ opacity: .95; }}
      100% {{ opacity: .92; transform: rotate(-8deg) scale(1); }} }}
    {REDUCE}
  </style>
  {frame(p, w, h)}
  <g class="fade">
    <text x="40" y="94" class="name">Jack<tspan class="dot">.</tspan></text>
    <text x="44" y="128" class="role">SDET  ·  AGENTIC WORKFLOWS  ·  OPEN SOURCE</text>
  </g>
  <line x1="44" y1="152" x2="836" y2="152" class="rule"/>
  {''.join(rows)}
  <g class="seal" style="opacity:.92" transform="rotate(-8 788 92)" filter="url(#ink)">
    <rect x="740" y="44" width="96" height="96" rx="6" fill="none" stroke="{p['seal']}" stroke-width="3"/>
    <rect x="747" y="51" width="82" height="82" rx="3" fill="none" stroke="{p['seal']}" stroke-width="1"/>
    <text x="788" y="98" text-anchor="middle" class="big">MERGED</text>
    <text x="788" y="117" text-anchor="middle" class="small">UPSTREAM · {FACTS['as_of'].split()[-1]}</text>
  </g>
</svg>
"""


def roller(x, y, value, cls, delay):
    """An odometer: each digit is a 0-9 column clipped to one cell, rolling up to its value."""
    cell, width = 64, 34
    out = []
    for i, ch in enumerate(str(value)):
        n = int(ch)
        cx = x + i * width
        digits = "".join(f'<text x="{cx}" y="{y + k * cell}" class="{cls}">{k}</text>' for k in range(10))
        out.append(
            f'<clipPath id="cell{i}_{x}"><rect x="{cx - 2}" y="{y - 52}" width="{width}" height="{cell}"/></clipPath>'
            f'<g clip-path="url(#cell{i}_{x})"><g class="roll" '
            f'style="--y:{-n * cell}px;animation-delay:{delay + i * .12:.2f}s">{digits}</g></g>'
        )
    return "".join(out)


def workflow(p):
    """How the work is done (agents do the legwork, I own the call), ending in the result."""
    steps = [
        ("AGENTS", "sweep", "releases, upstream"),
        ("AGENTS", "reproduce", "failing test first"),
        ("SECOND MODEL", "review", "independent check"),
        ("ME", "decide", "impact, not count"),
        ("ME", "ship", "small PR, follow-up"),
    ]
    x0, gap, ly = 62, 122, 118
    x_end = x0 + gap * (len(steps) - 1)
    nodes = []
    for i, (who, step, note) in enumerate(steps):
        x = x0 + i * gap
        d = 0.5 + i * 0.28
        human = who == "ME"
        nodes.append(
            f'<g class="pop" style="animation-delay:{d:.2f}s">'
            f'<text x="{x}" y="{ly - 22}" class="who{" me" if human else ""}" text-anchor="middle">{who}</text>'
            f'<circle cx="{x}" cy="{ly}" r="6" class="{"node me" if human else "node"}"/>'
            f'<text x="{x}" y="{ly + 30}" class="step" text-anchor="middle">{step}</text>'
            f'<text x="{x}" y="{ly + 48}" class="snote" text-anchor="middle">{note}</text></g>'
        )
    run = x_end - x0
    w, h = 880, 200
    rx = 652
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img"
  aria-labelledby="t d">
  <title id="t">How I work</title>
  <desc id="d">Agents sweep releases and upstream changes and reproduce bugs with a failing test; a second model
    reviews independently; I decide by impact and ship small PRs with follow-up. Result: {FACTS['merged']} merged
    upstream pull requests, {FACTS['aibrix']} of them in vLLM AIBrix and {FACTS['xinference']} in Xinference, iterating with maintainers
    ({FACTS['as_of']}).</desc>
  <defs>{GRAIN.format(g=p['grain'])}</defs>
  <style>
    .kicker {{ font: 500 12px {MONO}; fill: {p['muted']}; letter-spacing: 2.6px; }}
    .motto {{ font: italic 400 16px {SERIF}; fill: {p['ink']}; }}
    .who {{ font: 600 9.5px {MONO}; fill: {p['muted']}; letter-spacing: 1.4px; }}
    .who.me {{ fill: {p['seal']}; }}
    .node {{ fill: {p['paper']}; stroke: {p['ink']}; stroke-width: 1.5; }}
    .node.me {{ fill: {p['seal']}; stroke: {p['seal']}; }}
    .step {{ font: 600 13.5px {MONO}; fill: {p['ink']}; }}
    .snote {{ font: 400 11px {MONO}; fill: {p['muted']}; }}
    .wire {{ stroke: {p['rule']}; stroke-width: 1.5; stroke-dasharray: {run}; animation: draw 1.2s cubic-bezier(.6,0,.2,1) .2s both; }}
    .vrule {{ stroke: {p['rule']}; }}
    .pop {{ animation: fade .5s ease-out both; }}
    .num {{ font: 600 54px {MONO}; fill: {p['ink']}; }}
    .label {{ font: 600 13px {MONO}; fill: {p['ink']}; }}
    .sub {{ font: 400 11.5px {MONO}; fill: {p['muted']}; }}
    .roll {{ transform: translateY(var(--y)); animation: roll 1.5s cubic-bezier(.2,.75,.15,1) both; }}
    .pulse {{ fill: {p['seal']}; opacity: 0; animation: travel 4.8s cubic-bezier(.45,0,.25,1) 2.2s infinite; }}
    @keyframes draw {{ from {{ stroke-dashoffset: {run}; }} to {{ stroke-dashoffset: 0; }} }}
    @keyframes fade {{ from {{ opacity: 0; transform: translateY(5px); }} to {{ opacity: 1; transform: none; }} }}
    @keyframes roll {{ from {{ transform: translateY(0); }} }}
    @keyframes travel {{ 0% {{ opacity: 0; transform: translateX(0); }} 8% {{ opacity: 1; }}
      80% {{ opacity: 1; transform: translateX({run}px); }} 92%, 100% {{ opacity: 0; transform: translateX({run}px); }} }}
    {REDUCE}
  </style>
  {frame(p, w, h)}
  <text x="44" y="46" class="kicker">HOW I WORK</text>
  <text x="{rx - 52}" y="46" class="motto" text-anchor="end">agents do the legwork · I own the call</text>
  <line x1="{x0}" y1="{ly}" x2="{x_end}" y2="{ly}" class="wire"/>
  {''.join(nodes)}
  <circle cx="{x0}" cy="{ly}" r="3.5" class="pulse"/>
  <line x1="{rx - 30}" y1="30" x2="{rx - 30}" y2="172" class="vrule"/>
  {roller(rx, 104, FACTS['merged'], 'num', 1.9)}
  <g class="pop" style="animation-delay:2.4s">
    <text x="{rx}" y="134" class="label">merged upstream</text>
    <text x="{rx}" y="154" class="sub">{FACTS['aibrix']} AIBrix · {FACTS['xinference']} Xinference</text>
    <text x="{rx}" y="171" class="sub">iterating with maintainers</text>
  </g>
</svg>
"""


def _ledger():
    """Merged upstream PRs by area, largest area first, oldest PR first. Size: "M" = 100+ changed lines, "S" = under
    100. "R" marks a release regression found by bisecting a release pair (the ledger's "regression" flag)."""
    areas = {}
    for p in sorted(PRS, key=lambda p: (p["merged"], p["repo"], p["number"])):
        areas.setdefault(p["area"], []).append(p)
    return [(area, " · ".join(name(r) for r, _ in Counter(p["repo"] for p in prs).most_common()),
             [p["size"] + ("R" if p["regression"] else "") for p in prs])
            for area, prs in sorted(areas.items(), key=lambda kv: (-len(kv[1]), kv[0]))]


LEDGER = _ledger()


def ledger(p):
    """Every merged upstream PR as a block, grouped by area and coloured by size."""
    total = sum(len(r[2]) for r in LEDGER)
    medium = sum(1 for r in LEDGER for b in r[2] if b.startswith("M"))
    regress = sum(1 for r in LEDGER for b in r[2] if b.endswith("R"))
    x_lab, x_bar, bh = 44, 236, 14
    unit = min(34, (790 - x_bar) // max(len(r[2]) for r in LEDGER))  # long rows shrink their blocks to fit
    bw = unit - 6
    y0, step = 116, 30
    rows, k = [], 0
    for i, (area, where, blocks) in enumerate(LEDGER):
        y = y0 + i * step
        cells = []
        for j, b in enumerate(blocks):
            x = x_bar + j * unit
            cls = "blk m" if b.startswith("M") else "blk s"
            mark = (f'<path d="M{x + bw / 2} {y - bh - 9}l4 4-4 4-4-4z" class="reg"/>' if b.endswith("R") else "")
            cells.append(f'<g class="pop" style="animation-delay:{0.35 + k * 0.05:.2f}s">'
                         f'<rect x="{x}" y="{y - bh + 2}" width="{bw}" height="{bh}" rx="3" class="{cls}"/>{mark}</g>')
            k += 1
        end = x_bar + len(blocks) * unit
        rows.append(
            f'<text x="{x_lab}" y="{y}" class="area">{escape(area)}</text>{"".join(cells)}'
            f'<text x="{end + 4}" y="{y}" class="cnt">{len(blocks)}</text>'
        )
    y_foot = y0 + (len(LEDGER) - 1) * step + 40
    others = FACTS["projects"] - 2
    w, h = 880, y_foot + 28
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img"
  aria-labelledby="t d">
  <title id="t">What got merged</title>
  <desc id="d">{total} merged upstream pull requests, {medium} of them 100 or more changed lines. By area:
    {escape('; '.join(f'{a} {len(b)}' for a, wh, b in LEDGER))}. {regress} were release regressions found by bisecting.
    Across {FACTS['projects']} projects: AIBrix, Xinference and {others} others.</desc>
  <defs>{GRAIN.format(g=p['grain'])}</defs>
  <style>
    .kicker {{ font: 500 12px {MONO}; fill: {p['muted']}; letter-spacing: 2.6px; }}
    .motto {{ font: italic 400 16px {SERIF}; fill: {p['ink']}; }}
    .legend {{ font: 400 11px {MONO}; fill: {p['muted']}; }}
    .area {{ font: 600 13px {MONO}; fill: {p['ink']}; }}
    .cnt {{ font: 600 13px {MONO}; fill: {p['ink']}; }}
    .where {{ font: 400 11.5px {MONO}; fill: {p['muted']}; }}
    .blk.m {{ fill: {p['seal']}; }}
    .blk.s {{ fill: {p['ink']}; opacity: .78; }}
    .reg {{ fill: {p['seal']}; }}
    .pop {{ transform-box: fill-box; transform-origin: center; animation: pop .35s cubic-bezier(.3,1.5,.5,1) both; }}
    @keyframes pop {{ from {{ opacity: 0; transform: scale(.4); }} to {{ opacity: 1; transform: none; }} }}
    {REDUCE}
  </style>
  {frame(p, w, h)}
  <text x="44" y="46" class="kicker">WHAT GOT MERGED</text>
  <text x="836" y="46" class="motto" text-anchor="end">{total} upstream PRs · {medium} medium · {total - medium} small</text>
  <rect x="44" y="64" width="12" height="9" rx="2" class="blk m"/><text x="62" y="72" class="legend">100+ lines</text>
  <rect x="152" y="64" width="12" height="9" rx="2" class="blk s"/><text x="170" y="72" class="legend">smaller</text>
  <path d="M250 64l4 4-4 4-4-4z" class="reg"/><text x="262" y="72" class="legend">release regression, bisected</text>
  {''.join(rows)}
  <line x1="44" y1="{y_foot - 18}" x2="836" y2="{y_foot - 18}" stroke="{p['rule']}"/>
  <text x="44" y="{y_foot}" class="where">{FACTS['projects']} projects · AIBrix, Xinference and {others} others</text>
</svg>
"""


def readme():
    total = len(PRS)
    medium = sum(1 for p in PRS if p["size"] == "M")
    regress = sum(1 for p in PRS if p["regression"])
    top = f"{FACTS['aibrix']} in vLLM AIBrix and {FACTS['xinference']} in Xinference"
    areas = ", ".join(f"{area.replace('&', 'and')} {len(blocks)}" for area, _, blocks in LEDGER)
    query = "author:Jackmeson1 is:pr is:merged " + " ".join(f"repo:{r}" for r in sorted(REPO_COUNTS))
    link = f"https://github.com/search?q={quote_plus(query)}&type=pullrequests&s=created&o=desc"
    return f"""<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/card-dark.svg">
  <img alt="Jack. SDET, agentic workflows, open source. Agentic coding is here. Open source iterates faster than ever. I'm in: finding, fixing, getting it merged." src="assets/card-light.svg" width="100%">
</picture>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/flow-dark.svg">
  <img alt="How I work: agents sweep and reproduce, a second model reviews, I decide and ship. {total} merged upstream PRs, {top}." src="assets/flow-light.svg" width="100%">
</picture>

<a href="{link}">
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/merged-dark.svg">
  <img alt="What got merged: {total} upstream PRs across {FACTS['projects']} projects, {medium} medium and {total - medium} small, by area: {areas}; {regress} release regressions found by bisecting" src="assets/merged-light.svg" width="100%">
</picture>
</a>
"""


if __name__ == "__main__":
    for old in HERE.glob("stats-*.svg"):
        old.unlink()
    outputs = {HERE.parent / "README.md": readme()}
    for mode, pal in PALETTES.items():
        outputs.update({HERE / f"card-{mode}.svg": card(pal), HERE / f"flow-{mode}.svg": workflow(pal),
                        HERE / f"merged-{mode}.svg": ledger(pal)})
    for path, text in outputs.items():
        with open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write(text)
    print("built", sorted(p.name for p in outputs), f"({FACTS['merged']} PRs, {FACTS['projects']} projects)")
