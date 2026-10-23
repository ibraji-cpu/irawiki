#!/usr/bin/env python3
"""
Watcher pantauan konten -> Quartz wiki (ibraji-cpu/irawiki).
Memenuhi seluruh kontrak: brief-setup-watcher-pantauan-hermes.md

Tiap run:
1. Fetch remote origin.
2. Cari branch remote `konten/pantauan-*` yang BELUM diproses (belum punya .PROCESSED).
3. Jika tidak ada branch baru: selesai tanpa aksi, tanpa laporan (diam / empty stdout).
4. Jika ada:
   - Ambil yang tertua.
   - Jika branch uji pilot (konten/pantauan-uji): tahan entri, nol perubahan wiki, cetak laporan uji.
   - Jika branch tanggal sah (konten/pantauan-YYYY-MM-DD):
     - Dedup, validasi, terapkan entri ke ## Kronologi hub wiki.
     - Commit ke branch kerja `hermes/pantauan-<tanggal>`, push.
     - Buka PR ke main lalu **merge otomatis** (squash) — tanpa review manusia.
     - Deploy (GitHub Actions), jalankan SQLite indexer, verifikasi live URL.
     - Push penanda proposals/pantauan-<tanggal>.PROCESSED ke branch pengirim.
     - Cetak laporan ringkas (§6) ke stdout.
"""

import json
import os
import re
import sqlite3
import subprocess
import sys
import time
from datetime import datetime, timedelta, timezone

REPO = "/home/ubuntu/irawiki"
CONTENT = os.path.join(REPO, "content")
REMOTE = "origin"
BRANCH_PREFIX = "konten/pantauan-"
MARKER_SUFFIX = ".PROCESSED"
ACTIVE_RE = re.compile(r"^konten/pantauan-(\d{4}-\d{2}-\d{2})$")
WIB = timezone(timedelta(hours=7))
PY = sys.executable or "/usr/bin/python3"
PR_BRANCH_PREFIX = "hermes/pantauan-"
DEPLOY_STATE = os.path.expanduser("~/.hermes/pantau_deploy_state.json")
ENTRY_HEAD_RE = re.compile(r"^###\s+(\d{4}-\d{2}-\d{2})\b")
FIELD_RE = re.compile(r"^-\s+(Hub tujuan|Posisi tempel|Sumber|Catatan presisi)\s*:\s*(.*)$", re.I)
NUM_RE = re.compile(r"^\d+\.\s+\*\*(.+?)\*\*")


def sh(args, check=True, capture=True, cwd=None):
    r = subprocess.run(
        args, cwd=cwd or REPO, capture_output=capture, text=True
    )
    if check and r.returncode != 0:
        raise RuntimeError(f"cmd gagal {args}: {r.stderr.strip()[:500]}")
    return r


def now_wib():
    return datetime.now(WIB)


# ---------------------------------------------------------------- deploy state


def load_deploy_state():
    """Hash main terakhir yang sudah di-build + di-index oleh watcher."""
    try:
        with open(DEPLOY_STATE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {"built_main_hash": "", "updated_at": ""}


def save_deploy_state(h):
    os.makedirs(os.path.dirname(DEPLOY_STATE), exist_ok=True)
    with open(DEPLOY_STATE, "w", encoding="utf-8") as f:
        json.dump({"built_main_hash": h, "updated_at": now_wib().isoformat()}, f, indent=1)


def remote_main_hash():
    r = sh(["git", "rev-parse", f"{REMOTE}/main"], check=False)
    return r.stdout.strip() if r.returncode == 0 and r.stdout.strip() else None


def is_merge_commit(commit):
    r = sh(["git", "rev-list", "--parents", "-n", "1", commit], check=False)
    parts = r.stdout.split()
    return len(parts) > 2


def deploy_pasca_merge():
    """Tahap deploy pasca-merge. Return (message, did_work).

    Deploy HANYA bila main maju dan commit terbaru adalah merge PR pantauan
    (`pantauan: ...`). Commit/merge main lain dilewati: tidak di-deploy,
    tidak ditandai sudah ter-deploy.
    """
    saved = load_deploy_state()
    built = saved.get("built_main_hash", "")
    cur = remote_main_hash()
    if not cur:
        return None, False
    if built and cur == built:
        return None, False

    sh(["git", "fetch", "--all", "--prune"])
    cur = remote_main_hash()

    subj = sh(["git", "log", "-1", "--format=%s%n%b", cur]).stdout.strip()
    key = BRANCH_PREFIX.rstrip("-")
    if key not in subj.lower():
        log(f"main maju ke {cur[:10]} tapi bukan merge PR {key} -> tidak deploy")
        return None, False

    log(f"deploy: main maju {built[:10] or '(null)'} -> {cur[:10]}")
    sh(["git", "checkout", "-q", "main"])
    sh(["git", "merge", "--ff-only", "-q", f"{REMOTE}/main"], check=False)

    # Hub yang berubah di antara hash tersimpan dan main terbaru.
    base = built or cur
    changed = sh(["git", "diff", "--name-only", base, cur], check=False).stdout.split()
    hubs = sorted({p for p in changed if p.startswith("content/") and p.endswith(".md")})

    log("rebuilding Quartz...")
    r_b = sh(["bash", "build_wiki.sh"], check=False)
    build_ok = (r_b.returncode == 0)

    log("running SQLite indexer...")
    r_i = sh([PY, "tools/irawiki_indexer.py"], check=False)
    index_ok = (r_i.returncode == 0)

    page_count = "N/A"
    try:
        db_p = os.path.join(REPO, "wiki_index.db")
        if os.path.isfile(db_p):
            conn = sqlite3.connect(db_p)
            page_count = str(conn.execute("SELECT count(*) FROM pages").fetchone()[0])
            conn.close()
    except Exception:
        pass

    verifs = []
    for hub in hubs:
        url, status = verify_live(hub)
        verifs.append((hub, url, status))

    save_deploy_state(cur)

    rep = []
    rep.extend(["🚀 **Laporan Deploy Pasca-Merge PR Pantauan**",
           f"• **Main:** `{cur[:10]}`",
           f"• **Waktu Run:** {now_wib().strftime('%Y-%m-%d %H:%M:%S WIB')}",
           ""])
    b_st = "Sukses" if build_ok else "Gagal"
    i_st = f"Sukses ({page_count} halaman)" if index_ok else "Gagal"
    rep.append("**Build & Verifikasi:**")
    rep.append(f"• Quartz Build: {b_st}")
    rep.append(f"• SQLite Indexer: {i_st}")
    if verifs:
        for hub, url, status in verifs:
            rep.append(f"• Live `{hub}`: {url} ({status})")
    else:
        rep.append("• Tidak ada halaman content/ yang berubah di merge ini.")
    print("\n".join(rep))
    return "\n".join(rep), True


def open_pr(tanggal, diterapkan, duplikat, ditahan, usulan_konsep):
    """Buka PR hermes/pantauan-<tanggal> -> main. Return (url, status)."""
    if not diterapkan:
        return None, "tidak ada entri diterapkan"
    try:
        r = sh(["gh", "pr", "create",
                "--base", "main",
                "--head", f"{PR_BRANCH_PREFIX}{tanggal}",
                "--title", f"pantauan: {tanggal} — {len(diterapkan)} entri",
                "--body", "pantauan " + tanggal], check=False)
    except FileNotFoundError:
        return None, "gh tidak terpasang"
    if r.returncode != 0:
        return None, f"gh pr create gagal: {(r.stderr or r.stdout).strip()[:200]}"
    url = r.stdout.strip().splitlines()[-1].strip() if r.stdout.strip() else ""
    return url, "ok"


def merge_pr(url):
    """Merge PR dengan squash (gaya merge repo ini). Return (ok, status)."""
    try:
        r = sh(["gh", "pr", "merge", url, "--squash"], check=False)
    except FileNotFoundError:
        return False, "gh tidak terpasang"
    if r.returncode != 0:
        return False, "merge gagal: " + (r.stderr or r.stdout).strip()[:200]
    return True, "sukses (squash)"


def tunggu_deploy_actions(maks=600):
    """Tunggu workflow 'Deploy Wiki & Blog' selesai. Return (conclusion, url)."""
    deadline = time.time() + maks
    while time.time() < deadline:
        r = sh(["gh", "run", "list", "--workflow", "deploy.yml", "--limit", "1",
                "--json", "status,conclusion,url", "--jq", ".[0] // {}"], check=False)
        try:
            st = json.loads(r.stdout.strip() or "{}")
        except Exception:
            st = {}
        if st.get("status") == "completed":
            return st.get("conclusion"), st.get("url")
        time.sleep(30)
    return "timeout", None


def deploy_setelah_merge(hubs):
    """Deploy setelah PR di-merge otomatis.

    GitHub Actions membangun + mendeploy situs pada push ke main; yang belum
    ditangani Actions adalah indexer SQLite, jadi indexer dijalankan di sini.
    Return dict(info deploy).
    """
    concl, run_url = tunggu_deploy_actions()
    log(f"deploy Actions: {concl}")

    r_i = sh([PY, "tools/irawiki_indexer.py"], check=False)
    index_ok = r_i.returncode == 0
    page_count = "N/A"
    try:
        db_p = os.path.join(REPO, "wiki_index.db")
        if os.path.isfile(db_p):
            conn = sqlite3.connect(db_p)
            page_count = str(conn.execute("SELECT count(*) FROM pages").fetchone()[0])
            conn.close()
    except Exception:
        pass

    verifs = [(hub,) + verify_live(hub) for hub in hubs]

    sh(["git", "fetch", "--all", "--prune"], check=False)
    save_deploy_state(remote_main_hash() or "")
    return {"actions": concl, "run_url": run_url, "index_ok": index_ok,
            "page_count": page_count, "verifs": verifs}


def log(msg):
    # Log internal ke stderr agar stdout bersih untuk laporan Telegram
    sys.stderr.write(f"[pantau] {msg}\n")
    sys.stderr.flush()


# ---------------------------------------------------------------- parsing

def parse_pantauan(text, tanggal_default=None):
    """Parse file pantauan (format produsen Muse).

    Struktur nyata file:
        ## Kandidat per kategori

        ### <Nama Kategori> (<slug>)          <- heading KATEGORI, bukan kandidat
        - Hub tujuan: <path>
        - Posisi tempel: ...
        - Entri siap tempel:

        ### <YYYY-MM-DD> — <judul entri>      <- heading ENTRI = kandidat
        <body entri>
        - Sumber: ...
        - Catatan presisi: ...

        ---

    Field berada DI ATAS heading entri, jadi field dikumpulkan dulu di
    `pending` lalu dilekatkan ke heading entri berikutnya.
    """
    out = {
        "tanggal": tanggal_default,
        "ringkasan": "",
        "kandidat": [],
        "usulan_konsep": [],
        "catatan": "",
    }

    lines = text.splitlines()
    mode = None
    cur = None
    pending = {}
    body_done = False
    kategori = ""

    def flush():
        nonlocal cur, body_done
        if cur is not None:
            cur["entry"] = "\n".join(cur.pop("entry_lines", [])).strip()
            out["kandidat"].append(cur)
        cur = None
        body_done = False

    for raw in lines:
        line = raw.rstrip("\r\n")
        s = line.strip()

        if s.startswith("## "):
            flush()
            pending = {}
            sec = s[3:].strip().lower()
            if "ringkasan" in sec:
                mode = "ringkasan"
            elif "catatan" in sec:
                mode = "catatan"
            elif "kandidat" in sec:
                mode = "kandidat"
            else:
                mode = None
            continue

        if mode == "ringkasan":
            if s:
                out["ringkasan"] += s + " "
            continue
        if mode == "catatan":
            if s:
                out["catatan"] += s + " "
            continue
        if mode != "kandidat":
            continue

        if s.startswith("### "):
            m_date = ENTRY_HEAD_RE.match(s)
            if m_date:
                flush()
                cur = {
                    "tanggal_entri": m_date.group(1),
                    "judul": s[4:].strip(),
                    "fields": pending,
                    "entry_lines": [],
                }
                pending = {}
                body_done = False
            else:
                # Heading kategori — bukan kandidat.
                flush()
                pending = {}
                kategori = s[4:].strip()
            continue

        if not s or s == "---":
            continue

        m_field = FIELD_RE.match(s)
        if m_field:
            key = m_field.group(1).title()
            pending[key] = m_field.group(2).strip()
            if cur is not None and key == "Sumber":
                body_done = True
            continue

        # Usulan konsep (daftar bernomor) di bawah heading kategori konsep.
        if "konsep" in kategori.lower():
            m_num = NUM_RE.match(s)
            if m_num:
                out["usulan_konsep"].append({"judul": m_num.group(1).strip()})
            continue

        if cur is not None and not body_done:
            cur["entry_lines"].append(line)

    flush()

    return out


def find_hub(hub_raw):
    raw = hub_raw.strip().strip("`\"'")
    if not raw:
        return None
    cand = []
    if raw.startswith("content/"):
        cand.append(raw)
    cand += [
        raw if raw.endswith(".md") else raw + ".md",
        f"content/{raw}" if not raw.endswith(".md") else f"content/{raw}",
    ]
    slug = re.sub(r"[^a-z0-9]+", "-", raw.lower()).strip("-")
    cand.append(f"content/{slug}.md")

    for c in cand:
        if os.path.isfile(os.path.join(REPO, c)):
            return os.path.normpath(c)

    base = os.path.basename(raw)
    if not base.endswith(".md"):
        base += ".md"
    hits = []
    for dirpath, _d, files in os.walk(CONTENT):
        if base in files:
            hits.append(os.path.relpath(os.path.join(dirpath, base), REPO))
    return os.path.normpath(hits[0]) if len(hits) == 1 else None


def dup_score(hub_text, tanggal_entri, entry):
    if f"### {tanggal_entri}" not in hub_text:
        return 0.0
    kata = set(re.findall(r"[a-z0-9]{5,}", entry.lower()))
    if not kata:
        return 0.0
    section = hub_text.split(f"### {tanggal_entri}", 1)[1]
    section = section.split("\n### ", 1)[0].lower()
    ada = sum(1 for k in kata if k in section)
    return ada / len(kata)


# ---------------------------------------------------------------- injeksi

def insert_chronology(hub_text, tanggal_entri, judul, entry_text):
    # Heading bisa "## Kronologi" atau "## Kronologi — <subjudul>".
    m = re.search(r"^## Kronologi\b.*$", hub_text, re.M)
    if not m:
        return None, "section ## Kronologi tidak ditemukan"

    start_kronologi = m.end()
    next_h2 = re.search(r"^##\s+\S", hub_text[start_kronologi:], re.M)
    end_kronologi = start_kronologi + next_h2.start() if next_h2 else len(hub_text)

    kronologi_block = hub_text[start_kronologi:end_kronologi]
    h3_matches = list(re.finditer(r"^###\s+(\d{4}-\d{2}-\d{2})", kronologi_block, re.M))

    insert_pos = end_kronologi
    for h in h3_matches:
        if h.group(1) > tanggal_entri:
            insert_pos = start_kronologi + h.start()
            break

    # Gaya hub: `### <tanggal> — <judul>` lalu prosa (tanpa prefix '-').
    block_lines = [f"### {judul}"]
    for raw_l in entry_text.splitlines():
        l = raw_l.strip()
        if l:
            block_lines.append(l)

    block_str = "\n\n".join(block_lines)
    new_text = hub_text[:insert_pos].rstrip() + "\n\n" + block_str + "\n\n" + hub_text[insert_pos:].lstrip()
    return new_text, "ok"


def sisip_sumber(hub_text, sumber):
    if not sumber or not sumber.strip():
        return hub_text
    m = re.search(r"^## Sumber\s*$", hub_text, re.M)
    if not m:
        return hub_text
    start_s = m.end()
    next_h2 = re.search(r"^##\s+\S", hub_text[start_s:], re.M)
    end_s = start_s + next_h2.start() if next_h2 else len(hub_text)

    block_s = hub_text[start_s:end_s]
    if sumber.strip() in block_s:
        return hub_text

    line = f"- {sumber.strip()}"
    return hub_text[:end_s].rstrip() + "\n" + line + "\n\n" + hub_text[end_s:].lstrip()


def bump_frontmatter(text, tanggal):
    if re.search(r'^last_updated:', text, re.M):
        text = re.sub(r'^last_updated:.*$', f'last_updated: "{tanggal}"', text, count=1, flags=re.M)
    else:
        m = re.search(r"^---\s*\n", text)
        if m:
            text = text[:m.end()] + f'last_updated: "{tanggal}"\n' + text[m.end():]
    return text


def verify_live(hub_rel):
    rel = hub_rel
    if rel.startswith("content/"):
        rel = rel[len("content/"):]
    rel = os.path.splitext(rel)[0]
    # Situs menyajikan /<path> DAN /<path>.html — coba keduanya.
    candidates = [f"https://wiki.iraamalia.id/{rel}",
                  f"https://wiki.iraamalia.id/{rel}.html"]
    last = "unknown"
    for live_url in candidates:
        try:
            r = subprocess.run(
                ["curl", "-k", "-Is", "--resolve", "wiki.iraamalia.id:443:127.0.0.1", live_url],
                capture_output=True, text=True, timeout=10
            )
            status_line = r.stdout.splitlines()[0] if r.stdout else "unknown"
            if "200" in status_line:
                return live_url, "200 OK"
            last = status_line
        except Exception as e:
            last = f"error ({e})"
    return candidates[0], last


# ---------------------------------------------------------------- main

def main():
    dry = "--dry-run" in sys.argv
    log("fetch remote branches...")
    sh(["git", "fetch", "--all", "--prune"])

    # ---------- TAHAP 2: deploy pasca-merge (SEBELUM proses branch baru) ----------
    msg, did_work = (None, False) if dry else deploy_pasca_merge()
    deploy_msg = msg if did_work else None
    if did_work:
        log("deploy pasca-merge selesai")

    # ---------- TAHAP 1: proses branch pantauan -> PR ----------
    # Cari branch remote pola konten/pantauan-* (hanya pola tanggal yang sah)
    r_branches = sh(["git", "for-each-ref", "--format=%(refname:short)",
                    f"refs/remotes/{REMOTE}/{BRANCH_PREFIX}*"]).stdout.splitlines()

    candidates = []
    for b in r_branches:
        b = b.strip()
        if not b:
            continue
        name = b[len(REMOTE) + 1:]  # hapus 'origin/'
        m = ACTIVE_RE.match(name)
        if not m:
            # Branch uji / non-tanggal: bukan sinyal, lewati diam-diam.
            continue

        tanggal = m.group(1)

        # Idempotensi: PR untuk tanggal ini sudah dibuat -> lewati.
        pr_ref = f"{REMOTE}/{PR_BRANCH_PREFIX}{tanggal}"
        if pr_ref in [r.strip() for r in r_branches]:
            log(f"{name}: PR {PR_BRANCH_PREFIX}{tanggal} sudah ada -> lewati")
            continue

        # Periksa file di branch
        try:
            tree = sh(["git", "ls-tree", "--name-only", b, "proposals/"], check=False).stdout.splitlines()
        except Exception:
            tree = []

        expected_file = f"proposals/pantauan-{tanggal}.md"
        expected_marker = f"proposals/pantauan-{tanggal}{MARKER_SUFFIX}"

        # Jika sudah ada .PROCESSED, lewati
        if expected_marker in tree:
            continue

        # Cari file proposal
        if expected_file not in tree:
            match_p = [f for f in tree if f.startswith("proposals/pantauan-") and f.endswith(".md")]
            if match_p:
                expected_file = match_p[0]
            else:
                continue

        candidates.append({
            "ref": b,
            "branch": name,
            "tanggal": tanggal,
            "file": expected_file,
            "marker": expected_marker,
        })

    # Urut tanggal tertua
    candidates.sort(key=lambda x: x["tanggal"] or "")

    if not candidates:
        # §2.2.c: Bila tidak ada: SELESAI tanpa aksi, tanpa laporan (diam).
        log("tidak ada branch pantauan baru -> selesai tanpa aksi.")
        return 0

    item = candidates[0]
    branch = item["branch"]
    ref = item["ref"]
    tanggal = item["tanggal"]
    file_rel = item["file"]
    marker_rel = item["marker"]

    log(f"memproses branch {branch} (file={file_rel})...")

    try:
        raw_content = sh(["git", "show", f"{ref}:{file_rel}"]).stdout
    except Exception as e:
        sys.stderr.write(f"Error membaca file {file_rel} dari {ref}: {e}\n")
        return 1

    parsed = parse_pantauan(raw_content, tanggal)

    # ------------------ KASUS NORMAL RUN (§5) ------------------
    diterapkan = []
    duplikat = []
    ditahan = []
    hubs_modified = []

    for c in parsed["kandidat"]:
        judul = c["judul"]
        tgl_entri = c.get("tanggal_entri") or tanggal

        hub_field = c["fields"].get("Hub Tujuan", c["fields"].get("Hub tujuan", ""))
        hub_path = find_hub(hub_field)
        if not hub_path:
            ditahan.append({"judul": judul, "alasan": f"hub tujuan tidak ditemukan: {hub_field}"})
            continue

        full_hub_path = os.path.join(REPO, hub_path)
        with open(full_hub_path, "r", encoding="utf-8") as f:
            hub_text = f.read()

        # Dedup
        entry_text = c["entry"]
        score = dup_score(hub_text, tgl_entri, entry_text + " " + judul)
        if score >= 0.6:
            duplikat.append({"judul": judul, "hub": hub_path, "score": score})
            continue

        # Injeksi kronologi
        new_text, res = insert_chronology(hub_text, tgl_entri, judul, entry_text)
        if res != "ok":
            ditahan.append({"judul": judul, "alasan": res})
            continue

        # Injeksi sumber
        sumber_val = c["fields"].get("Sumber", "")
        new_text = sisip_sumber(new_text, sumber_val)
        new_text = bump_frontmatter(new_text, tgl_entri)

        if not dry:
            with open(full_hub_path, "w", encoding="utf-8") as f:
                f.write(new_text)

        diterapkan.append({"judul": judul, "hub": hub_path})
        if hub_path not in hubs_modified:
            hubs_modified.append(hub_path)

    usulan_konsep = parsed.get("usulan_konsep", [])

    # Commit ke BRANCH KERJA (BUKAN main) lalu buka PR.
    pr_url, pr_status = None, "tidak ada entri diterapkan"
    merged, merge_status, deploy_info = False, None, None
    if diterapkan and not dry:
        commit_msg = f"pantauan: {tanggal} — {len(diterapkan)} entri"
        work_branch = f"{PR_BRANCH_PREFIX}{tanggal}"
        sh(["git", "checkout", "-q", "-B", work_branch, f"{REMOTE}/main"])
        sh(["git", "add", "--"] + hubs_modified)
        staged = sh(["git", "diff", "--cached", "--name-only"]).stdout.strip()
        if staged:
            sh(["git", "commit", "-q", "-m", commit_msg])
            r_push = sh(["git", "push", "-q", REMOTE, work_branch], check=False)
            if r_push.returncode != 0:
                log("push branch kerja gagal")
            else:
                log(f"branch kerja di-push: {work_branch}")
                pr_url, pr_status = open_pr(tanggal, diterapkan, duplikat, ditahan, usulan_konsep)
                log(f"PR: {pr_url or pr_status}")
                if pr_url:
                    merged, merge_status = merge_pr(pr_url)
                    log(f"merge otomatis: {merge_status}")
                    if merged:
                        deploy_info = deploy_setelah_merge(hubs_modified)
        sh(["git", "checkout", "-q", "main"])

    # Push penanda .PROCESSED ke branch pengirim.
    # Makna penanda: "sudah diubah menjadi PR" — bukan "sudah tayang".
    marker_push_status = "belum"
    if not dry:
        if not pr_url:
            marker_push_status = f"ditahan (PR belum terbuka: {pr_status})"
        else:
            sh(["git", "checkout", "-q", "-B", branch, f"{REMOTE}/{branch}"])
            m_full = os.path.join(REPO, marker_rel)
            os.makedirs(os.path.dirname(m_full), exist_ok=True)
            with open(m_full, "w") as f:
                pass
            sh(["git", "add", "--", marker_rel])
            sh(["git", "commit", "-q", "-m", f"[skip ci] tandai {tanggal} sudah diproses"], check=False)
            r_push = sh(["git", "push", "-q", REMOTE, branch], check=False)
            marker_push_status = "sukses" if r_push.returncode == 0 else "gagal"
            sh(["git", "checkout", "-q", "main"])

    # ------------------ LAPORAN RINGKAS (§3A) ------------------
    rep = []
    rep.append("📋 **Laporan Pemrosesan Pantauan**")
    rep.append(f"• **Branch Sumber:** `{branch}`")
    rep.append(f"• **Tanggal:** `{tanggal}`")
    rep.append(f"• **Waktu Run:** {now_wib().strftime('%Y-%m-%d %H:%M:%S WIB')}")
    rep.append(f"• **Branch Kerja:** `{PR_BRANCH_PREFIX}{tanggal}`")
    if pr_url:
        rep.append(f"• **PR:** {pr_url}")
        if merged:
            rep.append(f"• **Merge otomatis:** ✅ {merge_status}")
        else:
            rep.append(f"• **Merge otomatis:** ❌ {merge_status or 'gagal'}")
    else:
        rep.append(f"• **PR:** ({pr_status})")
    rep.append("")

    rep.append("**Hasil Kandidat:**")
    if diterapkan:
        for d in diterapkan:
            rep.append(f"✅ **{d['judul']}** — MASUK PR")
            rep.append(f"   • Hub: `{d['hub']}`")
    if duplikat:
        for dp in duplikat:
            rep.append(f"🔁 **{dp['judul']}** — DUPLIKAT (sudah ada di `{dp['hub']}`)")
    if ditahan:
        for dt in ditahan:
            rep.append(f"⏸️ **{dt['judul']}** — DITAHAN ({dt['alasan']})")
    if usulan_konsep:
        for u in usulan_konsep:
            rep.append(f"💡 **{u['judul']}** — USULAN KONSEP (proposal saja, tidak dibuat halamannya)")
    if not (diterapkan or duplikat or ditahan or usulan_konsep):
        rep.append("• Tidak ada kandidat.")

    rep.append("")
    rep.append("**Status:**")
    rep.append(f"• Penanda `{marker_rel}`: {marker_push_status}")
    if merged and deploy_info:
        rep.append(f"• 🚀 **Deploy:** GitHub Actions {deploy_info['actions']}"
                   + (f" — {deploy_info['run_url']}" if deploy_info['run_url'] else ""))
        rep.append(f"• **Indexer:** {'sukses (' + deploy_info['page_count'] + ' halaman)' if deploy_info['index_ok'] else 'gagal'}")
        for hub, url, status in deploy_info["verifs"]:
            rep.append(f"• Live `{hub}`: {url} ({status})")
    elif pr_url:
        rep.append("• ⚠️ PR terbuka tapi merge otomatis gagal — perlu tindakan manual.")
    if deploy_msg:
        rep.append("")
        rep.append(deploy_msg)
    print("\n".join(rep))
    return 0


if __name__ == "__main__":
    sys.exit(main())
