import { FullSlug, resolveRelative } from "../util/path"
import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"

/** Satu seksi daftar (judul + filter + urutan). */
interface SectionOptions {
  /** Judul section, mis. "Baru Update" */
  title?: string
  /** Urutan: "updated" (terbaru dulu) atau "title" (A–Z) */
  sort?: "updated" | "title"
  /** Batas jumlah item */
  limit?: number
  /** Batasi ke halaman ber-tag tertentu (mis. ["topik"]) */
  filterTags?: string[]
  /** Batasi ke halaman di folder tertentu (prefix slug, mis. ["aktor"]) */
  filterFolders?: string[]
  /** Batasi ke halaman dengan frontmatter `entity_type` tertentu (mis. ["topik"]) */
  filterEntityTypes?: string[]
  /** Tampilkan tanggal di samping judul */
  showDate?: boolean
  /** Tampilkan tag */
  showTags?: boolean
}

interface Options extends SectionOptions {
  /** "index" = hanya homepage, "not-index" = kecuali homepage, "all" = semua */
  condition?: "index" | "not-index" | "all"
  /**
   * Beberapa seksi sekaligus. Bila diisi, opsi seksi tunggal di level atas
   * (title, filterTags, dst.) dipakai sebagai default untuk tiap seksi.
   */
  sections?: SectionOptions[]
}

/**
 * Seksi default homepage: aktor terbaru dan hub (halaman topik) terbaru.
 * Aktor diambil dari folder `aktor/` (bukan tag — tag `aktor` tidak konsisten).
 * Hub = halaman ber-`entity_type: topik` (living document / hub topik).
 */
const DEFAULT_SECTIONS: SectionOptions[] = [
  { title: "Terbaru di Wiki (Aktor)", filterFolders: ["aktor"] },
  { title: "Terbaru di Wiki (Hub)", filterEntityTypes: ["topik"] },
]

const MONTHS = ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"]

function fmtDateID(d: Date): string {
  return `${d.getUTCDate()} ${MONTHS[d.getUTCMonth()]} ${d.getUTCFullYear()}`
}

/** Tanggal pembaruan: frontmatter `updated`/`modified`, lalu turunan `dates.modified`. */
function getUpdated(f: any): Date | undefined {
  const fm = f?.frontmatter ?? {}
  const raw = fm.updated ?? fm.modified ?? f?.dates?.modified
  if (!raw) return undefined
  const d = new Date(String(raw))
  return isNaN(d.getTime()) ? undefined : d
}

/** Tanggal terbit: frontmatter `date`, lalu turunan `dates.created`. */
function getCreated(f: any): Date | undefined {
  const fm = f?.frontmatter ?? {}
  const raw = fm.date ?? f?.dates?.created
  if (!raw) return undefined
  const d = new Date(String(raw))
  return isNaN(d.getTime()) ? undefined : d
}

/** Halaman yang tidak layak tampil di daftar: homepage, 404, tag index, folder index. */
function isSkippable(f: any): boolean {
  const slug = f?.slug ?? ""
  if (!slug || slug === "index" || slug === "404") return true
  if (slug.startsWith("tags/")) return true
  if (slug.endsWith("/index")) return true
  if (f?.unlisted === true) return true
  return false
}

function collect(allFiles: any[], opts: SectionOptions): any[] {
  const list = allFiles.filter((f: any) => {
    if (isSkippable(f)) return false
    if (opts.filterTags && opts.filterTags.length > 0) {
      const tags: string[] = (f?.frontmatter?.tags ?? []).map((t: string) => String(t).toLowerCase())
      if (!opts.filterTags.some((t) => tags.includes(t.toLowerCase()))) return false
    }
    if (opts.filterFolders && opts.filterFolders.length > 0) {
      const slug = String(f?.slug ?? "")
      if (!opts.filterFolders.some((dir) => slug.startsWith(`${dir.replace(/\/+$/, "")}/`)))
        return false
    }
    if (opts.filterEntityTypes && opts.filterEntityTypes.length > 0) {
      const et = String(f?.frontmatter?.entity_type ?? "").toLowerCase()
      if (!opts.filterEntityTypes.some((t) => t.toLowerCase() === et)) return false
    }
    return true
  })

  if (opts.sort === "title") {
    list.sort((a: any, b: any) =>
      String(a.frontmatter?.title ?? a.slug).localeCompare(String(b.frontmatter?.title ?? b.slug), "id"),
    )
  } else {
    list.sort((a: any, b: any) => {
      const ad = getUpdated(a)?.getTime() ?? getCreated(a)?.getTime() ?? 0
      const bd = getUpdated(b)?.getTime() ?? getCreated(b)?.getTime() ?? 0
      if (ad !== bd) return bd - ad
      return String(a.frontmatter?.title ?? a.slug).localeCompare(
        String(b.frontmatter?.title ?? b.slug),
        "id",
      )
    })
  }

  return opts.limit ? list.slice(0, opts.limit) : list
}

const HomeListBody: QuartzComponent = ({
  fileData,
  allFiles,
  title,
  sort,
  limit,
  filterTags,
  filterFolders,
  filterEntityTypes,
  showDate,
  showTags,
}: QuartzComponentProps) => {
  const pages = collect(allFiles, { sort, limit, filterTags, filterFolders, filterEntityTypes })
  if (pages.length === 0) return null

  return (
    <section class="ira-home-section">
      {title && <h2 class="ira-home-title">{title}</h2>}
      <ul class="ira-home-list">
        {pages.map((page: any) => {
          const slug = page.slug as FullSlug
          const pageTitle = page.frontmatter?.title ?? slug
          const tags: string[] = page.frontmatter?.tags ?? []
          const date = getUpdated(page) ?? getCreated(page)
          return (
            <li>
              <a href={resolveRelative(fileData.slug!, slug)} class="internal internal-link">
                {pageTitle}
              </a>
              {showDate && date && (
                <span class="ira-home-date"> — {fmtDateID(date)}</span>
              )}
              {showTags && tags.length > 0 && (
                <span class="ira-home-tags">
                  {" "}
                  {tags.map((t) => `#${t}`).join(" ")}
                </span>
              )}
            </li>
          )
        })}
      </ul>
    </section>
  )
}

HomeListBody.displayName = "HomeListBody"
HomeListBody.css = `
.ira-home-section {
  margin-top: 1.75rem;
}
.ira-home-title {
  font-size: 1.1rem;
  margin: 0 0 0.75rem 0;
  padding-bottom: 0.35rem;
  border-bottom: 1px solid var(--lightgray);
  color: var(--dark);
}
.ira-home-list {
  margin: 0;
  padding-left: 1.25rem;
}
.ira-home-list > li {
  margin-bottom: 0.4rem;
}
.ira-home-list > li > a {
  color: var(--secondary);
}
.ira-home-date {
  color: var(--gray);
  font-size: 0.8rem;
}
.ira-home-tags {
  color: var(--gray);
  font-size: 0.78rem;
}
`

/**
 * Konstruktor HomeList.
 *
 * Komponen dalam dibuat di dalam konstruktor supaya setiap instance menutup
 * (closure) opsi miliknya sendiri — kalau opsi disimpan di properti modul,
 * dua instance dengan opsi berbeda akan saling menimpa.
 *
 * Default: dua seksi (`DEFAULT_SECTIONS`) — "Terbaru di Wiki (Aktor)" dan
 * "Terbaru di Wiki (Hub)" — dengan `showDate` aktif. Pemanggil dari
 * `layout.byPageType.*.positions` di quartz.config.yaml di-instantiate TANPA
 * opsi, jadi seksi & judulnya harus punya nilai default di sini.
 *
 * Bila pemanggil memberi `title`/filter tanpa `sections`, komponen kembali ke
 * mode satu seksi seperti sebelumnya.
 */
export default ((opts?: Options) => {
  const { condition = "index", sections: userSections, ...sectionDefaults } = opts ?? {}
  const base: SectionOptions = {
    sort: "updated",
    limit: 12,
    showDate: true,
    ...sectionDefaults,
  }
  const singleMode =
    !userSections &&
    (sectionDefaults.title !== undefined ||
      sectionDefaults.filterTags !== undefined ||
      sectionDefaults.filterFolders !== undefined ||
      sectionDefaults.filterEntityTypes !== undefined)
  const sections: SectionOptions[] = singleMode
    ? [base]
    : (userSections ?? DEFAULT_SECTIONS).map((s) => ({ ...base, ...s }))

  const HomeList: QuartzComponent = (props) => {
    const isIndex = props.fileData.slug === "index" || props.fileData.slug === "404"
    if (condition === "not-index" && isIndex) return null
    if (condition === "index" && !isIndex) return null
    return (
      <>
        {sections.map((s) => (
          <HomeListBody {...props} {...s} />
        ))}
      </>
    )
  }

  HomeList.displayName = "HomeList"
  HomeList.css = HomeListBody.css
  return HomeList
}) satisfies QuartzComponentConstructor
