#!/usr/bin/env python3
"""Recorta cada peca de uma folha (fitas, clipes, adesivos) em PNGs soltos, com fundo transparente.

Uso:  python3 separa-fitas.py <folha.png|jpg> [pasta-de-saida] [prefixo] [quantas]
Ex.:  python3 separa-fitas.py fitas.png img/fitas fita
      python3 separa-fitas.py clipes.png img/clipes clipe 12   # so as 12 maiores
Saida: <pasta>/<prefixo>-01.png, -02.png, ...
"""
import sys, os
import numpy as np
from PIL import Image

LIMIAR_BRANCO = 243     # acima disso em R, G e B conta como fundo
AREA_MINIMA   = 2500    # descarta respingo e marca d'agua solta
MARGEM        = 2

def rotular(mask):
    """Componentes conexos 4-vizinhos, sem scipy."""
    h, w = mask.shape
    rot = np.zeros((h, w), np.int32)
    atual = 0
    pilha = []
    for y0 in range(h):
        for x0 in range(w):
            if not mask[y0, x0] or rot[y0, x0]:
                continue
            atual += 1
            pilha.append((y0, x0))
            rot[y0, x0] = atual
            while pilha:
                y, x = pilha.pop()
                for dy, dx in ((1,0),(-1,0),(0,1),(0,-1)):
                    ny, nx = y+dy, x+dx
                    if 0 <= ny < h and 0 <= nx < w and mask[ny, nx] and not rot[ny, nx]:
                        rot[ny, nx] = atual
                        pilha.append((ny, nx))
    return rot, atual

def main():
    if len(sys.argv) < 2:
        print(__doc__); return 1
    origem = sys.argv[1]
    saida = sys.argv[2] if len(sys.argv) > 2 else 'img/fitas'
    prefixo = sys.argv[3] if len(sys.argv) > 3 else 'fita'
    quantas = int(sys.argv[4]) if len(sys.argv) > 4 else 0
    os.makedirs(saida, exist_ok=True)

    im = Image.open(origem).convert('RGB')
    a = np.asarray(im)
    conteudo = ~np.all(a >= LIMIAR_BRANCO, axis=2)

    # fecha buracos finos entre pedaços da mesma fita (dilata e volta)
    g = conteudo.copy()
    for _ in range(2):
        g[:-1] |= g[1:]; g[1:] |= g[:-1]
        g[:, :-1] |= g[:, 1:]; g[:, 1:] |= g[:, :-1]

    rot, n = rotular(g)
    pecas = []
    for i in range(1, n+1):
        ys, xs = np.where(rot == i)
        if len(ys) < AREA_MINIMA:
            continue
        pecas.append((len(ys), ys.min(), ys.max(), xs.min(), xs.max()))
    pecas.sort(key=lambda p: -p[0])          # maiores primeiro
    if quantas:
        pecas = pecas[:quantas]
    pecas.sort(key=lambda p: (p[1], p[3]))   # de volta a ordem da folha
    for k, (_, ymin, ymax, xmin, xmax) in enumerate(pecas, 1):
        y0, y1 = max(ymin-MARGEM, 0), min(ymax+1+MARGEM, a.shape[0])
        x0, x1 = max(xmin-MARGEM, 0), min(xmax+1+MARGEM, a.shape[1])
        alfa = (conteudo[y0:y1, x0:x1] * 255).astype(np.uint8)
        Image.fromarray(np.dstack([a[y0:y1, x0:x1], alfa]), 'RGBA').save(
            os.path.join(saida, '%s-%02d.png' % (prefixo, k)))
    print('recortadas:', len(pecas), '->', saida)
    return 0

if __name__ == '__main__':
    sys.exit(main())
