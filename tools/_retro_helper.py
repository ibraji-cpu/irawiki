"""Helper retrofit playbook: edit bertarget dengan assert."""
from pathlib import Path

ROOT = Path("/home/ubuntu/irawiki")


def rep(path, pairs):
    p = Path(path)
    if not p.is_absolute():
        p = ROOT / p
    t = p.read_text(encoding="utf-8")
    for old, new in pairs:
        n = t.count(old)
        if n != 1:
            raise SystemExit(f"ANCHOR {n}x di {p.name}: {old[:90]!r}")
        t = t.replace(old, new, 1)
    p.write_text(t, encoding="utf-8")
    return p


def ins_before(path, anchor, block):
    return rep(path, [(anchor, block + anchor)])


def ins_after(path, anchor, block):
    return rep(path, [(anchor, anchor + block)])


def touch_fm(path, date="2026-10-20"):
    p = Path(path)
    if not p.is_absolute():
        p = ROOT / p
    lines = p.read_text(encoding="utf-8").splitlines(keepends=True)
    out = []
    for ln in lines:
        if ln.startswith("updated:"):
            out.append(f"updated: '{date}'\n")
        elif ln.startswith("last_updated:"):
            out.append(f'last_updated: "{date}"\n')
        else:
            out.append(ln)
    p.write_text("".join(out), encoding="utf-8")
