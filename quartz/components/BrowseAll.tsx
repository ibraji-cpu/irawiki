import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"

const BrowseAll: QuartzComponent = (_props: QuartzComponentProps) => {
  return (
    <div className="browse-all" style={{ marginTop: "1rem" }}>
      <h3 style={{ marginBottom: "0.5rem", fontSize: "0.95rem" }}>Atau Telusuri Semua</h3>
      <a href="/tags/" className="internal" style={{ fontSize: "0.9rem", color: "var(--secondary)" }}>
        Browse semua artikel →
      </a>
    </div>
  )
}

BrowseAll.displayName = "BrowseAll"

export default (() => BrowseAll) satisfies QuartzComponentConstructor
