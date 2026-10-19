import { PageFrame, PageFrameProps } from "./types"
import HeaderConstructor from "../Header"

const Header = HeaderConstructor()

const MONTHS = ["Jan", "Feb", "Mar", "Apr", "Mei", "Jun", "Jul", "Agu", "Sep", "Okt", "Nov", "Des"]

function fmtIso(value: unknown): string | undefined {
  if (!value) return undefined
  const d = new Date(String(value))
  if (isNaN(d.getTime())) return undefined
  return d.toISOString()
}

function fmtDate(value: unknown): string | undefined {
  if (!value) return undefined
  const d = new Date(String(value))
  if (isNaN(d.getTime())) return undefined
  return `${d.getUTCDate()} ${MONTHS[d.getUTCMonth()]} ${d.getUTCFullYear()}`
}

function PageDates({ fileData }: { fileData: any }) {
  const slug = String(fileData?.slug ?? "")
  if (!slug || slug === "index" || slug === "404" || slug.startsWith("tags/") || slug.endsWith("/index")) {
    return null
  }
  const fm = fileData?.frontmatter ?? {}
  const published = fmtDate(fm.date) ?? fmtDate(fileData?.dates?.created)
  const modified = fmtDate(fm.updated) ?? fmtDate(fm.modified) ?? fmtDate(fileData?.dates?.modified)
  const publishedIso = fmtIso(fm.date) ?? fmtIso(fileData?.dates?.created)
  const modifiedIso = fmtIso(fm.updated) ?? fmtIso(fm.modified) ?? fmtIso(fileData?.dates?.modified)
  if (!published && !modified) return null
  return (
    <p class="ira-dates">
      {published && <span>Diterbitkan: <time datetime={publishedIso}>{published}</time></span>}
      {published && modified && <span> · </span>}
      {modified && <span>Diperbarui: <time datetime={modifiedIso}>{modified}</time></span>}
    </p>
  )
}

/**
 * The default page frame — three-column layout with left sidebar, center
 * content (header + body + afterBody), and right sidebar, followed by a footer.
 *
 * This is the original Quartz layout, extracted from renderPage.tsx.
 */
export const DefaultFrame: PageFrame = {
  name: "default",
  render({
    componentData,
    header,
    beforeBody,
    pageBody: Content,
    afterBody,
    left,
    right,
    footer,
  }: PageFrameProps) {
    return (
      <>
        <div class="left sidebar">
          {left.map((BodyComponent) => (
            <BodyComponent {...componentData} />
          ))}
        </div>
        <div class="center">
          <div class="page-header">
            <Header {...componentData}>
              {header.map((HeaderComponent) => (
                <HeaderComponent {...componentData} />
              ))}
            </Header>
            <div class="popover-hint">
              {beforeBody.map((BodyComponent) => (
                <BodyComponent {...componentData} />
              ))}
              <PageDates fileData={componentData.fileData} />
            </div>

          </div>
          <Content {...componentData} />
          <hr />
          <div class="page-footer">
            {afterBody.map((BodyComponent) => (
              <BodyComponent {...componentData} />
            ))}
          </div>
        </div>
        <div class="right sidebar">
          {right.map((BodyComponent) => (
            <BodyComponent {...componentData} />
          ))}
        </div>
        {footer.map((FooterComponent) => (
          <FooterComponent {...componentData} />
        ))}
      </>
    )
  },
}
