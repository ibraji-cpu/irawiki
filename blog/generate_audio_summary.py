#!/usr/bin/env python3
"""
Generate ringkasan audio otomatis untuk artikel blog Hugo.
Usage: python3 generate_audio_summary.py <path-to-md-file> [--force]

Alur:
1. Baca artikel (support posts/<slug>.md dan page bundle posts/<slug>/index.md)
2. Generate ringkasan ~240 kata (±2 menit) via Gemini
3. Convert ke MP3 via Gemini TTS (voice Aoede) + ffmpeg (PCM -> MP3)
4. Simpan ke static/audio/<slug>.mp3 + <slug>.summary.txt
5. Print AUDIO_PATH:/audio/<slug>.mp3 untuk dipakai publish.sh
"""

import os
import re
import sys
import argparse
import subprocess
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path("/home/ubuntu/.hermes/.env"))

from google import genai
from google.genai import types

BLOG_ROOT = Path("/home/ubuntu/irawiki/blog")

# gemini-2.5-flash sudah 404 untuk akun baru (Okt 2026) -> pakai alias *-latest
SUMMARY_MODEL = os.environ.get("BLOG_SUMMARY_MODEL", "gemini-flash-latest")
TTS_MODEL = os.environ.get("BLOG_TTS_MODEL", "gemini-3.8-flash-tts")
# Rantai model TTS: 2.5-preview kuotanya cepat habis (429) -> jangan langsung jatuh ke edge-tts.
TTS_MODELS = [TTS_MODEL, "gemini-3.8-flash-tts", "gemini-3.1-flash-tts-preview", "gemini-2.5-flash-preview-tts"]
VOICE_NAME = "Aoede"

# Fallback LLM via provider trustisgold (OpenAI-compatible)
FALLBACK_BASE_URL = os.environ.get("BLOG_FALLBACK_BASE_URL", "https://api.trustisgold.web.id/v1")
FALLBACK_MODEL = os.environ.get("BLOG_FALLBACK_MODEL", "tig/deepseek-v4-1-flash-UNRESTRICTED")
FALLBACK_KEY_ENV = "TRUSTISGOLD_API_KEY"

# Batas keras durasi audio (user: maksimum 2 menit)
MAX_AUDIO_SECONDS = float(os.environ.get("BLOG_MAX_AUDIO_SECONDS", "120"))

VOICE_STYLE = (
    "Voice: Native Indonesian speaker, warm vocal smile, casual but highly informative, "
    "mature female, articulate, natural and relatable, positive and supportive energy. "
    "Tempo 110-125 WPM. Baca dengan tenang dan jelas.\n\n"
)


def get_api_key() -> str:
    key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not key:
        print("ERROR: GEMINI_API_KEY / GOOGLE_API_KEY tidak ditemukan di ~/.hermes/.env")
        sys.exit(1)
    return key


def resolve_article(path: Path) -> tuple[str, Path]:
    """Kembalikan (slug, md_path). Slug dari nama folder bundle atau nama file."""
    path = path.resolve()
    if path.name == "index.md":
        return path.parent.name, path
    return path.stem, path


def parse_frontmatter(text: str) -> dict:
    m = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    fm: dict[str, str] = {}
    if not m:
        return fm
    for line in m.group(1).splitlines():
        kv = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if kv:
            fm[kv.group(1)] = kv.group(2).strip().strip('"').strip("'")
    return fm


def strip_markdown(md: str) -> str:
    s = re.sub(r"```.*?```", "", md, flags=re.DOTALL)
    s = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", s)
    s = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", s)
    s = re.sub(r"^\s*#{1,6}\s*", "", s, flags=re.MULTILINE)
    s = re.sub(r"[*_`>]", "", s)
    s = re.sub(r"^\s*[-–—]\s*", "", s, flags=re.MULTILINE)
    s = re.sub(r"\n{3,}", "\n\n", s)
    return s.strip()


def generate_summary(title: str, content: str, api_key: str) -> str:
    prompt = (
        "Tuliskan ringkasan artikel berikut dalam Bahasa Indonesia untuk dibacakan sebagai audio "
        "ringkasan dengan durasi MAKSIMAL 2 menit (sekitar 230-250 kata). "
        "Aturan: langsung ke isi tanpa pembuka seperti 'Berikut ringkasan' atau 'Artikel ini membahas'; "
        "gunakan kalimat pendek dan mengalir enak didengar; sebutkan topik utama di kalimat pertama; "
        "tutup dengan satu kalimat ajakan singkat untuk membaca artikel lengkapnya. "
        "Tanpa markdown, tanpa bullet, hanya paragraf teks biasa.\n\n"
        f"Judul: {title}\n\nIsi artikel:\n{content[:12000]}"
    )

    # 1) Provider utama: trustisgold (sesuai permintaan user)
    text = summary_via_trustisgold(prompt)
    if text:
        return text

    # 2) Fallback: Gemini API langsung.
    #    thinking_budget=0 WAJIB: tanpa itu budget habis untuk token berpikir
    #    dan output terpotong di tengah kalimat (gejala: 16 kata, finish=MAX_TOKENS).
    print("   ⚠️ trustisgold gagal, coba Gemini API...")
    try:
        client = genai.Client(api_key=api_key)
        resp = client.models.generate_content(
            model=SUMMARY_MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                max_output_tokens=4000,
                temperature=0.7,
                thinking_config=types.ThinkingConfig(thinking_budget=0),
            ),
        )
        gem = (resp.text or "").strip()
        if len(gem.split()) >= 80:
            print("   (sumber: Gemini API)")
            return gem
        print(f"   ⚠️ Gemini hanya menghasilkan {len(gem.split())} kata")
    except Exception as e:
        print(f"   ⚠️ Gemini gagal ({str(e)[:120]})")

    # 3) Fallback terakhir: LLM Hermes (provider + fallback_providers dari config.yaml)
    return summary_via_hermes_cli(prompt)


def summary_via_trustisgold(prompt: str) -> str | None:
    """Fallback langsung ke provider trustisgold (OpenAI-compatible).

    Model deepseek-v4-1-flash (reasoning) kadang mengembalikan content kosong (respons reasoning-only)
    atau gagal transien -> coba beberapa kali sebelum menyerah.
    """
    key = os.environ.get(FALLBACK_KEY_ENV)
    if not key:
        print(f"   ⚠️ {FALLBACK_KEY_ENV} tidak diset, lewati fallback trustisgold")
        return None

    try:
        from openai import OpenAI

        client = OpenAI(base_url=FALLBACK_BASE_URL, api_key=key)
    except Exception as e:
        print(f"   ⚠️ trustisgold client gagal ({str(e)[:120]})")
        return None

    for attempt in range(1, 4):
        try:
            resp = client.chat.completions.create(
                model=FALLBACK_MODEL,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=4000,
                temperature=0.7,
            )
            msg = resp.choices[0].message
            text = (msg.content or "").strip()
            # Sebagian model reasoning menaruh teks di reasoning_content
            if len(text.split()) < 80:
                extra = (getattr(msg, "reasoning_content", None) or "").strip()
                if len(extra.split()) > len(text.split()):
                    text = extra
            if len(text.split()) >= 80:
                print(f"   (sumber: trustisgold / {FALLBACK_MODEL})")
                return text
            print(f"   ⚠️ trustisgold percobaan {attempt}: hanya {len(text.split())} kata "
                  f"(finish={resp.choices[0].finish_reason})")
        except Exception as e:
            print(f"   ⚠️ trustisgold percobaan {attempt} gagal ({str(e)[:120]})")
    return None


def summary_via_hermes_cli(prompt: str) -> str:
    """Fallback terakhir: `hermes -z` (provider + fallback_providers dari config.yaml)."""
    tmp = Path("/tmp/blog_summary_prompt.txt")
    tmp.write_text(prompt, encoding="utf-8")
    try:
        res = subprocess.run(
            ["hermes", "-z", tmp.read_text(encoding="utf-8")],
            capture_output=True,
            text=True,
            timeout=300,
        )
    except subprocess.TimeoutExpired:
        raise RuntimeError("Fallback LLM (hermes -z) timeout setelah 300 detik")
    finally:
        tmp.unlink(missing_ok=True)

    out = (res.stdout or "").strip()
    # Buang baris status/log Hermes, ambil paragraf terpanjang
    lines = [ln.strip() for ln in out.splitlines() if ln.strip()]
    lines = [ln for ln in lines if not ln.startswith(("ℹ", "✅", "⚠", "🚀", "[", "Error"))]
    text = max(lines, key=len) if lines else ""
    if len(text.split()) < 80:
        raise RuntimeError(
            f"Fallback LLM gagal menghasilkan ringkasan memadai (exit={res.returncode}): {out[:300]}"
        )
    print("   (sumber: fallback LLM)")
    return text


EDGE_TTS_BIN = os.environ.get(
    "BLOG_EDGE_TTS_BIN",
    "/home/ubuntu/.hermes/installs/5f0a1ff4045d044e/environments/53dc588fb4a8495a9f208fe1fd522d26/venv/bin/edge-tts",
)
EDGE_VOICE = os.environ.get("BLOG_EDGE_VOICE", "id-ID-GadisNeural")


def synthesize_edge(text: str, out_mp3: Path) -> bool:
    """Fallback TTS via edge-tts (Microsoft, gratis). Suara perempuan Indonesia."""
    if not Path(EDGE_TTS_BIN).exists():
        print(f"   ⚠️ edge-tts tidak ada di {EDGE_TTS_BIN}")
        return False
    out_mp3.parent.mkdir(parents=True, exist_ok=True)
    res = subprocess.run(
        [EDGE_TTS_BIN, "--voice", EDGE_VOICE, "--rate", "-5%",
         "--text", text, "--write-media", str(out_mp3)],
        capture_output=True, text=True, timeout=300,
    )
    if res.returncode != 0 or not out_mp3.exists() or out_mp3.stat().st_size == 0:
        print(f"   ⚠️ edge-tts gagal: {(res.stderr or res.stdout)[-200:]}")
        return False
    print(f"   (sumber TTS: edge-tts / {EDGE_VOICE})")
    return True


def probe_duration(mp3: Path) -> float:
    """Durasi detik via ffprobe; 0.0 kalau gagal dibaca."""
    try:
        res = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "default=nw=1:nk=1", str(mp3)],
            capture_output=True, text=True, timeout=60,
        )
        return float((res.stdout or "0").strip() or 0)
    except Exception:
        return 0.0


def enforce_max_duration(mp3: Path, max_seconds: float) -> float:
    """Percepat audio dengan ffmpeg atempo (pitch aman) agar <= max_seconds."""
    dur = probe_duration(mp3)
    if dur <= 0 or dur <= max_seconds:
        return dur

    factor = dur / max_seconds
    # atempo hanya menerima 0.5-2.0 per filter -> rantai kalau perlu
    chain, remaining = [], factor
    while remaining > 2.0:
        chain.append("atempo=2.0")
        remaining /= 2.0
    chain.append(f"atempo={remaining:.4f}")

    tmp = mp3.with_suffix(".speed.mp3")
    res = subprocess.run(
        ["ffmpeg", "-y", "-i", str(mp3), "-filter:a", ",".join(chain),
         "-acodec", "libmp3lame", "-q:a", "2", str(tmp)],
        capture_output=True, text=True,
    )
    if res.returncode != 0:
        print(f"   ⚠️ gagal mempercepat audio: {res.stderr[-200:]}")
        return dur

    tmp.replace(mp3)
    new_dur = probe_duration(mp3)
    print(f"   ⏩ dipercepat x{factor:.2f} agar ≤{max_seconds:.0f}s ({dur:.0f}s → {new_dur:.0f}s)")
    return new_dur


def synthesize(text: str, out_mp3: Path, api_key: str) -> None:
    last_err = ""
    for model in dict.fromkeys(TTS_MODELS):
        try:
            _synthesize_gemini(text, out_mp3, api_key, model)
            print(f"   (sumber TTS: Gemini / {model} / voice {VOICE_NAME})")
            return
        except Exception as e:
            last_err = str(e)
            print(f"   ⚠️ Gemini TTS {model} gagal ({last_err[:120]})")
    print("   ⚠️ semua model Gemini TTS gagal, coba edge-tts...")
    if not synthesize_edge(text, out_mp3):
        raise RuntimeError(f"Semua jalur TTS gagal. Gemini: {last_err[:300]}")


def _synthesize_gemini(text: str, out_mp3: Path, api_key: str, model: str) -> None:
    client = genai.Client(api_key=api_key)
    resp = client.models.generate_content(
        model=model,
        contents=VOICE_STYLE + text,
        config=types.GenerateContentConfig(
            response_modalities=["AUDIO"],
            speech_config=types.SpeechConfig(
                voice_config=types.VoiceConfig(
                    prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name=VOICE_NAME)
                )
            ),
        ),
    )

    audio_data = None
    for part in resp.candidates[0].content.parts:
        if part.inline_data and part.inline_data.data:
            audio_data = part.inline_data.data
            break
    if not audio_data:
        raise RuntimeError("Tidak ada data audio pada respons TTS")

    out_mp3.parent.mkdir(parents=True, exist_ok=True)
    raw = out_mp3.with_suffix(".raw")
    raw.write_bytes(audio_data)

    # Gemini TTS mengeluarkan PCM 24kHz mono 16-bit -> wajib dikonversi ke MP3
    cmd = [
        "ffmpeg", "-y",
        "-f", "s16le", "-ar", "24000", "-ac", "1",
        "-i", str(raw),
        "-acodec", "libmp3lame", "-q:a", "2",
        str(out_mp3),
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    raw.unlink(missing_ok=True)
    if res.returncode != 0:
        raise RuntimeError(f"ffmpeg gagal: {res.stderr[-400:]}")


def add_audio_path_to_frontmatter(md_path: Path, rel_path: str) -> bool:
    """Sisipkan/refresh audio_path di frontmatter. True kalau file berubah."""
    text = md_path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    if not m:
        return False

    line = f'audio_path: "{rel_path}"'
    if re.search(r"^audio_path:.*$", m.group(1), re.MULTILINE):
        if line in m.group(1):
            return False
        new_fm = re.sub(r"^audio_path:.*$", line, m.group(1), flags=re.MULTILINE)
    else:
        new_fm = m.group(1).rstrip("\n") + "\n" + line

    md_path.write_text(
        text[: m.start(1)] + new_fm + text[m.end(1):], encoding="utf-8"
    )
    return True


def main() -> None:
    ap = argparse.ArgumentParser(description="Generate ringkasan audio artikel blog")
    ap.add_argument("md_file", help="Path .md artikel (posts/<slug>.md atau posts/<slug>/index.md)")
    ap.add_argument("--output-dir", default=str(BLOG_ROOT / "static" / "audio"))
    ap.add_argument("--force", action="store_true", help="Timpa audio yang sudah ada")
    ap.add_argument("--update-frontmatter", action="store_true",
                    help="Tulis audio_path ke frontmatter artikel")
    args = ap.parse_args()

    md_path = Path(args.md_file)
    if not md_path.exists():
        print(f"ERROR: File tidak ditemukan: {md_path}")
        sys.exit(1)

    slug, md_path = resolve_article(md_path)
    text = md_path.read_text(encoding="utf-8")
    fm = parse_frontmatter(text)

    if fm.get("draft") == "true" and not args.force:
        print(f"SKIP (draft): {slug}")
        sys.exit(0)

    out_dir = Path(args.output_dir)
    out_mp3 = out_dir / f"{slug}.mp3"
    rel_path = f"/audio/{slug}.mp3"

    if out_mp3.exists() and not args.force:
        print(f"SKIP (audio sudah ada): {out_mp3}")
        if args.update_frontmatter and add_audio_path_to_frontmatter(md_path, rel_path):
            print(f"   frontmatter diperbarui: {rel_path}")
        print(f"AUDIO_PATH:{rel_path}")
        sys.exit(0)

    title = fm.get("title") or slug.replace("-", " ").title()
    body = re.sub(r"^---\n.*?\n---\n", "", text, flags=re.DOTALL)
    content = strip_markdown(body)

    print(f"📄 Artikel : {title}")
    print(f"📝 Konten  : {len(content)} karakter")

    api_key = get_api_key()

    print(f"🧠 Membuat ringkasan ({SUMMARY_MODEL})...")
    summary = generate_summary(title, content, api_key)
    words = len(summary.split())
    print(f"📋 Ringkasan: {words} kata (±{words / 150 * 60:.0f} detik)")

    print(f"🎙️  TTS {' → '.join(dict.fromkeys(TTS_MODELS))} / voice {VOICE_NAME}...")
    synthesize(summary, out_mp3, api_key)
    enforce_max_duration(out_mp3, MAX_AUDIO_SECONDS)

    size_kb = out_mp3.stat().st_size / 1024
    print(f"✅ Audio: {out_mp3} ({size_kb:.0f} KB)")

    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / f"{slug}.summary.txt").write_text(summary, encoding="utf-8")

    if args.update_frontmatter:
        if add_audio_path_to_frontmatter(md_path, rel_path):
            print(f"   frontmatter diperbarui: {rel_path}")

    print(f"AUDIO_PATH:{rel_path}")


if __name__ == "__main__":
    main()
