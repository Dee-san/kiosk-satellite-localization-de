# Changelog

Notable changes to Kiosk Satellite Localization are listed below, newest first. This repository does not publish releases. Kiosk Satellite imports reviewed translations from a pinned commit and includes them in app releases.

## History

- Retain merged contribution records using an explicit trusted default-branch checkout and the GitHub API version that includes the merge commit SHA.

- Report contributor acceptance as a required commit status and keep the detailed evidence check separate so accepted PRs do not remain pending in branch protection.

- Add English and Spanish text for Voice Satellite chime selection, previews and local sound storage.

- Require complete current catalogs for new-language PRs while allowing focused corrections to existing languages. Catalog validation uses trusted target-branch tooling and reports missing messages and source changes that need review.
- Add community previews, retained acceptance and merge evidence verification, maintainer review records, native language names and public credit generation. Imports preserve previously enabled languages and require complete reviewed catalogs before a new language is enabled.
- Clarify AI-assisted translation in contributor agreement and repository license version 1.1. Permit disclosed service processing, require optional training and sharing controls to be disabled and keep broader provider permissions subject to explicit approval. Retain the accepted PR disclosures and require fresh acceptance when they change.

- Support complete-language PRs beyond 100 files in contributor acceptance. Read every page of the PR file list, verify that it is complete and retain the existing evidence size limits.

- Add English and Spanish text for the screen-off timer option that shows a plain black screen at zero brightness (#614).

- Add English and Spanish text for floating Voice Satellite timers, pause and resume gestures, cancellation, saved positioning and local timer alerts (#612).

- Add English and Spanish text for camera date and time overlays and their optional black background (#609).

- Add English and Spanish text for inviting fleet members by IP address and remote admin port, including lookup validation and the invitation flow.

- Add font compatibility guidance and PR rendering status fields. New languages need a rendering review before shipping. Contributors can suggest fonts for maintainer integration under their own licenses. Untested translations and small corrections remain welcome.

- Update English and Spanish fleet and intercom guidance to include saved members. Add the saved-address mismatch error and use discovery-neutral empty-list labels.

- Add English and Spanish text for the Voice Satellite setting that returns to the previous app after a background voice interaction.

- Approve 107 Spanish messages for app-list failures and plugin repository, validation, package and update errors. Approve remote Overview as another location for nine existing Camera and Camera Streams messages. All 3148 messages have reviewed Spanish translations.

- Approve seven Spanish translations for screen-off and restart errors in remote Overview and the Settings location of three existing backup-validation messages. All 3041 messages now have reviewed Spanish translations.

- Approve 37 Spanish messages for At a Glance states, APK update failures and Shizuku errors. Approve the shared battery-permission explanation in App Launcher. All 3034 messages have reviewed Spanish translations.

- Approve Welcome as another location for the existing Language title and description. Spanish wording is unchanged and all 2997 messages remain reviewed.

- Add 73 author-approved Spanish messages for File Manager, kiosk notices, screensaver playback errors, Settings search and remote warnings. All 2997 catalog messages have approved Spanish translations.

- Add three author-approved Spanish messages for the Settings footer, coffee support link and plugin-window Close tooltip. All 2924 catalog messages have approved Spanish translations.

- Add 16 author-approved Spanish messages for Android service notifications, the Accessibility description and QR scanning. Generate Android resources through the shared catalog pipeline. All 2921 catalog messages have approved Spanish translations.

- Add 17 author-approved Spanish messages for remote login, connection recovery, update reload notices and native network errors. All 2905 catalog messages have approved Spanish translations.

- Add 34 author-approved Spanish messages for setup permissions, backup restore and initial password errors. All 2888 catalog messages have approved Spanish translations.

- Add 17 author-approved Spanish messages for setup dashboard selection and Voice Satellite recommendations. All 2854 catalog messages have approved Spanish translations.

- Add 105 author-approved Spanish messages for remote Overview status, attention notices, screenshots, quick controls and dashboard selection. All 2837 catalog messages have approved Spanish translations.

- Add 64 author-approved Spanish messages for the rest of Voice Satellite, including Wake Word tuning, cached models, the tester, Appearance and search. All 2732 catalog messages have approved Spanish translations.

- Add 49 author-approved Spanish messages for Voice Satellite setup, main controls, background listening and permissions. All 2668 catalog messages have approved Spanish translations.

- Add 114 author-approved Spanish messages for the remaining ESPHome settings, Bluetooth devices, Notifications, Announcements, GPS Sensor and permissions. All 2619 catalog messages have approved Spanish translations.

- Add 50 author-approved Spanish messages for ESPHome setup, excluded entities and Advanced settings. All 2505 catalog messages have approved Spanish translations.

- Add 17 author-approved Spanish messages for Lockdown settings, permissions and both device shields. All 2455 catalog messages have approved Spanish translations.

- Add 43 author-approved Spanish messages for Logs, the web console, About and update controls. All 2438 catalog messages have approved Spanish translations.

- Add 222 author-approved Spanish messages for Fleet Management and Plugin Manager, including profiles, invitations, plugin installation, actions and outputs. All 2395 catalog messages have approved Spanish translations.

- Apply the same larger aggregate Spanish review limit to snapshots and local records while preserving the existing individual catalog file limit.

- Add 184 author-approved Spanish messages for App Launcher settings, app selection, Gestures, action editors and the hand tester. All 2173 catalog messages have approved Spanish translations.

- Add 83 author-approved Spanish messages for Kiosk Mode, permissions, PIN prompts and Home Launcher status. Use "Lanzador de Inicio" for Home Launcher. All 1989 catalog messages have approved Spanish translations.

- Add 141 author-approved Spanish messages for Intercom settings, call controls, announcements and shared sound pickers. All 1906 catalog messages have approved Spanish translations.

- Add 15 author-approved Spanish messages for DLNA settings, playback notices and shared port validation. All 1765 catalog messages have approved Spanish translations.

- Add 99 author-approved Spanish messages for remaining Media Player settings, playback controls, queues, chapters and speaker grouping. All 1750 catalog messages have approved Spanish translations.

- Add 24 author-approved Spanish messages for Sonos playback options and speaker management. All 1651 catalog messages have approved Spanish translations.

- Add 76 author-approved Spanish messages for Media Player setup and two remote browser permission notices. Use "Reproduciendo Ahora" consistently across the catalog. All 1627 catalog messages have approved Spanish translations.

- Add 25 author-approved Spanish messages for Web Browsing, split into navigation, cache and security and JavaScript editors. All 1549 catalog messages have approved Spanish translations.

- Add 15 author-approved Spanish messages for live camera views, including connection status, playback failures and retry notices. All 1524 catalog messages have approved Spanish translations.

- Add 112 author-approved Spanish messages for Camera Streams, split into imports, servers, camera editors, views, playback and errors. All 1509 catalog messages have approved Spanish translations.

- Add 127 author-approved Spanish messages for Camera settings, split into general controls, motion sensing, streaming controls, status, permissions and remote snapshots. All 1397 catalog messages have approved Spanish translations.

- Add 75 author-approved Spanish messages for Motion, Face, Proximity and Person Detection, camera previews and person sensor permissions. All 1270 catalog messages have approved Spanish translations. Keep sensor names and ADB commands unchanged and distinguish occupancy status from the Clear action.

- Add 106 author-approved Spanish messages for Screensaver Widgets and At a Glance, split into six templates for global settings, widget editing, weather, entity selection and row appearance. All 1195 catalog messages have approved Spanish translations.

- Add 205 author-approved Spanish messages for Screensaver media settings, including Home Assistant Media, Local Media, Photo Gallery, Immich and Camera Streams. Split Immich templates by visible settings groups and use "Immich" for its mode label and page name. All 1089 catalog messages have approved Spanish translations.

- Add 174 author-approved Spanish messages for Screensaver controls, Clock settings, schedules and shared time and color pickers. Keep mode names and font weights distinct and document each template by its visible UI path.

- Add 93 author-approved Spanish translations for Screen & Audio across five sections. Include hardware-dependent notices, microphone channels and disconnected audio devices.

- Add 128 messages with author-approved Spanish translations for Home Assistant Setup, split by its visible subpages. Include connection results, dashboard selection, rotation, theme choices and update-filter status. Keep shared actions in the common file. Use "panel de control" consistently for dashboard across Spanish translations.
- Add sectioned Device settings templates and 309 author-approved Spanish messages, covering both interfaces. Expand the common actions file and document each new section in the translator guide. Pin the English source manifest to the committed Device implementation.
- Add Settings menu and search templates plus device drawer actions and update dialogs, with author-approved Spanish translations using "protector de pantalla" for screensaver. Preserve plugin-supplied names and provide a local preview command that does not mark translations as approved.
- Add the Device > User Interface language selector messages with author-approved Spanish wording.
- Add author-approved Spanish translations for all 69 messages and record their review for a future app import.
- Name translation sections after visible UI pages and document exact device and remote administration paths. Remove the hidden Start URL setting from the catalog.
- Split the first English catalog into common actions, setup pages and settings sections with matching Spanish translation files.
- Separate screen context, short descriptions and translator notes. Keep application setting mappings outside the ARB files.
- Add catalog validation, source digests and owner review tooling for pinned Spanish imports into Kiosk Satellite.
- Document the initial translation scope and add a catalog validation check for PRs.
- Add README banners for light and dark themes.
- Store acceptance records on the localization repository's contributor-records branch using the built-in workflow token.
- Add the PR template and contributor acceptance workflow with retained evidence and renewed acceptance after changes.
- Check contributor identity, agreement revisions and merged translation content before reporting acceptance.
- Add acceptance workflow tests and a contributor guide.
- Add a welcoming README with ways to help and contribution steps.
- Replace the repository license with terms limited to Kiosk Satellite localization and its contribution process.
- Add a contributor rulebook covering translation standards, review and PR acceptance.
- Add a contributor agreement granting exclusive worldwide usage rights while contributors retain copyright ownership.
- Document PR checkbox acceptance, contributor credits and privacy practices.
