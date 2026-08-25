---
name: typo3-form-yaml
description: Create, configure, review, or style versioned TYPO3 v14 EXT:form YAML in an extension or site package. Use for Configuration/Form form sets, .form.yaml definitions, extension-path persistence, YAML form-editor setup, form template overrides, or CSS/Tailwind integration; do not use for Extbase plugin forms or FlexForms.
license: CC-BY-4.0
compatibility: Requires TYPO3 v14 with typo3/cms-form; verify the installed minor version before selecting auto-discovery or legacy YAML registration.
---

# TYPO3 Form YAML

Manage source-controlled TYPO3 `EXT:form` configuration and definitions in the
owning extension or site package. The default is versioned extension-path YAML;
database storage is an explicit alternative, not an automatic migration.

## Workflow

1. **Classify the form and version.** Confirm the request concerns `EXT:form`,
   identify the exact TYPO3 v14 minor release, the owning package, current
   storage location, and whether editors must save definitions. Do not apply
   this skill to Extbase forms or FlexForms.
   **Complete when:** the correct storage and registration branch is selected.
2. **Inspect before changing configuration.** Read repository instructions,
   current form setup, form definitions, template overrides, and asset build.
   For v14.2+ use a `Configuration/Form/<Set>/config.yaml` form set when the
   installed project supports auto-discovery; for earlier v14 minors, use the
   frontend and backend registration pattern in the reference.
   **Complete when:** the form setup loads in every required frontend and
   backend context without competing configuration paths.
3. **Implement the smallest source-controlled change.** Keep framework setup
   under `Configuration/Form/` and definitions under
   `Resources/Private/Forms/`. Prefer shared prototype defaults, then
   form-specific YAML, then a Fluid override only when markup must change. Do
   not enable save/delete access to extension paths unless the user has chosen
   that editor workflow.
   **Complete when:** configuration, definition, and template ownership are
   clear and no unrelated storage mechanism has changed.
4. **Keep styling buildable.** Use built-in class attributes before custom
   templates. If classes occur in YAML, make the project's CSS build scan or
   safelist them; avoid dynamically composed utility names.
   **Complete when:** generated CSS contains the classes emitted by the form.
5. **Validate safely.** Configuration and template edits change project files;
   obtain authorization before applying them. Run authorized asset and cache
   steps, inspect parsed Form YAML in TYPO3 where available, and verify the
   mounted form URL. Submit valid and invalid input in a safe environment.
   **Complete when:** the intended form renders, validation and finishers still
   work, and the browser-visible output matches the requested change.

## Reference

Read [references/typo3-v14-form-patterns.md](references/typo3-v14-form-patterns.md)
for version gates, layouts, persistence, YAML examples, styling, editor
configuration, and verification details.
