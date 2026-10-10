"""Render the profile banner, once per theme.

    python tools/banner.py   ->  assets/banner-light.svg, assets/banner-dark.svg

The palette is the portfolio's (Nord). GitHub shows an SVG in <img>,
which blocks web fonts and scripts, so everything moves with SMIL.

The banner is the name and a desk, nothing the README already says:
a laptop mid-keystroke, a mug going cold, a plant, a chess game in
progress, and a window that is day in the light theme and night in
the dark one.
"""
import os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(HERE), "assets")

W, H = 1280, 340

THEMES = {
    "light": dict(night=False, bg="#ECEFF4", raised="#E5E9F0", line="#D8DEE9", ink="#2E3440",
                  ink2="#485265", ink3="#5E6A83", accent="#1E768F", soft="#88C0D0",
                  desk="#D8DEE9", edge="#C2CAD8", screen="#2E3440", bezel="#3B4252",
                  sky="#BFDDE8", mug="#5E81AC", pot="#D08770", leaf="#7FA36A", leaf2="#A3BE8C",
                  sq_a="#D8DEE9", sq_b="#AEB8CA", white="#FFFFFF", glow="#88C0D0"),
    "dark":  dict(night=True, bg="#2E3440", raised="#3B4252", line="#434C5E", ink="#ECEFF4",
                  ink2="#D8DEE9", ink3="#A3AFC2", accent="#88C0D0", soft="#4C7A8A",
                  desk="#3B4252", edge="#4C566A", screen="#242933", bezel="#4C566A",
                  sky="#1F2430", mug="#81A1C1", pot="#D08770", leaf="#8FBC8F", leaf2="#A3BE8C",
                  sq_a="#4C566A", sq_b="#3B4252", white="#ECEFF4", glow="#88C0D0"),
}

SANS = "'Bricolage Grotesque', 'Segoe UI', Helvetica, Arial, sans-serif"

DESK = 262  # y of the desk top

# Code on the laptop screen: per line, an indent and (width, colour key) tokens.
CODE = [
    (0, [(26, "kw"), (52, "fn"), (18, "p")]),
    (14, [(34, "kw"), (60, "id"), (22, "p")]),
    (28, [(20, "kw"), (44, "str")]),
    (14, [(40, "fn"), (30, "id"), (12, "p")]),
    (14, [(26, "kw"), (54, "id")]),
    (0, [(10, "p")]),
]
TOKENS = dict(kw="#B48EAD", fn="#88C0D0", id="#D8DEE9", str="#A3BE8C", p="#81A1C1")
CODE_LOOP = 9.0


def keys(times, total):
    return ";".join("%.4f" % (t / total) for t in times)


def laptop(c):
    sx, sy, sw, sh = 800, 116, 196, 128  # screen
    out = [
        # a soft pool of screen light on the desk
        '<ellipse cx="%d" cy="%d" rx="150" ry="10" fill="%s" opacity="0.18">'
        '<animate attributeName="opacity" values="0.14;0.22;0.14" dur="4s" repeatCount="indefinite"/></ellipse>'
        % (sx + sw / 2, DESK + 2, c["glow"]),
        '<rect x="%d" y="%d" width="%d" height="%d" rx="9" fill="%s"/>' % (sx - 8, sy - 8, sw + 16, sh + 14, c["bezel"]),
        '<rect x="%d" y="%d" width="%d" height="%d" rx="3" fill="%s"/>' % (sx, sy, sw, sh, c["screen"]),
        '<circle cx="%d" cy="%d" r="1.6" fill="%s"/>' % (sx + sw / 2, sy - 4, c["ink3"]),
        # base: a slab, wider at the front
        '<path d="M %d %d L %d %d L %d %d Q %d %d %d %d L %d %d Q %d %d %d %d Z" fill="%s"/>'
        % (sx - 14, sy + sh + 6, sx + sw + 14, sy + sh + 6, sx + sw + 26, DESK - 3,
           sx + sw + 26, DESK, sx + sw + 20, DESK, sx - 20, DESK, sx - 26, DESK, sx - 26, DESK - 3, c["edge"]),
        '<rect x="%d" y="%d" width="40" height="3" rx="1.5" fill="%s" opacity="0.6"/>' % (sx + sw / 2 - 20, DESK - 6, c["bezel"]),
    ]
    # Lines type in one after another, sit for a beat, then the screen clears.
    x0, y0, lh = sx + 14, sy + 20, 17
    t, spans = 0.6, []
    for indent, toks in CODE:
        w = sum(tw for tw, _ in toks) + 5 * (len(toks) - 1)
        dur = w / 70.0
        spans.append((t, t + dur, indent, w))
        t += dur + 0.35
    clear = CODE_LOOP - 0.8
    lines, clips = [], []
    for i, ((indent, toks), (s, e, _, w)) in enumerate(zip(CODE, spans)):
        y = y0 + i * lh
        clips.append(
            '<clipPath id="ln%d"><rect x="%d" y="%d" height="10" width="0">'
            '<animate attributeName="width" values="0;0;%d;%d;0" keyTimes="0;%s;1" dur="%gs" repeatCount="indefinite"/>'
            '</rect></clipPath>' % (i, x0 + indent, y - 5, w, w, keys([s, e, clear], CODE_LOOP), CODE_LOOP))
        x, rects = x0 + indent, []
        for tw, k in toks:
            rects.append('<rect x="%d" y="%d" width="%d" height="5" rx="2.5" fill="%s"/>' % (x, y - 2, tw, TOKENS[k]))
            x += tw + 5
        lines.append('<g clip-path="url(#ln%d)">%s</g>' % (i, "".join(rects)))
    # The cursor rides the end of whichever line is being typed.
    times, xs, ys = [0.0], [x0], [y0 - 5]
    for i, (s, e, indent, w) in enumerate(spans):
        times += [s - 0.01, s, e]  # wait at the end of the last line, then jump
        xs += [xs[-1], x0 + indent, x0 + indent + w + 2]
        ys += [ys[-1]] + [y0 + i * lh - 5] * 2
    times += [clear, clear + 0.01, CODE_LOOP]
    xs += [xs[-1], x0, x0]
    ys += [ys[-1], y0 - 5, y0 - 5]
    cursor = (
        '<rect width="2" height="10" fill="%s">'
        '<animate attributeName="x" values="%s" keyTimes="%s" dur="%gs" repeatCount="indefinite"/>'
        '<animate attributeName="y" values="%s" keyTimes="%s" dur="%gs" calcMode="discrete" repeatCount="indefinite"/>'
        '<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.5;1" dur="1s" repeatCount="indefinite"/></rect>'
        % (c["accent"] if c["night"] else c["soft"],
           ";".join("%.1f" % v for v in xs), keys(times, CODE_LOOP), CODE_LOOP,
           ";".join("%.1f" % v for v in ys), keys(times, CODE_LOOP), CODE_LOOP))
    return out + lines + [cursor], clips


def mug(c):
    x, w, h = 1030, 40, 44
    y = DESK - h
    out = [
        '<path d="M %d %d q 16 0 16 13 q 0 13 -16 13" fill="none" stroke="%s" stroke-width="5"/>'
        % (x + w - 2, y + 9, c["mug"]),
        '<path d="M %d %d h %d v %d q 0 7 -7 7 h %d q -7 0 -7 -7 Z" fill="%s"/>'
        % (x, y, w, h - 7, -(w - 14), c["mug"]),
        '<rect x="%d" y="%d" width="%d" height="5" rx="2.5" fill="%s" opacity="0.35"/>' % (x, y, w, c["white"]),
    ]
    # Steam: three wisps rising out of phase.
    for k, dx in enumerate((10, 20, 30)):
        out.append(
            '<path d="M %d %d c -5 -6 5 -10 0 -16 c -5 -6 5 -10 0 -16" fill="none" stroke="%s" '
            'stroke-width="2.2" stroke-linecap="round" opacity="0">'
            '<animateTransform attributeName="transform" type="translate" values="0 4;0 -14" '
            'dur="3.2s" begin="%.1fs" repeatCount="indefinite"/>'
            '<animate attributeName="opacity" values="0;0.55;0" dur="3.2s" begin="%.1fs" repeatCount="indefinite"/></path>'
            % (x + dx, y - 4, c["ink3"], -k * 1.05, -k * 1.05))
    return out


def plant(c):
    x = 744
    leaves = [(-26, -34), (22, -30), (-8, -52), (12, -48), (-30, -16), (28, -14)]
    out = ['<g><animateTransform attributeName="transform" type="rotate" values="-2.5 %d %d;2.5 %d %d;-2.5 %d %d" '
           'dur="6s" repeatCount="indefinite"/>' % (x, DESK - 34, x, DESK - 34, x, DESK - 34)]
    for k, (lx, ly) in enumerate(leaves):
        ang = -60 if lx < 0 else 60
        if abs(lx) < 15:
            ang = -20 if lx < 0 else 20
        out.append(
            '<ellipse cx="%d" cy="%d" rx="7" ry="17" fill="%s" transform="rotate(%d %d %d)"/>'
            % (x + lx * 0.7, DESK - 34 + ly * 0.7, c["leaf"] if k % 2 else c["leaf2"], ang, x + lx * 0.7, DESK - 34 + ly * 0.7))
    out.append('</g>')
    out.append('<path d="M %d %d h 40 l -5 34 h -30 Z" fill="%s"/>' % (x - 20, DESK - 34, c["pot"]))
    out.append('<rect x="%d" y="%d" width="46" height="7" rx="2" fill="%s"/>' % (x - 23, DESK - 38, c["pot"]))
    return out


# The board is drawn in perspective: a trapezoid, back edge narrower.
BX0, BX1, BACK, FRONT = 1102, 1222, 226, 251
COLS, ROWS = 6, 3


def board_point(u, v):
    """u across (0..1), v from back (0) to front (1)."""
    y = BACK + (FRONT - BACK) * v
    inset = 10 * (1 - v)
    return BX0 - 10 + inset + (BX1 - BX0 + 20 - 2 * inset) * u, y


def square_centre(col, row):
    return board_point((col + 0.5) / COLS, (row + 0.5) / ROWS)


KNIGHT = ("M -8 0 L 8 0 L 8 -3 L 5 -4 L 4 -11 C 7 -15 7 -21 3 -25 C 0 -27 -3 -26 -6 -23 "
          "L -10 -17 L -9 -14 L -5 -15 L -3 -13 L -6 -6 L -6 -4 L -8 -3 Z")
PAWN = "M -7 0 L 7 0 L 7 -3 L 3 -5 L 2 -12 L 4 -13 L 4 -15 L -4 -15 L -4 -13 L -2 -12 L -3 -5 L -7 -3 Z"


def chess(c):
    out = []
    for row in range(ROWS):
        for col in range(COLS):
            pts = [board_point(col / COLS, row / ROWS), board_point((col + 1) / COLS, row / ROWS),
                   board_point((col + 1) / COLS, (row + 1) / ROWS), board_point(col / COLS, (row + 1) / ROWS)]
            out.append('<path d="M %s Z" fill="%s"/>' % (" L ".join("%.1f %.1f" % p for p in pts),
                                                        c["sq_a"] if (row + col) % 2 else c["sq_b"]))
    fl, fr = board_point(0, 1), board_point(1, 1)
    out.append('<rect x="%.1f" y="%d" width="%.1f" height="%d" fill="%s"/>' % (fl[0], FRONT, fr[0] - fl[0], DESK - FRONT, c["edge"]))

    def piece(path, x, y, fill, stroke, head=None, scale=1.0):
        h = '<circle cx="0" cy="%d" r="4.2" fill="%s" stroke="%s" stroke-width="1.4"/>' % (head, fill, stroke) if head else ""
        return ('<g transform="translate(%.1f %.1f) scale(%.2f)"><path d="%s" fill="%s" stroke="%s" stroke-width="1.4" '
                'stroke-linejoin="round"/>%s</g>' % (x, y, scale, path, fill, stroke, h))

    # Two pawns hold still; the knight hops an L out and, later, back.
    out.append(piece(PAWN, *square_centre(4, 0), c["white"], c["ink3"], head=-19, scale=1.15))
    out.append(piece(PAWN, *square_centre(1, 0), c["white"], c["ink3"], head=-19, scale=1.15))
    a, b = square_centre(1, 2), square_centre(3, 1)
    mid = ((a[0] + b[0]) / 2, min(a[1], b[1]) - 16)
    hop = 0.7
    loop = 10.0
    t = [0, 3.0, 3.0 + hop / 2, 3.0 + hop, 8.0, 8.0 + hop / 2, 8.0 + hop, loop]
    pos = [a, a, mid, b, b, mid, a, a]
    out.append(
        '<g><animateTransform attributeName="transform" type="translate" values="%s" keyTimes="%s" '
        'dur="%gs" repeatCount="indefinite"/>%s</g>'
        % (";".join("%.1f %.1f" % p for p in pos), keys(t, loop), loop,
           piece(KNIGHT, 0, 0, c["bezel"], c["ink"] if c["night"] else c["bezel"], scale=1.3)))
    return out


def window(c):
    x, y, w, h = 1100, 40, 118, 104
    out = [
        '<clipPath id="sky"><rect x="%d" y="%d" width="%d" height="%d" rx="4"/></clipPath>' % (x, y, w, h),
    ]
    sky = ['<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>' % (x, y, w, h, c["sky"])]
    if c["night"]:
        sky.append('<circle cx="%d" cy="%d" r="15" fill="#EBCB8B"/>' % (x + 80, y + 30))
        sky.append('<circle cx="%d" cy="%d" r="13" fill="%s"/>' % (x + 87, y + 25, c["sky"]))
        for k, (sx, sy) in enumerate([(18, 18), (40, 44), (28, 78), (62, 14), (96, 70), (70, 88), (12, 52)]):
            sky.append('<circle cx="%d" cy="%d" r="1.6" fill="#ECEFF4"><animate attributeName="opacity" '
                       'values="0.2;1;0.2" dur="%.1fs" begin="%.1fs" repeatCount="indefinite"/></circle>'
                       % (x + sx, y + sy, 2.4 + k * 0.5, -k * 0.7))
    else:
        sky.append('<circle cx="%d" cy="%d" r="14" fill="#EBCB8B"/>' % (x + 82, y + 30))
        cloud = ('<g fill="#FFFFFF" opacity="0.95"><ellipse cx="0" cy="0" rx="18" ry="9"/>'
                 '<circle cx="-8" cy="-6" r="8"/><circle cx="6" cy="-8" r="10"/></g>')
        for k, (cy, dur) in enumerate([(60, 26), (82, 38)]):
            sky.append('<g><animateTransform attributeName="transform" type="translate" values="%d %d;%d %d" '
                       'dur="%ds" begin="%ds" repeatCount="indefinite"/>%s</g>'
                       % (x - 30, y + cy, x + w + 30, y + cy, dur, -k * 17, cloud))
    out.append('<g clip-path="url(#sky)">%s</g>' % "".join(sky))
    out.append('<rect x="%d" y="%d" width="%d" height="%d" rx="4" fill="none" stroke="%s" stroke-width="6"/>' % (x, y, w, h, c["edge"]))
    out.append('<path d="M %d %d v %d M %d %d h %d" stroke="%s" stroke-width="4"/>' % (x + w / 2, y, h, x, y + h / 2, w, c["edge"]))
    out.append('<rect x="%d" y="%d" width="%d" height="6" rx="2" fill="%s"/>' % (x - 8, y + h, w + 16, c["edge"]))
    return out


def render(name, c):
    code, clips = laptop(c)
    win = window(c)
    scene = win[1:] + [
        '<rect x="690" y="%d" width="560" height="12" rx="3" fill="%s"/>' % (DESK, c["desk"]),
        '<rect x="690" y="%d" width="560" height="3" fill="%s"/>' % (DESK + 12, c["edge"]),
    ] + plant(c) + code + mug(c) + chess(c)

    svg = """<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Rishabh Sharma, at a desk: a laptop mid-keystroke, a steaming mug, a plant, and a chess game in progress.">
  <style>
    .sans {{ font-family: {SANS}; }}
  </style>
  <defs>
    <pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse">
      <circle cx="2" cy="2" r="1.1" fill="{line}"/>
    </pattern>
    <clipPath id="card"><rect width="{W}" height="{H}" rx="18"/></clipPath>
    {skyclip}
    {clips}
  </defs>
  <g clip-path="url(#card)">
    <rect width="{W}" height="{H}" fill="{bg}"/>
    <rect width="{W}" height="{H}" fill="url(#dots)"/>
  </g>
  <rect x="0.5" y="0.5" width="{W1}" height="{H1}" rx="18" fill="none" stroke="{line}"/>

  <text x="96" y="196" class="sans" font-size="72" font-weight="700" fill="{ink}" letter-spacing="-1.5">Rishabh <tspan font-style="italic" fill="{accent}">Sharma</tspan></text>

  {scene}
</svg>
""".format(W=W, H=H, W1=W - 1, H1=H - 1, SANS=SANS, skyclip=win[0],
           clips="\n    ".join(clips), scene="\n  ".join(scene), **c)
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "banner-%s.svg" % name), "w", encoding="utf-8") as f:
        f.write(svg)


if __name__ == "__main__":
    for name, c in THEMES.items():
        render(name, c)
    print("wrote assets/banner-light.svg, assets/banner-dark.svg")
