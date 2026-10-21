import { loadQuartzConfig, loadQuartzLayout } from "./quartz/plugins/loader/config-loader"
import { componentRegistry } from "./quartz/components/registry"
import SchemaOrg from "./quartz/components/SchemaOrg"
import Relations from "./quartz/components/Relations"
import IraBanner from "./quartz/components/IraBanner"
import HomeList from "./quartz/components/HomeList"

// Register custom components
componentRegistry.register("SchemaOrg", SchemaOrg, "local")
componentRegistry.register("Relations", Relations, "local")
componentRegistry.register("IraBanner", IraBanner, "local")
componentRegistry.register("HomeList", HomeList, "local")

const config = await loadQuartzConfig()
export default config
export const layout = await loadQuartzLayout()
