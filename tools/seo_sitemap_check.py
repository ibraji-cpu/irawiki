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

missing = sorted(u for u in html if u not in locs)
extra = sorted(u for u in locs if not u.endswith('.xml') and u.rstrip('/') + '.html' not in html and u.rstrip('/') != 'https://wiki.iraamalia.id')
print('sitemap locs:', len(locs))
print('html pages:', len(html))
print('missing from sitemap:', len(missing))
for u in missing[:15]:
    print('  -', u)
print('locs without html:', len(extra))
for u in extra[:10]:
    print('  ?', u)
