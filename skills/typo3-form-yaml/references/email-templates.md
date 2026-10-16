# Customizing TYPO3 EXT:form Emails: Design, Images, and SVGs

The TYPO3 Form Framework uses `TYPO3\CMS\Form\Domain\Finishers\EmailFinisher` for both `EmailToReceiver` and `EmailToSender`. Under the hood, TYPO3 renders emails using `TYPO3\CMS\Core\Mail\FluidEmail`, generating multipart MIME messages with both HTML (`.fluid.html`) and plain-text (`.fluid.txt`) bodies.

This guide shows how to override email templates, customize layout and styles to match brand designs, access form values, and safely embed images and SVG graphics across email clients.

---

## 1. Architecture of Form Emails

### 1.1 Core Components
- **Finisher:** `EmailToReceiver` (notification to website owner) and `EmailToSender` (confirmation to form submitter). Both use `EmailFinisher`.
- **Engine:** `FluidEmail` built with `Symfony\Component\Mime\Email`.
- **Default Template:** `Default.fluid.html` and `Default.fluid.txt` located in `EXT:form/Resources/Private/Frontend/Templates/Finishers/Email/`.
- **Default Layout:** `<f:layout name="SystemEmail" />` provided by `EXT:core/Resources/Private/Layouts/SystemEmail.fluid.html`.

### 1.2 Available Template Variables
Inside the email Fluid templates, the following variables are automatically available:
- `{form}`: The `FormRuntime` instance. Individual submitted field values can be accessed via `{form.fieldName}` or `{form.formValues.fieldName}`.
- `{title}`: The email title (defaults to the subject).
- `{messageBefore}`: Rich text entered in the form editor to appear before values.
- `{messageAfter}`: Rich text entered in the form editor to appear after values.
- `{hideFormValues}`: Boolean indicating whether form values should be suppressed.
- `{languageKey}`: Frontend language identifier for translations.
- `{normalizedParams.siteUrl}`: The fully qualified website base URL (e.g. `https://www.example.com/`).
- `{typo3.sitename}`: Name of the TYPO3 site.
- Any custom variables defined under finisher `options.variables`.

---

## 2. Registering Custom Email Template Paths

You can override email template paths globally in your site package's form framework YAML (`Configuration/Form/<Set>/config.yaml`), or per form definition in `.form.yaml`.

### 2.1 Global Site Package Configuration

Register template, partial, and layout paths in `Configuration/Form/<Set>/config.yaml`:

```yaml
prototypes:
  standard:
    finishersDefinition:
      EmailToReceiver:
        options:
          templateName: 'Default'
          templateRootPaths:
            20: 'EXT:site_package/Resources/Private/Templates/Form/Finishers/Email/'
          partialRootPaths:
            20: 'EXT:site_package/Resources/Private/Partials/Form/Finishers/Email/'
          layoutRootPaths:
            20: 'EXT:site_package/Resources/Private/Layouts/Form/Finishers/Email/'
      EmailToSender:
        options:
          templateName: 'Confirmation'
          templateRootPaths:
            20: 'EXT:site_package/Resources/Private/Templates/Form/Finishers/Email/'
          partialRootPaths:
            20: 'EXT:site_package/Resources/Private/Partials/Form/Finishers/Email/'
          layoutRootPaths:
            20: 'EXT:site_package/Resources/Private/Layouts/Form/Finishers/Email/'
```

### 2.2 Form-Specific Definition (`.form.yaml`)

Specify custom templates or paths directly on a form's finisher:

```yaml
finishers:
  -
    identifier: EmailToSender
    options:
      subject: 'Thank you for your inquiry'
      recipients:
        '{email}': '{name}'
      senderAddress: 'noreply@example.com'
      senderName: 'Acme Corp'
      addHtmlPart: true
      templateName: 'CustomerConfirmation'
      templateRootPaths:
        20: 'EXT:site_package/Resources/Private/Templates/Form/Finishers/Email/'
      layoutRootPaths:
        20: 'EXT:site_package/Resources/Private/Layouts/Form/Finishers/Email/'
      variables:
        portalUrl: 'https://customer.example.com'
```

---

## 3. Designing Custom Email Templates

HTML emails must use bulletproof table-based layouts, inline CSS styles, and responsive email design practices. Always pair an HTML template (`.fluid.html`) with a plain-text counterpart (`.fluid.txt`).

### 3.1 Custom HTML Template (`CustomerConfirmation.fluid.html`)

Create `EXT:site_package/Resources/Private/Templates/Form/Finishers/Email/CustomerConfirmation.fluid.html`:

```html
<html xmlns="http://www.w3.org/1999/xhtml"
    xmlns:f="http://typo3.org/ns/TYPO3/CMS/Fluid/ViewHelpers"
    xmlns:formvh="http://typo3.org/ns/TYPO3/CMS/Form/ViewHelpers"
    data-namespace-typo3-fluid="true">
<f:layout name="BrandEmail" />

<f:section name="Title">{title}</f:section>

<f:section name="Main">
    <h2 style="margin: 0 0 16px 0; font-family: Helvetica, Arial, sans-serif; font-size: 22px; color: #1e293b;">
        Hello {form.name},
    </h2>
    <p style="margin: 0 0 16px 0; font-family: Helvetica, Arial, sans-serif; font-size: 15px; line-height: 1.6; color: #334155;">
        Thank you for getting in touch. We have received your message and will respond within one business day.
    </p>

    <!-- Summary Box -->
    <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%" style="margin: 24px 0; background-color: #f8fafc; border: 1px solid #e2e8f0; border-radius: 8px;">
        <tr>
            <td style="padding: 20px;">
                <h3 style="margin: 0 0 12px 0; font-family: Helvetica, Arial, sans-serif; font-size: 16px; color: #0f172a;">
                    Summary of your submission:
                </h3>
                <table role="presentation" border="0" cellpadding="6" cellspacing="0" width="100%" style="font-family: Helvetica, Arial, sans-serif; font-size: 14px; color: #334155;">
                    <tr>
                        <td width="30%" style="font-weight: bold; border-bottom: 1px solid #e2e8f0;">Email:</td>
                        <td style="border-bottom: 1px solid #e2e8f0;">{form.email}</td>
                    </tr>
                    <f:if condition="{form.phone}">
                        <tr>
                            <td style="font-weight: bold; border-bottom: 1px solid #e2e8f0;">Phone:</td>
                            <td style="border-bottom: 1px solid #e2e8f0;">{form.phone}</td>
                        </tr>
                    </f:if>
                    <tr>
                        <td valign="top" style="font-weight: bold;">Message:</td>
                        <td><f:format.nl2br>{form.message}</f:format.nl2br></td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>

    <p style="margin: 0; font-family: Helvetica, Arial, sans-serif; font-size: 14px; color: #64748b;">
        Need urgent help? Visit our <a href="{portalUrl}" style="color: #4f46e5; text-decoration: underline;">Customer Portal</a>.
    </p>
</f:section>
</html>
```

### 3.2 Custom Plain-Text Template (`CustomerConfirmation.fluid.txt`)

Create `EXT:site_package/Resources/Private/Templates/Form/Finishers/Email/CustomerConfirmation.fluid.txt`:

```text
Hello {form.name},

Thank you for getting in touch. We have received your message and will respond within one business day.

SUMMARY OF YOUR SUBMISSION:
--------------------------------------------------
Name:    {form.name}
Email:   {form.email}
<f:if condition="{form.phone}">Phone:   {form.phone}
</f:if>Message:
{form.message}
--------------------------------------------------

Need urgent help? Visit our Customer Portal: {portalUrl}

--
{typo3.sitename}
```

### 3.3 Custom Layout (`BrandEmail.fluid.html`)

Create `EXT:site_package/Resources/Private/Layouts/Form/Finishers/Email/BrandEmail.fluid.html` with your custom email header, logo banner, main container, and footer:

```html
<!DOCTYPE html>
<html xmlns="http://www.w3.org/1999/xhtml"
      xmlns:f="http://typo3.org/ns/TYPO3/CMS/Fluid/ViewHelpers">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title><f:render section="Title" optional="true" /></title>
</head>
<body style="margin: 0; padding: 0; background-color: #f1f5f9; -webkit-text-size-adjust: 100%; -ms-text-size-adjust: 100%;">
    <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%" style="background-color: #f1f5f9;">
        <tr>
            <td align="center" style="padding: 24px 12px;">
                <!-- Main Card (600px max) -->
                <table role="presentation" border="0" cellpadding="0" cellspacing="0" width="100%" style="max-width: 600px; background-color: #ffffff; border-radius: 8px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.1);">
                    <!-- Header -->
                    <tr>
                        <td align="center" style="background-color: #0f172a; padding: 32px 24px;">
                            <!-- Header Logo Image -->
                            <f:render partial="EmailHeaderLogo" />
                        </td>
                    </tr>
                    <!-- Body Content -->
                    <tr>
                        <td style="padding: 32px 24px;">
                            <f:render section="Main" />
                        </td>
                    </tr>
                    <!-- Footer -->
                    <tr>
                        <td style="background-color: #f8fafc; padding: 24px; border-top: 1px solid #e2e8f0; text-align: center; font-family: Helvetica, Arial, sans-serif; font-size: 12px; color: #94a3b8; line-height: 1.5;">
                            <p style="margin: 0 0 8px 0;">This email was sent by {typo3.sitename}.</p>
                            <p style="margin: 0;">&copy; {f:format.date(date: 'now', format: 'Y')} Acme Corp. All rights reserved.</p>
                        </td>
                    </tr>
                </table>
            </td>
        </tr>
    </table>
</body>
</html>
```

---

## 4. Embedding Images and SVG Graphics

Embedding graphics in HTML emails requires strict attention to email client compatibility.

### 4.1 Embedding Standard Images (PNG, JPEG, WebP)

Email clients require **absolute URLs** (including protocol and domain). Relative paths (`/Resources/...`) fail to load.

#### Option A: `f:uri.image` with `absolute="1"` (Recommended)
```html
<img src="{f:uri.image(src: 'EXT:site_package/Resources/Public/Images/email-header.png', absolute: 1, width: 600)}"
     width="600"
     height="180"
     alt="Welcome Header"
     style="display: block; width: 100%; max-width: 600px; height: auto; border: 0; outline: none; -ms-interpolation-mode: bicubic;" />
```

#### Option B: `normalizedParams.siteUrl` with `f:uri.resource`
```html
<img src="{normalizedParams.siteUrl}{f:uri.resource(path: 'EXT:site_package/Resources/Public/Images/logo.png')}"
     width="180"
     height="45"
     alt="Company Logo"
     style="display: block; border: 0; outline: none;" />
```

> **Rules for Email Images:**
> 1. Always specify explicit HTML attributes `width="..."` and `height="..."`. Microsoft Outlook (Windows desktop) ignores CSS dimensions and renders images at their raw physical pixel dimensions.
> 2. Always set `style="display: block; border: 0; outline: none;"` to prevent 2px–3px white space gaps under images in email client tables.
> 3. Provide descriptive `alt` text since many email clients block external images until approved by the user.

---

### 4.2 Handling SVG Graphics in Emails

#### The Compatibility Challenge:
- **Major email clients DO NOT support SVG:**
  - **Microsoft Outlook (Windows desktop 2013–2024):** Uses Microsoft Word as its rendering engine, which has zero SVG support. An `<img src="...svg">` renders as a broken red 'X' box.
  - **Gmail (Web, Android, iOS):** For security reasons, Gmail **strips all raw `<svg>` tags** from the markup and refuses to render SVG files referenced in `<img>` tags.
  - **Yahoo Mail and corporate webmails:** Often block or strip vector graphics.
  - Only Apple Mail and iOS Mail offer native SVG support.

#### Solution 1: Automatic On-The-Fly Rasterization with `<f:image>` (Universal Compatibility)
TYPO3's graphical processing pipeline (GraphicsMagick/ImageMagick) can convert an SVG into a crisp, high-DPI PNG on the fly. Specify `fileExtension="png"`:

```html
<f:image src="EXT:site_package/Resources/Public/Images/logo.svg"
         fileExtension="png"
         width="360c"
         height="90c"
         absolute="1"
         alt="Company Logo"
         style="display: block; width: 180px; height: 45px; border: 0; outline: none;" />
```

**Why this is the industry standard:**
- Renders an SVG from version control without manual exports.
- Output is rendered at double resolution (`width="360"`) and displayed at half size (`width: 180px`), ensuring razor-sharp clarity on Retina and 4K displays.
- Fully compatible with 100% of email clients, including Gmail and desktop Outlook.

#### Solution 2: Outlook Conditional Comments with SVG Fallback
If you wish to serve genuine SVGs to Apple Mail while delivering PNGs to Outlook:

```html
<!--[if mso]>
    <img src="{f:uri.image(src: 'EXT:site_package/Resources/Public/Images/logo.png', absolute: 1)}"
         width="180" height="45" alt="Logo" border="0" style="display: block;" />
<![endif]-->
<!--[if !mso]><!-->
    <img src="{f:uri.image(src: 'EXT:site_package/Resources/Public/Images/logo.svg', absolute: 1)}"
         width="180" height="45" alt="Logo" style="display: block; border: 0;" />
<!--<![endif]-->
```
*(Note: Because Gmail also blocks SVGs and ignores Outlook conditional comments, Solution 1 using `fileExtension="png"` remains the safest universal pattern).*

---

## 5. Attaching Files and Form Uploads

`EmailFinisher` automatically handles attachments uploaded by visitors:

- **User Uploads:** If your form contains `FileUpload` or `ImageUpload` elements, `EmailFinisher` has `attachUploads: true` enabled by default, attaching submitted files directly to the outgoing email.
- **Disabling Upload Attachments:** Set `options.attachUploads: false` on the finisher if you prefer storing uploads on the server and only sending download links.

---

## 6. Verification and Testing Workflow

1. **Send Test Mails:** Submit the form in a staging or development environment connected to a local mail catcher (such as **Mailpit** or **MailHog**).
2. **Inspect Multipart Structure:** Confirm that the email contains both `text/html` and `text/plain` parts.
3. **Verify Asset URLs:** Check that image `src` attributes are absolute `https://...` URLs accessible to external recipients.
4. **Cross-Client Testing:** Test the rendered HTML across Outlook, Gmail (mobile and desktop), and Apple Mail using tools like Litmus, Email on Acid, or test mailboxes.
