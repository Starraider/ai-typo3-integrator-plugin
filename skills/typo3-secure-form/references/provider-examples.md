# Provider Examples: evoweb/recaptcha

Concrete starting points for `evoweb/recaptcha` with `typo3/cms-form` and
`evoweb/sf-register`. They complement the provider-neutral
[form-security-guide.md](form-security-guide.md). Option names, adapter
classes, and set identifiers differ between package versions: confirm each one
against the installed package source and its current documentation before use.
Never commit real keys.

## Installation and Site Set dependencies

```bash
ddev composer require evoweb/recaptcha evoweb/sf-register
```

List the dependencies in the site package set so their TypoScript and form
configuration load (identifiers must match the installed sets):

```yaml
# packages/my-site-package/Configuration/Sets/MySitePackage/config.yaml
name: my-vendor/my-site-package
dependencies:
  - evoweb/recaptcha
  - typo3/form
  - evoweb/sf-register-maximum
```

## Runtime configuration (`EXTENSIONS.recaptcha`)

Example keys as used in `config/system/settings.php`. Fill secrets from the
environment (for example via `config/system/additional.php`), not from source
control:

```php
'recaptcha' => [
    'api_server' => 'https://www.google.com/recaptcha/enterprise.js', // or the classic api.js
    'verify_server' => 'https://www.google.com/recaptcha/api/siteverify',
    'enforceCaptcha' => '0',
    'robotMode' => '0',
    'lang' => '',
    'public_key' => '',
    'private_key' => '',
    'invisible_public_key' => '',
    'invisible_private_key' => '',
],
```

### reCAPTCHA Enterprise / Google Cloud migration notes

- Frontend: load `https://www.google.com/recaptcha/enterprise.js` and call the
  `grecaptcha.enterprise` namespace instead of `grecaptcha`.
- Backend: migrated keys continue to work with the legacy `siteverify`
  endpoint. A full Enterprise integration may move to the GCP
  `assessments.create` API, which requires a service account.
- Testing: Enterprise has no shared public test keys. Create
  environment-specific keys in the Google Cloud console and use its testing
  options (for example a fixed testing score or challenge).

## EXT:form

Register the element in the form set (for example
`Configuration/Form/SiteForms/config.yaml`):

```yaml
prototypes:
  standard:
    formElementsDefinition:
      Recaptcha:
        properties:
          containerClassAttribute: 'mb-5'
```

Add the element and validator to the target definition only:

```yaml
identifier: contactForm
type: Form
prototypeName: standard
renderingOptions:
  submitButtonLabel: Submit
  honeypot:
    enable: true
renderables:
  - type: Page
    identifier: page-1
    renderables:
      # ... other fields ...
      - type: Recaptcha
        identifier: recaptcha-1
        label: reCAPTCHA
        renderingOptions:
          doNotShowLabel: true
        validators:
          - identifier: Recaptcha
```

The old version of this skill also set `renderingOptions.useInvisibleRecaptcha: true`
for invisible mode. Check that the installed provider version supports this
option before using it.

## sf_register

```typoscript
plugin.tx_sfregister.settings {
    captcha.recaptcha = Evoweb\Recaptcha\Adapter\SfRegisterAdapter
    fields.configuration.captcha.type = Recaptcha
    validation.create.captcha = Evoweb\SfRegister\Validation\Validator\CaptchaValidator(type = recaptcha)
}
```

A honeypot in a custom registration partial must have a matching server-side
empty-field check:

```html
<div class="sr-only" aria-hidden="true">
    <label for="register-website">Leave this field blank</label>
    <input type="text" id="register-website" name="tx_sfregister_form[website]" tabindex="-1" autocomplete="off" />
</div>
```

Enterprise score-based token in Fluid (the server must still validate it):

```html
<f:asset.script identifier="google_recaptcha_enterprise_api" async="true"
    src="https://www.google.com/recaptcha/enterprise.js?render={settings.captcha.recaptcha.public_key}" />
<f:asset.script identifier="recaptcha_enterprise_submission">
document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('#your-registration-form-id').forEach(function (form) {
        form.addEventListener('submit', function (event) {
            const tokenField = form.querySelector('.recaptcha-v3-token-field');
            if (tokenField && !tokenField.value) {
                event.preventDefault();
                grecaptcha.enterprise.ready(function () {
                    grecaptcha.enterprise.execute('{settings.captcha.recaptcha.public_key}', {action: 'registration'})
                        .then(function (token) { tokenField.value = token; form.submit(); });
                });
            }
        });
    });
});
</f:asset.script>
```

Inline scripts like this one need a CSP nonce or a hash, or they have to move
into an external asset.

## CSP sources commonly required by Google reCAPTCHA

```yaml
# config/sites/<site-id>/csp.yaml
enforce:
  inheritDefault: true
  mutations:
    - mode: extend
      directive: script-src
      sources: ['https://www.google.com/recaptcha/', 'https://www.gstatic.com/recaptcha/']
    - mode: extend
      directive: frame-src
      sources: ['https://www.google.com/recaptcha/', 'https://recaptcha.google.com/']
    - mode: extend
      directive: connect-src
      sources: ['https://www.google.com/recaptcha/'] # needed for Enterprise token requests
```

Roll out with report-only disposition first (see `typo3-csp`).

## Provider-specific troubleshooting

| Symptom | Likely cause | Check |
| --- | --- | --- |
| Blank space instead of widget | Missing public key or wrong script URL | `public_key` in runtime config; 403/404 in console |
| "CAPTCHA invalid" on every submit | Site key and secret from different projects, or domain not allowed | Key pair and domain list in the Google/GCP console |
| `grecaptcha.enterprise is undefined` | Classic `api.js` loaded with Enterprise code | `api_server` points to `enterprise.js` |
| Silent failures, no token | `connect-src` missing from CSP | Effective CSP header |
| Test environment warnings | Classic v2 test keys used with Enterprise | Dedicated test keys with testing options |
| Changes not visible | Cached configuration | `ddev typo3 cache:flush` |
