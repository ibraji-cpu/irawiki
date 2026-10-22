import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"

/**
 * Komponen "Relasi" (Anggota dari / Pemimpin dari / Pemilik dari / Terkait dengan).
 *
 * Nilai frontmatter field ini adalah NAMA ENTITAS (mis. "DPR RI"), bukan slug.
 * Komponen lama memakainya langsung sebagai `href="/${item}"` -> URL salah -> 404.
 *
 * Versi ini me-resolve nama -> slug halaman lewat indeks `allFiles` (slug, title,
 * aliases, dan stem nama file). Bila tidak ketemu, item dirender sebagai teks biasa
 * (tanpa tautan) sehingga tidak pernah menghasilkan 404.
 */

const RELATION_FIELDS: { key: string; label: string }[] = [
  { key: "member_of", label: "Anggota dari" },
  { key: "leader_of", label: "Pemimpin dari" },
  { key: "owner_of", label: "Pemilik dari" },
  { key: "related", label: "Terkait dengan" },
]

const SKIP = new Set(["", "[]", "_belum ada data_", "tidak diketahui", "belum ada data", "n/a", "-"])

function slugify(text: string): string {
  return text
    .toLowerCase()
    .trim()
    .replace(/[\[\]]/g, "")
    .replace(/[^a-z0-9\s-]/g, "")
    .replace(/\s+/g, "-")
    .replace(/-+/g, "-")
    .replace(/^-|-$/g, "")
}

function buildLookup(
  allFiles: QuartzComponentProps["allFiles"],
): Map<string, { slug: string; title: string }> {
  const map = new Map<string, { slug: string; title: string }>()
  const set = (key: string, value: { slug: string; title: string }) => {
    if (key && !map.has(key)) map.set(key, value)
  }
  for (const f of allFiles) {
    const rawTitle = (f as { title?: unknown }).title
    const fmTitle = f.frontmatter?.title
    const stem = (f.slug.split("/").pop() ?? f.slug).replace(/-/g, " ").replace(/\b\w/g, (c) => c.toUpperCase())
    const title =
      typeof rawTitle === "string" && rawTitle.length > 0
        ? rawTitle
        : typeof fmTitle === "string" && fmTitle.length > 0
          ? fmTitle
          : stem
    set(f.slug.toLowerCase(), { slug: f.slug, title })
    set(slugify(f.slug), { slug: f.slug, title })
    set(slugify(f.slug.split("/").pop() ?? ""), { slug: f.slug, title })
    set(slugify(title), { slug: f.slug, title })
    const aliases = f.frontmatter?.aliases
    if (Array.isArray(aliases)) {
      for (const a of aliases) {
        if (typeof a === "string") set(slugify(a), { slug: f.slug, title })
      }
    } else if (typeof aliases === "string") {
      set(slugify(aliases), { slug: f.slug, title })
    }
  }
  return map
}

const Relations: QuartzComponent = ({ fileData, allFiles }: QuartzComponentProps) => {
  const fm = fileData.frontmatter
  if (!fm || !allFiles) return null

  const lookup = buildLookup(allFiles)

  const sections = RELATION_FIELDS.map(({ key, label }) => {
    const value = fm[key]
    if (!value) return null
    const raw = Array.isArray(value) ? value : [value]
    const items = raw
      .filter((v): v is string => typeof v === "string")
      .map((v) => v.trim().replace(/^["']|["']$/g, ""))
      .filter((v) => !SKIP.has(v.toLowerCase()))
      .map((v) => {
        const clean = v.replace(/^\[\[|\]\]$/g, "")
        const resolved = lookup.get(slugify(clean))
        return { label: resolved?.title ?? clean, slug: resolved?.slug ?? null }
      })
    return items.length > 0 ? { label, items } : null
  }).filter((s): s is { label: string; items: { label: string; slug: string | null }[] } => s !== null)

  if (sections.length === 0) return null

  return (
    <div
      className="relations-section"
      style={{ marginTop: "2rem", paddingTop: "1rem", borderTop: "1px solid var(--lightgray)" }}
    >
      <h3 style={{ marginBottom: "0.5rem" }}>Relasi</h3>
      <div style={{ display: "flex", flexDirection: "column", gap: "0.5rem" }}>
        {sections.map(({ label, items }) => (
          <div key={label} style={{ display: "flex", gap: "0.5rem", alignItems: "baseline" }}>
            <span style={{ fontWeight: 500, minWidth: "120px", fontSize: "0.9rem", color: "var(--darkgray)" }}>
              {label}:
            </span>
            <span style={{ fontSize: "0.9rem" }}>
              {items.map((item, i) => (
                <span key={`${item.slug ?? item.label}-${i}`}>
                  {i > 0 && ", "}
                  {item.slug ? (
                    <a href={`/${item.slug}`} className="internal" style={{ color: "var(--secondary)" }}>
                      {item.label}
                    </a>
                  ) : (
                    <span style={{ color: "var(--darkgray)" }}>{item.label}</span>
                  )}
                </span>
              ))}
            </span>
          </div>
        ))}
      </div>
    </div>
  )
}

Relations.css = `
  .relations-section {
    background: var(--lightgray);
    padding: 1rem;
    border-radius: 4px;
  }
  .relations-section h3 {
    margin-top: 0;
  }
`

export default (() => Relations) satisfies QuartzComponentConstructor
