# Registration Workflow Reference

This reference describes the technical contract for a TYPO3 v14 registration
flow using `sf_register`, `felogin`, and `bw_captcha`. Confirm exact settings,
template names, and adapter APIs against the installed extension versions
before implementation.

## State model

| Event | Enabled | Protected group | Access result |
| --- | --- | --- | --- |
| Visitor submits a valid registration | No | No | Cannot log in. |
| Visitor confirms email | No | No | Cannot log in; administrator review is pending. |
| Administrator accepts | Yes | Yes | Can log in and access the protected page. |
| Administrator declines | No | No | Cannot log in. |

Do not use an interim group that grants access. Configure the final group only
for acceptance, and keep registration/confirmation autologin disabled.

## Configuration evidence to inspect

Before changing configuration, collect:

- the active `sf_register` settings after Site Set, TypoScript, and FlexForm
  merging;
- the `fe_users` storage PID used by both registration and `felogin`;
- page IDs for registration, confirmation, login, and protected content;
- final group, administrator recipient, sender, and reply-to values; and
- installed `sf_register`, `felogin`, and `bw_captcha` documentation/source.

For confirmation before administrator approval, `sf_register` documents the
`confirmEmailPostCreate` and `acceptEmailPostConfirm` flow controls. Its
`enableConfirmationButtonForEmailLinks` and
`forceConfirmationButtonForEmailLinks` settings protect state-changing links
from scanner and preview requests when both are enabled. Validate the effective
values in the running frontend configuration, not just a source YAML file.

## Dependency and site-set boundary

The project needs compatible `evoweb/sf-register`, `typo3/cms-felogin`, and
`blueways/bw-captcha` packages. Add dependencies and documented Site Sets only
after authorization. The site set names and configuration locations may differ
between installed versions, so inspect package metadata before editing the
owning site package.

Do not add a second frontend-login mechanism. `sf_register` and `felogin` must
operate on the same configured frontend-user storage.

## bw_captcha adapter boundary

`bw_captcha` provides an accessible TYPO3 Form CAPTCHA element; `sf_register`
requires an adapter that extends its installed captcha adapter base class and
implements the version's rendering and validation contract.

1. Inspect the installed `bw_captcha` source for its supported rendering and
   validation service/API. Do not access or compare undocumented session keys
   directly.
2. Implement the adapter in the site package and register it under a project
   key in `sf_register` settings.
3. Configure the corresponding field type and mandatory server-side validator
   only for the Create action, using the installed extension's static field
   configuration or supported PSR-14 event.
4. Render the extension-provided/compatible CAPTCHA partial with labelled input,
   refresh, and audio controls. Preserve the extension's CSP-safe JavaScript
   initialization and routes.

The result must reject missing or invalid CAPTCHA server-side and retain
keyboard/audio accessibility. Use the installed package as the source of truth
for CSS classes, partial name, PageType routes, and reinitialization behavior.

## Administrator decision and email safety

Prefer the documented `sf_register` email action flow for accept/decline, with
least-privileged administrators. A manual List-module edit is a recovery path,
not the normal process, because it can bypass extension notifications and state
handling.

Generate confirmation, acceptance, and decline links with the extension's
ViewHelper. Never build them manually or expose passwords, confirmation hashes,
or unnecessary submitted data. Keep HTML and plain-text notices equivalent in
their action, outcome, and support contact. See
[email-customization.md](email-customization.md) for templates and review
criteria.

## Login and page protection

Place a normal `felogin` element on the public login page. Configure only
authorized redirect destinations, keep registration/confirmation/login pages
public, and restrict the destination page using the final frontend group. Test
the redirect and access rule using a fresh anonymous session.

## Verification matrix

| Scenario | Expected result |
| --- | --- |
| Invalid or missing CAPTCHA | No `fe_users` record is created. |
| Valid registration | Account remains disabled and outside the protected group. |
| Confirmation email link is scanned | No state transition occurs until the intended confirmation interaction. |
| Confirmed account | Still disabled and unable to access protected content. |
| Decline action | Remains disabled; intended decline message is sent. |
| Accept action | Becomes enabled, receives only the final group, and gets the intended message. |
| Final-group login | `felogin` succeeds and the protected page becomes reachable. |
| Message rendering | Test mailbox shows correct recipient, sender/reply-to, action links, HTML, and plain text. |

Use a test account and local/staging mailbox such as DDEV Mailpit. Never send
verification traffic to production recipients or include secrets/hashes in test
evidence.

## Primary sources

- [sf_register configuration](https://docs.typo3.org/p/evoweb/sf-register/14.0/en-us/Configuration/Index.html)
- [sf_register email configuration](https://docs.typo3.org/p/evoweb/sf-register/14.0/en-us/Configuration/Emails/Index.html)
- [sf_register extension points](https://docs.typo3.org/p/evoweb/sf-register/14.0/en-us/Extendability/Index.html)
- [TYPO3 felogin](https://docs.typo3.org/c/typo3/cms-felogin/main/en-us/Index.html)
- [bw_captcha](https://github.com/maikschneider/bw_captcha)
