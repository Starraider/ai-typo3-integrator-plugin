# Multi-Step and Conditional Dynamic Forms in TYPO3 EXT:form

This guide details how to build multi-page wizard forms and create dynamic conditional forms in `typo3/cms-form` where fields or subsequent steps appear conditionally based on previous user input (e.g., asking how many people are registering, and then collecting details for each person).

---

## 1. Multi-Step Forms (Multiple Pages)

In the Form Framework, multi-step forms are structured by declaring multiple `Page` renderable elements under `renderables:` in the `.form.yaml` definition.

### 1.1 Multi-Page Structure and Navigation

```yaml
identifier: event-registration
label: 'Event Registration'
type: Form
prototypeName: standard
renderingOptions:
  submitButtonLabel: 'Complete Registration'
renderables:
  -
    type: Page
    identifier: page-attendee-count
    label: 'Step 1: Ticket Quantity'
    renderingOptions:
      nextButtonLabel: 'Next: Attendee Details'
    renderables:
      -
        type: SingleSelect
        identifier: attendeeCount
        label: 'How many attendees are you registering?'
        defaultValue: '1'
        properties:
          options:
            '1': '1 Attendee'
            '2': '2 Attendees'
            '3': '3 Attendees'
        validators:
          -
            identifier: NotEmpty

  -
    type: Page
    identifier: page-attendee-details
    label: 'Step 2: Attendee Details'
    renderingOptions:
      previousButtonLabel: 'Back'
      nextButtonLabel: 'Next: Review'
    renderables:
      # Attendee 1 (always required)
      -
        type: Fieldset
        identifier: attendee-1
        label: 'Attendee 1 (Primary Contact)'
        renderables:
          -
            type: Text
            identifier: name-1
            label: 'Full Name'
            validators:
              -
                identifier: NotEmpty
          -
            type: Email
            identifier: email-1
            label: 'Email Address'
            validators:
              -
                identifier: NotEmpty
              -
                identifier: EmailAddress

  -
    type: SummaryPage
    identifier: page-summary
    label: 'Step 3: Review & Confirm'
    renderingOptions:
      previousButtonLabel: 'Back'
      nextButtonLabel: 'Confirm & Register'
```

### 1.2 Multi-Step Execution Rules
1. **State Persistence (`FormState`):** TYPO3 automatically serializes submitted values across steps into the encrypted `__state` argument. Values from Step 1 are preserved and accessible in Step 2, Step 3, and throughout finisher execution.
2. **Step Validation:** When the user clicks "Next", only the form elements on the current `Page` are validated. Subsequent pages are not validated until the user reaches and submits them.
3. **Summary Page (`SummaryPage`):** A dedicated renderable type (`type: SummaryPage`) that automatically renders a read-only table of all previously completed values before final submission.
4. **CAPTCHA Placement:** In multi-step forms, place the `Captcha` element on the **final interactive step** before the final submit button.

---

## 2. Conditional and Dynamic Forms (Variants)

TYPO3 Form Framework uses **Variants** (`variants:`) powered by Symfony Expression Language to dynamically show, hide, enable, disable, or alter form elements and entire pages based on previous selections.

### 2.1 Variables Available in Variant Conditions
Inside any variant `condition: '...'`, the following variables are available to evaluate:
- `formValues`: An associative array of all values submitted so far. Access field values via `formValues['fieldIdentifier']`.
- `stepIdentifier`: The identifier of the current `Page` (e.g. `'page-attendee-details'`).
- `stepType`: The type of current page (e.g. `'Page'`, `'SummaryPage'`).
- `finisherIdentifier`: Active finisher identifier during finisher execution.
- `site`: The current Site (`SiteInterface`).
- `siteLanguage`: The current SiteLanguage (`SiteLanguage`).

### 2.2 Enabling and Disabling Elements
When a form element has `renderingOptions.enabled: false`, TYPO3:
1. **Skips rendering** the element in the HTML markup.
2. **Bypasses all validators** on that element so required fields that are hidden do not trigger validation errors.
3. Suppresses that element from finisher data and emails (unless explicitly targeted).

If a parent container (such as a `Fieldset`, `GridRow`, or `Page`) is disabled, all nested children are automatically disabled.

---

## 3. Real-World Pattern: Dynamic Attendee Registration

Below is a complete pattern demonstrating a dynamic multi-step form where Step 1 asks for the number of people, and Step 2 conditionally reveals details fields for each person based on that selection.

```yaml
identifier: dynamic-event-registration
label: 'Dynamic Attendee Registration'
type: Form
prototypeName: standard
renderingOptions:
  submitButtonLabel: 'Complete Registration'
renderables:
  # ==========================================
  # STEP 1: QUANTITY SELECTION
  # ==========================================
  -
    type: Page
    identifier: step-quantity
    label: 'Step 1: Number of Attendees'
    renderingOptions:
      nextButtonLabel: 'Continue to Attendee Information'
    renderables:
      -
        type: SingleSelect
        identifier: attendeeCount
        label: 'Number of Attendees'
        defaultValue: '1'
        properties:
          options:
            '1': '1 Person'
            '2': '2 People'
            '3': '3 People'
        validators:
          -
            identifier: NotEmpty

  # ==========================================
  # STEP 2: CONDITIONAL ATTENDEE DETAILS
  # ==========================================
  -
    type: Page
    identifier: step-details
    label: 'Step 2: Attendee Details'
    renderingOptions:
      previousButtonLabel: 'Previous Step'
      nextButtonLabel: 'Review Registration'
    renderables:
      # Attendee 1: Always enabled
      -
        type: Fieldset
        identifier: attendee-1-box
        label: 'Attendee 1 (Primary Contact)'
        renderables:
          -
            type: Text
            identifier: name_1
            label: 'Name (Person 1)'
            validators:
              -
                identifier: NotEmpty
          -
            type: Email
            identifier: email_1
            label: 'Email (Person 1)'
            validators:
              -
                identifier: NotEmpty
              -
                identifier: EmailAddress

      # Attendee 2: Only enabled if attendeeCount >= 2
      -
        type: Fieldset
        identifier: attendee-2-box
        label: 'Attendee 2'
        renderingOptions:
          enabled: false
        variants:
          -
            identifier: show-attendee-2
            condition: 'formValues["attendeeCount"] in ["2", "3"]'
            renderingOptions:
              enabled: true
        renderables:
          -
            type: Text
            identifier: name_2
            label: 'Name (Person 2)'
            validators:
              -
                identifier: NotEmpty
          -
            type: Email
            identifier: email_2
            label: 'Email (Person 2)'
            validators:
              -
                identifier: NotEmpty
              -
                identifier: EmailAddress

      # Attendee 3: Only enabled if attendeeCount == 3
      -
        type: Fieldset
        identifier: attendee-3-box
        label: 'Attendee 3'
        renderingOptions:
          enabled: false
        variants:
          -
            identifier: show-attendee-3
            condition: 'formValues["attendeeCount"] == "3"'
            renderingOptions:
              enabled: true
        renderables:
          -
            type: Text
            identifier: name_3
            label: 'Name (Person 3)'
            validators:
              -
                identifier: NotEmpty
          -
            type: Email
            identifier: email_3
            label: 'Email (Person 3)'
            validators:
              -
                identifier: NotEmpty
              -
                identifier: EmailAddress

  # ==========================================
  # STEP 3: REVIEW & CAPTCHA
  # ==========================================
  -
    type: SummaryPage
    identifier: step-summary
    label: 'Step 3: Review & Confirm'
    renderingOptions:
      previousButtonLabel: 'Edit Information'
    renderables:
      -
        type: Captcha
        identifier: captcha
        label: 'Security Check'
        properties:
          fluidAdditionalAttributes:
            required: 'required'
            autocomplete: 'off'
        validators:
          -
            identifier: NotEmpty

finishers:
  -
    identifier: EmailToReceiver
    options:
      subject: 'New Event Registration ({form.attendeeCount} Attendees)'
      recipients:
        admin@example.com: 'Event Coordinator'
      senderAddress: 'noreply@example.com'
  -
    identifier: Confirmation
    options:
      message: 'Thank you! Your registration has been received.'
```

---

## 4. Conditionally Skipping Entire Pages

You can also apply variants directly to a `Page` renderable to skip an entire page based on prior answers:

```yaml
renderables:
  -
    type: Page
    identifier: page-billing
    label: 'Billing Details'
    renderingOptions:
      enabled: true
    variants:
      # If payment is free, skip the billing page completely
      -
        identifier: skip-billing-for-free-tickets
        condition: 'formValues["ticketType"] == "free"'
        renderingOptions:
          enabled: false
```

When `renderingOptions.enabled: false` is applied to a page, clicking "Next" on the preceding step skips the disabled page and advances directly to the next enabled step.

---

## 5. Single-Page Dynamic Toggles (Progressive Enhancement)

While multi-step forms evaluate conditions between page submissions on the server, forms that require **instant client-side toggling on the same page** (e.g. toggling a "Company Name" input when selecting "Business" vs "Private") benefit from a progressive enhancement approach:

1. **Markup with data attributes:** Configure custom container classes or HTML5 data attributes in YAML:
   ```yaml
   -
     type: RadioButton
     identifier: customerType
     label: 'Customer Type'
     defaultValue: 'private'
     properties:
       options:
         private: 'Private Customer'
         business: 'Business Customer'
   -
     type: Text
     identifier: companyName
     label: 'Company Name'
     properties:
       containerClassAttribute: 'form-element js-toggle-field'
       fluidAdditionalAttributes:
         data-depends-on: 'customerType'
         data-depends-value: 'business'
   ```
2. **Client-side JavaScript:** A lightweight vanilla JS helper toggles the visibility and required status of elements matching `data-depends-on`.
3. **Server-side safety:** Pair client-side toggling with a server-side variant condition (`condition: 'formValues["customerType"] != "business"'` with `renderingOptions.enabled: false`) to guarantee data integrity even if client-side scripts are disabled or bypassed.
