"""Reel 15 s — Cabra Negra × influencers.

uv run --with numpy --with pillow --with imageio-ffmpeg python build.py
Sale en salida/cabra_negra_influencers.mp4 (1080x1920, 30 fps).
"""

import math
import subprocess
import wave
from pathlib import Path

import imageio_ffmpeg
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

FF = imageio_ffmpeg.get_ffmpeg_exe()
RAIZ = Path(__file__).parent
FOTOS = RAIZ / "fuentes/fotos"
VIDEOS = RAIZ / "fuentes/videos"
ASSETS = Path.home() / "Documents/Cabra_Negra/sitio/assets"
FUENTES = Path.home() / "Documents/Cabra_Negra/sitio/cotizacion/fuentes"
SALIDA = RAIZ / "salida"
SALIDA.mkdir(exist_ok=True)

W, H, FPS = 1080, 1920, 30
DUR = 15.0
N = int(DUR * FPS)

# Paleta oficial (catálogo 2026)
CARBON = (12, 16, 19)
BRASA = (200, 121, 47)
ASCUA = (248, 156, 60)
BLANCO = (255, 255, 255)

F_BOLD = str(FUENTES / "Outfit-Bold.ttf")
F_SEMI = str(FUENTES / "Outfit-SemiBold.ttf")


def fuente(ruta, tam):
    return ImageFont.truetype(ruta, tam)


# ---------------------------------------------------------------- easing
def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def out_cubic(x):
    x = clamp(x)
    return 1 - (1 - x) ** 3


def in_out_cubic(x):
    x = clamp(x)
    return 4 * x**3 if x < 0.5 else 1 - (-2 * x + 2) ** 3 / 2


def out_back(x, s=1.6):
    x = clamp(x)
    return 1 + (s + 1) * (x - 1) ** 3 + s * (x - 1) ** 2


# ---------------------------------------------------------------- fuentes de imagen
def cargar_foto(nombre, crop=None, modo="cover"):
    im = Image.open(FOTOS / nombre).convert("RGB")
    if crop:
        im = im.crop(crop)
    if modo == "contain":
        # fondo desenfocado + foto completa encima
        fondo = cubrir(im, 1.0, 0.5, 0.5).filter(ImageFilter.GaussianBlur(40))
        fondo = Image.blend(fondo, Image.new("RGB", (W, H), CARBON), 0.45)
        k = W / im.width
        fg = im.resize((W, round(im.height * k)), Image.LANCZOS)
        fondo.paste(fg, (0, (H - fg.height) // 2))
        return fondo
    return im


def cubrir(im, zoom, cx, cy):
    """Recorta im a 9:16 (cover) con zoom alrededor de (cx, cy) relativos."""
    w, h = im.size
    k = max(W / w, H / h) * zoom
    bw, bh = W / k, H / k
    x0 = clamp(cx * w - bw / 2, 0, w - bw)
    y0 = clamp(cy * h - bh / 2, 0, h - bh)
    return im.resize((W, H), Image.BICUBIC, box=(x0, y0, x0 + bw, y0 + bh))


def decodificar(video, t0, dur, crop=None):
    """Frames de un tramo de video como lista de PIL (resolución de origen)."""
    vf = []
    if crop:
        x, y, cw, ch = crop
        vf.append(f"crop={cw}:{ch}:{x}:{y}")
    vf.append("fps=30")
    filtro = ",".join(vf)
    sonda = subprocess.run(
        [FF, "-v", "error", "-ss", str(t0), "-i", str(VIDEOS / video), "-t", str(dur),
         "-vf", filtro + ",scale=iw:ih", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
        capture_output=True, check=True,
    ).stdout
    cw, ch = (crop[2], crop[3]) if crop else (576, 1024)
    tam = cw * ch * 3
    return [
        Image.frombytes("RGB", (cw, ch), sonda[i : i + tam])
        for i in range(0, len(sonda) - tam + 1, tam)
    ]


# ---------------------------------------------------------------- guion
# Tarjeta de story de IG (lobogrill_, brass.mx, elguayabo.mx): recorte al interior
TARJETA = (58, 104, 460, 818)

TOMAS = [
    # (inicio, fin, tipo, fuente, opciones)
    dict(t=1.25, fin=2.00, foto="1.jpg", crop=(10, 150, 728, 1427), tag="@robegrill", cy=0.45),
    dict(t=2.00, fin=3.00, video="v04.mp4", ss=9.4, tag=None),
    dict(t=3.00, fin=4.00, video="v02.mp4", ss=11.3, tag="@pardetres_mx"),
    dict(t=4.00, fin=4.75, foto="4.jpg", crop=(90, 160, 810, 1440), tag="@lobogrill_"),
    dict(t=4.75, fin=5.75, video="v11.mp4", ss=15.0, crop=TARJETA, tag="@brass.mx"),
    dict(t=5.75, fin=6.50, foto="12.jpg", modo="contain", tag=None),
    dict(t=6.50, fin=7.50, video="v03.mp4", ss=9.4, crop=(36, 66, 500, 889), tag="@fooddealers.mx"),
    dict(t=7.50, fin=8.50, video="v14.mp4", ss=7.6, crop=(29, 40, 524, 932), tag="@chefdieguillo"),
    dict(t=8.50, fin=9.25, foto="3.jpg", tag=None, cy=0.55),
    dict(t=9.25, fin=10.00, video="v05.mp4", ss=19.6, crop=TARJETA, tag="@elguayabo.mx"),
    dict(t=10.00, fin=10.75, foto="13.jpg", crop=(170, 0, 1070, 1600), tag=None),
    dict(t=10.75, fin=11.50, video="v13.mp4", ss=20.4, tag=None),
    dict(t=11.50, fin=11.75, foto="7.jpg", modo="contain", tag=None),
    dict(t=11.75, fin=12.00, foto="8.jpg", crop=(60, 0, 960, 1600), tag=None),
    dict(t=12.00, fin=12.25, foto="10.jpg", modo="contain", tag=None),
    dict(t=12.25, fin=13.00, foto="11.jpg", tag="@elcapiperez", cy=0.55),
]
INTRO = dict(t=0.0, fin=1.25, video="v12.mp4", ss=25.4, crop=TARJETA)
T_OUTRO = 13.0

# Transición en cada corte (por índice del corte de entrada)
TRANS = {
    1.25: "flash", 2.00: "zoom", 3.00: "whip", 4.00: "chevron", 4.75: "zoom",
    5.75: "whipv", 6.50: "flash", 7.50: "whip", 8.50: "zoom", 9.25: "chevron",
    10.00: "whipv", 10.75: "zoom", 11.50: "corte", 11.75: "corte", 12.00: "corte",
    12.25: "flash", 13.00: "chevron",
}
VENT = 0.12  # media ventana de transición (s)


def preparar(toma):
    if "foto" in toma:
        im = cargar_foto(toma["foto"], toma.get("crop"), toma.get("modo", "cover"))
        toma["src"] = im
    else:
        dur = toma["fin"] - toma["t"] + 2 * VENT + 0.1
        toma["frames"] = decodificar(toma["video"], max(0, toma["ss"] - VENT), dur, toma.get("crop"))
    return toma


def imagen_toma(toma, t, zoom_extra=1.0):
    """Cuadro de la toma en el tiempo global t (puede salirse un poco de su rango)."""
    dur = toma["fin"] - toma["t"]
    p = (t - toma["t"]) / dur
    if "src" in toma:
        z = (1.02 + 0.08 * p) * zoom_extra
        cx = 0.5 + 0.02 * (p - 0.5)
        return cubrir(toma["src"], z, cx, toma.get("cy", 0.5))
    fr = toma["frames"]
    i = int(round((t - toma["t"] + VENT) * FPS))
    i = max(0, min(len(fr) - 1, i))
    z = (1.03 + 0.04 * p) * zoom_extra
    return cubrir(fr[i], z, 0.5, toma.get("cy", 0.5))


# ---------------------------------------------------------------- elementos gráficos
LOGO = Image.open(ASSETS / "logo-blanco.png").convert("RGBA")
CABRA = Image.open(ASSETS / "cabra-blanca.png").convert("RGBA")
CABRA_N = Image.open(ASSETS / "cabra-naranja.png").convert("RGBA")
MARCA = CABRA.resize((96, round(96 * CABRA.height / CABRA.width)), Image.LANCZOS)
MARCA.putalpha(MARCA.getchannel("A").point(lambda a: a * 0.85))


def chevron(desp, ancho=260, color=BRASA, alfa=255):
    """Banda diagonal en chevrón (motivo de marca) desplazada horizontalmente."""
    capa = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(capa)
    punta = 420  # cuánto avanza la punta del chevrón
    x = desp
    pts = [(x, 0), (x + ancho, 0), (x + ancho + punta, H / 2), (x + ancho, H), (x, H), (x + punta, H / 2)]
    d.polygon(pts, fill=color + (alfa,))
    return capa, x  # x = borde trasero


def mascara_chevron(x_trasero):
    """Máscara de lo que queda detrás (a la izquierda) del borde trasero."""
    m = Image.new("L", (W, H), 0)
    punta = 420
    d = ImageDraw.Draw(m)
    d.polygon([(-10, 0), (x_trasero, 0), (x_trasero + punta, H / 2), (x_trasero, H), (-10, H)], fill=255)
    return m


def pastilla(texto, avance):
    """Etiqueta con el @ del creador. avance 0..1 (entrada)."""
    f = fuente(F_BOLD, 54)
    bb = f.getbbox(texto)
    tw = bb[2] - bb[0]
    ico = 62
    pw, ph = tw + ico + 34 + 44, 92
    capa = Image.new("RGBA", (pw, ph), (0, 0, 0, 0))
    d = ImageDraw.Draw(capa)
    d.rounded_rectangle((0, 0, pw - 1, ph - 1), radius=ph // 2, fill=BRASA + (255,))
    c = CABRA.resize((ico, round(ico * CABRA.height / CABRA.width)), Image.LANCZOS)
    capa.alpha_composite(c, (24, (ph - c.height) // 2))
    d.text((24 + ico + 16, ph / 2 - 3), texto, font=f, fill=BLANCO, anchor="lm")
    x = -pw + (70 + pw) * out_back(avance, 1.3)
    return capa, (round(x), 1330)


def texto_mascara(capa, texto, f, x, y, avance, color, ancla="la"):
    """Línea de texto que sube desde una máscara (reveal)."""
    bb = f.getbbox(texto, anchor=ancla)
    lw, lh = bb[2] - bb[0] + 20, bb[3] - bb[1] + 30
    linea = Image.new("RGBA", (lw, lh), (0, 0, 0, 0))
    dy = round((1 - out_cubic(avance)) * lh)
    ImageDraw.Draw(linea).text((10 - bb[0], 10 - bb[1] + dy), texto, font=f, fill=color, anchor=ancla)
    capa.alpha_composite(linea, (round(x), round(y)))
    return lh


# ---------------------------------------------------------------- intro y outro
def cuadro_intro(t):
    base = imagen_toma(INTRO, t, 1.0 + 0.04 * t)
    base = base.filter(ImageFilter.GaussianBlur(3))
    base = Image.blend(base, Image.new("RGB", (W, H), CARBON), 0.55).convert("RGBA")
    # banda chevrón cruzando al arrancar
    x = -900 + 2400 * in_out_cubic(t / 0.9)
    banda, _ = chevron(x, 180, BRASA, 230)
    base.alpha_composite(banda)
    capa = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    k = fuente(F_SEMI, 46)
    g = fuente(F_BOLD, 132)
    texto_mascara(capa, "COLABORACIONES", k, 80, 640, (t - 0.10) / 0.35, ASCUA)
    texto_mascara(capa, "LOS QUE", g, 72, 720, (t - 0.20) / 0.35, BLANCO)
    texto_mascara(capa, "SABEN, YA", g, 72, 860, (t - 0.30) / 0.35, BLANCO)
    texto_mascara(capa, "TRAEN SU", g, 72, 1000, (t - 0.40) / 0.35, BLANCO)
    texto_mascara(capa, "CABRA.", g, 72, 1140, (t - 0.50) / 0.35, BRASA)
    base.alpha_composite(capa)
    return base.convert("RGB")


def cuadro_outro(t):
    """t local desde T_OUTRO."""
    base = Image.new("RGBA", (W, H), CARBON + (255,))
    # chevrones de fondo
    for i, (desfase, ancho, alfa) in enumerate([(0.0, 200, 70), (0.08, 120, 140), (0.16, 60, 255)]):
        x = -1400 + 1500 * out_cubic((t - desfase) / 0.7) + i * 260
        banda, _ = chevron(x, ancho, BRASA, alfa)
        base.alpha_composite(banda)
    # logo
    a = out_back((t - 0.25) / 0.6, 1.4)
    if a > 0:
        lw = round(760 * (0.6 + 0.4 * a))
        logo = LOGO.resize((lw, round(lw * LOGO.height / LOGO.width)), Image.LANCZOS)
        alfa = clamp((t - 0.25) / 0.25)
        logo.putalpha(logo.getchannel("A").point(lambda v: v * alfa))
        base.alpha_composite(logo, ((W - logo.width) // 2, 640 - logo.height // 2))
    lin = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    f1 = fuente(F_SEMI, 64)
    f2 = fuente(F_BOLD, 74)
    tx = "La parrilla comienza aquí."
    texto_mascara(lin, tx, f1, (W - f1.getlength(tx)) / 2 - 10, 1040, (t - 0.65) / 0.4, BLANCO)
    tx2 = "@cabranegramx"
    texto_mascara(lin, tx2, f2, (W - f2.getlength(tx2)) / 2 - 10, 1150, (t - 0.80) / 0.4, ASCUA)
    tx3 = "Productos parrilleros personalizados"
    f3 = fuente(F_SEMI, 40)
    texto_mascara(lin, tx3, f3, (W - f3.getlength(tx3)) / 2 - 10, 1270, (t - 0.95) / 0.4, (190, 190, 190))
    base.alpha_composite(lin)
    return base.convert("RGB")


# ---------------------------------------------------------------- composición
def toma_en(t):
    for tm in TOMAS:
        if tm["t"] <= t < tm["fin"]:
            return tm
    return None


def render_base(t):
    """Imagen sin transiciones en t."""
    if t < INTRO["fin"]:
        return cuadro_intro(t)
    if t >= T_OUTRO:
        return cuadro_outro(t - T_OUTRO)
    return imagen_toma(toma_en(t), t)


def con_overlays(im, t):
    """Marca de agua + etiqueta del creador sobre las tomas."""
    if t < INTRO["fin"] or t >= T_OUTRO:
        return im
    tm = toma_en(t)
    im = im.convert("RGBA")
    # degradado inferior sutil para que la etiqueta lea
    im.alpha_composite(GRAD)
    im.alpha_composite(MARCA, (W - MARCA.width - 56, 90))
    if tm and tm.get("tag"):
        av = (t - tm["t"] - 0.06) / 0.32
        if av > 0:
            capa, pos = pastilla(tm["tag"], av)
            im.alpha_composite(capa, pos)
    return im.convert("RGB")


def _grad():
    g = np.zeros((H, W, 4), np.uint8)
    y = np.linspace(0, 1, H)[:, None]
    a = np.clip((y - 0.55) / 0.45, 0, 1) ** 1.6 * 150
    g[..., :3] = CARBON
    g[..., 3] = a.astype(np.uint8)
    return Image.fromarray(g, "RGBA")


GRAD = _grad()


def cuadro_final(t):
    # ¿estamos cerca de un corte?
    for c, tipo in TRANS.items():
        if abs(t - c) < VENT and tipo != "corte":
            p = (t - (c - VENT)) / (2 * VENT)  # 0..1 a lo largo de la ventana
            antes = con_overlays(render_cerca(c - 1e-3, t), t if t < c else c - 1e-3)
            despues = con_overlays(render_cerca(c, t), t if t >= c else c)
            return transicion(tipo, p, antes, despues, t, c)
    im = con_overlays(render_base(t), t)
    for c, tipo in TRANS.items():
        if tipo == "corte" and 0 <= t - c < 1 / FPS:
            im = Image.blend(im, Image.new("RGB", (W, H), BLANCO), 0.35)
    return im


def render_cerca(lado, t):
    """Renderiza la toma que vive en `lado` pero en el tiempo t (para el traslape)."""
    if lado < INTRO["fin"]:
        return cuadro_intro(min(t, INTRO["fin"]))
    if lado >= T_OUTRO:
        return cuadro_outro(max(0.0, t - T_OUTRO))
    return imagen_toma(toma_en(lado), t)


def desenfoque_h(im, px):
    a = np.asarray(im).astype(np.float32)
    n = 7
    acc = np.zeros_like(a)
    for k in range(n):
        acc += np.roll(a, int((k / (n - 1) - 0.5) * px), axis=1)
    return Image.fromarray((acc / n).astype(np.uint8))


def desenfoque_v(im, px):
    a = np.asarray(im).astype(np.float32)
    n = 7
    acc = np.zeros_like(a)
    for k in range(n):
        acc += np.roll(a, int((k / (n - 1) - 0.5) * px), axis=0)
    return Image.fromarray((acc / n).astype(np.uint8))


def transicion(tipo, p, A, B, t, c):
    if tipo == "flash":
        src = A if p < 0.5 else B
        k = 1 - abs(p - 0.5) * 2  # pico en el corte
        return Image.blend(src, Image.new("RGB", (W, H), (255, 236, 214)), 0.85 * k**1.5)
    if tipo == "zoom":
        if p < 0.5:
            q = p / 0.5
            z = 1 + 0.35 * q**2
            im = cubrir(A, z, 0.5, 0.5).filter(ImageFilter.GaussianBlur(10 * q))
        else:
            q = (1 - p) / 0.5
            z = 1 + 0.35 * q**2
            im = cubrir(B, z, 0.5, 0.5).filter(ImageFilter.GaussianBlur(10 * q))
        return im
    if tipo in ("whip", "whipv"):
        e = in_out_cubic(p)
        lienzo = Image.new("RGB", (W, H))
        if tipo == "whip":
            off = round(e * W)
            lienzo.paste(A, (-off, 0))
            lienzo.paste(B, (W - off, 0))
            vel = math.sin(math.pi * p)
            return desenfoque_h(lienzo, 260 * vel)
        off = round(e * H)
        lienzo.paste(A, (0, -off))
        lienzo.paste(B, (0, H - off))
        vel = math.sin(math.pi * p)
        return desenfoque_v(lienzo, 300 * vel)
    if tipo == "chevron":
        # la banda naranja barre de izquierda a derecha y deja B detrás
        x = -800 + (W + 900) * in_out_cubic(p)
        banda, xt = chevron(x, 300, BRASA, 255)
        m = mascara_chevron(xt)
        im = Image.composite(B, A, m).convert("RGBA")
        im.alpha_composite(banda)
        return im.convert("RGB")
    return B


# ---------------------------------------------------------------- audio (síntesis propia, sin licencias)
SR = 44100


def audio():
    n = int(DUR * SR)
    out = np.zeros(n, np.float32)
    tt = np.arange(n) / SR
    rng = np.random.default_rng(7)
    BEAT = 0.5  # 120 BPM, los cortes caen en la rejilla

    def poner(señal, t0, g=1.0):
        i = int(t0 * SR)
        if i >= n:
            return
        j = min(n, i + len(señal))
        out[i:j] += señal[: j - i] * g

    def kick():
        d = int(0.35 * SR)
        x = np.arange(d) / SR
        f = 48 + 110 * np.exp(-x * 38)
        fase = 2 * np.pi * np.cumsum(f) / SR
        return np.sin(fase) * np.exp(-x * 9)

    def hat(dec=55):
        d = int(0.08 * SR)
        x = np.arange(d) / SR
        r = rng.standard_normal(d)
        r = np.diff(r, prepend=0)  # paso alto simple
        return r * np.exp(-x * dec) * 0.25

    def clap():
        d = int(0.25 * SR)
        x = np.arange(d) / SR
        r = rng.standard_normal(d)
        env = np.exp(-x * 18) + 0.6 * np.exp(-((x - 0.012) * 300) ** 2) + 0.5 * np.exp(-((x - 0.024) * 300) ** 2)
        return np.diff(r, prepend=0) * env * 0.35

    def bajo(freq, dur):
        d = int(dur * SR)
        x = np.arange(d) / SR
        s = np.sin(2 * np.pi * freq * x) + 0.35 * np.sin(4 * np.pi * freq * x)
        env = np.minimum(1, x / 0.005) * np.exp(-x * 3.5)
        return s * env * 0.32

    def whoosh(dur=0.35, sube=True):
        d = int(dur * SR)
        x = np.linspace(0, 1, d)
        r = rng.standard_normal(d)
        # filtro paso banda barrido (media móvil variable aproximada)
        y = np.zeros(d)
        a = 0.0
        for i in range(d):
            k = 0.02 + 0.5 * (x[i] if sube else 1 - x[i])
            a += k * (r[i] - a)
            y[i] = a
        env = np.sin(np.pi * x) ** 2
        return y * env * 0.5

    def impacto():
        d = int(1.6 * SR)
        x = np.arange(d) / SR
        f = 40 + 70 * np.exp(-x * 20)
        s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-x * 2.6)
        r = rng.standard_normal(d) * np.exp(-x * 7) * 0.25
        return s + r

    # Intro: riser de ruido + tonos que suben hasta el drop en 1.25
    d = int(1.25 * SR)
    x = np.arange(d) / SR
    riser = rng.standard_normal(d) * (x / 1.25) ** 2 * 0.12
    tono = np.sin(2 * np.pi * np.cumsum(110 + 330 * (x / 1.25) ** 2) / SR) * (x / 1.25) ** 2 * 0.12
    out[:d] += riser + tono
    poner(kick(), 0.0, 0.7)
    poner(kick(), 0.75, 0.5)

    # Groove 1.25 → 13.0
    notas = [55.0, 55.0, 65.41, 49.0]  # La, La, Do, Sol (graves)
    t = 1.25
    k = 0
    while t < T_OUTRO - 1e-6:
        poner(kick(), t, 0.95)
        if k % 2 == 1:
            poner(clap(), t, 1.0)
        poner(hat(), t + 0.25, 0.9)
        poner(hat(80), t + 0.125, 0.4)
        poner(hat(80), t + 0.375, 0.4)
        poner(bajo(notas[(k // 2) % 4], 0.45), t, 1.0)
        t += BEAT
        k += 1
    # whoosh en cada transición
    for c, tipo in TRANS.items():
        if tipo != "corte" and 1.25 < c < T_OUTRO:
            poner(whoosh(0.3), c - 0.18, 0.55)
    # stutter: hats extra
    for c in (11.5, 11.75, 12.0):
        poner(hat(30), c, 1.2)
    # Outro: impacto + acorde que se apaga
    poner(impacto(), T_OUTRO, 0.9)
    d = int(2.0 * SR)
    x = np.arange(d) / SR
    acorde = sum(np.sin(2 * np.pi * f * x) for f in (220.0, 261.63, 329.63, 440.0)) / 4
    poner(acorde * np.exp(-x * 1.4) * 0.22 * np.minimum(1, x / 0.02), T_OUTRO)

    # Master: compresión suave + fade final
    out = np.tanh(out * 1.3) * 0.85
    fade = np.ones(n)
    fi = int(0.4 * SR)
    fade[-fi:] = np.linspace(1, 0, fi)
    out *= fade
    est = np.stack([out, out], 1)
    pcm = (est * 32767).astype(np.int16)
    ruta = SALIDA / "musica.wav"
    with wave.open(str(ruta), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())
    return ruta


# ---------------------------------------------------------------- main
def main(solo=None):
    preparar(INTRO)
    for tm in TOMAS:
        preparar(tm)
    if solo is not None:
        for t in solo:
            cuadro_final(t).save(SALIDA / f"prueba_{t:05.2f}.jpg", quality=88)
        return
    wav = audio()
    destino = SALIDA / "cabra_negra_influencers.mp4"
    proc = subprocess.Popen(
        [FF, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
         "-r", str(FPS), "-i", "-", "-i", str(wav), "-c:v", "libx264", "-preset", "medium",
         "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-shortest",
         "-movflags", "+faststart", str(destino)],
        stdin=subprocess.PIPE,
    )
    for i in range(N):
        t = i / FPS
        proc.stdin.write(cuadro_final(t).tobytes())
        if i % 60 == 0:
            print(f"{t:5.1f}s", flush=True)
    proc.stdin.close()
    proc.wait()
    print(destino)


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "prueba":
        main([0.4, 1.2, 1.3, 1.6, 2.6, 3.0, 3.6, 4.3, 5.3, 6.1, 7.0, 8.0, 8.8, 9.6, 10.4, 11.1, 11.6, 12.6, 13.3, 14.5])
    else:
        main()
