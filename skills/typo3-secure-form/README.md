# TYPO3 Form Security

Use this skill to harden TYPO3 `EXT:form` and `sf_register` submissions with the installed CAPTCHA provider, honeypot measures, CSP review, and project-specific verification.

## What this skill solves

It covers security controls for `typo3/cms-form` and `evoweb/sf-register`, including the installed provider's server-side checks, appropriate Content Security Policy directives, credential boundaries, and safe non-production testing. It does not replace the approval-gated `bw_captcha` registration workflow.

## Use when

- Securing an EXT:form contact, request, or application form.
- Adding the installed CAPTCHA provider to a TYPO3 frontend form or registration flow.
- Reviewing CAPTCHA validation, honeypot behaviour, CSP requirements, or secret handling.
- Investigating spam submissions or failed validation in a local TYPO3 environment.

## Expected outputs

- A security-focused form or registration configuration matched to the installed TYPO3 and CAPTCHA extensions.
- Client and server-side validation wiring, including required CSP changes.
- A non-production test plan that covers valid, invalid, and spam-like submissions.
- Clearly documented operational follow-up such as secret provisioning, without storing secrets in the skill.

## Context requirements

- TYPO3 version, installed form/registration extensions, and project instructions.
- Whether the target is EXT:form, `sf_register`, or both.
- The CAPTCHA provider, credential-provisioning process, CSP policy, and safe test environment.

## Installation

This directory is an Agent Skill supplied by the `typo3-extension-skills` plugin. It uses the portable Agent Skills core and is automatically discoverable by compatible Agent Plugin clients from `skills/typo3-secure-form/`.

## Example prompts

- "Harden our TYPO3 EXT:form contact form with its installed CAPTCHA provider and update CSP safely."
- "Review why our sf_register CAPTCHA accepts spam submissions."
- "Create a local DDEV verification checklist for reCAPTCHA and honeypot behaviour."

## Validation

Read [the form-security guide](references/form-security-guide.md), follow the project's `AGENTS.md` if present, and test form submissions only in a non-production environment. Verify valid submissions, invalid CAPTCHA responses, honeypot triggers, and browser CSP behaviour.

## Related skills

- `typo3-form-yaml` — for YAML-defined EXT:form structure and styling.
- `typo3-frontend-registration` — for approval-gated registration workflows that need form hardening.

## License

This project and all contained Agent Skills are licensed under the [Creative Commons Attribution 4.0 International License (CC BY 4.0)](../../LICENSE).

Copyright (c) 2026 Sven Kalbhenn ([https://www.skom.de](https://www.skom.de)).
