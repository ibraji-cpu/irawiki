#!/usr/bin/env python3
"""Autolink wiki — versi perbaikan (idempoten).

Perbaikan dari versi lama:
  1. HANYA body yang diproses (frontmatter tidak pernah disentuh).
  2. Satu-pass: teks dipecah pada link/kode yang sudah ada, hanya segmen
     teks biasa yang diproses -> tidak mungkin menghasilkan nesting [[[[.
  3. Hanya menautkan target yang BENAR-BENAR ada (slug atau alias di frontmatter)
     -> tidak menghasilkan 404.
  4. Hanya kemunculan PERTAMA tiap entitas per file (gaya Wikipedia).
  5. Lewati self-link, heading, code block, inline code, URL, markdown link.

Pemakaian:
  python3 autolink_wiki.py --dry-run
  python3 autolink_wiki.py --apply
"""
import os
import re
import sys
import yaml

CONTENT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "content")
FM_RE = re.compile(r"^(---\r?\n.*?\r?\n---\r?\n?)(.*)$", re.DOTALL)

# Segmen yang dilindungi: tidak boleh ditautkan
PROTECT_RE = re.compile(
    r"```.*?```"          # code block
    r"|`[^`\n]*`"         # inline code
    r"|\[\[[^\]]*\]\]"    # wiki link yang sudah ada
    r"|\[[^\]\n]*\]\([^)\n]*\)"  # markdown link
    r"|https?://\S+"      # URL
    r"|^\s{0,3}#{1,6}\s.*$",     # heading
    re.DOTALL | re.MULTILINE,
)


def split_fm(txt):
    m = FM_RE.match(txt)
    return (m.group(1), m.group(2)) if m else ("", txt)


def load_entities():
    """slug -> (title, aliases) dan peta term-lower -> slug."""
    entities = {}
    by_term = {}
    for root, _d, files in os.walk(CONTENT):
        for fn in files:
            if not fn.endswith(".md") or fn.lower() == "index.md":
                continue
            slug = fn[:-3]
            with open(os.path.join(root, fn), encoding="utf-8") as f:
                txt = f.read()
            fm, _ = split_fm(txt)
            meta = {}
            if fm:
                try:
                    meta = yaml.safe_load(fm.strip().strip("-").strip()) or {}
                except Exception:
                    meta = {}
            terms = set()
            title = meta.get("title")
            if isinstance(title, str) and title.strip():
                terms.add(title.strip())
            aliases = meta.get("aliases") or []
            if isinstance(aliases, list):
                for a in aliases:
                    if isinstance(a, str) and a.strip() and not a.strip().startswith("/"):
                        terms.add(a.strip())
            # nama file dengan spasi juga dianggap nama
            terms.add(slug.replace("-", " "))
            entities[slug] = terms
            for t in terms:
                key = t.lower()
                # jangan override term yang sudah punya slug lain (hindari ambiguitas)
                if key not in by_term or by_term[key] == slug:
                    by_term[key] = slug
    return entities, by_term


def main():
    apply = "--apply" in sys.argv
    entities, by_term = load_entities()

    # hanya term yang >= 3 karakter, urut panjang -> pendek
    terms = sorted([t for t in by_term if len(t) > 2], key=len, reverse=True)
    if not terms:
        print("Tidak ada entitas.")
        return
    term_re = re.compile(
        r"(?<![A-Za-z0-9_])(" + "|".join(re.escape(t) for t in terms) + r")(?![A-Za-z0-9_])",
        re.IGNORECASE,
    )

    files_changed = 0
    links_added = 0
    samples = []

    for root, _d, files in os.walk(CONTENT):
        for fn in sorted(files):
            if not fn.endswith(".md") or fn.lower() == "index.md":
                continue
            path = os.path.join(root, fn)
            slug = fn[:-3]
            with open(path, encoding="utf-8") as f:
                txt = f.read()
            fm, body = split_fm(txt)
            if not body:
                continue

            # seed: entitas yang sudah punya link di body (idempoten + sekali per file)
            seen = set()
            for ex in re.findall(r"\[\[([^\]]+)\]\]", body):
                tgt = ex.split("|")[0].strip()
                seen.add(tgt)
            added = 0

            def do_segment(seg):
                nonlocal added
                def repl(m):
                    nonlocal added
                    matched = m.group(1)
                    target = by_term.get(matched.lower())
                    if not target or target == slug or target in seen:
                        return matched
                    seen.add(target)
                    added += 1
                    if len(samples) < 40:
                        samples.append((os.path.relpath(path, CONTENT), matched, target))
                    return f"[[{target}|{matched}]]"
                return term_re.sub(repl, seg)

            # pecah body pada segmen terproteksi
            out = []
            pos = 0
            for m in PROTECT_RE.finditer(body):
                out.append(do_segment(body[pos:m.start()]))
                out.append(m.group(0))
                pos = m.end()
            out.append(do_segment(body[pos:]))
            new_body = "".join(out)

            if new_body != body:
                files_changed += 1
                links_added += added
                if apply:
                    with open(path, "w", encoding="utf-8") as f:
                        f.write(fm + new_body)

    print(f"{'APPLIED' if apply else 'DRY-RUN'}: {files_changed} file, {links_added} link baru")
    print("=" * 70)
    for p, t, tgt in samples:
        print(f"  {p}: '{t}' -> [[{tgt}]]")


if __name__ == "__main__":
    main()
