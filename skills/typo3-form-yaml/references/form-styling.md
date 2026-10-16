# TYPO3 Form Styling: Bootstrap, Tailwind, and StyleX

This reference provides dedicated instructions for integrating and styling `typo3/cms-form` markup and classes in three frontend environments:
1. **Bootstrap Package (`bk2k/bootstrap-package`)**
2. **Tailwind CSS**
3. **StyleX Connector (`skom/stylex-connector`)**

---

## 1. Bootstrap Package (`bk2k/bootstrap-package`)

### 1.1 Architecture in TYPO3 v14
In TYPO3 v14, the legacy form templates were removed (`Breaking-106596-RemoveLegacyFormTemplates`), making modern Bootstrap 5-compatible markup the default core standard. The core partials emit standard Bootstrap 5 elements:
- Inputs: `.form-control`
- Dropdowns: `.form-select`
- Checkboxes & Radios: `.form-check`, `.form-check-input`, `.form-check-label`
- Floating Labels: `.form-floating`
- Field Spacing & Labels: `.mb-3`, `.form-label`
- Validation Feedback: `.is-invalid`, `.invalid-feedback`

When `bk2k/bootstrap-package` is installed, it provides a form set (`Configuration/Form/BootstrapPackage/config.yaml`) that imports standard definitions and registers extension paths.

### 1.2 Configuring Bootstrap Classes via Site Package Form YAML
You can customize Bootstrap classes globally for your site package in `Configuration/Form/<Set>/config.yaml`:

```yaml
name: 'vendor/site-package/forms'
label: 'Site Forms'
priority: 200

prototypes:
  standard:
    formElementsDefinition:
      Text:
        properties:
          containerClassAttribute: 'form-element mb-3'
          elementClassAttribute: 'form-control'
          elementErrorClassAttribute: 'is-invalid'
          labelClassAttribute: 'form-label'
      Textarea:
        properties:
          containerClassAttribute: 'form-element mb-3'
          elementClassAttribute: 'form-control'
          elementErrorClassAttribute: 'is-invalid'
          labelClassAttribute: 'form-label'
      Checkbox:
        properties:
          containerClassAttribute: 'form-check mb-3'
          elementClassAttribute: 'form-check-input'
          elementErrorClassAttribute: 'is-invalid'
          labelClassAttribute: 'form-check-label'
      SingleSelect:
        properties:
          containerClassAttribute: 'form-element mb-3'
          elementClassAttribute: 'form-select'
          elementErrorClassAttribute: 'is-invalid'
          labelClassAttribute: 'form-label'
```

### 1.3 Multi-Column Grid Layouts with Bootstrap
To render form elements side-by-side using Bootstrap's grid system, use the `GridRow` and `GridColumn` renderables in your `.form.yaml` definition:

```yaml
renderables:
  -
    type: Page
    identifier: page-1
    label: 'Contact'
    renderables:
      -
        type: GridRow
        identifier: row-1
        label: 'Name Row'
        properties:
          containerClassAttribute: 'row g-3 mb-3'
        renderables:
          -
            type: Text
            identifier: firstName
            label: 'First name'
            properties:
              containerClassAttribute: 'col-md-6'
              elementClassAttribute: 'form-control'
          -
            type: Text
            identifier: lastName
            label: 'Last name'
            properties:
              containerClassAttribute: 'col-md-6'
              elementClassAttribute: 'form-control'
```

### 1.4 Overriding Bootstrap Partials
When you need customized HTML structure (for example, Bootstrap `input-group` with prefix icons or buttons), register custom partial paths in your form configuration:

```yaml
prototypes:
  standard:
    formElementsDefinition:
      Form:
        renderingOptions:
          partialRootPaths:
            200: 'EXT:site_package/Resources/Private/Partials/Form/'
```

Copy the respective core partial from `EXT:form/Resources/Private/Frontend/Partials/` into your site package and customize the markup.

---

## 2. Tailwind CSS

### 2.1 Strategy: Direct Utility Classes vs. Semantic Component Classes

There are two primary approaches for styling TYPO3 forms with Tailwind CSS:

#### Approach A: Direct Utility Classes in YAML
Define Tailwind utility classes directly in the YAML properties (`containerClassAttribute`, `elementClassAttribute`, etc.):

```yaml
prototypes:
  standard:
    formElementsDefinition:
      Text:
        properties:
          containerClassAttribute: 'space-y-1 mb-4'
          elementClassAttribute: 'block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 text-sm'
          elementErrorClassAttribute: 'border-red-500 text-red-900 focus:border-red-500 focus:ring-red-500'
          labelClassAttribute: 'block text-sm font-medium text-gray-700'
```

> **CRITICAL REQUIREMENT: Tailwind Content Scanning**
> If utility classes are stored inside `.yaml` files, Tailwind will purge them unless the YAML directory is included in Tailwind's content scan.
>
> - **Tailwind v4 (CSS entrypoint):**
>   ```css
>   @source "../../Resources/Private/Forms/**/*.yaml";
>   @source "../../Configuration/Form/**/*.yaml";
>   @source "../../Resources/Private/**/*.html";
>   ```
> - **Tailwind v3 (`tailwind.config.js`):**
>   ```javascript
>   module.exports = {
>     content: [
>       "./Resources/Private/Forms/**/*.yaml",
>       "./Configuration/Form/**/*.yaml",
>       "./Resources/Private/**/*.html"
>     ],
>     // ...
>   };
>   ```
> Always use complete, static class names in YAML. Tailwind cannot detect dynamically concatenated class strings.

#### Approach B: Semantic CSS Classes with `@apply` (Recommended)
Keep your Form YAML clean and decoupled by using semantic class names in YAML, then mapping them in your site package stylesheet with `@apply`:

**Form Setup YAML (`Configuration/Form/<Set>/config.yaml`):**
```yaml
prototypes:
  standard:
    formElementsDefinition:
      Form:
        renderingOptions:
          fieldProperties:
            errorMsgClassAttribute: 'form-error-msg'
      Text:
        properties:
          containerClassAttribute: 'form-field'
          elementClassAttribute: 'form-input'
          elementErrorClassAttribute: 'form-input--error'
          labelClassAttribute: 'form-label'
      Textarea:
        properties:
          containerClassAttribute: 'form-field'
          elementClassAttribute: 'form-textarea'
          elementErrorClassAttribute: 'form-textarea--error'
          labelClassAttribute: 'form-label'
```

**Site Package CSS (`Resources/Public/Css/form.css` or entrypoint):**
```css
.form-field {
    @apply mb-4;
}

.form-label {
    @apply block text-sm font-semibold text-slate-800 mb-1.5;
}

.form-input,
.form-textarea {
    @apply block w-full rounded-lg border border-slate-300 bg-white px-3.5 py-2.5 text-sm text-slate-900 shadow-sm transition-colors focus:border-indigo-600 focus:outline-none focus:ring-1 focus:ring-indigo-600;
}

.form-input--error,
.form-textarea--error {
    @apply border-red-500 text-red-900 focus:border-red-500 focus:ring-red-500;
}

.form-error-msg {
    @apply mt-1 text-xs font-medium text-red-600;
}
```

---

## 3. StyleX Connector (`skom/stylex-connector`)

### 3.1 Understanding StyleX in TYPO3
`skom/stylex-connector` compiles styles defined in JavaScript (`.stylex.js`) into atomic CSS at build time and outputs a mapping manifest (`stylex-manifest.json`). In Fluid templates, classes are resolved dynamically via the `{stylex:class(...)}` ViewHelper using semantic style keys (such as `styles: 'Form.input'`).

Because EXT:form YAML properties (`elementClassAttribute`) expect literal class strings and cannot evaluate Fluid ViewHelpers at YAML parse time, the cleanest integration is via **targeted Fluid partial overrides**.

### 3.2 Setting Up the Form Partial Override

1. In your site package's form framework YAML (`Configuration/Form/<Set>/config.yaml`), register custom partial root paths:

```yaml
prototypes:
  standard:
    formElementsDefinition:
      Form:
        renderingOptions:
          partialRootPaths:
            200: 'EXT:site_package/Resources/Private/Partials/Form/'
```

2. Create a StyleX definition file in your frontend build (e.g. `packages/site_package/Resources/Private/Frontend/Styles/Form.stylex.js`):

```javascript
import * as stylex from '@stylexjs/stylex';

export const formStyles = stylex.create({
  container: {
    marginBottom: '1rem',
    display: 'flex',
    flexDirection: 'column',
  },
  label: {
    fontSize: '0.875rem',
    fontWeight: 600,
    color: '#1e293b',
    marginBottom: '0.375rem',
  },
  input: {
    display: 'block',
    width: '100%',
    borderRadius: '0.5rem',
    borderWidth: '1px',
    borderStyle: 'solid',
    borderColor: '#cbd5e1',
    backgroundColor: '#ffffff',
    padding: '0.625rem 0.875rem',
    fontSize: '0.875rem',
    color: '#0f172a',
    outline: 'none',
  },
  inputError: {
    borderColor: '#ef4444',
    color: '#991b1b',
  },
  errorMessage: {
    marginTop: '0.25rem',
    fontSize: '0.75rem',
    color: '#ef4444',
  },
});
```

3. Export the style rules from your Vite entrypoint so `@stylexjs/unplugin` includes them in `stylex-manifest.json`:

```javascript
// main.js
export { formStyles as Form } from './Styles/Form.stylex.js';
```

4. Override the text field partial in `EXT:site_package/Resources/Private/Partials/Form/Text.html` (or `Field/Field.html`):

```html
<html
    xmlns:f="http://typo3.org/ns/TYPO3/CMS/Fluid/ViewHelpers"
    xmlns:formvh="http://typo3.org/ns/TYPO3/CMS/Form/ViewHelpers"
    xmlns:stylex="http://typo3.org/ns/Skom/StylexConnector/ViewHelpers"
    data-namespace-typo3-fluid="true">
<formvh:renderRenderable renderable="{element}">
    <div class="{stylex:class(styles: 'Form.container')}">
        <label for="{element.uniqueIdentifier}" class="{stylex:class(styles: 'Form.label')}">
            {formvh:translateElementProperty(element: element, property: 'label')}
            <f:if condition="{element.required}">
                <span class="required">*</span>
            </f:if>
        </label>
        <f:form.textfield
            property="{element.identifier}"
            id="{element.uniqueIdentifier}"
            value="{element.value}"
            class="{stylex:class(styles: 'Form.input', when: {element.hasErrors: 'Form.inputError'})}"
            additionalAttributes="{formvh:translateElementProperty(element: element, property: 'fluidAdditionalAttributes')}"
        />
        <f:if condition="{element.hasErrors}">
            <f:for each="{element.validationResults.errors}" as="error">
                <span class="{stylex:class(styles: 'Form.errorMessage')}">
                    {formvh:translateElementError(element: element, error: error)}
                </span>
            </f:for>
        </f:if>
    </div>
</formvh:renderRenderable>
</html>
```

### 3.3 Coexistence with Bootstrap Package
When using `skom/stylex-connector` alongside `bk2k/bootstrap-package`:
- Bootstrap Package provides unlayered CSS by default. Set `useCSSLayers: false` in `@stylexjs/unplugin` options inside `vite.config.js`.
- If custom CSS layers (`@layer bootstrap, stylex;`) are explicitly configured in your project, verify that Bootstrap's styles do not override atomic StyleX classes.
- Validate generated keys before deployment:
  ```bash
  vendor/bin/typo3 stylex:validate --required-key Form.input
  ```
