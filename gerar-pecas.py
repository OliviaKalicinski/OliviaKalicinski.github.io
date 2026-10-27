#!/usr/bin/env python3
"""Lista as imagens que o board pode acrescentar ao mural."""
import json, os, glob
RAIZ = os.path.dirname(os.path.abspath(__file__))
PASTAS = ['img/recorte/*.png', 'img/pecas/*.webp', 'img/creators/*.jpg',
          'img/banana/*.jpg', 'img/banana/pdf/*.jpeg', 'img/pf/*.jpg',
          'img/lps/*.jpg', 'img/cdd/*.png', 'img/fitas/*.png',
          'img/clipes/*.png', 'img/*.png', 'img/*.jpg']
vistos, saida = set(), []
for padrao in PASTAS:
    for f in sorted(glob.glob(os.path.join(RAIZ, padrao))):
        rel = os.path.relpath(f, RAIZ)
        if rel in vistos or '/para-recortar/' in rel or '/tentativa-local/' in rel:
            continue
        vistos.add(rel)
        saida.append(rel)
with open(os.path.join(RAIZ, 'pecas-disponiveis.json'), 'w') as fh:
    json.dump(saida, fh, ensure_ascii=False, indent=1)
print('%d imagens' % len(saida))
