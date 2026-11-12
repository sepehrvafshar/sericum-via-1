import re, base64, mimetypes, sys
site, out = sys.argv[1], sys.argv[2]
src = open(site + '/index.html', encoding='utf-8').read()

def sub(m):
    p = m.group(0)
    mt = mimetypes.guess_type(p)[0] or ('font/woff2' if p.endswith('.woff2') else 'application/octet-stream')
    return 'data:%s;base64,%s' % (mt, base64.b64encode(open(site + '/' + p, 'rb').read()).decode())

src = re.sub(r'assets/[^"&\s)]+', sub, src)
open(out, 'w', encoding='utf-8').write(src)
