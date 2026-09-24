---
name: typo3-ext-container
description: Build or review TYPO3 nested-content and grid CTypes with b13/container. Use for B13\Container\Tca\Registry, ContainerConfiguration, ContainerProcessor, ContentAreaProcessor (TYPO3 v14+), two- or three-column containers, editor-facing container options, backend previews, responsive container rendering in a site package, or integrating EXT:container with Content Blocks (friendsoftypo3/content-blocks).
license: CC-BY-4.0
compatibility: Requires a TYPO3 project using b13/container; verify the installed extension and TYPO3 versions before applying version-specific APIs.
---

# TYPO3 Container

Create a project-owned `b13/container` CType that follows the target site's
existing TCA, TypoScript, Fluid, icon, and CSS conventions. This skill does not
own generic TYPO3 backend layouts or a new design system.

## Workflow

1. **Establish the target.** Read repository instructions; identify the owning
   site package, TYPO3 and `b13/container` versions, existing container CTypes,
   command wrapper, and CSS framework. Inspect `composer.json`, the installed
   package, and existing TCA/Fluid conventions before choosing APIs or paths.
   **Complete when:** the requested grid, columns, editor options, and
   framework are explicit; ask for a choice if the framework is not evident.
2. **Confirm the change boundary.** Describe planned Composer, schema, cache,
   asset-build, and frontend changes before making them. Obtain authorization
   before installing dependencies, changing database schema, or modifying
   production content configuration. Never edit `vendor/`.
   **Complete when:** the target files and state-changing commands are known.
3. **Register the CType.** Use the Registry and a stable project-prefixed CType
   identifier, unique `colPos` values, localized labels, and an existing or
   project-owned icon. Preserve the registry-generated TCA setup; extend it
   rather than replacing its `showitem` configuration.
   **Complete when:** the CType appears in the intended wizard group and its
   grid matches the requested editable columns.
4. **Add only necessary options and rendering.** Add prefixed `tt_content`
   fields and matching schema only for requested styling controls. Configure
   TypoScript from `lib.contentElement` and use `ContainerProcessor` to expose
   each child column. Map stored option values to classes from the detected
   framework; do not invent framework-agnostic CSS or dynamically construct
   Tailwind utilities.
   **Complete when:** every configured field is visible only for relevant
   CTypes and every column has matching registration and rendering.
5. **Apply restrictions and previews cautiously.** Follow the installed
   `b13/container` documentation for allowed/disallowed child types and any
   `content_defender` integration; do not assume a core API from another TYPO3
   version. Add a backend preview or PSR-14 listener only for a demonstrated
   editor or cross-cutting need.
   **Complete when:** restrictions and previews match installed-package
   behavior rather than a copied version-specific example.
6. **Verify end to end.** Run the project’s authorized schema/update, asset,
   and cache commands. Check the content-element wizard, edit form, backend
   grid, and rendered page at desktop and mobile widths. Test each changed
   option and a container with child content in every declared column.
   **Complete when:** database columns, processed children, responsive layout,
   and editor controls all behave as specified.

## Integration with Content Blocks (friendsoftypo3/content-blocks)

When the project uses `friendsoftypo3/content-blocks`, the workflow for adding
a container CType changes significantly. Content Blocks handles CType
registration, labels, icons, and the frontend Fluid template. EXT:container
provides only the column grid and backend preview.

**Do not** use `Registry::configureContainer()` in this mode. Instead:

1. **Define a Content Block** (`config.yaml`) with `group: container` and
   `saveAndClose: true`. Omit Collection fields for child columns.

   ```yaml
   name: vendor/two-column-container
   typeName: vendor_two_columns_container
   group: container
   saveAndClose: true
   fields:
     - identifier: header
       useExistingField: true
   ```

2. **Register the column grid directly in TCA** (not via the Registry):

   ```php
   // EXT:site_package/Configuration/TCA/Overrides/tt_content.php
   use B13\Container\Tca\ContainerConfiguration;

   $containerConfiguration = new ContainerConfiguration(
       cType: 'vendor_two_columns_container',
       label: '',       // managed by Content Blocks labels.xlf
       description: '', // managed by Content Blocks labels.xlf
       grid: [
           [
               ['name' => 'Left',  'colPos' => 200],
               ['name' => 'Right', 'colPos' => 201],
           ],
       ]
   );
   $GLOBALS['TCA']['tt_content']['containerConfiguration'][$containerConfiguration->getCType()] = $containerConfiguration->toArray();
   ```

   > EXT:container **4.0.0+**: Preview renderer override is no longer required;
   > Content Blocks handles it automatically.

3. **Add a TypoScript ContainerProcessor** to the Content Block's rendering:

   ```typoscript
   tt_content.vendor_two_columns_container {
       dataProcessing {
           100 = B13\Container\DataProcessing\ContainerProcessor
           100 { colPos = 200 as = children_left }
           110 = B13\Container\DataProcessing\ContainerProcessor
           110 { colPos = 201 as = children_right }
       }
   }
   ```

   **TYPO3 v14+ alternative** — use `ContentAreaProcessor` for automatic lazy
   loading of columns into the `content` variable:

   ```typoscript
   tt_content.vendor_two_columns_container {
       dataProcessing {
           100 = B13\Container\DataProcessing\ContentAreaProcessor
       }
   }
   ```

4. **Render children** in the Content Block's `templates/frontend.fluid.html`:

   With `ContainerProcessor`:
   ```html
   <f:for each="{children_left}" as="child">
       <f:format.raw>{child.renderedContent}</f:format.raw>
   </f:for>
   ```

   With `ContentAreaProcessor` (v14+):
   ```html
   <f:if condition="{content.200}">{content.200 -> f:render.contentArea()}</f:if>
   <f:if condition="{content.201}">{content.201 -> f:render.contentArea()}</f:if>
   ```

**Summary of responsibility split:**

| Concern | Owner |
|---|---|
| CType registration | Content Blocks (`config.yaml`) |
| Labels / description / icon | Content Blocks (`labels.xlf`, `assets/icon.svg`) |
| Column grid (colPos) | EXT:container (TCA `containerConfiguration`) |
| Backend preview | EXT:container ≥ 4.0 (automatic) |
| Frontend Fluid template | Content Blocks (`templates/frontend.fluid.html`) |

Always pair this skill with the `typo3-content-blocks` skill when working in
this combined mode.

## References

Read [references/container-patterns.md](references/container-patterns.md) for
Registry, TCA, TypoScript, Fluid, backend-preview, and troubleshooting patterns.
Treat it as a starting pattern and reconcile it with the installed package
before implementation.
