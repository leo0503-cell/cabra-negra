"""Cotización de sitio web para Cabra Negra — setup único.

Todo lo editable vive en el bloque PARÁMETROS. Para cambiar el precio
tocas una sola línea (PARTIDAS) y el subtotal, IVA y total se recalculan.

    uv run --with reportlab python cotizar.py
"""
from pathlib import Path
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import letter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

# ─────────────────────────── PARÁMETROS ───────────────────────────
CLIENTE      = "Cabra Negra"
DOCUMENTO    = "Cotización — Sitio web oficial"
FECHA        = "23 de septiembre de 2026"
FOLIO        = "MECHA-2026-CN-01"
VIGENCIA     = "30 días naturales"
PROVEEDOR    = "Mecha · Leonardo Padilla"
CONTACTO     = "<correo de Mecha> · <teléfono de Mecha>"
IVA          = 0.16

# (concepto, detalle, importe MXN antes de IVA)
PARTIDAS = [
    ("Diseño y desarrollo del sitio",
     "Seis secciones, responsivo de celular a escritorio, sobre la identidad "
     "oficial del Catálogo 2026.", 9_500),
    ("Escena de apertura con video atado al scroll",
     "Motor a medida: el video avanza y retrocede con el scroll, con paneles "
     "y carrusel de producto encadenados.", 6_500),
    ("Producción del video de apertura",
     "12.6 s construidos con la fotografía del propio catálogo. Codificado "
     "para que el rebobinado sea fluido.", 4_000),
    ("Recuperación y preparación de assets",
     "Logotipo recuperado con transparencia, 23 fotos de producto y 18 "
     "logotipos de clientes, optimizados para web.", 3_500),
    ("Formulario de pedido conectado a WhatsApp",
     "El cliente llena producto, cantidad, grabado y destino; el mensaje "
     "llega ya redactado.", 1_500),
    ("Publicación y puesta en marcha",
     "Dominio, hosting, certificado SSL, SEO base, sitemap y tarjeta de "
     "vista previa para WhatsApp y redes.", 1_500),
]

CIFRAS = [
    ("10", "líneas de producto"),
    ("23", "fotos de producto"),
    ("18", "logos de clientes"),
    ("6", "secciones"),
]

RECURRENTES = [
    ("Dominio .mx", "Primer año", "~$617"),
    ("Dominio .mx", "Renovación anual", "~$716"),
    ("Hosting", "Anual, dentro de la infraestructura de Mecha",
     "<lo que decidas cobrar>"),
    ("Mantenimiento", "Opcional, se cotiza aparte",
     "<lo que decidas cobrar>"),
]

NO_INCLUYE = [
    "Tienda en línea, carrito o cobro dentro del sitio.",
    "Fotografía o video nuevos de producto.",
    "Alta y administración de correos corporativos.",
    "Textos adicionales a los que ya trae el sitio, y traducción.",
    "Campañas de pauta en Meta: se cotizan por separado.",
    "Cambios posteriores a la ronda de ajustes incluida.",
]

CONDICIONES = [
    ("Forma de pago", "50% al aceptar la cotización y 50% contra publicación."),
    ("Tiempo de entrega", "El sitio ya está construido. Se publica dentro de los "
                          "3 días hábiles siguientes a recibir el número de "
                          "WhatsApp de ventas y la decisión de dominio."),
    ("Ajustes incluidos", "Una ronda de cambios de texto e imágenes antes de publicar."),
    ("Antes de pagar", "Puedes revisar el sitio completo y funcionando."),
    ("Vigencia", f"Esta cotización es válida por {VIGENCIA} a partir de la fecha."),
]

PENDIENTES = [
    "Número de WhatsApp de ventas — sin él, el formulario no envía.",
    "Dominio que se va a registrar (por ejemplo, cabranegra.mx).",
    "Dirección del taller, si quieren mostrarla.",
]

# ─────────────────────────── ESTILO ───────────────────────────
CARBON = HexColor("#0C1013")
BRASA  = HexColor("#C8792F")
ASCUA  = HexColor("#F89C3C")
PAPEL  = HexColor("#F8F4EC")
TINTA  = HexColor("#1A1613")
GRIS   = HexColor("#6E6963")
LINEA  = HexColor("#DED5C4")
BLANCO = HexColor("#FFFFFF")

W, H = letter
MX = 46                      # margen lateral
AN = W - MX * 2              # ancho útil

RAIZ = Path(__file__).resolve().parent
for peso in ("Light", "Regular", "Medium", "SemiBold", "Bold"):
    pdfmetrics.registerFont(TTFont(f"Outfit-{peso}", RAIZ / "fuentes" / f"Outfit-{peso}.ttf"))
L, R, M, S, B = "Outfit-Light", "Outfit-Regular", "Outfit-Medium", "Outfit-SemiBold", "Outfit-Bold"


def dinero(n):
    return f"${n:,.0f}"


def parte(c, texto, x, y, ancho, fuente=R, tam=8.6, alto=11.4, color=TINTA):
    """Dibuja texto con salto de línea y devuelve la y final."""
    c.setFont(fuente, tam)
    c.setFillColor(color)
    palabras, linea = texto.split(), ""
    for p in palabras:
        prueba = f"{linea} {p}".strip()
        if pdfmetrics.stringWidth(prueba, fuente, tam) <= ancho:
            linea = prueba
        else:
            c.drawString(x, y, linea)
            y -= alto
            linea = p
    if linea:
        c.drawString(x, y, linea)
        y -= alto
    return y


def rotulo(c, texto, x, y, color=BRASA, tam=6.8):
    c.setFont(S, tam)
    c.setFillColor(color)
    c.drawString(x, y, texto.upper())


def seccion(c, num, eyebrow, titulo, y):
    rotulo(c, f"{num} · {eyebrow}", MX, y)
    y -= 15
    c.setFont(B, 14.5)
    c.setFillColor(TINTA)
    c.drawString(MX, y, titulo)
    return y - 17


def caja(c, x, y, ancho, alto, relleno=BLANCO, borde=LINEA, barra=None):
    c.setFillColor(relleno)
    c.setStrokeColor(borde)
    c.setLineWidth(0.6)
    c.roundRect(x, y - alto, ancho, alto, 3, stroke=1, fill=1)
    if barra:
        c.setFillColor(barra)
        c.rect(x, y - alto, 2.4, alto, stroke=0, fill=1)


def pie(c, n, total):
    c.setFont(L, 7)
    c.setFillColor(GRIS)
    c.drawString(MX, 30, f"{CLIENTE} · {DOCUMENTO} · Folio {FOLIO}")
    c.drawRightString(W - MX, 30, f"Página {n} de {total}")


# ─────────────────────────── PÁGINA 1 ───────────────────────────
def pagina1(c):
    alto_enc = 132
    c.setFillColor(CARBON)
    c.rect(0, H - alto_enc, W, alto_enc, stroke=0, fill=1)
    c.setFillColor(BRASA)
    c.rect(0, H - alto_enc, W, 3, stroke=0, fill=1)

    logo = RAIZ.parent / "assets" / "cabra-blanca.png"
    if logo.exists():
        c.drawImage(str(logo), MX, H - 52, width=26, height=23,
                    mask="auto", preserveAspectRatio=True, anchor="nw")

    c.setFont(S, 8)
    c.setFillColor(ASCUA)
    c.drawString(MX + 33, H - 45, CLIENTE.upper())

    c.setFont(B, 20)
    c.setFillColor(HexColor("#F2EDE6"))
    c.drawString(MX, H - 76, DOCUMENTO)

    c.setFont(L, 9)
    c.setFillColor(HexColor("#A8A29A"))
    c.drawString(MX, H - 93, f"Preparada por {PROVEEDOR}  ·  {FECHA}  ·  Folio {FOLIO}")

    # chips
    x = MX
    for chip in ("Pago único de setup", f"Vigencia: {VIGENCIA}", "Entrega: 3 días hábiles"):
        an = pdfmetrics.stringWidth(chip, M, 7.6) + 20
        c.setFillColor(HexColor("#20262B"))
        c.roundRect(x, H - 120, an, 17, 8.5, stroke=0, fill=1)
        c.setFont(M, 7.6)
        c.setFillColor(HexColor("#E4DED4"))
        c.drawString(x + 10, H - 114.5, chip)
        x += an + 7

    y = H - alto_enc - 30

    # 01 · qué se entrega
    y = seccion(c, "01", "Qué se entrega", "Un sitio, no una plantilla", y)
    y = parte(c,
              "El sitio está construido sobre la identidad oficial del Catálogo 2026 y con la "
              "fotografía de sus propias piezas. La apertura es una escena de video que avanza "
              "y retrocede conforme el visitante hace scroll — el mismo recurso que usan las "
              "marcas grandes para que el material se sienta antes de leerse.",
              MX, y, AN, L, 9.2, 12.4, GRIS)
    y -= 10

    # cifras
    an_t = (AN - 3 * 8) / 4
    for i, (cifra, etq) in enumerate(CIFRAS):
        x = MX + i * (an_t + 8)
        caja(c, x, y, an_t, 46)
        c.setFont(B, 17)
        c.setFillColor(BRASA)
        c.drawString(x + 11, y - 24, cifra)
        c.setFont(L, 7.4)
        c.setFillColor(GRIS)
        c.drawString(x + 11, y - 37, etq)
    y -= 46 + 24

    # 02 · qué incluye
    y = seccion(c, "02", "Qué incluye", "Las seis partidas del trabajo", y)
    for i, (concepto, detalle, _) in enumerate(PARTIDAS):
        alto = 42
        caja(c, MX, y, AN, alto, barra=BRASA)
        c.setFont(S, 6.6)
        c.setFillColor(BRASA)
        c.drawString(MX + 12, y - 14, f"{i + 1:02d}")
        c.setFont(S, 9.6)
        c.setFillColor(TINTA)
        c.drawString(MX + 30, y - 14, concepto)
        parte(c, detalle, MX + 30, y - 26, AN - 44, L, 8.2, 10.4, GRIS)
        y -= alto + 7

    y -= 8
    rotulo(c, "Lo que hace falta para publicar", MX, y)
    y -= 13
    for p in PENDIENTES:
        c.setFillColor(ASCUA)
        c.circle(MX + 3, y + 3, 2, stroke=0, fill=1)
        y = parte(c, p, MX + 12, y, AN - 12, L, 8.4, 11, GRIS) - 2

    pie(c, 1, 2)


# ─────────────────────────── PÁGINA 2 ───────────────────────────
def pagina2(c):
    y = H - 54
    rotulo(c, CLIENTE, MX, y, BRASA, 7.4)
    y -= 26

    # 03 · inversión
    y = seccion(c, "03", "Inversión", "Pago único de setup", y)

    col_imp = W - MX - 6
    c.setFillColor(HexColor("#EFE8DA"))
    c.rect(MX, y - 15, AN, 15, stroke=0, fill=1)
    c.setFont(S, 6.8)
    c.setFillColor(GRIS)
    c.drawString(MX + 10, y - 10.5, "CONCEPTO")
    c.drawRightString(col_imp, y - 10.5, "IMPORTE MXN")
    y -= 15

    for i, (concepto, _, importe) in enumerate(PARTIDAS):
        if i % 2 == 0:
            c.setFillColor(BLANCO)
            c.rect(MX, y - 21, AN, 21, stroke=0, fill=1)
        c.setFont(R, 9)
        c.setFillColor(TINTA)
        c.drawString(MX + 10, y - 14, concepto)
        c.setFont(M, 9)
        c.drawRightString(col_imp, y - 14, dinero(importe))
        c.setStrokeColor(LINEA)
        c.setLineWidth(0.5)
        c.line(MX, y - 21, W - MX, y - 21)
        y -= 21

    subtotal = sum(p[2] for p in PARTIDAS)
    iva = subtotal * IVA
    total = subtotal + iva

    for etq, val, fuerte in (("Subtotal", subtotal, False),
                             (f"IVA {IVA:.0%}", iva, False)):
        c.setFont(R if not fuerte else B, 9)
        c.setFillColor(GRIS)
        c.drawRightString(col_imp - 96, y - 14, etq)
        c.setFillColor(TINTA)
        c.drawRightString(col_imp, y - 14, dinero(val))
        y -= 19

    y -= 3
    c.setFillColor(CARBON)
    c.rect(MX, y - 34, AN, 34, stroke=0, fill=1)
    c.setFillColor(BRASA)
    c.rect(MX, y - 34, 3, 34, stroke=0, fill=1)
    c.setFont(S, 8)
    c.setFillColor(ASCUA)
    c.drawString(MX + 16, y - 14, "TOTAL A PAGAR")
    c.setFont(L, 7.4)
    c.setFillColor(HexColor("#A8A29A"))
    c.drawString(MX + 16, y - 26, "Pago único. No hay mensualidad por el sitio.")
    c.setFont(B, 17)
    c.setFillColor(BLANCO)
    c.drawRightString(col_imp, y - 22, f"{dinero(total)} MXN")
    y -= 34 + 26

    # 04 · recurrentes
    y = seccion(c, "04", "Aparte del setup", "Lo que se paga cada año", y)
    y = parte(c,
              "Estos costos no son de Mecha: son del dominio y del servidor. Se los "
              "transparentamos para que no haya sorpresas en la renovación.",
              MX, y, AN, L, 8.6, 11.2, GRIS)
    y -= 8

    c.setFillColor(HexColor("#EFE8DA"))
    c.rect(MX, y - 14, AN, 14, stroke=0, fill=1)
    c.setFont(S, 6.6)
    c.setFillColor(GRIS)
    c.drawString(MX + 10, y - 10, "CONCEPTO")
    c.drawString(MX + 130, y - 10, "PERIODO")
    c.drawRightString(col_imp, y - 10, "APROXIMADO")
    y -= 14
    for concepto, periodo, monto in RECURRENTES:
        c.setFont(M, 8.4)
        c.setFillColor(TINTA)
        c.drawString(MX + 10, y - 13, concepto)
        c.setFont(L, 8.4)
        c.setFillColor(GRIS)
        c.drawString(MX + 130, y - 13, periodo)
        c.setFont(M, 8.4)
        c.setFillColor(TINTA if monto.startswith("~") else ASCUA)
        c.drawRightString(col_imp, y - 13, monto)
        c.setStrokeColor(LINEA)
        c.setLineWidth(0.5)
        c.line(MX, y - 19, W - MX, y - 19)
        y -= 19
    y -= 18

    # 05 · condiciones + no incluye, a dos columnas
    y = seccion(c, "05", "Condiciones", "Cómo se trabaja", y)
    col = (AN - 16) / 2
    y_cond = y
    for etq, txt in CONDICIONES:
        c.setFont(S, 7.6)
        c.setFillColor(BRASA)
        c.drawString(MX, y_cond, etq)
        y_cond = parte(c, txt, MX, y_cond - 11, col, L, 8.2, 10.4, GRIS) - 7

    y_no = y
    c.setFont(S, 7.6)
    c.setFillColor(GRIS)
    c.drawString(MX + col + 16, y_no, "NO INCLUYE")
    y_no -= 13
    for p in NO_INCLUYE:
        c.setFillColor(LINEA)
        c.rect(MX + col + 16, y_no + 3, 5, 1.6, stroke=0, fill=1)
        y_no = parte(c, p, MX + col + 27, y_no, col - 27, L, 8.2, 10.4, GRIS) - 3

    y = min(y_cond, y_no) - 14
    caja(c, MX, y, AN, 38, relleno=HexColor("#FBF7EF"), barra=BRASA)
    c.setFont(S, 8.4)
    c.setFillColor(TINTA)
    c.drawString(MX + 14, y - 15, "Para aceptar")
    parte(c, f"Responde a este documento y arrancamos. Dudas: {CONTACTO}",
          MX + 14, y - 27, AN - 28, L, 8.2, 10.4, GRIS)

    pie(c, 2, 2)


def main():
    salida = RAIZ / "Cabra_Negra_Cotizacion_Sitio_Web.pdf"
    c = canvas.Canvas(str(salida), pagesize=letter)
    c.setTitle(f"{CLIENTE} — {DOCUMENTO}")
    c.setAuthor(PROVEEDOR)

    for dibuja in (pagina1, pagina2):
        c.setFillColor(PAPEL)
        c.rect(0, 0, W, H, stroke=0, fill=1)
        dibuja(c)
        c.showPage()

    c.save()
    sub = sum(p[2] for p in PARTIDAS)
    print(f"{salida}")
    print(f"subtotal {dinero(sub)} · IVA {dinero(sub * IVA)} · total {dinero(sub * (1 + IVA))}")


if __name__ == "__main__":
    main()
