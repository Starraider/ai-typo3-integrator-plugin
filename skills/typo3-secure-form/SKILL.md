---
name: typo3-secure-form
description: Harden TYPO3 EXT:form or sf_register frontend forms against automated submissions. Use for honeypot, evoweb/recaptcha, server-side CAPTCHA validation, CAPTCHA CSP, secure credential handling, or non-production form-security verification; do not use it to weaken authentication or store production secrets.
license: CC-BY-4.0
compatibility: Requires TYPO3 with typo3/cms-form or evoweb/sf-register; CAPTCHA configuration must match the installed provider extension and a safe test environment.
---

# TYPO3 Form Security

Harden a targeted frontend form or registration flow without weakening the
existing access model. Select the actual form stack first: `EXT:form`,
`sf_register`, or both. This skill does not replace the dedicated
approval-gated `bw_captcha` registration workflow.

## Workflow

1. **Classify the form and threat boundary.** Read repository instructions,
   identify the form stack, installed TYPO3 and CAPTCHA extensions, expected
   submission path, and current spam/failure symptom. Check current primary
   TYPO3 and extension documentation before version-specific changes.
   **Complete when:** the control is matched to the real form integration, not
   only its rendered markup.
2. **Inspect configuration and secret handling.** Locate the existing form
   definition, TypoScript/site set, template, CSP, and environment-specific
   credentials. Keep site keys and production secrets out of version control,
   logs, prompts, and browser-visible output. Do not change an active provider
   or create a new Google/Cloud account without explicit authorization.
   **Complete when:** configuration ownership and the secure credential source
   are known.
3. **Implement layered, server-side protection.** Retain the form framework's
   CSRF and validation behavior; add a honeypot where supported and configure
   the installed CAPTCHA provider's server-side validator. For `sf_register`,
   use the provider's documented adapter and validation hook. Add only the CSP
   sources required by the provider and test report-only policy first when the
   project supports it.
   **Complete when:** bypassing or omitting a client-side token causes server
   validation to reject the submission.
4. **Validate without real users.** Configuration, CSP, and credentials affect
   runtime behavior, so obtain authorization before mutation. Test in a local
   or staging environment with a test mailbox: valid submission, invalid or
   missing CAPTCHA, honeypot trigger, blocked provider resource, and CSP
   console/network behavior. Clear caches only through the project workflow.
   **Complete when:** the intended submission works, all negative cases fail
   safely, and no sensitive value appears in the test evidence.

## References

Read [references/form-security-guide.md](references/form-security-guide.md) for
the provider-neutral configuration boundary, CSP workflow, verification matrix,
and troubleshooting guidance. Use the installed provider's current
documentation for exact option names and template markup.
