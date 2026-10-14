"""Builds the profile SVGs (light and dark). Edit FACTS, then run: python assets/build.py

The SVGs animate with CSS only (no script), and their resting state is the final frame, so static renderers and
prefers-reduced-motion both show the finished picture.
"""
from pathlib import Path

FACTS = {
    "merged": 25,  # merged PRs in other people's repositories
    "projects": 5,  # AIBrix, GPUStack, SQLFluff, Semantic Router, REA
    "aibrix": 19,  # merged in vllm-project/aibrix
    "as_of": "Oct 2026",
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
        ("evidence", "a failing test, or it isn't a bug"),
        ("restraint", "small PRs in the house style, no noise"),
        ("follow-through", "every review note answered"),
    ]
    rows = []
    for i, (verb, note) in enumerate(lines):
        y = 196 + i * 30
        rows.append(
            f'<g class="type" style="animation-delay:{0.9 + i * 0.75:.2f}s">'
            f'<text x="44" y="{y}" class="mark">✓</text>'
            f'<text x="70" y="{y}" class="verb">{verb}</text>'
            f'<text x="214" y="{y}" class="note">{note}</text></g>'
        )
    cy = 196 + (len(lines) - 1) * 30
    cx = 214 + round(len(lines[-1][1]) * 8.45) + 8
    end = 0.9 + (len(lines) - 1) * 0.75 + 0.6
    w, h = 880, 280
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img"
  aria-labelledby="t d">
  <title id="t">Jack</title>
  <desc id="d">QA engineer and open-source contributor. Evidence: a failing test, or it isn't a bug. Restraint: small
    PRs in the house style. Follow-through: every review note answered.</desc>
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
    .mark {{ font: 600 14px {MONO}; fill: {p['seal']}; }}
    .verb {{ font: 600 14px {MONO}; fill: {p['ink']}; }}
    .note {{ font: 400 14px {MONO}; fill: {p['muted']}; }}
    .rule {{ stroke: {p['rule']}; stroke-width: 1; stroke-dasharray: 792; animation: draw 1.1s cubic-bezier(.6,0,.2,1) .2s both; }}
    .fade {{ animation: fade .9s ease-out .1s both; }}
    .type {{ animation: type .55s steps(26, end) both; }}
    .cursor {{ fill: {p['seal']}; animation: blink 1.05s steps(1, end) {end:.2f}s infinite backwards; }}
    .seal {{ transform-box: fill-box; transform-origin: center; animation: stamp .42s cubic-bezier(.3,1.6,.5,1) {end + .3:.2f}s both; }}
    .seal text {{ fill: {p['seal']}; }}
    .seal .big {{ font: 700 17px {SERIF}; letter-spacing: 1.5px; }}
    .seal .small {{ font: 700 7.6px {MONO}; letter-spacing: .6px; }}
    @keyframes draw {{ from {{ stroke-dashoffset: 792; }} to {{ stroke-dashoffset: 0; }} }}
    @keyframes fade {{ from {{ opacity: 0; transform: translateY(6px); }} to {{ opacity: 1; transform: none; }} }}
    @keyframes type {{ from {{ clip-path: inset(0 100% 0 0); }} to {{ clip-path: inset(0 0 0 0); }} }}
    @keyframes blink {{ 0% {{ opacity: 0; }} 50% {{ opacity: 1; }} }}
    @keyframes stamp {{ 0% {{ opacity: 0; transform: rotate(-8deg) scale(1.7); }} 70% {{ opacity: .95; }}
      100% {{ opacity: .92; transform: rotate(-8deg) scale(1); }} }}
    {REDUCE}
  </style>
  {frame(p, w, h)}
  <g class="fade">
    <text x="40" y="94" class="name">Jack<tspan class="dot">.</tspan></text>
    <text x="44" y="128" class="role">QA ENGINEER  ·  OPEN-SOURCE CONTRIBUTOR</text>
  </g>
  <line x1="44" y1="152" x2="836" y2="152" class="rule"/>
  {''.join(rows)}
  <rect x="{cx}" y="{cy - 13}" width="8" height="16" class="cursor"/>
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
    upstream pull requests, {FACTS['aibrix']} of them in vLLM AIBrix, iterating with maintainers
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
    <text x="{rx}" y="154" class="sub">{FACTS['aibrix']} in vLLM AIBrix</text>
    <text x="{rx}" y="171" class="sub">iterating with maintainers</text>
  </g>
</svg>
"""


if __name__ == "__main__":
    here = Path(__file__).parent
    for old in here.glob("stats-*.svg"):
        old.unlink()
    for mode, pal in PALETTES.items():
        for name, svg in ((f"card-{mode}.svg", card(pal)), (f"flow-{mode}.svg", workflow(pal))):
            with open(here / name, "w", encoding="utf-8", newline="\n") as f:
                f.write(svg)
    print("built", sorted(p.name for p in here.glob("*.svg")))
