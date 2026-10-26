import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"

const TentangLink: QuartzComponent = (_props: QuartzComponentProps) => {
  return (
    <div className="ira-tentang-link">
      <a href="https://wiki.iraamalia.id/tentang" className="ira-tentang-link-anchor">
        Tentang Wiki Ini →
      </a>
    </div>
  )
}

TentangLink.displayName = "TentangLink"

TentangLink.css = `
.ira-tentang-link {
  margin-top: 0.5rem;
}
.ira-tentang-link-anchor {
  font-size: 0.9rem;
  color: var(--secondary);
}
`

export default (() => TentangLink) satisfies QuartzComponentConstructor
