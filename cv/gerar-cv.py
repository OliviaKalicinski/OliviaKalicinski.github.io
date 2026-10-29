#!/usr/bin/env python3
"""Gera Olivia_Kalicinski_CV.pdf.

Refaz em codigo o CV de duas paginas que antes so existia como PDF pronto:
mesma paleta, mesma grade, agora versionado junto com o site.

    python3 gerar-cv.py            # escreve Olivia_Kalicinski_CV.pdf aqui do lado

Os numeros do texto saem do que ja esta publicado no site e no LinkedIn.
Valor de venda, verba e margem da Lets Fly nao entram (decisao de 21/10/2026).
"""

from pathlib import Path

from reportlab.lib.colors import Color
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas

AQUI = Path(__file__).parent
SAIDA = AQUI / "Olivia_Kalicinski_CV.pdf"
FOTO = AQUI / "foto.jpg"
FOTO_QUADRADA = AQUI / "foto-quadrada.jpg"

LARGURA, ALTURA = A4            # 595.28 x 841.89 pt

PAPEL = Color(242 / 255, 235 / 255, 221 / 255)
VERMELHO = Color(184 / 255, 57 / 255, 42 / 255)
TINTA = Color(67 / 255, 63 / 255, 57 / 255)
CLARO = Color(120 / 255, 113 / 255, 103 / 255)

MARGEM = 42
ESQ = MARGEM                    # coluna larga: texto corrido
ESQ_W = 300
DIR = 378                       # coluna estreita: foto e fichas
DIR_W = LARGURA - MARGEM - DIR  # 175.28

SITE = "olivia-kalicinski.vercel.app"
LINKEDIN = "linkedin.com/in/olivia-kalicinski"
EMAIL = "olivia.kalicinski@gmail.com"


# ---------------------------------------------------------------- utilidades

def y(topo):
    """Converte distancia do topo da pagina em coordenada do ReportLab."""
    return ALTURA - topo


def quebrar(texto, fonte, corpo, largura):
    """Quebra o texto em linhas que cabem na largura dada."""
    linhas, atual = [], ""
    for palavra in texto.split():
        teste = f"{atual} {palavra}".strip()
        if stringWidth(teste, fonte, corpo) <= largura:
            atual = teste
        else:
            if atual:
                linhas.append(atual)
            atual = palavra
    if atual:
        linhas.append(atual)
    return linhas


def espacado(c, x, yy, texto, fonte, corpo, espaco):
    """Desenha o texto com espaco extra entre as letras e devolve a largura."""
    for letra in texto:
        c.drawString(x, yy, letra)
        x += stringWidth(letra, fonte, corpo) + espaco
    return x


class Folha:
    """Desenha na pagina guardando onde cada coluna parou."""

    def __init__(self, c):
        self.c = c
        self.fundo()

    def fundo(self):
        self.c.setFillColor(PAPEL)
        self.c.rect(0, 0, LARGURA, ALTURA, stroke=0, fill=1)

    def texto(self, x, topo, texto, *, fonte="Helvetica", corpo=9.0,
              cor=TINTA, entrelinha=1.45, largura=None):
        """Escreve um paragrafo e devolve onde ele terminou (dist. do topo)."""
        largura = largura or ESQ_W
        self.c.setFillColor(cor)
        self.c.setFont(fonte, corpo)
        linha_altura = corpo * entrelinha
        for i, linha in enumerate(quebrar(texto, fonte, corpo, largura)):
            self.c.drawString(x, y(topo + corpo + i * linha_altura), linha)
        n = len(quebrar(texto, fonte, corpo, largura))
        return topo + corpo + (n - 1) * linha_altura

    def etiqueta(self, x, topo, texto, *, corpo=7.6):
        """Rotulo de secao dentro de um retangulo fino vermelho."""
        pad_x, pad_y = 5, 3.4
        largura = stringWidth(texto, "Helvetica-Bold", corpo) + pad_x * 2
        altura = corpo + pad_y * 2
        self.c.setStrokeColor(VERMELHO)
        self.c.setLineWidth(0.7)
        self.c.rect(x, y(topo + altura), largura, altura, stroke=1, fill=0)
        self.c.setFillColor(VERMELHO)
        self.c.setFont("Helvetica-Bold", corpo)
        self.c.drawString(x + pad_x, y(topo + altura - pad_y - 0.6), texto)
        return topo + altura

    def bullet(self, x, topo, texto, *, largura=None, corpo=9.0):
        largura = largura or ESQ_W
        recuo = 9
        self.c.setFillColor(VERMELHO)
        self.c.setFont("Helvetica", corpo)
        self.c.drawString(x, y(topo + corpo), "•")
        return self.texto(x + recuo, topo, texto, corpo=corpo,
                          largura=largura - recuo)

    def rodape(self, pagina):
        linha = ALTURA - 800
        self.c.setStrokeColor(VERMELHO)
        self.c.setLineWidth(0.8)
        self.c.line(MARGEM, linha, LARGURA - MARGEM, linha)
        self.c.setFont("Helvetica-Bold", 6.6)
        self.c.setFillColor(VERMELHO)
        espacado(self.c, MARGEM, linha - 13, "OLIVIA KALICINSKI",
                 "Helvetica-Bold", 6.6, 0.8)
        direita = f"CURRICULUM VITAE / {pagina}"
        larg = (stringWidth(direita, "Helvetica-Bold", 6.6)
                + 0.8 * (len(direita) - 1))
        espacado(self.c, LARGURA - MARGEM - larg, linha - 13, direita,
                 "Helvetica-Bold", 6.6, 0.8)


# ------------------------------------------------------------------ pagina 1

def pagina_um(c):
    f = Folha(c)

    # nome, em duas linhas, como no original
    c.setFillColor(VERMELHO)
    c.setFont("Helvetica-Bold", 55.5)
    c.drawString(ESQ, y(87.6), "OLIVIA")
    c.drawString(ESQ, y(145.9), "KALICINSKI")

    c.setFont("Helvetica-Bold", 9.6)
    espacado(c, ESQ, y(169.9), "GROWTH / CREATIVE / CRO",
             "Helvetica-Bold", 9.6, 0.9)

    # filete e frase no alto a direita
    c.setStrokeColor(VERMELHO)
    c.setLineWidth(0.9)
    c.line(DIR + 12, y(44), DIR + 12, y(82))
    frase = ["Strategy, creative", "and the systems",
             "that make them work."]
    c.setFont("Helvetica", 8.4)
    for i, linha in enumerate(frase):
        c.drawString(DIR + 24, y(53 + i * 12.4), linha)

    # ---- coluna da esquerda
    t = f.etiqueta(ESQ, 196, "Profile")
    t = f.texto(ESQ, t + 11,
                "I launch and grow DTC businesses, connecting paid acquisition, "
                "creator-led creative, lifecycle and conversion. I lead the team, "
                "own the acquisition P&L and build the technology behind the work.")
    t = f.texto(ESQ, t + 14,
                "Six years in a family business, a marketing internship at "
                "L’Oréal and an independent visual arts practice inform "
                "how I combine commercial judgement with storytelling.")

    t = f.etiqueta(ESQ, t + 26, "Current role")
    c.setFillColor(TINTA)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(ESQ, y(t + 23), "Head of Growth")
    c.setFillColor(VERMELHO)
    c.setFont("Helvetica", 8.4)
    c.drawString(ESQ, y(t + 36), "Lets Fly / Comida de Dragão")
    c.drawString(ESQ, y(t + 47.5), "Jan 2025 – present · Brazil")
    t = t + 47.5

    t = f.texto(ESQ, t + 13,
                "Launched the DTC brand of an insect-protein biotech. Lead four "
                "people across paid media, creative, creators and CRM; own "
                "acquisition, CRO, retention and the Shopify storefront.")

    bullets = [
        "Inverted where company revenue comes from: B2B was 87% of it in "
        "Jan–Apr 2025; in the same months of 2026, DTC and resale are 67% "
        "and B2C grew more than tenfold.",
        "Built an in-house creator programme instead of hiring an agency: "
        "233 active partners across 25 Brazilian states.",
        "Rebuilt a landing page: initiated checkout rose from 1.0% to 5.9%, "
        "attention on the page from 3.1s to 12.2s.",
        "Build and maintain 20+ React/TypeScript landing pages, dashboards, "
        "GA4 tracking and agent automations.",
    ]
    for texto in bullets:
        t = f.bullet(ESQ, t + 12, texto)

    # ---- coluna da direita
    foto_topo, foto_h = 212, 222
    c.drawImage(str(FOTO), DIR, y(foto_topo + foto_h), DIR_W, foto_h,
                preserveAspectRatio=False, mask=None)

    t = f.etiqueta(DIR, foto_topo + foto_h + 20, "Contact")
    t += 11
    linhas = [(EMAIL, f"mailto:{EMAIL}"),
              (SITE, f"https://{SITE}"),
              (LINKEDIN, f"https://{LINKEDIN}"),
              ("Rio de Janeiro, Brazil · GMT-3", None)]
    c.setFont("Helvetica", 8.2)
    for texto, url in linhas:
        c.setFillColor(TINTA)
        c.drawString(DIR, y(t + 8.2), texto)
        if url:
            largura = stringWidth(texto, "Helvetica", 8.2)
            c.linkURL(url, (DIR, y(t + 10), DIR + largura, y(t - 1)),
                      relative=0, thickness=0)
        t += 11.6

    t = f.etiqueta(DIR, t + 13, "Languages")
    t += 11
    for idioma, nivel in [("Portuguese", "native"),
                          ("English", "full professional"),
                          ("German", "intermediate"),
                          ("Spanish", "elementary")]:
        c.setFillColor(TINTA)
        c.setFont("Helvetica", 8.2)
        c.drawString(DIR, y(t + 8.2), idioma)
        c.setFillColor(CLARO)
        c.drawString(DIR + 58, y(t + 8.2), nivel)
        t += 11.6

    t = f.etiqueta(DIR, t + 13, "Work arrangement")
    f.texto(DIR, t + 11,
            "Brazil-based contractor. Open to international remote "
            "opportunities.", largura=DIR_W)

    # o rodape da pagina carrega o endereco do portfolio, nao um slogan
    c.setFillColor(VERMELHO)
    c.setFont("Helvetica-Bold", 26)
    c.drawString(ESQ, y(764), SITE)
    larg = stringWidth(SITE, "Helvetica-Bold", 26)
    c.linkURL(f"https://{SITE}", (ESQ, y(770), ESQ + larg, y(736)),
              relative=0, thickness=0)
    c.setFont("Helvetica", 8.4)
    c.drawString(ESQ, y(782), "Selected work, written up in full.")

    f.rodape(1)
    c.showPage()


# ------------------------------------------------------------------ pagina 2

def pagina_dois(c):
    f = Folha(c)

    c.setFillColor(VERMELHO)
    c.setFont("Helvetica-Bold", 43)
    c.drawString(ESQ, y(76.6), "EXPERIENCE")
    c.setFont("Helvetica", 8.8)
    c.drawString(ESQ, y(96), "Commercial thinking. Creative judgement. "
                             "Hands-on execution.")

    largura_toda = LARGURA - MARGEM * 2
    t = f.etiqueta(ESQ, 130, "Selected growth results / Lets Fly")
    resultados = [
        "Reached 5,077 buyers in 598 municipalities across 26 Brazilian "
        "states; 15.1% of them bought more than once.",
        "Found the purchase event firing on order creation instead of "
        "payment, which inflated every platform ROAS by about 12%, and the "
        "Meta click id being dropped between domains, leaving only 57% of "
        "purchases identified. Both fixed in code; contribution margin per "
        "landing page is now the budgeting rule.",
        "Identified an ad driving 29 of 63 purchases on 13% of spend. Fixing "
        "its destination helped lift weekly purchases from 34 to 40 and "
        "reduce CPA from R$102 to R$95.",
        "Diagnosed misleading free-shipping copy at checkout. After the "
        "change, abandonment in the R$140–150 cart band fell from 53.7% "
        "to 30.0%.",
    ]
    for texto in resultados:
        t = f.bullet(ESQ, t + 12, texto, largura=largura_toda)

    base = t + 30

    # ---- esquerda: empregos anteriores
    te = f.etiqueta(ESQ, base, "Earlier experience")
    cargos = [
        ("Visual Artist", "Independent / Jan 2021 – Feb 2025",
         "Ceramics, photography and installation. Awarded at Festival do "
         "Minuto 2024; Casero Art Residency 2024; exhibitions at Casa da "
         "Escada Colorida and EAV Parque Lage. Commissioned photography "
         "and video."),
        ("Project & Marketing Manager", "Sítio Solidão / Apr 2015 – May 2021",
         "Created the trade marketing department and hired and trained a "
         "team of 14. Managed key retail accounts including Zona Sul and "
         "Hortifruti; led marketing, PR and operational improvements."),
        ("Trainee / Recruitment & Commercial", "Airswift / Feb 2014 – Mar 2015",
         "Recruitment and client-facing commercial work. Training in Houston "
         "with international teams."),
        ("DMI Intern / Garnier", "L’Oréal / Oct 2012 – Apr 2013",
         "Global skincare and deodorant product concepts, packaging and "
         "campaign briefs, market analysis and consumer research."),
    ]
    for titulo, onde, texto in cargos:
        te += 16
        c.setFillColor(VERMELHO)
        c.setFont("Helvetica-Bold", 10)
        c.drawString(ESQ, y(te + 10), titulo)
        te += 10
        c.setFillColor(CLARO)
        c.setFont("Helvetica", 7.8)
        c.drawString(ESQ, y(te + 10), onde)
        te += 10
        te = f.texto(ESQ, te + 4, texto, corpo=8.4)

    # ---- direita: o que ela faz e onde estudou
    td = f.etiqueta(DIR, base, "Capabilities")
    blocos = [
        ("Growth", ["Meta, Google & TikTok Ads", "Creator programmes",
                    "Email & WhatsApp lifecycle", "CRO, checkout & pricing"]),
        ("Data & build", ["GA4 · UTMs · SQL", "Dashboards · Shopify",
                          "React · TypeScript", "HTML/CSS · Git",
                          "Agent automation"]),
    ]
    for titulo, itens in blocos:
        td += 17
        c.setFillColor(VERMELHO)
        c.setFont("Helvetica-Bold", 9)
        c.drawString(DIR, y(td + 9), titulo)
        td += 13
        c.setFillColor(TINTA)
        c.setFont("Helvetica", 8.2)
        for item in itens:
            c.drawString(DIR, y(td + 8.2), item)
            td += 11.4

    td = f.etiqueta(DIR, td + 14, "Education")
    formacao = [
        ("PUC-Rio / 2016",
         "Postgraduate, Governance in Family Businesses"),
        ("Ibmec / 2010 – 2013",
         "Bachelor of Business Administration"),
        ("Art & development",
         "Parque Lage; Casero residency; critical mentorships with André "
         "Penteado and Ana Elisa Lizidia, both on scholarship, and with "
         "Bruno Miguel."),
    ]
    for titulo, texto in formacao:
        td += 15
        c.setFillColor(VERMELHO)
        c.setFont("Helvetica-Bold", 8.6)
        c.drawString(DIR, y(td + 8.6), titulo)
        td += 10
        td = f.texto(DIR, td + 2, texto, corpo=8.2, largura=DIR_W)

    lado = 172
    foto_topo = max(te, td) + 26
    foto_topo = min(foto_topo, 800 - 16 - lado)
    c.drawImage(str(FOTO_QUADRADA), ESQ, y(foto_topo + lado), lado, lado,
                preserveAspectRatio=False, mask=None)

    f.rodape(2)
    c.showPage()


def main():
    c = canvas.Canvas(str(SAIDA), pagesize=A4)
    c.setTitle("Olivia Kalicinski | Growth, Creative & CRO")
    c.setAuthor("Olivia Kalicinski")
    c.setSubject("Curriculum vitae")
    c.setCreator("gerar-cv.py")
    pagina_um(c)
    pagina_dois(c)
    c.save()
    print(f"{SAIDA}  ({SAIDA.stat().st_size / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
