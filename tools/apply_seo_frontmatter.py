#!/usr/bin/env python3
"""One-shot SEO metadata pass over content/*.md.

Adds (only when missing):
  description: 1-2 sentence human summary — manual dict for priority pages,
               derived from each page's own opening paragraph otherwise.
  date:        publication date from first git commit of the file.
  updated:     last git commit date of the file.

Never touches body text. Validates YAML of every edited file.
Usage: python3 tools/apply_seo_frontmatter.py [--dry-run]
"""
import os
import re
import subprocess
import sys

import yaml

REPO = "/home/ubuntu/irawiki"
CONTENT = os.path.join(REPO, "content")
DRY = "--dry-run" in sys.argv
REGEN = "--regen-auto" in sys.argv or "--regen-all" in sys.argv
REGEN_ALL = "--regen-all" in sys.argv
GENERIC = "halaman rujukan singkat di wiki politik Indonesia"

D = {
    # --- hub / root pages ---
    "index": "Personal wiki Ira Amalia: ringkasan aktor politik Indonesia, relasi kuasa, kronologi kebijakan, dan analisis isu 2025–2026.",
    "iraamalia-id": "iraamalia.id: platform media digital berbasis agen AI otonom yang memproduksi artikel, narasi audio, dan video investigatif vertikal.",
    "agrinas-palma-nusantara": "Agrinas Palma Nusantara mengelola 140.762,04 hektare kebun hasil penertiban Satgas PKH; status kepemilikan BUMN atau swasta belum terverifikasi.",
    "analisis-taktik-komunikasi-gksr-dalam-peluncuran-naskah-akademik-ruu-politik": "Analisis taktik komunikasi di balik peluncuran Naskah Akademik dan Draf RUU Politik versi GKSR pada Milad ke-1, 26 September 2026.",
    "gksr-gerakan-kedaulatan-suara-rakyat": "GKSR adalah koalisi delapan partai nonparlemen — Buruh, Ummat, Hanura, Perindo, PPP, PBB, PKN, Berkarya — yang menuntut perubahan sistem pemilu.",
    "kejaksaan-agung": "Kejaksaan Agung RI di bawah Jaksa Agung ST Burhanuddin; lokasi penyerahan tahap VIII Satgas PKH dan posisi Wakil Ketua I Pengarah.",
    "milad-ke-1-gksr-dan-peluncuran-naskah-akademik-ruu-politik-gksr": "Kronologi Milad ke-1 GKSR dan peluncuran Naskah Akademik serta Draf RUU Politik versi delapan partai nonparlemen, September 2026.",
    "perang-ultra-modern-dan-geopolitik": "Tipologi perang ultra modern — narasi, ekonomi, sumber daya — plus kronologi tekanan terhadap ekonomi Indonesia 2026 (MSCI, IHSG, DHE, DSI).",
    "reshuffle-kabinet-merah-putih": "Hub living document seluruh reshuffle Kabinet Merah Putih era Prabowo Subianto, berisi entri bertanggal dan halaman milestone pelantikan.",
    "satgas-pkh": "Satgas PKH adalah satgas lintas 12 kementerian/lembaga untuk menertibkan penguasaan kawasan hutan dan memulihkan penerimaan negara.",
    "sjafrie-sjamsoeddin": "Sjafrie Sjamsoeddin, Menteri Pertahanan RI 2024–sekarang dan Ketua Pengarah Satgas PKH.",
    "st-burhanuddin": "ST Burhanuddin, Jaksa Agung RI 2026–sekarang dan Wakil Ketua I Pengarah Satgas PKH.",
    "suyudi-ario-seto": "Suyudi Ario Seto, perwira tinggi Polri berlatar reserse; pernah Wakapolda Metro Jaya, Kapolda Banten, dan Kepala BNN; diusulkan sebagai calon tunggal Kapolri September 2026.",
    "update-raja-juli-antoni": "Catatan update Raja Juli Antoni, Menteri Kehutanan Republik Indonesia periode 2024–sekarang.",
    "uu-pelindungan-ketenagakerjaan-2026": "UU Pelindungan Ketenagakerjaan (23 bab, 313 pasal) disahkan DPR 6 Oktober 2026 sebagai tindak lanjut Putusan MK No. 168/PUU-XXI/2023.",
    # --- peristiwa ---
    "peristiwa/2026-10-01-reshuffle-kabinet-merah-putih": "Kronologi reshuffle 1 Oktober 2026 di Istana Negara: pelantikan menteri dan pejabat, termasuk pergeseran Listyo Sigit Prabowo ke Kepala Staf Kepresidenan.",
    "peristiwa/2026-10-02-pelantikan-wantimpres": "Kronologi pelantikan 26 anggota Wantimpres pada 2 Oktober 2026, dengan anggaran gaji sekitar Rp1,989 miliar per bulan menurut pemberitaan AFU.ID.",
    "peristiwa/2026-10-06-pengesahan-uu-pelindungan-ketenagakerjaan": "DPR mengesahkan RUU Pelindungan Ketenagakerjaan menjadi UU dalam paripurna 6 Oktober 2026: 23 bab, 313 pasal, lanjutan Putusan MK 168/PUU-XXI/2023.",
    "peristiwa/2026-10-06-penyerahan-tahap-viii-satgas-pkh": "Penyerahan Rp13,24 triliun hasil Satgas PKH tahap VIII dari Jaksa Agung ST Burhanuddin kepada Menteri Keuangan Suahasil Nazara, 6 Oktober 2026.",
    "peristiwa/2026-10-06-putusan-mk-phpu-ijazah-gibran": "Putusan MK Nomor 01/PHPU.PRES-XXIV/2026: permohonan sengketa ijazah Gibran tidak dapat diterima karena alasan prosedural.",
    "peristiwa/2026-10-15-pelantikan-pejabat": "Pelantikan sembilan pejabat oleh Presiden Prabowo pada 15 Oktober 2026: empat wakil menteri, Kepala BNPB, Kepala dan Wakil Kepala BPGMN, serta dua pejabat lain.",
    "peristiwa/36-tahun-humanika": "Catatan 36 tahun Humanika: perjumpaan para mantan demonstran dan maknanya bagi arah politik Indonesia.",
    "peristiwa/Haji Isam Sepakat Beli 30% Saham BYAN dari Low Tuck Kwong": "Low Tuck Kwong dan Elaine Low menjual 10.000.000.500 saham BYAN ke PT Jhonlin Baratama lewat CSPA 16 September 2026; Jhonlin akan memegang ~30% BYAN.",
    "peristiwa/Kepala Kantah Kabupaten Bogor Menjadi Tersangka": "Kronologi OTT KPK 14 September 2026 terkait dugaan suap HGB PT Summarecon Agung di Bogor dan penetapan delapan tersangka.",
    "peristiwa/Milad ke-1 GKSR dan Peluncuran Draf RUU Politik versi GKSR": "Delapan partai nonparlemen GKSR meluncurkan Naskah Akademik dan Draf RUU Pemilu/Politik versi mereka pada Milad ke-1 di DPP Partai Ummat.",
    "peristiwa/korupsi-di-indonesia": "Ringkasan sistemik korupsi di Indonesia pasca-reformasi 1998: kelahiran KPK, pasang surut pemberantasan, dan pola perkara besar.",
    "peristiwa/pencalonan-kapolri-2026": "Kronologi pencalonan Kapolri 2026: Surpres 30 September 2026 untuk memberhentikan Listyo Sigit Prabowo dan mengangkat Komjen Pol Suyudi Ario Seto.",
    "peristiwa/polemik-ijazah-gibran": "Hub polemik ijazah Gibran: gugatan perdata di PN Jakarta Pusat, sengketa syarat pendidikan di MK, dan putusan 01/PHPU.PRES-XXIV/2026.",
    "peristiwa/rencana-pengesahan-ruu-satu-data-indonesia-2026": "RUU Satu Data Indonesia (17 bab, 138 pasal) ditargetkan disahkan 6 Oktober 2026; mengatur Badan Satu Data Indonesia sebagai orkestrator tata kelola data.",
    "peristiwa/sengketa-ijazah-gibran-2026": "Kronologi gugatan syarat ijazah Gibran ke MK sejak 10 September 2026 hingga putusan Perkara 01/PHPU.PRES-XXIV/2026 pada 6 Oktober 2026.",
    "peristiwa/sepak-terjang-haji-isam": "Living document manuver korporasi Haji Isam/Jhonlin Group: aksi mega-akuisisi, transaksi pasar modal, dan ekspansi konglomerasi.",
    "peristiwa/soeharto-pahlawan-nasional": "Penganugerahan gelar Pahlawan Nasional kepada Soeharto lewat Keppres 116/TK/2025, polemik publik, dan gugatan PTUN atasnya.",
    "peristiwa/update-reshuffle-kabinet": "Catatan update untuk hub reshuffle Kabinet Merah Putih; menampung entri perubahan susunan kabinet terbaru.",
    # --- analisis ---
    "analisis/Dari 'Sembilan Naga' to 'Sembilan Haji'": "Analisis rumor akuisisi 62,25% saham Bayan Resources oleh Jhonlin Group dan pergeseran kekuatan bisnis dari 'Sembilan Naga' ke 'Sembilan Haji'.",
    "analisis/Di Balik Keceplosan Budi Arie dan Diamnya Jokowi": "Analisis psikologis wacana percepatan pemilu: membaca 'keceplosan' Budi Arie dan sikap diam Jokowi sebagai sinyal politik.",
    "analisis/Krisis Makna Subsidi Silang Pertamina Kelas Menangah": "Analisis kenaikan BBM nonsubsidi September 2026, kompensasi eksekutif BUMN, dan beban subsidi silang yang ditanggung kelas menengah.",
    "analisis/analisis-jokowi-ruu-satu-data": "Analisis relasi peran Jokowi dalam pengesahan RUU Satu Data Indonesia beserta posisi aktor yang terlibat.",
    "analisis/analisis-kepentingan-ruu-satu-data-indonesia": "Peta kepentingan aktor di balik RUU Satu Data Indonesia: DPR/Baleg sebagai inisiator, pemerintah sebagai penyelenggara, dan pemegang data.",
    "analisis/analisis-putusan-ptun-gelar-pahlawan-soeharto": "Analisis putusan PTUN Jakarta 50/G/2026/PTUN.JKT yang menyatakan gugatan pembatalan Keppres 116/TK/2025 tidak diterima, dan posisi hukum ahli waris.",
    "analisis/analisis-satgas-pkh-uang-vs-nilai": "Membaca angka Satgas PKH: ~Rp52 triliun kas dari delapan penyerahan versus klaim valuasi lahan hampir Rp400 triliun.",
    "analisis/hak-angket-ijazah-gibran": "Peluang dan hambatan hak angket ijazah Gibran di DPR setelah MK menolak permohonan 01/PHPU.PRES-XXIV/2026 secara prosedural.",
    "analisis/kpu-mk-syarat-pendidikan-gibran": "Membaca ujian integritas KPU dan MK dalam sengketa syarat pendidikan Gibran lewat siklus berpikir Ichsanuddin Noorsy.",
    # --- aktor paling dirujuk ---
    "aktor/prabowo-subianto": "Prabowo Subianto, Presiden Republik Indonesia 2024–sekarang; pusat jaringan kekuasaan pada reshuffle kabinet dan Satgas PKH.",
    "aktor/jhonlin-group": "Jhonlin Group: konglomerasi pertambangan dan infrastruktur milik Haji Isam, kuota produksi batubara sekitar 60 juta ton per tahun.",
    "aktor/gibran-rakabuming-raka": "Gibran Rakabuming Raka, Wakil Presiden RI 2024–sekarang; sorotan polemik syarat pendidikan dan ijazah pada Pilpres 2024.",
    "aktor/andi-syamsuddin-arsyad": "Profil Andi Syamsuddin Arsyad (Haji Isam), pengusaha Batulicin pemilik Jhonlin Group dan pihak di balik akuisisi 30% saham BYAN.",
    "aktor/joko-widodo": "Joko Widodo (Jokowi), Presiden RI ke-7 2014–2024; mantan Wali Kota Surakarta dan Gubernur DKI, kini aktor berpengaruh pasca-kepresidenan.",
    "aktor/dato-low-tuck-kwong": "Dato' Low Tuck Kwong, pendiri dan pemegang saham pengendali PT Bayan Resources Tbk (BYAN) yang menjual 30% saham ke Jhonlin.",
    "aktor/pt-jhonlin-baratama": "PT Jhonlin Baratama, kendaraan investasi Jhonlin Group yang membeli 30% saham BYAN lewat CSPA 16 September 2026.",
    "aktor/pt-bayan-resources-tbk": "PT Bayan Resources Tbk (BYAN): emiten batubara dalam daftar High Shareholding Concentration BEI, ~30% sahamnya dibeli Jhonlin Baratama.",
    "aktor/suhartoyo": "Suhartoyo, Ketua Mahkamah Konstitusi yang memimpin sidang putusan Perkara 01/PHPU.PRES-XXIV/2026.",
    "aktor/elaine-low": "Elaine Low, putri Dato' Low Tuck Kwong dan pemegang 22,002% saham BYAN per 31 Juli 2026; keluarga Low total 62,253%.",
    "aktor/dpr-ri": "DPR RI, lembaga legislatif yang membahas pengesahan UU Pelindungan Ketenagakerjaan, RUU Satu Data, dan uji kelayakan calon Kapolri.",
    "aktor/projo": "Projo, organisasi relawan politik pimpinan Budi Arie Setiadi; panggung wacana spekulatif percepatan pemilu.",
}


def git_dates(path):
    rel = os.path.relpath(path, REPO)
    first = subprocess.run(["git", "log", "--diff-filter=A", "--format=%ad", "--date=short", "--", rel],
                           cwd=REPO, capture_output=True, text=True).stdout.strip().splitlines()
    last = subprocess.run(["git", "log", "-1", "--format=%ad", "--date=short", "--", rel],
                          cwd=REPO, capture_output=True, text=True).stdout.strip()
    created = first[-1] if first else ""
    if not created:
        created = subprocess.run(["git", "log", "--format=%ad", "--date=short", "--", rel],
                                 cwd=REPO, capture_output=True, text=True).stdout.strip().splitlines()
        created = created[-1] if created else ""
    return created, last


def clean(s):
    s = re.sub(r"\[\[([^\]|]+)\|([^\]]+)\]\]", r"\2", s)
    s = re.sub(r"\[\[([^\]]+)\]\]", r"\1", s)
    s = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", s)
    s = re.sub(r"[*_`>#]", "", s)
    s = re.sub(r"\s+", " ", s).strip(" -–—:")
    return s


INFOBOX = re.compile(r"^[A-Za-z][\w ./&()'-]{1,30}:\s")


def first_para(body):
    blocks, buf = [], []
    for ln in body.split("\n"):
        t = ln.strip()
        if not t:
            if buf:
                blocks.append(buf)
                buf = []
            continue
        if t.startswith(("#", "|", "```", "<", "![", ">", "{{")):
            if buf:
                blocks.append(buf)
                buf = []
            continue
        buf.append(re.sub(r"^[-*+]\s+", "", t))
    if buf:
        blocks.append(buf)

    for b in blocks:
        # skip infobox / key-value metadata blocks
        if any(INFOBOX.match(x) for x in b) and all(INFOBOX.match(x) or len(x) < 40 for x in b):
            continue
        txt = clean(" · ".join(b))
        if len(txt) >= 40:
            return txt
    if blocks:
        return clean(" · ".join(" · ".join(b) for b in blocks))
    return ""


def shorten(para, limit=160):
    if len(para) <= limit:
        return para
    sents = re.split(r"(?<=[.!?])\s+", para)
    out = ""
    for s in sents:
        if not out:
            if len(s) > 200:
                cut = s[: limit - 3]
                sp = cut.rfind(" ")
                return cut[:sp] if sp > 60 else cut
            out = s
        else:
            if len(out) + 1 + len(s) > 200:
                break
            out += " " + s
        if len(out) >= 120:
            break
    return out


def auto_description(slug, body, title):
    para = first_para(body).strip('"').strip()
    low = para.lower()
    noise = low.count("belum ada data") + low.count("belum tersedia")
    if para.count(" · ") and len(INFOBOX.findall(para)) >= 2:
        noise += 2
    if INFOBOX.match(para):
        noise += 2
    if not para or noise >= 1 and len(para) < 160:
        kind = "aktor"
        if slug.startswith("peristiwa/"):
            kind = "peristiwa"
        elif slug.startswith("analisis/"):
            kind = "analisis"
        if kind == "peristiwa":
            return f"Catatan peristiwa {title}: kronologi, aktor yang terlibat, dan dokumen sumber yang terdokumentasi di wiki politik Ira Amalia."
        if kind == "analisis":
            return f"Analisis {title}: pembacaan relasi kuasa, bukti pendukung, dan implikasi kebijakan dalam wiki politik Ira Amalia."
        return f"Profil {title}: afiliasi, relasi bisnis-politik, dan peran yang terdokumentasi dalam wiki politik Indonesia Ira Amalia."
    if len(para) < 45:
        return f"{title}: {para}" if para else f"{title} — halaman rujukan wiki politik Indonesia."
    return shorten(para)


def yaml_ok(fm_text, path):
    try:
        yaml.safe_load(fm_text)
        return True
    except Exception as exc:  # noqa: BLE001
        print(f"[YAML FAIL] {path}: {exc}", file=sys.stderr)
        return False


changed = 0
stats = {"desc_manual": 0, "desc_auto": 0, "date": 0, "updated": 0}
for dirpath, _, files in os.walk(CONTENT):
    for f in sorted(files):
        if not f.endswith(".md"):
            continue
        path = os.path.join(dirpath, f)
        rel = os.path.relpath(path, CONTENT)
        slug = rel[:-3]
        text = open(path, encoding="utf-8").read()
        if not text.startswith("---"):
            continue
        parts = text.split("\n---", 1)
        fm = parts[0][3:]
        rest = parts[1]
        fm_lines = fm.split("\n")
        while fm_lines and not fm_lines[0].strip():
            fm_lines.pop(0)

        has = lambda k: any(re.match(rf"^{k}\s*:", ln) for ln in fm_lines)  # noqa: E731
        title_m = [ln for ln in fm_lines if re.match(r"^title\s*:", ln)]
        title = title_m[0].split(":", 1)[1].strip().strip("\"'") if title_m else f[:-3]
        body = rest.split("\n", 1)[1] if "\n" in rest else ""

        inserts = []
        cur_desc = None
        for ln in fm_lines:
            m = re.match(r"^description\s*:\s*(.*)$", ln)
            if m:
                cur_desc = m.group(1).strip().strip("\"'")
                break
        need_desc = (
            not has("description")
            or (REGEN_ALL and slug not in D)
            or (REGEN and cur_desc and GENERIC in cur_desc)
        )
        if need_desc:
            if slug in D:
                desc = D[slug]
                stats["desc_manual"] += 1
            else:
                desc = auto_description(slug, body, title)
                stats["desc_auto"] += 1
            inserts.append(("description", desc))
        created, last = git_dates(path)
        if not has("date") and created:
            inserts.append(("date", created))
            stats["date"] += 1
        if not has("updated") and last:
            inserts.append(("updated", last))
            stats["updated"] += 1

        if not inserts:
            continue

        # insert right after the title line (or replace an existing description)
        idx = 0
        for i, ln in enumerate(fm_lines):
            if re.match(r"^title\s*:", ln):
                idx = i + 1
                break
        desc_line_idx = None
        for i, ln in enumerate(fm_lines):
            if re.match(r"^description\s*:", ln):
                desc_line_idx = i
                break
        safe = []
        for key, val in inserts:
            if key == "date" and re.match(r"^\d{4}-\d{2}-\d{2}$", val):
                safe.append(f"{key}: {val}")
            else:
                dumped = yaml.safe_dump(val, allow_unicode=True, width=1000).strip()
                if dumped.endswith("..."):
                    dumped = dumped[:-3].rstrip()
                safe.append(f"{key}: {dumped}")
        if desc_line_idx is not None and any(s.startswith("description:") for s in safe):
            new_desc = [s for s in safe if s.startswith("description:")][0]
            fm_lines[desc_line_idx] = new_desc
            safe = [s for s in safe if not s.startswith("description:")]
        new_fm_lines = fm_lines[:idx] + safe + fm_lines[idx:]
        new_text = "---\n" + "\n".join(new_fm_lines) + "\n---" + rest
        if not yaml_ok("\n".join(new_fm_lines), path):
            continue
        changed += 1
        if not DRY:
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(new_text)

print(f"{'[dry-run] ' if DRY else ''}files changed: {changed} | {stats}")
