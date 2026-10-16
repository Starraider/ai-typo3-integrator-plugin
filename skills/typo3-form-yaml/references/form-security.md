# Form Security and Anti-Spam in TYPO3 EXT:form

This guide details how to protect TYPO3 `typo3/cms-form` forms against bots, spam, and security vulnerabilities using honeypots, Content Security Policy (CSP) headers, and the local, accessible CAPTCHA extension `blueways/bw-captcha`.

---

## 1. Honeypot Anti-Spam Protection

The Form Framework includes a built-in honeypot mechanism. When enabled, it dynamically injects an off-screen form element with a random alphanumeric name into the form. Legitimate human users do not see or fill in this field, but automated bots typically fill in every field they find. If the honeypot field contains any value upon submission, the form submission is rejected by `TYPO3\CMS\Form\Mvc\Validation\EmptyValidator`.

### 1.1 Prototype Configuration

In TYPO3 v14, honeypot protection is enabled by default in the `standard` prototype. You can explicitly configure or inspect it in your site package's form framework configuration (`Configuration/Form/<Set>/config.yaml` or prototype setup):

```yaml
prototypes:
  standard:
    formElementsDefinition:
      Form:
        renderingOptions:
          honeypot:
            enable: true
            formElementToUse: Honeypot
      Honeypot:
        implementationClassName: TYPO3\CMS\Form\Domain\Model\FormElements\GenericFormElement
        properties:
          containerClassAttribute: form-element
          elementClassAttribute: form-control
          elementErrorClassAttribute: ~
          renderAsHiddenField: false
          styleAttribute: 'position:absolute; margin:0 0 0 -999em;'
        variants:
          - identifier: hide-1
            renderingOptions:
              enabled: false
            condition: 'stepType == "SummaryPage" || finisherIdentifier in ["EmailToSender", "EmailToReceiver"]'
```

### 1.2 Disabling or Enabling per Form Definition

To toggle honeypot protection for a specific form definition, configure `renderingOptions.honeypot.enable` in the root of the `.form.yaml` file:

```yaml
identifier: contact-form
label: 'Contact Form'
type: Form
prototypeName: standard
renderingOptions:
  honeypot:
    enable: true
    formElementToUse: Honeypot
renderables:
  -
    type: Page
    identifier: page-1
    # ...
```

### 1.3 Critical Caveats: Static Caching and Accessibility

1. **Full-Page Static Caching (`EXT:staticfilecache` or reverse proxies):**
   - The Form Framework generates a new random honeypot field name on each form render and stores it in the user's session (`tx_form_honeypot_name_<page>`).
   - If static full-page caching is active on the form page, the static HTML will cache a single visitor's honeypot field name. When another visitor submits the page, their session will not match the cached honeypot field name, triggering false positive validation errors or spam rejections.
   - **Solution:** Always exclude pages containing forms from static full-page caches, or set `enable: false` on static-cached pages only when an alternative anti-spam barrier (such as CAPTCHA) is present.
2. **Accessibility & Screen Readers:**
   - The default core Honeypot uses `styleAttribute: 'position:absolute; margin:0 0 0 -999em;'` to move the field off-screen.
   - To prevent assistive technologies and tab navigation from focusing on the honeypot, verify that the rendered input has `tabindex="-1"` and `autocomplete="off"` or is wrapped in a container with `aria-hidden="true"`.

---

## 2. Content Security Policy (CSP) Headers

TYPO3 v14 provides native Content Security Policy management configured in `config/sites/<site-identifier>/csp.yaml` or via extension `Configuration/ContentSecurityPolicies.php`. Forms interact with CSP across four key directives:

### 2.1 Form Submission Targets (`form-action`)

The `form-action` directive controls valid targets for `<form action="...">` submissions:

```yaml
enforce:
  inheritDefault: true
  mutations:
    - mode: "extend"
      directive: "form-action"
      sources:
        - "'self'"
        # If your form posts to external payment providers or third-party CRM endpoints:
        # - "https://secure.payment-provider.example.com"
```

If `form-action` is not declared, browsers fall back to `default-src`. Restricting `form-action` to `'self'` prevents cross-site form submission hijacking.

### 2.2 Inline Styles vs. Honeypot (`style-src-attr`)

- The core `Honeypot` element uses an inline `style` attribute (`position:absolute; margin:0 0 0 -999em;`).
- TYPO3's default frontend CSP policy (`typo3/cms-frontend/Configuration/ContentSecurityPolicies.php`) includes `MutationMode::Set, Directive::StyleSrcAttr, SourceKeyword::unsafeInline`, allowing inline `style="..."` attributes on elements.
- **Harden without inline styles:** If your site enforces a strict CSP that blocks `style-src-attr 'unsafe-inline'`, the honeypot's inline styles will be blocked. To fix this, remove the inline style attribute in your prototype YAML and apply a stylesheet class (such as Bootstrap's `visually-hidden` or Tailwind's `sr-only`):

```yaml
prototypes:
  standard:
    formElementsDefinition:
      Honeypot:
        properties:
          containerClassAttribute: 'visually-hidden'
          styleAttribute: ''
```

### 2.3 Form Scripts and Nonces (`script-src`)

TYPO3 v14 uses nonces (`SourceKeyword::nonceProxy`) for frontend scripts. When adding JavaScript for AJAX form submission, multi-step validation, or CAPTCHA refresh:
- Inject scripts via Fluid's `<f:asset.script identifier="..." src="...">` ViewHelper rather than hardcoding raw `<script>` tags without nonces.
- TYPO3 automatically attaches the CSP nonce attribute to assets managed by AssetCollector.

---

## 3. blueways/bw-captcha Extension

The extension `blueways/bw-captcha` provides a local, accessible CAPTCHA element for `typo3/cms-form` without third-party dependencies, tracking, or external calls (GDPR/DSGVO compliant). It uses `gregwar/captcha`, generates inline WAV audio speech output, and supports instant AJAX image regeneration.

### 3.1 Installation

Install the extension via Composer:

```bash
composer require blueways/bw-captcha
```

Ensure the PHP GD extension (`ext-gd`) is active in your PHP runtime (standard in DDEV).

### 3.2 Site Set Activation (TYPO3 v14)

In TYPO3 v14, include the `blueways/bw-captcha` Site Set in your site configuration (`config/sites/<site-identifier>/config.yaml`):

```yaml
dependencies:
  - typo3/cms-form
  - blueways/bw-captcha
```

Alternatively, include the Site Set via the TYPO3 Backend in **Site Management > Sites > [Your Site] > Sets**.

### 3.3 Configuration and Site Settings

`bw_captcha` settings can be customized through the Site Settings module (or TypoScript setup):

| Setting | TypoScript / Definition Path | Default | Description |
|---|---|---|---|
| `lifetime` | `plugin.tx_bwcaptcha.settings.lifetime` | `3600` | Phrase session validity in seconds |
| `refreshButton` | `plugin.tx_bwcaptcha.settings.refreshButton` | `true` | Displays reload button |
| `audioButton` | `plugin.tx_bwcaptcha.settings.audioButton` | `true` | Displays audio speech output button |
| `length` | `plugin.tx_bwcaptcha.settings.length` | `5` | Number of characters in captcha |
| `charset` | `plugin.tx_bwcaptcha.settings.charset` | `abcdefghijklmnpqrstuvwxyz123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ` | Character set |
| `width` | `plugin.tx_bwcaptcha.settings.width` | `150` | Image width in pixels |
| `height` | `plugin.tx_bwcaptcha.settings.height` | `40` | Image height in pixels |
| `distortion` | `plugin.tx_bwcaptcha.settings.distortion` | `false` | Enable/disable wave distortion |

### 3.4 Middlewares and CSP Requirements for bw_captcha

`bw_captcha` operates two PSR-15 middlewares:
1. `bw-captcha/captcha` (`pageType: 3413`): Generates and returns the CAPTCHA image with HTTP headers `Cache-Control: no-cache, no-store, private`.
2. `bw-captcha/audio` (`pageType: 3414`): Decodes the encrypted phrase steganographically from the canvas image and generates WAV speech audio.

**CSP Requirements:**
- **Media (`media-src`):** The audio button plays audio synthesized in JavaScript and loaded via `window.URL.createObjectURL(blob)`. This requires `media-src blob:`. `bw_captcha` ships a core `Configuration/ContentSecurityPolicies.php` that automatically registers:
  ```php
  new Mutation(MutationMode::Extend, Directive::MediaSrc, SourceScheme::blob)
  ```
- **Connections (`connect-src`):** Audio playback fetches audio data via `fetch(audioUrl)`. Verify `connect-src` allows `'self'`.
- **Images (`img-src`):** Captcha images are loaded from the site's own origin (`'self'`). The audio player draws the image to a canvas via `toDataURL()`. Keep `img-src 'self'`.

### 3.5 Adding the Captcha Field to Form YAML

Add the `Captcha` renderable element to your `.form.yaml` definition:

```yaml
identifier: secure-contact
label: 'Contact form with CAPTCHA'
type: Form
prototypeName: standard
renderingOptions:
  submitButtonLabel: 'Send message'
renderables:
  -
    type: Page
    identifier: page-1
    label: 'Contact'
    renderables:
      -
        type: Text
        identifier: name
        label: 'Name'
        validators:
          -
            identifier: NotEmpty
      -
        type: Email
        identifier: email
        label: 'Email'
        validators:
          -
            identifier: NotEmpty
          -
            identifier: EmailAddress
      -
        type: Textarea
        identifier: message
        label: 'Message'
        validators:
          -
            identifier: NotEmpty
      -
        type: Captcha
        identifier: captcha
        label: 'Security Check'
        properties:
          elementClassAttribute: form-control
          elementErrorClassAttribute: is-invalid
          fluidAdditionalAttributes:
            autocomplete: 'off'
            required: 'required'
            placeholder: 'Enter the code above'
        validators:
          -
            identifier: NotEmpty
finishers:
  -
    identifier: EmailToReceiver
  -
    identifier: Confirmation
```

> **Note:** The `Captcha` element type automatically maps to `Blueways\BwCaptcha\Domain\Model\FormElements\CaptchaElement` and validates server-side using `Blueways\BwCaptcha\Validation\Validator\CaptchaValidator`. If the entered phrase does not match the session-stored phrase or has expired, validation fails with error code `1623240740` ("validator.captcha.notvalid").

### 3.6 Adding the Captcha via Form Editor (Backend GUI)

When editors build forms using the TYPO3 Form Editor backend module:
1. Open the form in **Web > Forms**.
2. Click **Create new element**.
3. Under the **Custom elements** group, select **Captcha** (icon: `t3-form-captcha-element`).
4. Configure the field label, placeholder, and grid column sizing.
5. In multi-step forms, place the Captcha on the final step before the submit button so the user solves it immediately before final submission.
