---
name: typo3-form-yaml
description: Create, configure, secure, and style versioned TYPO3 v14 EXT:form YAML in a site package or extension. Use for Configuration/Form form sets, .form.yaml definitions, multi-step/conditional forms, XLF localization, extension-path persistence, anti-spam security (honeypots, CSP, blueways/bw-captcha), and custom finisher emails with embedded images/SVGs. Covers styling for Bootstrap Package, Tailwind CSS, and skom/stylex-connector; do not use for Extbase plugin forms or FlexForms.
license: CC-BY-4.0
compatibility: Requires TYPO3 v14 with typo3/cms-form; verify installed packages before configuring form sets, security features, or styling pipelines.
---

# TYPO3 Form YAML

Manage source-controlled TYPO3 `EXT:form` configuration, anti-spam security, multi-step dynamic forms, multilingual XLF localization, custom finisher emails, and definitions in the owning extension or site package. The default is versioned extension-path YAML; database storage is an explicit alternative, not an automatic migration.

## Workflow

1. **Classify the form, version, and architecture.** Confirm the request concerns `EXT:form`, identify the exact TYPO3 v14 minor release (v14.2+ form-set auto-discovery vs v14.0–v14.1 legacy registration), storage location, and whether editors must save definitions. Do not apply this skill to Extbase plugin forms or FlexForms.
   **Complete when:** the correct registration and storage paths are selected.
2. **Harden form security and anti-spam.**
   - Configure the built-in honeypot (`renderingOptions.honeypot.enable: true`, `formElementToUse: Honeypot`). On pages with full-page static caching, disable static caching or prevent honeypot session token cache poisoning.
   - Enforce CSP compatibility: verify `form-action` permits the submission target, ensure `media-src blob:` and `connect-src 'self'` for audio speech output, and avoid inline styles if strict `style-src-attr` is enforced.
   - Install and configure `blueways/bw-captcha` for privacy-friendly, local CAPTCHA protection. Add the `Captcha` renderable to `.form.yaml` or Form Editor with accessible labels, reload button, and audio output. In multi-step forms, place CAPTCHA on the final step before submission.
   Read [references/form-security.md](references/form-security.md).
   **Complete when:** anti-spam mechanisms (honeypot, CSP rules, and CAPTCHA validation) are configured and reject invalid submissions server-side.
3. **Structure multi-step and conditional dynamic forms.**
   - Configure multi-step wizard flows using multiple `Page` renderable elements and optional `SummaryPage`.
   - Apply dynamic conditional logic via `variants:` and Expression Language (`condition: 'formValues["attendeeCount"] in ["2", "3"]'`), using `renderingOptions.enabled: false` to hide and bypass validation on irrelevant fields or pages.
   - For same-page instant toggling, pair client-side data attributes with server-side variant conditions to protect validation integrity.
   Read [references/multistep-conditional-forms.md](references/multistep-conditional-forms.md).
   **Complete when:** multi-step navigation works, conditional fields enable/disable based on prior input, and unnecessary validators are skipped.
4. **Translate and localize forms.**
   - Register XLF translation files via `renderingOptions.translation.translationFiles` in `config.yaml` or `.form.yaml`.
   - Structure XLF keys according to the key chain hierarchy (`<formIdentifier>.element.<elementIdentifier>.properties.<property>`, options, and finisher subjects).
   - Ensure finisher emails adapt to the frontend language or enforce fixed back-office languages where needed.
   Read [references/form-localization.md](references/form-localization.md).
   **Complete when:** all form fields, options, buttons, validation messages, and finisher emails render in the visitor's active site language.
5. **Implement the smallest source-controlled change.** Keep framework setup under `Configuration/Form/<Set>/config.yaml` and definitions under `Resources/Private/Forms/`. Prefer shared prototype defaults, then form-specific YAML, then a Fluid override only when markup structure must change. Do not enable save/delete access to extension paths unless the user has chosen that editor workflow.
   **Complete when:** configuration, definition, and template ownership are clear and no unrelated storage mechanism has changed.
6. **Integrate styling for the active CSS architecture.**
   - **Bootstrap Package:** Rely on native TYPO3 v14 Bootstrap 5 markup (`form-control`, `form-select`, `form-check`, `mb-3`, `is-invalid`). Customize classes in prototype YAML or use `GridRow`/`GridColumn` for responsive grid layouts.
   - **Tailwind CSS:** When placing utility classes in YAML, ensure Tailwind scans Form YAML via `@source "../../Resources/Private/Forms/**/*.yaml"` (Tailwind v4) or `content` array (Tailwind v3), or use semantic classes mapped with `@apply`.
   - **StyleX Connector:** Override form partials (`partialRootPaths`) to apply atomic classes via `{stylex:class(styles: 'Form.input')}` from the registered StyleX manifest. Set `useCSSLayers: false` when paired with Bootstrap Package.
   Read [references/form-styling.md](references/form-styling.md).
   **Complete when:** generated CSS contains the classes emitted by the form and layout renders correctly.
7. **Customize finisher emails and media embedding.**
   - Configure custom template paths (`templateRootPaths`, `partialRootPaths`, `layoutRootPaths`) for `EmailToReceiver` and `EmailToSender` in `config.yaml` or `.form.yaml`.
   - Provide paired HTML (`.fluid.html`) and plain-text (`.fluid.txt`) templates using robust table layouts and inline styling.
   - Embed raster images with absolute URLs (`<img src="{f:uri.image(src: '...', absolute: 1)}" width="..." height="..." style="display:block; border:0;" />`).
   - Rasterize SVGs on the fly for broad email client support (`<f:image src="...svg" fileExtension="png" width="400c" absolute="1" />`) to avoid broken rendering in Gmail and Outlook.
   Read [references/email-templates.md](references/email-templates.md).
   **Complete when:** finisher email templates render branded HTML and plain-text versions, and embedded graphics display reliably across mail clients.
8. **Validate safely.** Configuration and template edits change project files; obtain authorization before applying them. Run authorized asset and cache steps, inspect parsed Form YAML in TYPO3, and verify the mounted form URL in a browser:
   - Submit valid input through all steps and verify finishers (including emails) execute as expected.
   - Test conditional branches (e.g., verifying fields for additional attendees are required only when selected).
   - Test multi-language display by switching frontend site languages.
   - Submit invalid input, empty honeypots, and invalid CAPTCHA to verify server-side validation error handling.
   - Inspect browser developer tools for CSP console violations or missing stylesheets.
   - Test generated emails in Mailpit/MailHog or real email clients for proper HTML layout, text fallback, and image rendering.
   Read [references/typo3-v14-form-patterns.md](references/typo3-v14-form-patterns.md).
   **Complete when:** the form renders across languages, dynamic conditions and multi-step navigation behave correctly, validations and finishers work, and emails match brand design.

## References

- Form security, honeypot, CSP, and bw_captcha: [references/form-security.md](references/form-security.md)
- Styling with Bootstrap Package, Tailwind, and StyleX: [references/form-styling.md](references/form-styling.md)
- Custom email templates, layout, and image/SVG embedding: [references/email-templates.md](references/email-templates.md)
- Multi-step wizard forms, conditions, and dynamic attendee fields: [references/multistep-conditional-forms.md](references/multistep-conditional-forms.md)
- Translating and localizing forms across site languages: [references/form-localization.md](references/form-localization.md)
- Core patterns, version gates, persistence, and YAML examples: [references/typo3-v14-form-patterns.md](references/typo3-v14-form-patterns.md)
