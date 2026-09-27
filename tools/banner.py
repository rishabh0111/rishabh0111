"""Render the profile banner, once per theme.

    python tools/banner.py   ->  assets/banner-light.svg, assets/banner-dark.svg

The palette is the portfolio's (Nord). GitHub shows an SVG in <img>,
which blocks web fonts, so every line whose width matters is pinned
with textLength: the typing reveal and the cursor then land on the
characters whatever font the viewer's system picks.
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "assets")

W, H = 1280, 340

THEMES = {
    "light": dict(bg="#ECEFF4", raised="#E5E9F0", line="#D8DEE9", ink="#2E3440",
                  ink2="#485265", ink3="#5E6A83", accent="#1E768F", soft="#88C0D0"),
    "dark":  dict(bg="#2E3440", raised="#3B4252", line="#434C5E", ink="#ECEFF4",
                  ink2="#D8DEE9", ink3="#A3AFC2", accent="#88C0D0", soft="#4C7A8A"),
}

PHRASES = [
    "I build LLM systems and the plumbing under them.",
    "I write about what breaks, and why.",
    "Everything here is open source.",
    "Questions and pull requests welcome.",
]

# What I'm up to, not a scoreboard: a kind and a line each.
NOW = [
    ("BUILDING", "AI that knows when to stop"),
    ("WRITING",  "System Design and DSA, free"),
    ("LEARNING", "fine-tuning and OpenTelemetry"),
    ("ASK ME",   "evals, Postgres, Kubernetes"),
]

MONO = "'Martian Mono', ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
SANS = "'Bricolage Grotesque', 'Segoe UI', Helvetica, Arial, sans-serif"

TYPE, ERASE, HOLD, GAP = 0.055, 0.022, 2.0, 0.35
X0, Y_TYPE, SIZE = 96, 236, 24
CW = SIZE * 0.6  # one character cell


def timeline():
    """Per phrase: (start, typed, held, erased) in seconds, and the loop length."""
    t, spans = 0.0, []
    for p in PHRASES:
        n = len(p)
        typed = t + n * TYPE
        held = typed + HOLD
        erased = held + n * ERASE
        spans.append((t, typed, held, erased))
        t = erased + GAP
    return spans, t


def discrete(points, total):
    """(time, value) steps -> SMIL values / keyTimes for calcMode=discrete."""
    points = sorted(points)
    if points[0][0] > 0:  # hidden until this phrase's turn
        points.insert(0, (0.0, 0))
    vals = ";".join("%.1f" % v for _, v in points) + ";%.1f" % points[-1][1]
    keys = ";".join("%.4f" % (tm / total) for tm, _ in points) + ";1"
    return vals, keys


def phrase_steps(i, spans):
    s, typed, held, erased = spans[i]
    n = len(PHRASES[i])
    pts = [(s + k * TYPE, k * CW) for k in range(n + 1)]
    pts += [(held + k * ERASE, (n - k) * CW) for k in range(1, n + 1)]
    return pts


def contours(c):
    """Slow-drifting topographic rings, the portfolio's background motif."""
    out = []
    cx, cy = 1010, 170
    for k in range(9):
        rx, ry = 70 + k * 38, 44 + k * 26
        wob = 6 + k * 1.5
        d = ("M %.1f %.1f " % (cx - rx, cy) +
             "C %.1f %.1f %.1f %.1f %.1f %.1f " % (cx - rx, cy - ry - wob, cx - rx * 0.1, cy - ry + wob, cx + rx * 0.35, cy - ry) +
             "C %.1f %.1f %.1f %.1f %.1f %.1f " % (cx + rx * 0.9, cy - ry - wob, cx + rx + wob, cy - ry * 0.4, cx + rx, cy + ry * 0.1) +
             "C %.1f %.1f %.1f %.1f %.1f %.1f " % (cx + rx - wob, cy + ry + wob, cx + rx * 0.1, cy + ry - wob, cx - rx * 0.3, cy + ry) +
             "C %.1f %.1f %.1f %.1f %.1f %.1f Z" % (cx - rx * 0.8, cy + ry + wob, cx - rx - wob, cy + ry * 0.5, cx - rx, cy))
        dur = 18 + k * 3
        out.append(
            '<path d="%s" fill="none" stroke="%s" stroke-width="1.2" opacity="%.2f">'
            '<animateTransform attributeName="transform" type="rotate" '
            'values="0 %d %d;%s %d %d;0 %d %d" dur="%ds" repeatCount="indefinite"/></path>'
            % (d, c["soft"], 0.55 - k * 0.04, cx, cy, "3" if k % 2 else "-3", cx, cy, cx, cy, dur))
    return "\n    ".join(out)


def render(name, c):
    spans, total = timeline()
    clips, texts, cursor_pts = [], [], []
    for i, p in enumerate(PHRASES):
        steps = phrase_steps(i, spans)
        vals, keys = discrete(steps, total)
        clips.append(
            '<clipPath id="t%d"><rect x="%d" y="%d" width="0" height="%d">'
            '<animate attributeName="width" values="%s" keyTimes="%s" dur="%.2fs" '
            'calcMode="discrete" repeatCount="indefinite"/></rect></clipPath>'
            % (i, X0, Y_TYPE - SIZE, SIZE + 12, vals, keys, total))
        texts.append(
            '<text x="%d" y="%d" clip-path="url(#t%d)" textLength="%.1f" '
            'lengthAdjust="spacingAndGlyphs" class="mono" font-size="%d" fill="%s">%s</text>'
            % (X0, Y_TYPE, i, len(p) * CW, SIZE, c["ink2"], p.replace("'", "&#8217;")))
        cursor_pts += [(tm, X0 + w) for tm, w in steps]
    cvals, ckeys = discrete(cursor_pts, total)

    pills = []
    for k, (kind, label) in enumerate(NOW):
        y = 58 + k * 60
        pills.append(
            '<g transform="translate(852 %d)" opacity="0">'
            '<animate attributeName="opacity" from="0" to="1" begin="%.1fs" dur="0.6s" fill="freeze"/>'
            '<rect width="364" height="46" rx="10" fill="%s" fill-opacity="0.88" stroke="%s"/>'
            '<rect x="0" y="10" width="3" height="26" rx="1.5" fill="%s"/>'
            '<text x="20" y="28" class="mono" font-size="11" letter-spacing="2" fill="%s" font-weight="600">%s</text>'
            '<text x="116" y="28.5" class="mono" font-size="13.5" fill="%s" textLength="%.1f" lengthAdjust="spacingAndGlyphs">%s</text>'
            '</g>' % (y, 0.4 + k * 0.25, c["raised"], c["line"], c["accent"], c["accent"], kind, c["ink2"],
                      len(label) * 13.5 * 0.6, label))

    svg = """<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Rishabh Sharma, AI engineer. I build LLM systems and the plumbing under them, and write about what breaks.">
  <style>
    .mono {{ font-family: {MONO}; }}
    .sans {{ font-family: {SANS}; }}
  </style>
  <defs>
    <pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse">
      <circle cx="2" cy="2" r="1.1" fill="{line}"/>
    </pattern>
    <linearGradient id="fade" x1="0" x2="1">
      <stop offset="0" stop-color="{bg}" stop-opacity="1"/>
      <stop offset="0.55" stop-color="{bg}" stop-opacity="0.2"/>
      <stop offset="1" stop-color="{bg}" stop-opacity="0"/>
    </linearGradient>
    <clipPath id="card"><rect width="{W}" height="{H}" rx="18"/></clipPath>
    {clips}
  </defs>
  <g clip-path="url(#card)">
    <rect width="{W}" height="{H}" fill="{bg}"/>
    <rect width="{W}" height="{H}" fill="url(#dots)"/>
    {contours}
    <rect width="{W}" height="{H}" fill="url(#fade)"/>
  </g>
  <rect x="0.5" y="0.5" width="{W1}" height="{H1}" rx="18" fill="none" stroke="{line}"/>

  <text x="{X0}" y="78" class="mono" font-size="15" letter-spacing="4" fill="{ink2}">RISHABH SHARMA/<tspan fill="{accent}">_<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.5;1" dur="1.1s" repeatCount="indefinite"/></tspan></text>

  <text x="{X0}" y="166" class="sans" font-size="76" font-weight="700" fill="{ink}" letter-spacing="-1.5">Rishabh <tspan font-style="italic" fill="{accent}">Sharma</tspan></text>

  <text x="{PX}" y="{Y_TYPE}" class="mono" font-size="{SIZE}" fill="{accent}">&#8250;</text>
  {texts}
  <rect x="{X0}" y="{CY}" width="{CWW}" height="{CH}" fill="{accent}">
    <animate attributeName="x" values="{cvals}" keyTimes="{ckeys}" dur="{total:.2f}s" calcMode="discrete" repeatCount="indefinite"/>
    <animate attributeName="opacity" values="1;1;0.15;0.15" keyTimes="0;0.5;0.5;1" dur="0.9s" repeatCount="indefinite"/>
  </rect>

  <circle cx="{DX}" cy="291" r="5" fill="{accent}"/>
  <circle cx="{DX}" cy="291" r="5" fill="none" stroke="{accent}">
    <animate attributeName="r" values="5;13" dur="2s" repeatCount="indefinite"/>
    <animate attributeName="opacity" values="0.8;0" dur="2s" repeatCount="indefinite"/>
  </circle>
  <text x="{SX}" y="296" class="mono" font-size="14" letter-spacing="1.5" fill="{ink3}" textLength="560" lengthAdjust="spacingAndGlyphs">AI · BACKEND · INFRASTRUCTURE  ·  GURUGRAM, INDIA</text>

  {pills}
</svg>
""".format(W=W, H=H, W1=W - 1, H1=H - 1, MONO=MONO, SANS=SANS, X0=X0, PX=X0 - 30,
           Y_TYPE=Y_TYPE, SIZE=SIZE, CY=Y_TYPE - SIZE + 4, CWW=int(CW * 0.9), CH=SIZE + 2,
           DX=X0 + 5, SX=X0 + 24, clips="\n    ".join(clips), texts="\n  ".join(texts),
           contours=contours(c), cvals=cvals, ckeys=ckeys, total=total,
           pills="\n  ".join(pills), **c)
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "banner-%s.svg" % name), "w", encoding="utf-8") as f:
        f.write(svg)


if __name__ == "__main__":
    for name, c in THEMES.items():
        render(name, c)
    print("wrote assets/banner-light.svg, assets/banner-dark.svg")
