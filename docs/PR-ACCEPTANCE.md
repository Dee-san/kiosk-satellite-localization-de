# Accepting the contributor agreement

The acceptance workflow adds a checkbox to your PR description. It links to a fixed version of the contributor agreement and identifies your exact contribution.

## Accepting your contribution

1. Open your translation PR with one language and one author.
2. Wait for the contributor agreement section to appear in the description.
3. Read the linked agreement and check the acceptance box using your own GitHub account.
4. Wait for the `contributor-acceptance` check to pass.

The checklist elsewhere in the template is for review information. It does not replace the agreement checkbox. You keep copyright and grant the exclusive worldwide usage rights described in the agreement.

## After changes

New commits, a changed PR description or updated agreement text require renewed acceptance. The description includes your AI assistance and rights disclosures. The workflow refreshes the declaration and clears its checkbox. Read the updated declaration and check it again after your last change.

Keep the generated declaration intact. A maintainer checking it for you does not count. If the section is missing or a check is still waiting after you accepted, ask the maintainer to recheck the PR. You may need to check the refreshed box again.

## Contributions with more than one author

Automatic acceptance supports one author per PR. It checks commit authors and rejects declared coauthor trailers. AI tools belong in the assistance disclosure in the PR description, not in coauthor commit trailers. If another person contributed wording or owns relevant rights, disclose that before acceptance. Split work into separate PRs where possible. Otherwise, the maintainer must arrange separate rights review. Do not claim sole authorship of someone else's work.

Your commit author email must be associated with your GitHub account so GitHub can identify the author. You can use your GitHub-provided private email address. A commit GitHub cannot associate with your account requires review.

## Records and review

The workflow retains the accepted agreement, declaration, GitHub account ID and username, acceptance timestamp and contribution snapshot on this repository's `contributor-records` branch. These records are public when the repository is public. Checks show acceptance status and the covered revision. Do not include private information in a translation or acceptance declaration. See the [privacy notice](CONTRIBUTOR-PRIVACY.md) for details.

A passing check confirms recorded acceptance. It does not replace language review or guarantee that a translation will ship in the next release. The maintainer still reviews the PR before merging it.
