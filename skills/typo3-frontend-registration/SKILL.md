---
name: typo3-frontend-registration
description: Implement or review a TYPO3 v14 protected frontend area with self-registration, email confirmation, administrator approval, CAPTCHA, group assignment, and felogin using sf_register and bw_captcha. Use for approval-gated member access; do not use it to define membership policy or replace an existing identity provider.
license: CC-BY-4.0
compatibility: Requires TYPO3 v14, evoweb/sf-register, typo3/cms-felogin, and blueways/bw-captcha; safe verification needs a non-production mailbox and test accounts.
---

# TYPO3 Protected Frontend Registration

Implement or assess an approval-gated registration flow whose only access path
is `submitted (disabled)` → `email confirmed (disabled)` → `admin accepted
(enabled, final group)`. This skill owns the technical flow, not eligibility or
privacy policy decisions.

## Workflow

1. **Establish the access contract.** Identify the user-storage folder,
   registration, confirmation, login, and protected-page IDs; final frontend
   group; administrator recipient; sender/reply-to; and confirmation policy.
   Confirm that no interim state receives the protected group or can log in.
   **Complete when:** the state transition and page/group ownership are agreed.
2. **Inspect dependencies and existing effective configuration.** Check the
   installed TYPO3, `sf_register`, `felogin`, and `bw_captcha` versions, site
   sets, FlexForms, TypoScript, user storage, and mail configuration. With
   authorization, install missing dependencies and add their documented site
   sets; keep registration and `felogin` on the same storage PID.
   **Complete when:** the proposed change uses the active project conventions
   and does not introduce a second login mechanism.
3. **Configure confirmation before approval.** Use the installed `sf_register`
   configuration to require user confirmation and administrator acceptance.
   Keep registration and confirmation autologin disabled, assign the final
   group only at acceptance, and enable the extension's confirmation-button
   protection against mail scanners. Inspect merged frontend TypoScript, not
   only a source file.
   **Complete when:** an unconfirmed, confirmed-pending, declined, and accepted
   user have the intended disabled/group states in effective configuration.
4. **Add accessible notifications and CAPTCHA.** Override only the necessary
   site-package templates; preserve extension-generated action links and
   provide meaningful HTML and plain-text bodies. Integrate `bw_captcha` with
   an `sf_register` adapter and validate server-side; display alone is not a
   control. Do not include passwords, hashes, or unnecessary personal data in
   messages.
   **Complete when:** every state-changing email works without scanner-triggered
   activation, and invalid CAPTCHA prevents account creation.
5. **Protect the destination.** Configure `felogin`, allowed redirects, and
   page access so registration, confirmation, and login remain public while
   only the final group reaches the protected page. Use least-privileged access
   for administrators handling registrations.
   **Complete when:** anonymous and interim-state users cannot reach protected
   content, while an accepted user can after normal login.
6. **Validate in a safe environment.** These changes can create accounts,
   change groups/pages, and route email. Obtain authorization before mutation;
   use test users and mailboxes, never production recipients. Execute the
   complete state matrix, inspect messages in a local mailbox such as Mailpit,
   and check effective settings after cache clear.
   **Complete when:** all negative paths remain denied and only the accepted
   account gets the final group and access.

## References

- [references/registration-workflow.md](references/registration-workflow.md)
  — configuration, CAPTCHA adapter boundary, state matrix, and Mailpit checks.
- [references/email-customization.md](references/email-customization.md) —
  Fluid templates, action links, and accessible mail-copy patterns.
