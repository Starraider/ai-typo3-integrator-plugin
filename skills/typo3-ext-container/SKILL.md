---
name: typo3-container
description: Build or review TYPO3 nested-content and grid CTypes with b13/container. Use for B13\Container\Tca\Registry, ContainerConfiguration, ContainerProcessor, two- or three-column containers, editor-facing container options, backend previews, or responsive container rendering in a site package.
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

## References

Read [references/container-patterns.md](references/container-patterns.md) for
Registry, TCA, TypoScript, Fluid, backend-preview, and troubleshooting patterns.
Treat it as a starting pattern and reconcile it with the installed package
before implementation.
