#!/usr/bin/env python3
"""Servidor local do site: serve os arquivos e grava o mural em layout.json."""
import json, os, datetime
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer

RAIZ = os.path.dirname(os.path.abspath(__file__))
BAK = os.path.join(RAIZ, 'layout-bak')

class H(SimpleHTTPRequestHandler):
    def __init__(self, *a, **kw):
        super().__init__(*a, directory=RAIZ, **kw)

    def do_POST(self):
        if self.path.rstrip('/') != '/salvar':
            self.send_error(404); return
        n = int(self.headers.get('Content-Length') or 0)
        corpo = self.rfile.read(n)
        try:
            dados = json.loads(corpo.decode('utf-8'))
        except Exception as e:
            self.send_error(400, str(e)); return
        os.makedirs(BAK, exist_ok=True)
        carimbo = datetime.datetime.now().strftime('%Y-%m-%d-%H%M%S')
        texto = json.dumps(dados, ensure_ascii=False, indent=1)
        with open(os.path.join(BAK, 'layout-%s.json' % carimbo), 'w') as f:
            f.write(texto)
        with open(os.path.join(RAIZ, 'layout.json'), 'w') as f:
            f.write(texto)
        r = json.dumps({'ok': True, 'em': carimbo}).encode()
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', str(len(r)))
        self.end_headers()
        self.wfile.write(r)

    def end_headers(self):
        self.send_header('Cache-Control', 'no-store')
        super().end_headers()

    def log_message(self, *a):
        pass

if __name__ == '__main__':
    import errno, sys
    try:
        s = ThreadingHTTPServer(('127.0.0.1', 4178), H)
    except OSError as e:
        if e.errno == errno.EADDRINUSE:
            print('O servidor ja esta rodando. Abra http://localhost:4178/index.html')
            print('Para derrubar o que esta na porta:  pkill -f serve.py')
            sys.exit(0)
        raise
    print('Site no ar: http://localhost:4178/index.html   (ctrl+c para parar)')
    try:
        s.serve_forever()
    except KeyboardInterrupt:
        print('\nparado')
