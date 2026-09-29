# Integration choices

Use this with the connector's `Documentation/Integrations/Index.rst`; the installed documentation is authoritative. Detect the active site setup from Composer requirements, Site Set dependencies, TypoScript, Vite imports, and rendered assets. A site can use more than one of these.

## Fluid Styled Content

Keep FSC's data processing and editor interface. Configure the site's template paths in its sitepackage, then copy and override only the content templates whose markup needs StyleX classes. Keep FSC CSS when those templates still rely on it. Check selector specificity and actual computed styles. If the sitepackage owns all relevant markup and drops FSC CSS, retain base typography and element rules for rich text in site CSS or explicit StyleX styles.

## Bootstrap Package

Retain its templates, Bootstrap CSS, and JavaScript unless the project explicitly changes ownership. Add StyleX classes to the site's selected overrides or custom content templates. Bootstrap Package normally supplies unlayered Bootstrap CSS, so use `useCSSLayers: false` in `@stylexjs/unplugin`. An `@layer bootstrap, stylex, overrides` declaration alone does not put Bootstrap CSS into a layer. Test a representative Bootstrap Package component and a StyleX styled element in the browser. If the project uses TypoScript CSS delivery rather than the documented Vite asset path, `overrideBootstrapPriority` only applies when the Bootstrap stylesheet key is `bootstrap` or `bootstrap_package_bootstrap`; check the real key first.

## Standalone Bootstrap

Identify whether Bootstrap is imported through Vite, a CDN, or TypoScript and keep its existing JavaScript behavior. For a normal unlayered Bootstrap stylesheet, use `useCSSLayers: false`. With the documented `<vite:asset>` delivery, keep `StylexConnector.includeCssViaTypoScript` false and check the actual cascade and load order. If a separate TypoScript CSS include is deliberately used, enable `overrideBootstrapPriority` only when that include's key is `bootstrap` or `bootstrap_cdn`; otherwise set its order in the site's own asset configuration. Use StyleX CSS layers and `declareCssLayers` only when Bootstrap is deliberately compiled into `@layer bootstrap` too, then inspect computed styles.

## Content Blocks

Keep a block's `.stylex.js` file beside the block, make it reachable from the Vite entrypoint, and use its manifest keys in that block's Fluid template. Each basename must be unique across imported StyleX files. Third-party block CSS remains a cascade participant; inspect affected selectors after integration.
