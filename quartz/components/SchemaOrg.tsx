import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"

const SchemaOrg: QuartzComponent = ({ cfg, fileData }: QuartzComponentProps) => {
  const slug = fileData.slug || ""
  const title = fileData.frontmatter?.title || ""
  const tags = fileData.frontmatter?.tags || []
  const date = fileData.frontmatter?.date || ""
  const description = fileData.description || ""
  
  const baseUrl = `https://${cfg.baseUrl}`
  const pageUrl = `${baseUrl}/${slug}`
  
  // Determine entity type from tags
  const personTags = ['tokoh', 'aktor', 'politikus', 'pengusaha', 'menteri', 'presiden', 'gubernur']
  const orgTags = ['partai', 'organisasi', 'perusahaan', 'bumn', 'yayasan']
  const techTags = ['analisis', 'geopolitik', 'kebijakan', 'ekonomi', 'riset', 'perang-modern', 'tipologi']
  const termTags = ['glosarium', 'istilah', 'definisi', 'konsep']
  
  const isPerson = tags.some(t => personTags.includes(t.toLowerCase()))
  const isOrg = tags.some(t => orgTags.includes(t.toLowerCase()))
  const isTech = tags.some(t => techTags.includes(t.toLowerCase()))
  const isTerm = tags.some(t => termTags.includes(t.toLowerCase()))
  
  // Generate main entity schema
  let mainSchema: Record<string, any> = {}
  
  if (isPerson) {
    mainSchema = {
      "@context": "https://schema.org",
      "@type": "Person",
      "name": title,
      "url": pageUrl,
      "description": description,
      "sameAs": [
        `https://id.wikipedia.org/wiki/${slug.replace(/-/g, '_')}`
      ]
    }
  } else if (isOrg) {
    mainSchema = {
      "@context": "https://schema.org",
      "@type": "Organization",
      "name": title,
      "url": pageUrl,
      "description": description,
      "sameAs": [
        `https://id.wikipedia.org/wiki/${slug.replace(/-/g, '_')}`
      ]
    }
  } else if (isTerm) {
    mainSchema = {
      "@context": "https://schema.org",
      "@type": "DefinedTerm",
      "name": title,
      "description": description,
      "url": pageUrl,
      "inDefinedTermSet": `${baseUrl}/`
    }
  } else {
    // TechArticle / Article for technical analytical entries
    mainSchema = {
      "@context": "https://schema.org",
      "@type": isTech ? "TechArticle" : "NewsArticle",
      "headline": title,
      "url": pageUrl,
      "datePublished": date,
      "author": {
        "@type": "Person",
        "name": "Ira Amalia",
        "url": "https://iraamalia.id/"
      },
      "publisher": {
        "@type": "Organization",
        "name": cfg.pageTitle,
        "url": "https://iraamalia.id/",
        "logo": {
          "@type": "ImageObject",
          "url": `${baseUrl}/static/covers/ira-amalia-cover.jpg`
        }
      }
    }
  }
  
  // BreadcrumbList
  const breadcrumbSchema = {
    "@context": "https://schema.org",
    "@type": "BreadcrumbList",
    "itemListElement": [
      {
        "@type": "ListItem",
        "position": 1,
        "name": "Home",
        "item": baseUrl
      },
      {
        "@type": "ListItem",
        "position": 2,
        "name": title,
        "item": pageUrl
      }
    ]
  }
  
  // Combine schemas
  const schemas = [mainSchema, breadcrumbSchema]
  
  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(schemas) }}
    />
  )
}

export default (() => SchemaOrg) satisfies QuartzComponentConstructor
