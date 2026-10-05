-- wiki_index.db — skema index turunan untuk Wiki Ira Amalia
-- Fase 2a. Index ini TURUNAN: bisa di-rebuild penuh dari Markdown kapan saja.
-- Jangan commit file .db ke git (lihat .gitignore).

PRAGMA journal_mode=WAL;
PRAGMA foreign_keys=ON;

-- Metadata index (schema version, last full rebuild)
CREATE TABLE IF NOT EXISTS index_meta(
  key   TEXT PRIMARY KEY,
  value TEXT
);

-- Halaman: satu baris per file Markdown
CREATE TABLE IF NOT EXISTS pages(
  path            TEXT PRIMARY KEY,   -- relatif terhadap content/, tanpa .md
  title           TEXT NOT NULL,
  type            TEXT,               -- aktor | peristiwa | organisasi | analisis | ...
  risiko_editorial TEXT,
  status          TEXT,               -- NULL | 'stub'
  updated_at      TEXT,
  content_hash    TEXT NOT NULL       -- sha256 isi file, untuk incremental
);

-- FTS5 full-text: page_path, title, section, body
-- Bobot kolom diatur saat query via bm25(chunks_fts, w_path, w_title, w_section, w_body)
CREATE VIRTUAL TABLE IF NOT EXISTS chunks_fts USING fts5(
  page_path,
  title,
  section,
  body,
  tokenize='unicode61 remove_diacritics 2'
);

-- FTS5 trigram untuk fuzzy matching nama entitas (mis. typo "Sukarno" -> "Soekarno")
CREATE VIRTUAL TABLE IF NOT EXISTS names_fts USING fts5(
  name,
  canonical,
  tokenize='trigram'
);

-- Entitas. PK = page_path: identitas halaman adalah path, BUKAN title
-- (repo punya 3 pasang halaman bertitle sama: joko-widodo/jokowi, dst).
-- `nama` = nama kanonis untuk tampilan & pencarian.
CREATE TABLE IF NOT EXISTS entities(
  page_path TEXT PRIMARY KEY REFERENCES pages(path) ON DELETE CASCADE,
  nama      TEXT NOT NULL,
  type      TEXT
);
CREATE INDEX IF NOT EXISTS idx_entities_nama ON entities(nama);
CREATE INDEX IF NOT EXISTS idx_entities_page ON entities(page_path);
CREATE INDEX IF NOT EXISTS idx_entities_type ON entities(type);

-- Relasi: dari frontmatter `relasi:` + relasi implisit 'menyebut' dari wikilinks
CREATE TABLE IF NOT EXISTS relations(
  id          INTEGER PRIMARY KEY,
  subjek      TEXT NOT NULL,
  predikat    TEXT NOT NULL,
  objek       TEXT NOT NULL,
  sumber      TEXT,                   -- URL atau NULL (fallback ke sumber level halaman)
  confidence  TEXT NOT NULL,          -- high | medium | low
  origin      TEXT NOT NULL DEFAULT 'frontmatter',  -- frontmatter | wikilink
  page_path   TEXT REFERENCES pages(path) ON DELETE CASCADE,
  keterangan  TEXT,
  UNIQUE(subjek, predikat, objek, page_path)
);
CREATE INDEX IF NOT EXISTS idx_rel_subjek ON relations(subjek);
CREATE INDEX IF NOT EXISTS idx_rel_objek  ON relations(objek);
CREATE INDEX IF NOT EXISTS idx_rel_page   ON relations(page_path);

-- Alias -> halaman kanonis (page_path)
CREATE TABLE IF NOT EXISTS aliases(
  alias     TEXT PRIMARY KEY,
  page_path TEXT NOT NULL REFERENCES entities(page_path) ON DELETE CASCADE
);
CREATE INDEX IF NOT EXISTS idx_aliases_page ON aliases(page_path);

-- Sumber per halaman
CREATE TABLE IF NOT EXISTS sources(
  page_path TEXT REFERENCES pages(path) ON DELETE CASCADE,
  url       TEXT,
  judul     TEXT,
  tanggal   TEXT,
  dokumen   TEXT,
  sumber_status TEXT,                 -- NULL | 'prosa'
  UNIQUE(page_path, url, judul, tanggal)
);
CREATE INDEX IF NOT EXISTS idx_sources_page ON sources(page_path);

-- ---------------------------------------------------------------- views
-- Relasi dengan nama tampilan (bukan path) untuk pembacaan manusia.
CREATE VIEW IF NOT EXISTS relations_view AS
SELECT r.id,
       COALESCE(es.nama, r.subjek) AS subjek,
       r.predikat,
       COALESCE(eo.nama, r.objek)  AS objek,
       r.sumber, r.confidence, r.origin, r.page_path, r.keterangan
FROM relations r
LEFT JOIN entities es ON es.page_path = r.subjek
LEFT JOIN entities eo ON eo.page_path = r.objek;

-- Halaman dengan jumlah relasi (derajat node).
CREATE VIEW IF NOT EXISTS entity_degree AS
SELECT e.nama, e.type, e.page_path,
       (SELECT COUNT(*) FROM relations r WHERE r.subjek = e.page_path) AS out_deg,
       (SELECT COUNT(*) FROM relations r WHERE r.objek  = e.page_path) AS in_deg
FROM entities e;
