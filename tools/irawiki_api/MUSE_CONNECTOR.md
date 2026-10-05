# IRAWIKI Custom Connector untuk Muse.ai

## Base URL
```
https://wiki.iraamalia.id
```

## Endpoints

### 1. GET /muse/stubs
Daftar halaman stub yang perlu enrichment.

**Query Params:**
- `entity_type` (optional): `aktor`, `peristiwa`, atau `analisis` (kosong = semua)
- `limit` (optional): max hasil, default 50

**Response:**
```json
{
  "total": 4,
  "entity_type": "all",
  "stubs": [
    {
      "id": "achmad-taufik-husein",
      "type": "aktor",
      "size_bytes": 263,
      "preview": "--- title: Achmad Taufik Husein..."
    }
  ]
}
```

---

### 2. GET /muse/stub/{entity_type}/{entity_id}
Detail stub + template untuk enrichment.

**Response:**
```json
{
  "entity_id": "achmad-taufik-husein",
  "entity_type": "aktor",
  "is_stub": true,
  "current_markdown": "---\ntitle: Achmad Taufik Husein...",
  "template": "---\ntitle: {{title}}\ncategory: aktor...",
  "related_entities": [
    {"type": "aktor", "id": "jokowi", "snippet": "..."}
  ]
}
```

---

### 3. GET /muse/templates/{entity_type}
Mengembalikan isi master template verbatim untuk entity_type tertentu.

**Path Params:**
- `entity_type`: `aktor`, `peristiwa`, atau `analisis`

**Response:**
```json
{
  "entity_type": "peristiwa",
  "template_file": "02_peristiwa_template.md",
  "content": "---\ntitle: \"[Nama/Judul Peristiwa]\"\ntags:\n- peristiwa\n..."
}
```

---

### 4. POST /muse/propose
Submit proposal enrichment atau halaman baru dari Muse.ai untuk human review.

**Auth:** Wajib API key (X-API-Key atau Authorization: Bearer)

**Request Body:**
```json
{
  "entity_id": "achmad-taufik-husein",
  "entity_type": "aktor",
  "proposed_markdown": "---\ntitle: Achmad Taufik Husein\n...",
  "reason": "Menambahkan riwayat jabatan dari sumber KPK",
  "source": "muse_ai"
}
```

**Response (200 - enrichment):**
```json
{
  "status": "success",
  "proposal_id": "a1b2c3d4",
  "message": "Enrichment proposal submitted for human review.",
  "entity_id": "achmad-taufik-husein",
  "entity_type": "aktor",
  "is_new_page": false
}
```

**Response (200 - halaman baru):**
```json
{
  "status": "success",
  "proposal_id": "b2c3d4e5",
  "message": "New page proposal submitted for human review.",
  "entity_id": "ruu-satu-data-indonesia-rencana-pengesahan",
  "entity_type": "peristiwa",
  "is_new_page": true
}
```

**Response (409 - duplikat PENDING):**
```json
{
  "detail": "sudah ada proposal PENDING untuk entity_id 'achmad-taufik-husein'"
}
```

**Response (400 - validasi frontmatter gagal):**
```json
{
  "detail": "Missing required frontmatter fields for peristiwa: tanggal"
}
```

**Response (401 - tanpa key):**
```json
{
  "status": "error",
  "message": "unauthorized"
}
```

---

### 5. GET /muse/proposals
List semua proposal (untuk review).

**Query Params:**
- `status` (optional): `PENDING`, `APPROVED`, `REJECTED`

**Response:**
```json
{
  "total": 1,
  "proposals": [
    {
      "id": "a1b2c3d4",
      "entity_id": "achmad-taufik-husein",
      "entity_type": "aktor",
      "reason": "Menambahkan riwayat jabatan",
      "source": "muse_ai",
      "is_new_page": false,
      "status": "PENDING",
      "created_at": "2026-10-05T02:00:00"
    }
  ]
}
```

---

### 6. POST /muse/proposals/{proposal_id}/approve
Setujui proposal dan merge ke content.

**Auth:** Wajib API key

**Response:**
```json
{
  "status": "approved",
  "proposal_id": "a1b2c3d4",
  "entity_id": "achmad-taufik-husein",
  "entity_type": "aktor",
  "is_new_page": false,
  "message": "Proposal merged into aktor/achmad-taufik-husein.md"
}
```

---

### 7. POST /muse/proposals/{proposal_id}/reject
Tolak proposal.

**Auth:** Wajib API key

**Response:**
```json
{
  "status": "rejected",
  "proposal_id": "a1b2c3d4"
}
```

---

## Alur Kerja di Muse.ai

### Enrichment (entity sudah ada)
1. **Muse** memanggil `GET /muse/stubs` untuk melihat daftar stub
2. **Muse** pilih satu stub, panggil `GET /muse/stub/{type}/{id}` untuk dapat template + konten saat ini
3. **Muse** generate enrichment berdasarkan template + reasoning
4. **Muse** submit via `POST /muse/propose` (is_new_page=false)
5. **Human** review di `GET /muse/proposals`, lalu approve/reject

### Halaman Baru (entity belum ada)
1. **Muse** menentukan entity_id baru (slug)
2. **Muse** panggil `GET /muse/templates/{entity_type}` untuk dapat template terbaru
3. **Muse** generate konten mengikuti template
4. **Muse** submit via `POST /muse/propose` (is_new_page=true)
5. **Human** review di `GET /muse/proposals`, lalu approve/reject
6. Setelah approve, file terbit di content/{entity_type}/{entity_id}.md

## Validasi Frontmatter Wajib

| entity_type | Field wajib | Tipe |
|-------------|-------------|------|
| aktor | `nama_lengkap` | string |
| peristiwa | `tanggal` | list of string |
| analisis | `aktor_fokus`, `peristiwa` | string |

## Contoh Prompt untuk Muse.ai

```
Cek https://wiki.iraamalia.id/muse/stubs untuk daftar halaman yang perlu diisi.
Pilih satu, ambil detailnya via /muse/stub/{type}/{id}, lalu buat proposal
enrichment via POST /muse/propose. Jangan langsung edit file, selalu lewat proposal.

Untuk halaman baru, panggil GET /muse/templates/{entity_type} untuk dapat
template terbaru, lalu submit via POST /muse/propose dengan entity_id baru.
```
