# Translate Kiosk Satellite

Translate the English text people see in Kiosk Satellite: button labels, headings, field labels, instructions and error messages. Write your translations in a file for your language under `translations/`.

For example, in this line:

```json
"commonNext": "Next"
```

**Translate `Next`. Keep `commonNext` exactly as it is.** That name lets the app find your translation.

## Start with two buttons

This example adds German translations for **Back** and **Next**. Use your own language when contributing.

1. Fork this repository so you have a copy you can edit. Read the [contributor rulebook](CONTRIBUTOR-RULES.md) and [agreement](CONTRIBUTOR-AGREEMENT.md) before submitting work.
2. Open [source/common_en.arb](../source/common_en.arb). This is your English reference. Leave it unchanged.
3. In your fork, open `translations/de/common_de.arb`. Create that folder and file if they do not exist. If the file already has translations, keep them and add or edit the relevant lines.

The English reference contains these entries among others:

```json
{
  "@@locale": "en",
  "commonBack": "Back",
  "@commonBack": {
    "context": "Common:Actions",
    "description": "Button to return to the previous step."
  },
  "commonNext": "Next",
  "@commonNext": {
    "context": "Common:Actions",
    "description": "Button to advance to the next step."
  }
}
```

For a new German file, the complete contents would be:

```json
{
  "@@locale": "de",
  "commonBack": "Zurück",
  "commonNext": "Weiter"
}
```

That translates two buttons. You do not need to finish the whole file or the whole app before opening a PR.

Notice what changed: `Back` became `Zurück` and `Next` became `Weiter`. The message names stayed the same. The `@commonBack` and `@commonNext` blocks were left out because they are instructions for you, not text shown in the app. `@@locale` identifies the language.

English and Spanish are maintained by Kiosk Satellite's author. **For Spanish, the corresponding file is [translations/es/common_es.arb](../translations/es/common_es.arb) and its language marker is `es`.** It contains translations reviewed by the author. The five English texts in that file are **Import**, **Back**, **Next**, **Finish** and **Working…**.

## What to translate and what to leave alone

| What you see in the English file | What you do |
| --- | --- |
| `"commonNext": "Next"` | Copy the line into your language's file and translate only `Next`. |
| `"settingHaUrlDescription": "e.g. https://homeassistant.local:8123, without a dashboard path."` | Translate this text too. It is help shown below a field. Preserve the URL. |
| A block named `@commonNext` or any other name starting with `@` | Read it for guidance. Do not translate or copy it. |
| `context`, `description`, `x-locations`, `x-notes` or `placeholders` inside an `@` block | These explain where and how the message is used. They are not app text. |
| `@@locale` | Include it once in your translation file with your language code. |

If you are unsure about a message, leave it out and ask in your PR. Do not insert an empty value or copy English just to fill the file. Keep translations that are already present unless you intend to improve them.

## Pick the next screen

Each English file has a matching file in your language. For example:

```text
Read:  source/setup_welcome_en.arb
Edit:  translations/de/setup_welcome_de.arb
```

Only the language changes in the filename. For Spanish, that same file is `translations/es/setup_welcome_es.arb`. For Brazilian Portuguese, use `translations/pt-BR/setup_welcome_pt_BR.arb` with `"@@locale": "pt_BR"`.

Use this table to choose what to work on. The paths use the English labels visible in the app. On the device, open **Settings** first. In remote administration, choose the page from the sidebar. **Device** is under the **System** sidebar heading.

| English reference | Text to translate | Where you see it |
| --- | --- | --- |
| [common_en.arb](../source/common_en.arb) | Import, Back, Next, Finish and Working… | First-time setup buttons. Import is under Welcome > Restore backup. |
| [setup_navigation_en.arb](../source/setup_navigation_en.arb) | Step names such as Welcome and Connect, plus their summaries | The list of steps during first-time setup |
| [setup_welcome_en.arb](../source/setup_welcome_en.arb) | Welcome heading, introduction, device name help, remote password instructions and restore instructions | First-time setup > Welcome |
| [setup_connect_en.arb](../source/setup_connect_en.arb) | Connection instructions, credential labels, QR scanning text and error messages | First-time setup > Connect. QR scanning is on the device. |
| [settings_home_assistant_setup_en.arb](../source/settings_home_assistant_setup_en.arb) | Home Assistant address and access token labels and help | Settings > Home Assistant Setup, above Validate connection. In remote administration, open Home Assistant Setup. |
| [settings_device_en.arb](../source/settings_device_en.arb) | Device name label and help | Settings > Device > Device name. In remote administration, open Device. The label also appears during remote setup. |
| [settings_device_remote_administration_en.arb](../source/settings_device_remote_administration_en.arb) | Remote management switch, Server port and Admin password labels and help | Settings > Device > Remote Administration. In remote administration, open Device > Remote Administration. |

First-time setup is the wizard shown before a kiosk is configured. Its **Connect** step is separate from the **Home Assistant Setup** settings page. The reference files also contain short explanations and, for shared settings, exact device and remote administration paths in `x-locations`.

These files cover the first translation scope. Other screens still use English and will get their own translation files later.

## Keep variables and formatting intact

Some messages contain a value supplied by the app. For example:

```json
"setupUnexpectedResponse": "Unexpected response ({error})"
```

Translate `Unexpected response` and preserve `{error}` exactly. You may move `{error}` to fit your sentence. Do not replace it with the example `HTTP 503`. The app supplies the actual error when it displays the message.

Preserve URLs and product names such as **Kiosk Satellite** and **Home Assistant**. Keep message names unchanged. A `\n` inside text represents a line break. Keep double quotes around names and values, separate entries with commas and omit the comma after the last entry. Write a quotation mark inside a value as `\"`.

Use plain text. HTML and plural or grammatical selection expressions are not supported yet. If a message needs a grammatical variant the file cannot express, ask in an issue before translating it.

## Check and submit

If you have Python 3 installed, run this from the repository's top-level folder:

```sh
python3 tools/catalog.py validate
```

For the German example above, the result includes `de/common_de.arb: 2/5 translated`. That means two of the five messages have translations. It is fine to submit that partial file.

Commit your translation files to your fork and open a PR against this repository. Fill in the PR template with your language, what you translated and your preferred public credit. Copy the `revision` value from [source/manifest.json](../source/manifest.json) into **English source revision**. Include the validation result if you ran it and say whether you checked the text in the app.

After opening the PR, follow the [acceptance guide](PR-ACCEPTANCE.md) to check the agreement box added by the workflow. If you are unsure how to create a file or open a PR, [open an issue](https://github.com/jxlarrea/kiosk-satellite-localization/issues) with your language and the step where you got stuck.

The maintainer reviews translations and includes approved wording in a future app release. Editing a translation file does not immediately change your installed app. If English wording changes later, the affected translations need another review.
