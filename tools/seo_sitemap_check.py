import os
import re

pub = '/home/ubuntu/irawiki/public'
sm = open(os.path.join(pub, 'sitemap.xml'), encoding='utf-8').read()
locs = set(re.findall(r'<loc>([^<]+)</loc>', sm))


def url_for(path):
    rel = os.path.relpath(path, pub)
    if rel == 'index.html':
        return 'https://wiki.iraamalia.id/'
    if rel.endswith('/index.html'):
        return 'https://wiki.iraamalia.id/' + rel[:-len('/index.html')] + '/'
    return 'https://wiki.iraamalia.id/' + rel[:-len('.html')]


html = []
for root, _, files in os.walk(pub):
    for f in files:
        if f.endswith('.html') and f != '404.html':
            html.append(url_for(os.path.join(root, f)))

# Quartz menulis loc tanpa trailing slash; html helper bisa menambahkannya.
def norm(u):
    return u.rstrip('/') or u

locs_n = {norm(u) for u in locs if not u.endswith('.xml')}
html_n = {norm(u) for u in html}

missing = sorted(u for u in html_n if u not in locs_n)
extra = sorted(u for u in locs_n if u not in html_n)
print('sitemap locs:', len(locs_n))
print('html pages:', len(html_n))
print('missing from sitemap:', len(missing))
for u in missing[:15]:
    print('  -', u)
print('locs without html:', len(extra))
for u in extra[:10]:
    print('  ?', u)
