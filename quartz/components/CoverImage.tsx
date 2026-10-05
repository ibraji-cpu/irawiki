import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"

interface Options {
  condition?: "index" | "not-index" | "all"
}

export default ((opts?: Options) => {
  const condition = opts?.condition ?? "all"

  const CoverImage: QuartzComponent = ({ fileData, displayClass }: QuartzComponentProps) => {
    const fm = fileData.frontmatter as Record<string, any> | undefined
    const cover = fm?.cover_image || fm?.image_url || fm?.thumbnail

    // Default cover global dari static/covers bila frontmatter tidak punya
    const defaultCover = "/static/covers/ira-amalia-hero.webp"
    const effectiveCover = cover || defaultCover

    // Skip berdasarkan kondisi halaman (index atau bukan)
    const isIndex = fileData.slug === "index" || fileData.slug === "404"
    if (condition === "not-index" && isIndex) return null
    if (condition === "index" && !isIndex) return null

    return (
      <div class={`cover-image ${displayClass ?? ""}`}>
        <img src={effectiveCover} alt="" loading="lazy" />
      </div>
    )
  }

  CoverImage.displayName = "CoverImage"
  CoverImage.css = `
.cover-image {
  margin-bottom: 2rem;
  overflow: hidden;
  border-radius: 8px;
}
.cover-image img {
  width: 100%;
  height: auto;
  display: block;
  object-fit: cover;
  max-height: 400px;
}
`

  return CoverImage
}) satisfies QuartzComponentConstructor
