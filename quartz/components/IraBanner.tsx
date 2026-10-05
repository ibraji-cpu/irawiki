import { QuartzComponent, QuartzComponentConstructor } from "./types"

interface Options {
  /** "all" = semua halaman, "not-index" = kecuali homepage, "index" = hanya homepage */
  condition?: "index" | "not-index" | "all"
  /** Path ke gambar banner, relatif dari root site */
  imagePath?: string
  /** Alt text untuk aksesibilitas */
  alt?: string
  /** Link tujuan saat banner diklik (opsional) */
  linkTo?: string
}

const defaultOpts: Required<Options> = {
  condition: "all",
  imagePath: "/static/ira-amalia-banner.png",
  alt: "Ira Amalia — Avatar Politik / Agen AI | iraamalia.id",
  linkTo: "",
}

const IraBanner: QuartzComponent = ({ fileData, displayClass }) => {
  const opts = (IraBanner as any)._opts as Required<Options>

  const isIndex = fileData.slug === "index" || fileData.slug === "404"
  if (opts.condition === "not-index" && isIndex) return null
  if (opts.condition === "index" && !isIndex) return null

  const img = (
    <img
      src={opts.imagePath}
      alt={opts.alt}
      class="ira-banner-img"
      loading="eager"
    />
  )

  return (
    <div class={`ira-banner-wrap ${displayClass ?? ""}`}>
      {opts.linkTo ? (
        <a href={opts.linkTo} class="ira-banner-link" aria-label={opts.alt}>
          {img}
        </a>
      ) : (
        img
      )}
    </div>
  )
}

IraBanner.displayName = "IraBanner"

IraBanner.css = `
.ira-banner-wrap {
  width: 100%;
  margin-bottom: 1.5rem;
  overflow: hidden;
  border-radius: 10px;
  box-shadow: 0 2px 12px rgba(0,0,0,0.10);
  line-height: 0;
}

.ira-banner-link {
  display: block;
  line-height: 0;
}

.ira-banner-img {
  width: 100%;
  height: auto;
  display: block;
  object-fit: cover;
  border-radius: 10px;
  max-height: 220px;
  object-position: center top;
  transition: opacity 0.2s ease;
}

.ira-banner-img:hover {
  opacity: 0.96;
}

@media (max-width: 800px) {
  .ira-banner-img {
    max-height: 160px;
  }
}
`

export default ((opts?: Options) => {
  const merged: Required<Options> = { ...defaultOpts, ...opts }
  ;(IraBanner as any)._opts = merged
  return IraBanner
}) satisfies QuartzComponentConstructor
