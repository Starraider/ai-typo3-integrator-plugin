# TYPO3 Form Security Guide

Use this reference after identifying the actual form stack and installed
CAPTCHA provider. It deliberately does not prescribe provider option names:
those vary by `evoweb/recaptcha` and TYPO3 version and must be confirmed from
the installed package or its current documentation.

## 1. Decide the control boundary

| Form stack | Integration boundary | Required outcome |
| --- | --- | --- |
| `typo3/cms-form` | Form setup and `.form.yaml` definition | The provider's element/validator is configured and the server rejects an invalid response. |
| `evoweb/sf-register` | Provider adapter, registration field configuration, and validator | A failed CAPTCHA blocks registration before a usable frontend account is created. |
| Custom Fluid/Extbase form | Its controller/service validation boundary | The server validates the CAPTCHA independently of browser JavaScript. |

Do not assume that displaying a provider widget means the server validates its
response. Retain TYPO3's existing CSRF protection, normal field validation, and
rate/abuse controls where configured.

## 2. Inspect before configuration

1. Record the TYPO3, `typo3/cms-form`, `sf_register`, and CAPTCHA-extension
   versions from Composer and the installed package.
2. Find the active form definition, form-set/TypoScript configuration, template
   override, site CSP file, and runtime credential source.
3. Read the provider's installed documentation and source configuration before
   choosing an element name, adapter, validator, endpoint, or Fluid markup.
4. Confirm whether the task modifies an existing provider or introduces one.
   Changing providers, adding external origins, and creating a provider account
   require explicit authorization.

## 3. Credentials and runtime configuration

- Keep production secret values in the project’s approved deployment secret
  store or environment-specific runtime configuration. Never put them in a
  committed example, test transcript, prompt, browser markup, or client-side
  configuration.
- A public site key is not a substitute for server-side validation; expose only
  the value the provider requires in the browser.
- Separate local/staging test settings from production. Use provider-supported
  test keys or a test project only when they match the selected provider and
  environment.
- Before changing `config/system/settings.php`, `additional.php`, or deployment
  variables, inspect the repository's existing configuration pattern and obtain
  authorization for the runtime change.

## 4. EXT:form hardening

1. In the active form set, make the installed provider's form element and
   validator available according to its documentation.
2. Add the provider element and validator to the targeted `.form.yaml` only;
   do not silently alter unrelated forms.
3. Enable the built-in honeypot where the form stack supports it. A honeypot is
   an additional signal, not a CAPTCHA replacement.
4. If class or template changes are needed, follow the owning form-YAML and
   asset-build workflow. Do not disable normal validators or finishers to make
   a CAPTCHA pass.

## 5. sf_register hardening

1. Use the installed provider's documented `sf_register` adapter, field type,
   and `validation.create` integration. Do not copy an adapter from a different
   provider or version.
2. Make the server-side validator mandatory for the registration action.
3. If adding a honeypot in a custom registration partial, add a corresponding
   server-side empty-field check; CSS hiding alone cannot validate it.
4. For the `bw_captcha` approval-gated flow, use
   `typo3-frontend-registration` and its dedicated adapter/state-matrix
   guidance instead of mixing Google reCAPTCHA assumptions into that flow.

## 6. CSP rollout

1. Inspect the provider's current required origins and the site's effective
   CSP. Add only the provider-specific `script-src`, `frame-src`, `connect-src`,
   or other directives that are actually needed.
2. Where TYPO3's site-specific CSP supports it, test additions using a report
   disposition before enforcing them. Keep `inheritDefault` behavior explicit
   and preserve unrelated project mutations.
3. Verify the response header and browser network/console evidence after a
   cache clear. Do not disable CSP globally to make the widget render.

## 7. Verification matrix

| Scenario | Expected result |
| --- | --- |
| Valid human submission | Submission follows the existing success path. |
| CAPTCHA missing, expired, or invalid | Server rejects the submission without sending mail or creating an account. |
| Honeypot populated | Server rejects or safely discards the submission according to project behavior. |
| Provider resource blocked | A clear failure is visible; no bypassed server validation occurs. |
| New CSP policy | Required provider requests load with no unrelated policy regression. |
| Safe test evidence | Test values, mail, logs, and screenshots contain no production secrets or real-user data. |

Run these in local or staging with a test mailbox. Add automated browser coverage
only when the repository already has an appropriate browser-test workflow.

## Troubleshooting

| Symptom | First checks |
| --- | --- |
| Widget does not render | Confirm public configuration, the installed provider integration, CSP sources, and asset loading. |
| Widget renders but spam succeeds | Confirm the server-side validator runs in the actual submission path and rejects an omitted token. |
| Every submission fails | Check environment-specific credentials, provider domain/test settings, server clock/network access, and the installed adapter version. |
| Browser shows CSP errors | Compare the effective CSP header with provider-documented origins; test a minimal report-only addition before enforcing. |

## Primary sources

- [TYPO3 Form documentation](https://docs.typo3.org/c/typo3/cms-form/main/en-us/)
- [evoweb/recaptcha documentation](https://docs.typo3.org/p/evoweb/recaptcha/main/en-us/)
- [sf_register documentation](https://docs.typo3.org/p/evoweb/sf-register/main/en-us/)
- [TYPO3 v14 CSP documentation](https://docs.typo3.org/m/typo3/reference-coreapi/14.3/en-us/ApiOverview/ContentSecurityPolicy/Index.html)
