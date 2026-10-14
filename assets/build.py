"""Builds the profile card SVGs (light and dark). Edit FACTS, then run: python assets/build.py

The SVGs animate with CSS only (no script), and their resting state is the final frame, so static renderers and
prefers-reduced-motion both show the finished card.
"""
from pathlib import Path

FACTS = {
    "merged": 25,  # merged upstream PRs (excluding own repos and the competition)
    "solved": 173,  # conjectures settled on The Last Math Competition (leaderboard 2026-10-11)
    "rank": 2,
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


def card(p):
    lines = [
        ("reproduce", "a failing test before any fix"),
        ("fix", "small, reviewable, in the house style"),
        ("review", "an independent check before it ships"),
        ("prove", "when it is math: Lean 4, no sorry"),
    ]
    rows = []
    for i, (verb, note) in enumerate(lines):
        y = 196 + i * 30
        d = 0.9 + i * 0.75
        rows.append(
            f'<g class="type" style="animation-delay:{d:.2f}s">'
            f'<text x="44" y="{y}" class="mark">✓</text>'
            f'<text x="70" y="{y}" class="verb">{verb}</text>'
            f'<text x="186" y="{y}" class="note">{note}</text></g>'
        )
    cursor_y = 196 + 3 * 30
    cursor_x = 186 + round(len(lines[-1][1]) * 8.45) + 8
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="880" height="330" viewBox="0 0 880 330" role="img"
  aria-labelledby="t d">
  <title id="t">Jack</title>
  <desc id="d">QA engineer and upstream fixer: reproduce with a failing test, fix small, review independently, prove in
    Lean 4.</desc>
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
    .cursor {{ fill: {p['seal']}; animation: blink 1.05s steps(1, end) 3.7s infinite backwards; }}
    .seal {{ transform-box: fill-box; transform-origin: center; animation: stamp .42s cubic-bezier(.3,1.6,.5,1) 4.15s both; }}
    .seal text {{ fill: {p['seal']}; }}
    .seal .big {{ font: 700 25px {SERIF}; letter-spacing: 3px; }}
    .seal .small {{ font: 700 8.5px {MONO}; letter-spacing: 1.4px; }}
    @keyframes draw {{ from {{ stroke-dashoffset: 792; }} to {{ stroke-dashoffset: 0; }} }}
    @keyframes fade {{ from {{ opacity: 0; transform: translateY(6px); }} to {{ opacity: 1; transform: none; }} }}
    @keyframes type {{ from {{ clip-path: inset(0 100% 0 0); }} to {{ clip-path: inset(0 0 0 0); }} }}
    @keyframes blink {{ 0% {{ opacity: 0; }} 50% {{ opacity: 1; }} }}
    @keyframes stamp {{ 0% {{ opacity: 0; transform: rotate(-8deg) scale(1.7); }} 70% {{ opacity: .95; }}
      100% {{ opacity: .92; transform: rotate(-8deg) scale(1); }} }}
    {REDUCE}
  </style>
  <rect x=".5" y=".5" width="879" height="329" rx="16" fill="{p['paper']}" stroke="{p['rule']}"/>
  <rect x=".5" y=".5" width="879" height="329" rx="16" fill="{p['paper']}" filter="url(#grain)"/>
  <g class="fade">
    <text x="40" y="94" class="name">Jack<tspan class="dot">.</tspan></text>
    <text x="44" y="128" class="role">QA ENGINEER  ·  UPSTREAM FIXER  ·  LEAN 4</text>
  </g>
  <line x1="44" y1="152" x2="836" y2="152" class="rule"/>
  {''.join(rows)}
  <rect x="{cursor_x}" y="{cursor_y - 13}" width="8" height="16" class="cursor"/>
  <g class="seal" style="opacity:.92" transform="rotate(-8 788 92)" filter="url(#ink)">
    <rect x="740" y="44" width="96" height="96" rx="6" fill="none" stroke="{p['seal']}" stroke-width="3"/>
    <rect x="747" y="51" width="82" height="82" rx="3" fill="none" stroke="{p['seal']}" stroke-width="1"/>
    <text x="788" y="98" text-anchor="middle" class="big">PASS</text>
    <text x="788" y="117" text-anchor="middle" class="small">VERIFIED · {FACTS['as_of'].split()[-1]}</text>
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
            f'<g clip-path="url(#cell{i}_{x})"><g class="roll" '
            f'style="--y:{-n * cell}px;animation-delay:{delay + i * .12:.2f}s">{digits}</g></g>'
        )
        out.append(
            f'<clipPath id="cell{i}_{x}"><rect x="{cx - 2}" y="{y - 52}" width="{width}" height="{cell}"/></clipPath>'
        )
    return "".join(out)


def stats(p):
    cols = [
        (44, FACTS["merged"], "merged upstream PRs", "AIBrix · GPUStack · SQLFluff · …"),
        (330, FACTS["solved"], "conjectures settled", "Lean 4 · audited · no sorry"),
        (616, FACTS["rank"], "Last Math Competition", f"leaderboard rank · {FACTS['as_of']}"),
    ]
    body = []
    for j, (x, value, label, sub) in enumerate(cols):
        d = 0.3 + j * 0.35
        lead = ""
        nx = x
        if j == 2:
            lead = f'<text x="{x}" y="78" class="num hash">#</text>'
            nx = x + 34
        body.append(
            f'{lead}{roller(nx, 78, value, "num", d)}'
            f'<g class="fade" style="animation-delay:{d + .5:.2f}s">'
            f'<text x="{x}" y="112" class="label">{label}</text>'
            f'<text x="{x}" y="132" class="sub">{sub}</text></g>'
        )
        if j:
            body.append(f'<line x1="{x - 22}" y1="34" x2="{x - 22}" y2="132" class="vrule" style="animation-delay:{d:.2f}s"/>')
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="880" height="160" viewBox="0 0 880 160" role="img"
  aria-labelledby="t d">
  <title id="t">Track record</title>
  <desc id="d">{FACTS['merged']} merged upstream pull requests; {FACTS['solved']} conjectures settled in Lean 4;
    rank {FACTS['rank']} on The Last Math Competition leaderboard ({FACTS['as_of']}).</desc>
  <defs>{GRAIN.format(g=p['grain'])}</defs>
  <style>
    .num {{ font: 600 54px {MONO}; fill: {p['ink']}; }}
    .hash {{ fill: {p['seal']}; }}
    .label {{ font: 600 13px {MONO}; fill: {p['ink']}; letter-spacing: .4px; }}
    .sub {{ font: 400 11.5px {MONO}; fill: {p['muted']}; }}
    .vrule {{ stroke: {p['rule']}; stroke-dasharray: 98; animation: draw .8s ease-out both; }}
    .roll {{ transform: translateY(var(--y)); animation: roll 1.5s cubic-bezier(.2,.75,.15,1) both; }}
    .fade {{ animation: fade .7s ease-out both; }}
    @keyframes roll {{ from {{ transform: translateY(0); }} }}
    @keyframes draw {{ from {{ stroke-dashoffset: 98; }} to {{ stroke-dashoffset: 0; }} }}
    @keyframes fade {{ from {{ opacity: 0; transform: translateY(5px); }} to {{ opacity: 1; transform: none; }} }}
    {REDUCE}
  </style>
  <rect x=".5" y=".5" width="879" height="159" rx="16" fill="{p['paper']}" stroke="{p['rule']}"/>
  <rect x=".5" y=".5" width="879" height="159" rx="16" fill="{p['paper']}" filter="url(#grain)"/>
  {''.join(body)}
</svg>
"""


if __name__ == "__main__":
    here = Path(__file__).parent
    for mode, pal in PALETTES.items():
        for name, svg in ((f"card-{mode}.svg", card(pal)), (f"stats-{mode}.svg", stats(pal))):
            with open(here / name, "w", encoding="utf-8", newline="\n") as f:
                f.write(svg)
    print("built", sorted(p.name for p in here.glob("*.svg")))
