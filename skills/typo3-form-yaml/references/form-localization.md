# Translating and Localizing Forms in TYPO3 EXT:form

This guide details how to translate forms in `typo3/cms-form` across multilingual TYPO3 websites using XLF localization files, translation key chains, and site language routing.

---

## 1. Architecture of Form Localization

TYPO3 Form Framework uses `TYPO3\CMS\Form\Service\TranslationService` to translate all visible form elements, placeholders, options, navigation buttons, validation messages, and finisher configurations.

### 1.1 How Translation Resolution Works
- The active language is automatically determined by the current frontend request (`$request->getAttribute('language')`) from your Site Configuration.
- When an element is rendered, TYPO3 queries the registered translation files using a prioritized **translation key chain**.
- If a translation key exists in the XLF file for the active language, that label is displayed. If not found, it falls back to the default language, and finally to the literal string declared in the Form YAML definition.

---

## 2. Registering Translation Files

You can register custom XLF translation files globally in your form framework prototype YAML (`Configuration/Form/<Set>/config.yaml`), or specifically for an individual form definition in `.form.yaml`.

### 2.1 Global Registration in Site Package (`config.yaml`)

```yaml
prototypes:
  standard:
    formElementsDefinition:
      Form:
        renderingOptions:
          translation:
            translationFiles:
              20: 'EXT:site_package/Resources/Private/Language/Form/locallang.xlf'
```

### 2.2 Form-Specific Registration (`.form.yaml`)

```yaml
identifier: contact-form
label: 'Contact Form'
type: Form
prototypeName: standard
renderingOptions:
  translation:
    translationFiles:
      20: 'EXT:site_package/Resources/Private/Language/Form/contact.xlf'
renderables:
  # ...
```

Translation files are evaluated in descending numeric key order (`20` overrides `10`).

---

## 3. Translation Key Chains and Hierarchy

When translating an element property, TYPO3 inspects keys in the following order:

### 3.1 Field Labels, Placeholders, and Descriptions
For a form element with identifier `email` in a form named `contact`:

| Priority | Translation Key Pattern | Example |
|---|---|---|
| **1 (Highest)** | `<formIdentifier>.element.<elementIdentifier>.<propertyType>.<property>` | `contact.element.email.properties.label` |
| **2** | `element.<elementIdentifier>.<propertyType>.<property>` | `element.email.properties.label` |
| **3 (Lowest)** | `element.<elementType>.<propertyType>.<property>` | `element.Text.properties.label` |

**Supported properties include:**
- `.properties.label`: Field label
- `.properties.elementDescription`: Helper text beneath the field
- `.properties.fluidAdditionalAttributes.placeholder`: Input placeholder text
- `.renderingOptions.nextButtonLabel`: Next button label on multi-step forms
- `.renderingOptions.previousButtonLabel`: Previous button label on multi-step forms

### 3.2 Select, Radio, and Checkbox Options
For an element `attendeeCount` with option value `2`:

| Priority | Translation Key Pattern | Example |
|---|---|---|
| **1** | `<formIdentifier>.element.<elementIdentifier>.properties.options.<optionValue>` | `event.element.attendeeCount.properties.options.2` |
| **2** | `element.<elementIdentifier>.properties.options.<optionValue>` | `element.attendeeCount.properties.options.2` |
| **3** | `element.<elementType>.properties.options.<optionValue>` | `element.SingleSelect.properties.options.2` |

### 3.3 Form Buttons
- Submit button: `<formIdentifier>.renderingOptions.submitButtonLabel` (e.g. `contact.renderingOptions.submitButtonLabel`)
- Multi-step next: `<formIdentifier>.element.<pageIdentifier>.renderingOptions.nextButtonLabel`
- Multi-step previous: `<formIdentifier>.element.<pageIdentifier>.renderingOptions.previousButtonLabel`

### 3.4 Finisher Options (Emails and Confirmations)
- Email subject: `<formIdentifier>.finisher.<finisherIdentifier>.subject` (e.g. `contact.finisher.EmailToSender.subject`)
- Email title: `<formIdentifier>.finisher.<finisherIdentifier>.title`
- Confirmation message: `<formIdentifier>.finisher.Confirmation.message`

### 3.5 Custom Validation Error Messages
- Element-specific error: `<formIdentifier>.validation.error.<elementIdentifier>.<errorCode>`
- Global error for element: `validation.error.<elementIdentifier>.<errorCode>`
- Generic error code: `validation.error.<errorCode>` (e.g. `1221559976` for `EmailAddress` validator)

---

## 4. Creating XLF Translation Files

Create your translation files under `EXT:site_package/Resources/Private/Language/Form/`.

### 4.1 Default Language File (`locallang.xlf` - English)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<xliff version="1.2" xmlns="urn:oasis:names:tc:xliff:document:1.2">
    <file source-language="en" datatype="plaintext" original="EXT:site_package/Resources/Private/Language/Form/locallang.xlf" date="2026-10-16T10:00:00Z" product-name="site_package">
        <header/>
        <body>
            <!-- Form: contact-form -->
            <trans-unit id="contact-form.element.name.properties.label" resname="contact-form.element.name.properties.label">
                <source>Your Name</source>
            </trans-unit>
            <trans-unit id="contact-form.element.name.properties.fluidAdditionalAttributes.placeholder" resname="contact-form.element.name.properties.fluidAdditionalAttributes.placeholder">
                <source>Jane Doe</source>
            </trans-unit>
            <trans-unit id="contact-form.element.email.properties.label" resname="contact-form.element.email.properties.label">
                <source>Email Address</source>
            </trans-unit>
            <trans-unit id="contact-form.element.message.properties.label" resname="contact-form.element.message.properties.label">
                <source>Your Message</source>
            </trans-unit>
            <trans-unit id="contact-form.renderingOptions.submitButtonLabel" resname="contact-form.renderingOptions.submitButtonLabel">
                <source>Send Inquiry</source>
            </trans-unit>
            <trans-unit id="contact-form.finisher.EmailToSender.subject" resname="contact-form.finisher.EmailToSender.subject">
                <source>Thank you for contacting us</source>
            </trans-unit>
            <trans-unit id="contact-form.finisher.Confirmation.message" resname="contact-form.finisher.Confirmation.message">
                <source>Thank you! Your message has been sent successfully.</source>
            </trans-unit>

            <!-- Multi-Step / Dynamic Event Registration -->
            <trans-unit id="event-registration.element.attendeeCount.properties.label" resname="event-registration.element.attendeeCount.properties.label">
                <source>Number of Attendees</source>
            </trans-unit>
            <trans-unit id="event-registration.element.attendeeCount.properties.options.1" resname="event-registration.element.attendeeCount.properties.options.1">
                <source>1 Person</source>
            </trans-unit>
            <trans-unit id="event-registration.element.attendeeCount.properties.options.2" resname="event-registration.element.attendeeCount.properties.options.2">
                <source>2 People</source>
            </trans-unit>
            <trans-unit id="event-registration.element.page-quantity.renderingOptions.nextButtonLabel" resname="event-registration.element.page-quantity.renderingOptions.nextButtonLabel">
                <source>Next: Attendee Information</source>
            </trans-unit>
        </body>
    </file>
</xliff>
```

### 4.2 German Translation File (`de.locallang.xlf`)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<xliff version="1.2" xmlns="urn:oasis:names:tc:xliff:document:1.2">
    <file source-language="en" target-language="de" datatype="plaintext" original="EXT:site_package/Resources/Private/Language/Form/locallang.xlf" date="2026-10-16T10:00:00Z" product-name="site_package">
        <header/>
        <body>
            <!-- Form: contact-form -->
            <trans-unit id="contact-form.element.name.properties.label" resname="contact-form.element.name.properties.label">
                <source>Your Name</source>
                <target>Ihr Name</target>
            </trans-unit>
            <trans-unit id="contact-form.element.name.properties.fluidAdditionalAttributes.placeholder" resname="contact-form.element.name.properties.fluidAdditionalAttributes.placeholder">
                <source>Jane Doe</source>
                <target>Max Mustermann</target>
            </trans-unit>
            <trans-unit id="contact-form.element.email.properties.label" resname="contact-form.element.email.properties.label">
                <source>Email Address</source>
                <target>E-Mail-Adresse</target>
            </trans-unit>
            <trans-unit id="contact-form.element.message.properties.label" resname="contact-form.element.message.properties.label">
                <source>Your Message</source>
                <target>Ihre Nachricht</target>
            </trans-unit>
            <trans-unit id="contact-form.renderingOptions.submitButtonLabel" resname="contact-form.renderingOptions.submitButtonLabel">
                <source>Send Inquiry</source>
                <target>Anfrage absenden</target>
            </trans-unit>
            <trans-unit id="contact-form.finisher.EmailToSender.subject" resname="contact-form.finisher.EmailToSender.subject">
                <source>Thank you for contacting us</source>
                <target>Vielen Dank für Ihre Nachricht</target>
            </trans-unit>
            <trans-unit id="contact-form.finisher.Confirmation.message" resname="contact-form.finisher.Confirmation.message">
                <source>Thank you! Your message has been sent successfully.</source>
                <target>Vielen Dank! Ihre Nachricht wurde erfolgreich übermittelt.</target>
            </trans-unit>

            <!-- Multi-Step / Dynamic Event Registration -->
            <trans-unit id="event-registration.element.attendeeCount.properties.label" resname="event-registration.element.attendeeCount.properties.label">
                <source>Number of Attendees</source>
                <target>Anzahl der Teilnehmer</target>
            </trans-unit>
            <trans-unit id="event-registration.element.attendeeCount.properties.options.1" resname="event-registration.element.attendeeCount.properties.options.1">
                <source>1 Person</source>
                <target>1 Person</target>
            </trans-unit>
            <trans-unit id="event-registration.element.attendeeCount.properties.options.2" resname="event-registration.element.attendeeCount.properties.options.2">
                <source>2 People</source>
                <target>2 Personen</target>
            </trans-unit>
            <trans-unit id="event-registration.element.page-quantity.renderingOptions.nextButtonLabel" resname="event-registration.element.page-quantity.renderingOptions.nextButtonLabel">
                <source>Next: Attendee Information</source>
                <target>Weiter: Angaben zu den Teilnehmern</target>
            </trans-unit>
        </body>
    </file>
</xliff>
```

---

## 5. Multi-Language Finisher Behavior

By default, finishers inherit the current language of the frontend user from the site configuration:
- In `EmailToSender` and `EmailToReceiver`, leaving `options.translation.language: ''` causes the email to use the language of the page where the form was submitted.
- Custom email templates (`.fluid.html`) receive `{languageKey}` as a variable, allowing localized email greetings or date formatting:
  ```html
  <f:translate key="email.greeting" extensionName="site_package" languageKey="{languageKey}" />
  ```
- If an internal notification email (`EmailToReceiver`) must always arrive in a fixed language (e.g., German for back-office staff regardless of what language the visitor used), set `options.translation.language: 'de'` on that specific finisher in `.form.yaml`.
