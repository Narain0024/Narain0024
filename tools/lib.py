"""Tiny hand-drawn-SVG toolkit used by build.py (no third-party deps besides fontTools for text measuring)."""
import base64, html, math, os, random
from fontTools.ttLib import TTFont

HERE = os.path.dirname(os.path.abspath(__file__))
PAPER, GRID, INK, PENCIL = "#f6f0e0", "#c4d2dc", "#2b2b2b", "#6b6b6b"
ORANGE, ORANGE_L, WHITE, TAPE = "#ff6a13", "#ffd9bb", "#fffaf0", "#e9dcb8"
DARK = "#1d1d1f"

# ---------- fonts ----------
def _b64(name):
    return base64.b64encode(open(os.path.join(HERE, "fonts", name), "rb").read()).decode()

FONT_CSS = (
    "@font-face{font-family:'ArchD';src:url(data:font/woff2;base64,%s) format('woff2');}"
    "@font-face{font-family:'PlexM';src:url(data:font/woff2;base64,%s) format('woff2');}"
    ".h{font-family:'ArchD','Segoe Print','Bradley Hand','Comic Sans MS',cursive}"
    ".m{font-family:'PlexM','Courier New',monospace}"
) % (_b64("architects-daughter-latin-400-normal.woff2"), _b64("ibm-plex-mono-latin-400-normal.woff2"))

class Metric:
    def __init__(self, fn):
        f = TTFont(os.path.join(HERE, "fonts", fn))
        self.cm, self.hm, self.upm = f.getBestCmap(), f["hmtx"], f["head"].unitsPerEm
    def w(self, t, size):
        sp = self.cm.get(32)
        return sum(self.hm[self.cm.get(ord(c), sp)][0] for c in t) * size / self.upm

ARCH = Metric("architects-daughter-latin-400-normal.woff")
MONO = Metric("ibm-plex-mono-latin-400-normal.woff")

def wrap(text, size, maxw, metric=ARCH):
    lines, cur = [], ""
    for word in text.split():
        t = (cur + " " + word).strip()
        if metric.w(t, size) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur); cur = word
    if cur: lines.append(cur)
    return lines

# ---------- primitives ----------
def path(d, stroke=INK, sw=2.2, fill="none", extra=""):
    return (f'<path d="{d}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" '
            f'stroke-linecap="round" stroke-linejoin="round" {extra}/>')

def jl(r, x1, y1, x2, y2, j=1.2):
    u = r.uniform
    return (f"M{x1+u(-j,j):.1f},{y1+u(-j,j):.1f} Q{(x1+x2)/2+u(-j,j):.1f},{(y1+y2)/2+u(-j,j):.1f} "
            f"{x2+u(-j,j):.1f},{y2+u(-j,j):.1f}")

def line(r, x1, y1, x2, y2, stroke=INK, sw=2.2, j=1.1):
    return path(jl(r, x1, y1, x2, y2, j), stroke, sw) + path(jl(r, x1, y1, x2, y2, j), stroke, sw * .5, extra='opacity=".55"')

def rect(r, x, y, w, h, stroke=INK, sw=2.2, fill=None, j=1.1, o=3):
    out = []
    if fill: out.append(f'<path d="M{x:.1f},{y:.1f}h{w:.1f}v{h:.1f}h{-w:.1f}z" fill="{fill}"/>')
    for a, b, c, d in [(x-o, y, x+w+o, y), (x+w, y-o, x+w, y+h+o), (x+w+o, y+h, x-o, y+h), (x, y+h+o, x, y-o)]:
        out.append(path(jl(r, a, b, c, d, j), stroke, sw))
    return "".join(out)

def blob_d(r, cx, cy, rx, ry, n=9, j=1.4):
    pts = []
    for i in range(n):
        a = 2*math.pi*i/n + r.uniform(-.1, .1)
        pts.append((cx+rx*math.cos(a)+r.uniform(-j, j), cy+ry*math.sin(a)+r.uniform(-j, j)))
    mids = [((pts[i][0]+pts[(i+1) % n][0])/2, (pts[i][1]+pts[(i+1) % n][1])/2) for i in range(n)]
    d = f"M{mids[-1][0]:.1f},{mids[-1][1]:.1f} "
    for i in range(n): d += f"Q{pts[i][0]:.1f},{pts[i][1]:.1f} {mids[i][0]:.1f},{mids[i][1]:.1f} "
    return d + "Z"

def circle(r, cx, cy, rad, stroke=INK, sw=2.2, fill="none"):
    return path(blob_d(r, cx, cy, rad, rad, 8, rad*.06), stroke, sw, fill)

def squig(x1, x2, y, amp=3, step=9, stroke=ORANGE, sw=2.6):
    d, x, up = f"M{x1},{y} ", x1, True
    while x < x2:
        d += f"Q{x+step/2:.1f},{y+(-amp if up else amp):.1f} {x+step:.1f},{y} "; x += step; up = not up
    return path(d, stroke, sw)

def arrow(r, x1, y1, x2, y2, bend=18, stroke=ORANGE, sw=2.4):
    dx, dy = x2-x1, y2-y1; L = math.hypot(dx, dy) or 1
    cx, cy = (x1+x2)/2 - dy/L*bend, (y1+y2)/2 + dx/L*bend
    tx, ty = x2-cx, y2-cy; tl = math.hypot(tx, ty) or 1; tx /= tl; ty /= tl
    def rot(a): return (-tx*math.cos(a)+ty*math.sin(a), -tx*math.sin(a)-ty*math.cos(a))
    h1, h2 = rot(math.radians(28)), rot(math.radians(-28))
    d = f"M{x1:.1f},{y1:.1f} Q{cx:.1f},{cy:.1f} {x2:.1f},{y2:.1f}"
    d += f" M{x2:.1f},{y2:.1f} l{h1[0]*11:.1f},{h1[1]*11:.1f} M{x2:.1f},{y2:.1f} l{h2[0]*11:.1f},{h2[1]*11:.1f}"
    return path(d, stroke, sw)

def T(x, y, s, size=22, fill=INK, anchor="start", rot=0, cls="h", extra=""):
    tr = f' transform="rotate({rot} {x} {y})"' if rot else ""
    return (f'<text x="{x}" y="{y}" class="{cls}" font-size="{size}" fill="{fill}" '
            f'text-anchor="{anchor}"{tr} {extra}>{html.escape(s)}</text>')

def highlighter(r, x, y, w, h, color=ORANGE, op=.38):
    return f'<path d="{blob_d(r, x+w/2, y+h/2, w/2+4, h/2, 10, 2.2)}" fill="{color}" opacity="{op}"/>'

def gear(r, cx, cy, rad, teeth=8, stroke=INK, sw=2.2, fill="none", spin=0):
    pts = []
    for i in range(teeth*2):
        a = math.pi*i/teeth; rr = rad if i % 2 == 0 else rad*.76
        for da in (-.12, .12) if i % 2 == 0 else (-.1, .1):
            pts.append((cx+rr*math.cos(a+da)+r.uniform(-.6, .6), cy+rr*math.sin(a+da)+r.uniform(-.6, .6)))
    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + "Z"
    out = path(d, stroke, sw, fill) + circle(r, cx, cy, rad*.3, stroke, sw*.8)
    if spin:
        out = (f'<g>{out}<animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" '
               f'to="{360 if spin > 0 else -360} {cx} {cy}" dur="{abs(spin)}s" repeatCount="indefinite"/></g>')
    return out

def tape(x, y, w=64, h=22, rot=-4):
    return (f'<g transform="rotate({rot} {x+w/2} {y+h/2})"><rect x="{x}" y="{y}" width="{w}" height="{h}" '
            f'fill="{TAPE}" opacity=".85"/><path d="M{x},{y}l-3,3l3,3l-3,3l3,3l-3,3l3,4M{x+w},{y}l3,3l-3,3l3,3l-3,3l3,3l-3,4" '
            f'stroke="{TAPE}" stroke-width="1.5" fill="none" opacity=".85"/></g>')

def graph_paper(w, h, holes=False, margin=None, step=24):
    d = ""
    for x in range(0, w+1, step): d += f"M{x},0V{h}"
    for y in range(0, h+1, step): d += f"M0,{y}H{w}"
    s = f'<rect width="{w}" height="{h}" fill="{PAPER}"/>'
    s += f'<path d="{d}" stroke="{GRID}" stroke-width=".9" opacity=".6"/>'
    if margin: s += f'<path d="M{margin},0V{h}" stroke="{ORANGE}" stroke-width="1.6" opacity=".55"/>'
    if holes:
        for y in range(34, h-10, 46):
            s += f'<circle cx="26" cy="{y}" r="8" fill="{DARK}" opacity=".85"/><circle cx="26" cy="{y}" r="11" fill="none" stroke="{PENCIL}" stroke-width="1.4" opacity=".6"/>'
    return s

class Doc:
    def __init__(self, w, h, title, desc=""):
        self.w, self.h, self.title, self.desc, self.parts = w, h, title, desc, []
    def add(self, *s): self.parts.extend(s); return self
    def render(self):
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" width="{self.w}" height="{self.h}" '
                f'role="img" aria-label="{html.escape(self.title)}"><title>{html.escape(self.title)}</title>'
                + (f'<desc>{html.escape(self.desc)}</desc>' if self.desc else "")
                + f'<style>{FONT_CSS}</style>' + "".join(self.parts) + "</svg>")

# ---------- characters & components ----------
def mascot(r, x, y, s=1.0, wave=False, look=0, face="smile"):
    o = []
    o.append(circle(r, -16, -8, 8, INK, 2.4, WHITE) + circle(r, 16, -8, 8, INK, 2.4, WHITE))
    o.append(rect(r, -22, -54, 44, 38, INK, 2.5, WHITE))
    o.append(rect(r, -9, -44, 18, 14, INK, 1.8, ORANGE_L) + f'<circle cx="0" cy="-37" r="3" fill="{ORANGE}"/>')
    o.append(line(r, -22, -46, -38, -30, INK, 2.4))
    if wave:
        o.append('<g>' + line(r, 22, -46, 38, -66, INK, 2.4) + circle(r, 40, -70, 5, INK, 2.2, WHITE)
                 + '<animateTransform attributeName="transform" type="rotate" values="-8 22 -46;14 22 -46;-8 22 -46" keyTimes="0;.5;1" dur="1.6s" repeatCount="indefinite"/></g>')
    else:
        o.append(line(r, 22, -46, 38, -30, INK, 2.4))
    o.append(rect(r, -30, -102, 60, 46, INK, 2.6, WHITE))
    o.append(line(r, -34, -86, -34, -72, INK, 3) + line(r, 34, -86, 34, -72, INK, 3))
    for ex in (-12, 12):
        o.append(circle(r, ex, -82, 7.5, INK, 2.2, WHITE) + f'<circle cx="{ex+look}" cy="-81" r="3" fill="{INK}"/>')
    if face == "smile": o.append(path("M-10,-67 Q0,-60 10,-67", INK, 2.4))
    elif face == "oh": o.append(circle(r, 0, -65, 3.5, INK, 2))
    else: o.append(path("M-9,-65 L-4,-68 L1,-64 L6,-68 L10,-65", INK, 2.2))
    o.append(line(r, 0, -102, 0, -116, INK, 2.4)
             + '<g>' + circle(r, 0, -121, 5.5, INK, 2, ORANGE) + '<animate attributeName="opacity" values="1;.3;1" dur="2.4s" repeatCount="indefinite"/></g>')
    bob = '<animateTransform attributeName="transform" type="translate" values="0 0;0 -3;0 0" dur="2.6s" repeatCount="indefinite"/>'
    return f'<g transform="translate({x} {y}) scale({s})"><g>' + "".join(o) + bob + '</g></g>'

def bubble(r, x, y, w, h, lines, size=18, tail=(0, 0), thought=False, rot=0):
    cx, cy = x + w/2, y + h/2
    s = f'<g transform="rotate({rot} {cx} {cy})">'
    s += f'<path d="{blob_d(r, cx, cy, w/2, h/2, 12, 1.6)}" fill="{WHITE}" stroke="{INK}" stroke-width="2.1"/>'
    if thought:
        s += circle(r, tail[0], tail[1], 5, INK, 1.8, WHITE) + circle(r, (tail[0]+cx)/2, (tail[1]+cy)/2+10, 3, INK, 1.6, WHITE)
    else:
        bx = min(max(tail[0], x+14), x+w-14)
        s += f'<path d="M{bx-9:.1f},{cy+h/2-3:.1f} L{tail[0]},{tail[1]} L{bx+9:.1f},{cy+h/2-4:.1f}" fill="{WHITE}" stroke="{INK}" stroke-width="2.1" stroke-linejoin="round"/>'
        s += f'<path d="M{bx-8:.1f},{cy+h/2-4:.1f} L{bx+8:.1f},{cy+h/2-5:.1f}" stroke="{WHITE}" stroke-width="4"/>'
    ty = cy - (len(lines)-1)*size*.55 + size*.33
    for i, ln in enumerate(lines):
        s += T(cx, f"{ty+i*size*1.1:.1f}", ln, size, INK, "middle")
    return s + "</g>"

def esp32(r, x, y, rot=0, s=1.0):
    o = [rect(r, 0, 0, 150, 62, INK, 2.4, "#fffdf6")]
    o.append(rect(r, 104, 6, 40, 50, INK, 1.8, "#efe7d0"))
    o.append(path("M110,14 h26 v7 h-26 v7 h26 v7 h-26 v7 h26 v7", ORANGE, 2))
    o.append(rect(r, 34, 14, 46, 34, INK, 2, "#dcdcdc") + T(57, 36, "ESP32", 14, INK, "middle", cls="m"))
    o.append(rect(r, -8, 20, 20, 22, INK, 2, "#cfcfcf"))
    for i in range(14):
        px = 14 + i*8.2
        o.append(f'<circle cx="{px:.1f}" cy="5" r="2" fill="{INK}"/><circle cx="{px:.1f}" cy="57" r="2" fill="{INK}"/>')
    o.append(rect(r, 18, 40, 9, 9, INK, 1.6, ORANGE_L) + f'<circle cx="94" cy="44" r="3.4" fill="{ORANGE}"><animate attributeName="opacity" values="1;.2;1" dur="1.8s" repeatCount="indefinite"/></circle>')
    return f'<g transform="translate({x} {y}) rotate({rot}) scale({s})">' + "".join(o) + "</g>"

def arduino(r, x, y, rot=0, s=1.0):
    o = [rect(r, 0, 0, 150, 104, INK, 2.4, "#f3f9f9")]
    o.append(rect(r, -10, 12, 36, 32, INK, 2, "#cfcfcf") + rect(r, -8, 62, 26, 22, INK, 2, "#222"))
    o.append(rect(r, 62, 38, 56, 18, INK, 2, "#2e2e2e"))
    for i in range(8):
        o.append(f'<path d="M{66+i*7},38v-5M{66+i*7},56v5" stroke="{INK}" stroke-width="1.6"/>')
    o.append(circle(r, 42, 74, 7, INK, 2, ORANGE) + circle(r, 108, 76, 12, INK, 2, "none"))
    o.append(path("M100,76c0-6,6-6,8,0s8,6,8,0", INK, 1.8))
    for i in range(10):
        o.append(f'<rect x="{40+i*9}" y="6" width="6" height="8" fill="{INK}"/><rect x="{40+i*9}" y="90" width="6" height="8" fill="{INK}"/>')
    o.append(T(75, 28, "UNO", 13, ORANGE, "middle", cls="m"))
    return f'<g transform="translate({x} {y}) rotate({rot}) scale({s})">' + "".join(o) + "</g>"

def wire(r, pts, stroke=ORANGE, sw=2.6, dash=""):
    d = f"M{pts[0][0]},{pts[0][1]} "
    for i in range(1, len(pts)):
        px, py = pts[i-1]; qx, qy = pts[i]
        d += f"Q{(px+qx)/2+r.uniform(-6,6):.1f},{(py+qy)/2+r.uniform(-6,6):.1f} {qx},{qy} "
    ex = f'stroke-dasharray="{dash}"' if dash else ""
    return path(d, stroke, sw, extra=ex) + f'<circle cx="{pts[0][0]}" cy="{pts[0][1]}" r="4" fill="{stroke}"/><circle cx="{pts[-1][0]}" cy="{pts[-1][1]}" r="4" fill="{stroke}"/>'

def circuit_line(r, x0, x1, y, stroke=ORANGE):
    """horizontal wire with resistor, capacitor and LED sprinkled in"""
    span = x1 - x0; a, b, c = x0 + span*.22, x0 + span*.52, x0 + span*.78
    s = line(r, x0, y, a, y, stroke, 2.4)
    s += path(f"M{a},{y} l6,-10 l10,20 l10,-20 l10,20 l10,-20 l6,10", stroke, 2.4)
    s += line(r, a+52, y, b-6, y, stroke, 2.4)
    s += line(r, b-6, y-12, b-6, y+12, stroke, 2.8) + line(r, b+6, y-12, b+6, y+12, stroke, 2.8)
    s += line(r, b+6, y, c-10, y, stroke, 2.4)
    s += path(f"M{c-10},{y-10} L{c+8},{y} L{c-10},{y+10}Z", stroke, 2.2, WHITE) + line(r, c+10, y-10, c+10, y+10, stroke, 2.6)
    s += line(r, c+10, y, x1, y, stroke, 2.4)
    s += f'<circle cx="{x0}" cy="{y}" r="4.5" fill="{stroke}"/><circle cx="{x1}" cy="{y}" r="4.5" fill="{stroke}"/>'
    s += (f'<circle cy="{y}" r="3.6" fill="{WHITE}" stroke="{stroke}" stroke-width="1.6"><animate attributeName="cx" values="{x0};{x1}" dur="4s" repeatCount="indefinite"/>'
          f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.08;.92;1" dur="4s" repeatCount="indefinite"/></circle>')
    return s

def icon(r, kind, x, y):
    g = f'<g transform="translate({x} {y})">'
    if kind == "drawer":
        g += rect(r, -22, -16, 44, 32, INK, 2.2, WHITE) + rect(r, -8, -4, 16, 7, ORANGE, 2.2, ORANGE_L)
    elif kind == "bulb":
        g += circle(r, 0, -6, 14, INK, 2.2, ORANGE_L) + rect(r, -6, 8, 12, 9, INK, 2, WHITE)
        g += "".join(line(r, a*20, -6 + b*20, a*28, -6 + b*28, ORANGE, 2.2) for a, b in [(0, -1), (-.8, -.7), (.8, -.7), (-1, 0), (1, 0)])
    elif kind == "chart":
        g += "".join(rect(r, -20+i*14, 14-h, 10, h, INK, 2, ORANGE_L if i == 1 else WHITE) for i, h in enumerate([14, 28, 20]))
    elif kind == "pencil":
        g += f'<g transform="rotate(-40)">' + rect(r, -6, -26, 12, 42, INK, 2.2, ORANGE_L) + path("M-6,16 L0,28 L6,16", INK, 2.2, WHITE) + line(r, -6, -18, 6, -18, INK, 2) + "</g>"
    elif kind == "robot":
        g += f'<g transform="translate(0 26)">' + mascot(r, 0, 0, .52) + "</g>"
    return g + "</g>"
