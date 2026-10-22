import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"

const LandingLink: QuartzComponent = (_props: QuartzComponentProps) => {
  return (
    <div className="ira-landing-link">
      <a href="https://iraamalia.id" className="ira-landing-link-anchor">
        Lihat Landing Page →
      </a>
    </div>
  )
}

LandingLink.displayName = "LandingLink"

LandingLink.css = `
.ira-landing-link {
  margin-top: 1rem;
}
.ira-landing-link-anchor {
  font-size: 0.9rem;
  color: var(--secondary);
}
`

export default (() => LandingLink) satisfies QuartzComponentConstructor
