"""Write <data-dir>/sources/sources_manifest.json: file, URL, retrieval timestamp, sha256, byte size for every source file.

URLs come from (1) CMS landing pages saved as p_*.html next to the downloads (href="/files/zip/..."), and
(2) an optional tab-separated fetch log (--fetch-log; columns: retrieved_iso, url, filename) for files fetched elsewhere.
Retrieval time defaults to file mtime (curl without -R writes download time). Symlinks are resolved and hashed.
"""
import argparse, datetime, glob, hashlib, json, os, re
from qad.research_tools.ma_enrollment import analysis as A

def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b''): h.update(chunk)
    return h.hexdigest()

def mtime(path):
    return datetime.datetime.fromtimestamp(os.path.getmtime(path)).astimezone().isoformat(timespec='seconds')

def landing_urls(src):
    urls = {}
    for h in glob.glob(os.path.join(src, '**', 'p_*.html'), recursive=True):
        for z in re.findall(r'href="(/files/zip/[^"]+\.zip)"', open(h, errors='ignore').read()):
            urls[os.path.basename(z)] = 'https://www.cms.gov' + z
    return urls

def build(src, fetch_log=None):
    log = {}
    if fetch_log:
        for line in open(fetch_log):
            p = line.rstrip('\n').split('\t')
            if len(p) >= 3: log[os.path.basename(p[2])] = (p[0], p[1])
    land = landing_urls(src); items = []
    for f in sorted(glob.glob(os.path.join(src, '**', '*'), recursive=True)):
        if os.path.isdir(f) or f.endswith(('.html', 'sources_manifest.json')): continue
        real = os.path.realpath(f); b = os.path.basename(f)
        it = dict(file=os.path.relpath(f, src), sha256=sha256(real), bytes=os.path.getsize(real))
        if real != os.path.abspath(f): it['resolves_to'] = real
        if b in log: it.update(retrieved=log[b][0], url=log[b][1])
        elif f.endswith('.zip'): it.update(retrieved=mtime(f), url=land.get(b))
        items.append(it)
    return items

def main(argv=None):
    ap = argparse.ArgumentParser(description='Build sources_manifest.json')
    ap.add_argument('--data-dir'); ap.add_argument('--fetch-log', help='optional TSV: retrieved_iso, url, filename')
    a = ap.parse_args(argv); A.configure(a.data_dir)
    items = build(A.SRC, a.fetch_log)
    json.dump(dict(generated=datetime.datetime.now().astimezone().isoformat(timespec='seconds'), files=items),
              open(os.path.join(A.SRC, 'sources_manifest.json'), 'w'), indent=1)
    print(len(items), 'files;', sum(1 for i in items if i['file'].endswith('.zip') and not i.get('url')), 'zips without URL')

if __name__ == '__main__':
    main()
