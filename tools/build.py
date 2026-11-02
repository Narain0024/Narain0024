import os, random, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib import *
from projects import PROJECTS

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")
os.makedirs(OUT, exist_ok=True)
def save(name, doc):
    open(os.path.join(OUT, name), "w", encoding="utf8").write(doc.render())
    print("wrote", name, round(os.path.getsize(os.path.join(OUT, name))/1024), "KB")

# ------------------------------------------------------------ banner
def banner():
    r = random.Random(11); W, H = 830, 330
    d = Doc(W, H, "Sai Narain, an engineer's field notebook: robotics, electronics and AI-assisted builds",
            "Hand-drawn notebook cover with an ESP32, an Arduino and a small robot")
    d.add(graph_paper(W, H, holes=True), tape(66, -4, 70, 24, -5), tape(W-150, -4, 70, 24, 6))
    d.add(T(92, 62, "~ field notebook, vol. 1 ~", 22, PENCIL, rot=-2))
    d.add(highlighter(r, 150, 100, 330, 56))
    d.add(T(88, 152, "Sai Narain", 78, INK, rot=-2))
    d.add(squig(92, 440, 176, 3.2, 10, draw=7))
    d.add(T(92, 218, "i take things apart", 31, INK, rot=-1.5), T(94, 254, "so i can build weirder ones.", 31, INK, rot=-1.5))
    d.add(T(94, 295, "robotics  /  electronics  /  ai-assisted builds", 20, ORANGE, rot=-1))
    d.add(arrow(r, 436, 76, 420, 108, 10), T(372, 66, "v1.0 (beta)", 19, ORANGE, rot=-4))
    d.add(circle(r, 538, 292, 26, "#b99b6a", 4, "none"), circle(r, 538, 292, 20, "#b99b6a", 2, "none"))
    d.add(arduino(r, 520, 36, -6)); d.add(esp32(r, 548, 176, 7))
    d.add(wire(r, [(522, 100), (500, 150), (545, 205)], ORANGE, 2.6)); d.add(wire(r, [(675, 40), (710, 120), (700, 215)], INK, 2, "5 5"))
    d.add(gear(r, 790, 40, 17, 8, INK, 2, ORANGE_L, spin=16), gear(r, 765, 70, 11, 6, INK, 1.8, spin=-11))
    d.add(sparkle(470, 34, 1.0, 3.1, 0), sparkle(502, 206, .8, 2.6, .9), sparkle(722, 168, .9, 3.4, 1.7), sparkle(806, 122, .7, 2.9, .4), sparkle(430, 296, .7, 3.3, 2.1))
    d.add(mascot(r, 772, 336, 1.25, wave=True, look=-2))
    d.add(bubble(r, 556, 262, 158, 62, ["psst... it", "compiles. mostly."], 15, tail=(736, 300), rot=-3))
    save("banner.svg", d)

# ------------------------------------------------------------ intro page
def intro():
    r = random.Random(5); W, H = 640, 580
    d = Doc(W, H, "Page 01: who's holding this pencil",
            "I take things apart to see how they tick, then build something stranger from the pieces. Arduino and ESP32 on the bench, AI as my pair-programmer, code and hardware talking to each other. Off the bench, I teach kids to build robots.")
    d.add(graph_paper(W, H, holes=True, margin=70), tape(W/2-30, -4, 70, 24, 2))
    d.add(T(96, 62, "page 01 :: who's holding this pencil?", 29, INK, rot=-1), squig(98, 560, 76, 3, 10, draw=9))
    para = ("I take things apart to see how they tick, then build something stranger from the pieces. "
            "Arduino and ESP32 on the bench, AI as my pair-programmer, code and hardware talking to each other. "
            "Off the bench, I teach kids to build robots.")
    y = 124
    for ln in wrap(para, 24, 500):
        d.add(T(96, y, ln, 24, INK)); y += 36
    d.add(highlighter(r, 96 + ARCH.w("I take things apart to see ", 24) - 4, 106, 138, 26, ORANGE, .3))
    y += 22
    for i, (txt, ck) in enumerate([("take it apart", 1), ("put it back together", 1), ("without leftover screws", 0)]):
        yy = y + i*38
        d.add(rect(r, 100, yy-20, 22, 22, INK, 2.2, WHITE))
        if ck: d.add(path(f"M104,{yy-9} l6,8 l13,-20", ORANGE, 3.6))
        d.add(T(136, yy, txt, 23, INK))
    d.add(T(100, y+122, "status: tinkering", 22, ORANGE, rot=-1), squig(100, 250, y+132, 2.6, 9, ORANGE, 2.2, draw=5))
    d.add(f'<circle cx="{100+ARCH.w("status: tinkering", 22)+18:.0f}" cy="{y+114}" r="6" fill="{ORANGE}"><animate attributeName="opacity" values="1;.2;1" dur="1.4s" repeatCount="indefinite"/></circle>', T(100, y+160, "(works on my bench. usually.)", 19, PENCIL, rot=-1))
    d.add(mascot(r, 556, 566, 1.3, look=3))
    d.add(bubble(r, 372, y-4, 158, 48, ["whatcha building?"], 18, tail=(520, y+66), rot=-2))
    save("page-01-intro.svg", d)

# ------------------------------------------------------------ section headers
def header(fn, title, note, ic, seed, accent_note=""):
    r = random.Random(seed); W, H = 640, 96
    d = Doc(W, H, title, note)
    d.add(graph_paper(W, H), icon(r, ic, 56, 42))
    d.add(highlighter(r, 104, 34, ARCH.w(title, 40) - 6, 24, ORANGE, .3), T(100, 56, title, 40, INK, rot=-1))
    d.add(T(W-24, 30, note, 17, PENCIL, "end", rot=2))
    d.add(circuit_line(r, 100, W-24, 84))
    save(fn, d)

# ------------------------------------------------------------ parts bin
BINS = [
    ("Robotics & Electronics", ["Arduino", "ESP32", "Sensors", "Motors", "Embedded Systems", "ROS2", "Gazebo", "Tinkercad", "Computer Vision", "OpenCV"], 600),
    ("CAD & Mechanical", ["SolidWorks", "CATIA", "CAD/CAM"], 600),
    ("Programming", ["Python", "SQL", "MySQL", "Git", "Linux", "VS Code"], 600),
    ("AI & Development", ["AI Tools", "Prompt Engineering", "AI-Assisted Development", "OpenAI API", "LangChain", "Hugging Face", "scikit-learn", "YOLOv8"], 600),
    ("Data & Analytics", ["Excel", "Power BI", "EDA", "Pandas", "NumPy", "Matplotlib", "Seaborn", "Jupyter"], 330),
]
def parts_bin():
    r = random.Random(23); W = 640; size = 19
    y, drawers = 28, []
    for name, items, dw in BINS:
        x0, rows, cx, cy = 20, [], 0, 0
        inner = dw - 44; row = []; rw = 0
        for it in items:
            w = ARCH.w(it, size) + 26
            if rw + w > inner and row: rows.append(row); row, rw = [], 0
            row.append((it, w)); rw += w + 10
        rows.append(row)
        h = 58 + len(rows)*44 + 14
        drawers.append((name, rows, dw, y, h)); y += h + 22
    H = y + 6
    d = Doc(W, H, "The parts bin: skills sorted into labelled drawers",
            "; ".join(f"{n}: {', '.join(i)}" for n, i, _ in BINS))
    d.add(graph_paper(W, H))
    for k, (name, rows, dw, y0, h) in enumerate(drawers):
        small = dw < 500; x0 = 20 + (230 if small else 0)
        d.add(f'<rect x="{x0+5}" y="{y0+6}" width="{dw}" height="{h}" fill="#000" opacity=".08"/>')
        d.add(rect(r, x0, y0, dw, h, INK, 2.6, "#f1e6c8", 1.4))
        d.add(rect(r, x0+14, y0+12, ARCH.w(name, 22)+30, 34, INK, 1.8, WHITE) + T(x0+29, y0+36, name, 22, INK))
        hx = x0 + dw - 78
        d.add(rect(r, hx, y0+14, 56, 12, INK, 2.2, ORANGE_L))
        if small: d.add(T(x0-14, y0+h-14, "side quest drawer", 18, ORANGE, "end", rot=-4), arrow(r, x0-8, y0+h-24, x0+4, y0+h-40, -10))
        for ri, row in enumerate(rows):
            tx = x0 + 22
            for it, w in row:
                ty = y0 + 62 + ri*44
                hot = it in ("Arduino", "ESP32", "AI-Assisted Development")
                tilt = r.uniform(-1.6, 1.6)
                wig = (f'<animateTransform attributeName="transform" type="rotate" values="-1.6 {tx+w/2:.0f} {ty+17};1.6 {tx+w/2:.0f} {ty+17};-1.6 {tx+w/2:.0f} {ty+17}" dur="{2.6+(len(it)%3)*.4}s" repeatCount="indefinite"/>' if hot else "")
                d.add(f'<g transform="rotate({tilt:.1f} {tx+w/2} {ty+17})"><g>' + rect(r, tx, ty, w, 34, ORANGE if hot else INK, 2, ORANGE_L if hot else WHITE, .9, 2)
                      + T(tx+13, ty+24, it, size, INK) + wig + "</g></g>")
                tx += w + 10
    save("parts-bin.svg", d)

# ------------------------------------------------------------ project pages
def doodle(r, kind, x, y):
    g = f'<g transform="translate({x} {y})">'
    if kind == "prompts":
        g += bubble(r, 6, 6, 120, 52, ["write a prompt"], 15, tail=(30, 76), rot=-2)
        g += bubble(r, 150, 40, 120, 52, ["tweak it. again."], 15, tail=(250, 108), rot=2)
        g += gear(r, 312, 38, 20, 8, INK, 2.2, ORANGE_L, spin=14) + arrow(r, 120, 80, 160, 100, 10, ORANGE, 2)
    elif kind == "finance":
        for i, h in enumerate([26, 40, 34, 58, 72]):
            g += rect(r, 20+i*34, 100-h, 24, h, INK, 2, ORANGE_L if i == 4 else WHITE, .9, 2)
        g += ('<path d="M18,70 L56,52 L92,60 L128,34 L172,10" fill="none" stroke="%s" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" pathLength="1" stroke-dasharray="1 1">'
              '<animate attributeName="stroke-dashoffset" values="1;0;0;1" keyTimes="0;.3;.85;1" dur="5s" repeatCount="indefinite"/></path>' % ORANGE)
        g += ('<g>' + arrow(r, 150, 20, 176, 8, 4, ORANGE, 2.6) + '<animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;.28;.36;.85;1" dur="5s" repeatCount="indefinite"/></g>')
        g += circle(r, 280, 52, 32, INK, 2.4, ORANGE_L) + T(280, 64, "$", 34, INK, "middle")
    elif kind == "esp32":
        g += esp32(r, 40, 20, -4, 1.45) + wire(r, [(10, 20), (20, 80), (50, 100)], ORANGE, 2.4)
    elif kind == "arduino":
        g += arduino(r, 50, 6, 3, 1.25)
    elif kind == "robot":
        g += mascot(r, 170, 118, 1.0, wave=True)
    elif kind == "gear":
        g += gear(r, 120, 56, 44, 10, INK, 2.4, ORANGE_L, spin=22) + gear(r, 200, 80, 26, 8, INK, 2.2, spin=-14)
    elif kind == "chart":
        g += "".join(rect(r, 40+i*40, 100-h, 28, h, INK, 2, WHITE) for i, h in enumerate([30, 55, 40, 75]))
    return g + "</g>"

def project_page(p, idx):
    r = random.Random(100+idx); W, H = 400, 350
    d = Doc(W, H, f"Notebook page: {p['name']}", f"{p['blurb']} Tech: {', '.join(p['stack'])}. Repo: {p['repo']}")
    tilt = p["tilt"]
    d.add(f'<g transform="rotate({tilt} 200 175)"><animateTransform attributeName="transform" type="rotate" values="{tilt-.7:.2f} 200 175;{tilt+.7:.2f} 200 175;{tilt-.7:.2f} 200 175" dur="{6+idx*1.3:.1f}s" repeatCount="indefinite"/>')
    d.add(f'<path d="M24,22 H380 V318 {" ".join(f"L{380-i*18:.0f},{318+r.uniform(0,9):.1f}" for i in range(1, 20))} L24,320 Z" fill="#000" opacity=".1" transform="translate(5 6)"/>')
    d.add(f'<path d="M20,18 H376 V314 {" ".join(f"L{376-i*18:.0f},{314+r.uniform(0,9):.1f}" for i in range(1, 20))} L20,316 Z" fill="{PAPER}" stroke="{PENCIL}" stroke-width="1.2"/>')
    grid = "".join(f"M20,{y}H376" for y in range(42, 312, 24)) 
    d.add(f'<path d="{grid}" stroke="{GRID}" stroke-width=".9" opacity=".7"/>', tape(166, 8, 66, 22, -3))
    d.add(rect(r, 40, 40, 316, 108, PENCIL, 1.4, WHITE, 1.2) + T(46, 36, "fig. 1", 15, PENCIL, rot=-2))
    d.add(doodle(r, p["doodle"], 40, 40))
    d.add(T(40, 186, p["name"], 29 if len(p["name"]) < 14 else 25, INK, rot=-.8), highlighter(r, 40, 192, min(ARCH.w(p["name"], 27), 320), 8, ORANGE, .45))
    y = 218
    for ln in wrap(p["blurb"], 16.5, 316)[:3]:
        d.add(T(40, y, ln, 16.5, INK)); y += 22
    d.add(T(40, 292, "BOM:", 14, ORANGE, cls="m"))
    tx = 90
    for s in p["stack"]:
        w = ARCH.w(s, 14.5) + 16
        if tx + w > 360: break
        d.add(rect(r, tx, 275, w, 23, INK, 1.4, ORANGE_L, .8, 1.5) + T(tx+8, 292, s, 14.5, INK)); tx += w + 8
    d.add(T(356, 308, "repo >>", 16, ORANGE, "end", rot=-2))
    d.add("</g>")
    save(f"page-{p['slug']}.svg", d)

def wip_page():
    r = random.Random(77); W, H = 400, 350
    d = Doc(W, H, "Notebook page being written: bench builds with Arduino, ESP32 and robots land here soon")
    d.add(f'<g transform="rotate(-1 200 175)">')
    d.add(f'<path d="M24,22 H380 V318 H24Z" fill="#000" opacity=".08" transform="translate(5 6)"/><rect x="20" y="18" width="356" height="296" fill="{PAPER}" stroke="{PENCIL}" stroke-width="1.4" stroke-dasharray="9 7"/>')
    d.add(f'<path d="{"".join(f"M20,{y}H376" for y in range(42, 312, 24))}" stroke="{GRID}" stroke-width=".9" opacity=".7"/>', tape(166, 8, 66, 22, 3))
    d.add(f'<g opacity=".8" stroke-dasharray="6 5"><animate attributeName="stroke-dashoffset" values="0;-11" dur="1.2s" repeatCount="indefinite"/>' + esp32(r, 72, 62, -3, 1.4).replace('stroke-width="2.4"', 'stroke-width="1.8"') + "</g>")
    d.add('<g>' + T(200, 56, "?", 56, ORANGE, "middle", rot=8) + '<animateTransform attributeName="transform" type="translate" values="0 0;0 -5;0 0" dur="2.2s" repeatCount="indefinite"/></g>',
          '<g>' + T(338, 150, "?", 40, ORANGE, "middle", rot=-10) + '<animateTransform attributeName="transform" type="translate" values="0 0;0 -4;0 0" dur="2.8s" begin=".6s" repeatCount="indefinite"/></g>')
    d.add(T(40, 232, "page 03 :: being written", 27, INK, rot=-1), highlighter(r, 40, 238, 240, 8, ORANGE, .45))
    d.add(T(40, 266, "bench builds (Arduino, ESP32, robots)", 16.5, INK), T(40, 288, "get taped in here soon.", 16.5, INK))
    d.add('<g>' + rect(r, 270, 168, 90, 34, ORANGE, 2.4) + T(315, 192, "WIP", 24, ORANGE, "middle", rot=-6)
          + '<animateTransform attributeName="transform" type="rotate" values="-3 315 185;3 315 185;-3 315 185" dur="2.4s" repeatCount="indefinite"/></g>')
    d.add("</g>")
    save("page-next.svg", d)

# ------------------------------------------------------------ stickers
def sticker(fn, label, seed, tilt, fill):
    r = random.Random(seed); W, H = 152, 64
    d = Doc(W, H, label)
    d.add(f'<g transform="rotate({tilt} 76 32)"><rect x="9" y="12" width="136" height="42" fill="#000" opacity=".1" transform="translate(3 4)"/>')
    d.add(rect(r, 8, 10, 136, 42, INK, 2.4, fill, 1.2) + T(76, 39, label, 21 if len(label) < 11 else 18, INK, "middle"))
    d.add("</g>"); save(fn, d)

# ------------------------------------------------------------ footer
def footer():
    r = random.Random(41); W, H = 640, 420
    d = Doc(W, H, "Serial monitor output: notebook loaded, still tinkering. Thanks for flipping through.",
            "Serial.begin(115200); sensors: curiosity OK; bugs: some, features: also some; status: still tinkering")
    d.add(graph_paper(W, H), tape(W/2-34, -4, 68, 24, -2))
    d.add(f'<rect x="45" y="50" width="560" height="238" fill="#000" opacity=".12"/>')
    d.add(rect(r, 40, 44, 560, 238, INK, 3, DARK, 1.4))
    d.add(f'<rect x="42" y="46" width="556" height="30" fill="#2c2c30"/>' + "".join(f'<circle cx="{62+i*22}" cy="61" r="6" fill="{c}"/>' for i, c in enumerate([ORANGE, "#c9c2ad", "#8a8577"])))
    d.add(T(330, 66, "Serial Monitor  -  115200 baud", 14, "#a9a9a9", "middle", cls="m"))
    lines = [("> Serial.begin(115200);", "#f0e9d6"), ("> notebook loaded ............ OK", "#f0e9d6"), ("> sensors: curiosity ......... OK", "#f0e9d6"),
             ("> bugs: some. features: also some.", "#f0e9d6"), ("> status: still tinkering", ORANGE)]
    dur = 11.0
    for i, (t, c) in enumerate(lines):
        on = (0.6 + i*1.1) / dur
        kt = f"0;{on:.3f};{on+.02:.3f};.9;.95;1"
        d.add(f'<g>' + T(64, 112+i*36, t, 17, c, cls="m") + f'<animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="{kt}" dur="{dur}s" repeatCount="indefinite"/></g>')
    on = (0.6 + 4*1.1 + .7) / dur
    d.add(f'<g><rect x="{64+MONO.w("> status: still tinkering", 17)+6:.0f}" y="{112+4*36-16}" width="10" height="20" fill="{ORANGE}">'
          f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;.5;.5;1" dur="1.1s" repeatCount="indefinite"/></rect>'
          f'<animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="0;{on:.3f};{on+.02:.3f};.9;.95;1" dur="{dur}s" repeatCount="indefinite"/></g>')
    d.add(T(60, 346, "~ Sai Narain", 46, ORANGE, rot=-4), squig(62, 280, 358, 3, 11, INK, 2))
    d.add(T(60, 392, "thanks for flipping through. go build something.", 21, INK, rot=-1))
    d.add(mascot(r, 566, 410, 1.0, wave=True, look=-3))
    save("footer.svg", d)

if __name__ == "__main__":
    banner(); intro(); parts_bin(); footer()
    header("hdr-parts-bin.svg", "the parts bin", "p.02 // skills, sorted", "drawer", 2)
    header("hdr-experiments.svg", "experiments", "p.03 // things that exist", "bulb", 3)
    header("hdr-side-notebook.svg", "side notebook", "p.04 // numbers, kept small", "chart", 4)
    header("hdr-building.svg", "currently building", "p.05 // wip, always", "pencil", 5)
    header("hdr-teaching.svg", "teaching corner", "p.06 // show and tell", "robot", 6)
    for i, p in enumerate(PROJECTS): project_page(p, i)
    wip_page()
    sticker("link-linkedin.svg", "LinkedIn", 1, -3, ORANGE_L); sticker("link-kaggle.svg", "Kaggle", 2, 2, WHITE)
    sticker("link-huggingface.svg", "Hugging Face", 3, -2, ORANGE_L); sticker("link-email.svg", "Email me", 4, 3, WHITE)
