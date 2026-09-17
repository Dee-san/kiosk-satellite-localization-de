# Contributor rulebook

These rules apply to community translations of Kiosk Satellite. See the [repository README](../README.md) for ways to help and how to get started.

## Starting a language

Check for an existing language or open PR. For a new language, open a localization issue with its language tag and the scope you can translate. Use a regional variant only when it serves a real wording difference. Coordinate with existing contributors rather than replacing their work without explanation.

Kiosk Satellite's author maintains English and Spanish. Report problems in those languages through an issue. Submit translations for other languages through PRs in this repository.

## Translation rules

1. Translate the intended meaning into natural language. Keep instructions clear and concise without weakening warnings or removing conditions.
2. Use the English source and its context. Report ambiguous source text instead of guessing.
3. Preserve IDs, placeholder names, URLs, configuration values, command examples and entity IDs. You may move a placeholder to fit your grammar.
4. Preserve product names such as Kiosk Satellite, Home Assistant and Voice Satellite. Refer to Voice Satellite as an integration.
5. Follow the language glossary when one is available and use consistent terminology. Use the target language's punctuation and grammar within these translation rules. Use American English when writing English repository documentation.
6. Use the plural forms required by your language. Preserve the required `other` branch and named select values. Do not replace a complete message with sentence fragments.
7. Do not insert HTML, scripts, tracking links, advertising, political commentary or personal information.
8. Leave untranslated entries absent. Do not use empty strings or copy English text just to increase coverage. Preserve an English product name when it is the correct translation.
9. Do not copy translations from another product, repository or translation database. Permission to reuse text does not prove that you can grant exclusive rights to it.
10. Machine translation may assist a fluent human, but that person must check every submitted message. Disclose assistance and verify that the tool's terms permit the intended use. Do not submit raw generated batches or use a tool when its output rights are unclear.
11. Do not use em dashes or en dashes in translated prose or repository documentation. Rephrase the sentence or use other punctuation without changing its meaning. Preserve technical values as required by rule 3.

## Opening a PR

Use one language per PR and keep the change focused. Edit the translation files only. Source changes, tooling and policy changes need a separate maintainer-led change.

Include the language tag, source revision, changed areas, your fluency, validation results and your preferred public credit. State which screens you tested. If you could not test in the app, say so. Small corrections and partial translations are welcome. A new language stays in draft until all messages in its initial supported scope are translated and reviewed and the language has been tested in the app.

Follow the validation instructions published with the translation files and resolve any failures reported by PR checks. Do not change workflow files to make your PR pass.

## Review and acceptance

A fluent reviewer checks the translation. Kiosk Satellite's author makes the final acceptance decision. Be respectful when discussing wording and explain regional choices. Do not treat machine translation output as proof that another contributor is wrong.

Push requested changes to the same PR. New changes require renewed review and agreement acceptance for the updated revision. After the last update, read the declaration and check the acceptance box yourself using your own GitHub account. Acceptance must be recorded for the current agreement version and PR revision before merging. A box left checked from an earlier revision does not cover a new one. A maintainer cannot accept for you.

Use one actual author per PR for the simple checkbox process. If another person writes replacement text, identify that contribution so the maintainer can obtain their separate recorded acceptance too. Do not accept for someone else's work without authority.

See the [PR acceptance guide](PR-ACCEPTANCE.md) for the checkbox steps and help with a waiting check.

A merged PR is not an immediate app update. Translations ship when Kiosk Satellite's author includes a reviewed snapshot in an app release. The author may edit, replace or remove accepted text under the contributor agreement. Historical credit remains unless you ask to remove your public attribution.

## Keeping translations current

English changes can mark translations as needing review. Update those messages against the new context. Older wording may remain visible in the repository as a suggestion while the app uses English fallback.

There is no ongoing support obligation after contributing. Other contributors may maintain the language later. Report translation bugs here with the KS version, language, screen, current wording and proposed correction. Remove tokens, addresses and other private details from screenshots.

## Ownership and credit

Kiosk Satellite remains Xavier Larrea's project. You retain copyright in your original translations and grant him exclusive worldwide rights to use, modify, distribute and sublicense them under the [contributor agreement](CONTRIBUTOR-AGREEMENT.md). To have a translation accepted, read the agreement at the version linked in your PR and check the acceptance box yourself. Copyright ownership does not transfer.

You will receive credit under your chosen public name when your contribution is accepted. Credit does not give you ownership of Kiosk Satellite, a share of revenue, a veto over edits or control over releases. Contributions are voluntary and unpaid, subject to any mandatory legal entitlement. The contributor agreement defines the legal terms and preserves your nonwaivable rights. This rulebook does not replace that agreement or the [repository license](../LICENSE).

Do not submit work unless you can grant the required exclusive rights. If your employer, a client or another author owns rights in the text, tell the maintainer before submitting it. Each rights holder must be covered. Do not put legal names, signatures or private contact information in a public PR. The [contributor privacy notice](CONTRIBUTOR-PRIVACY.md) explains how acceptance records and public credit are handled.
