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

English and Spanish are maintained by Kiosk Satellite's author. **For Spanish, the corresponding file is [translations/es/common_es.arb](../translations/es/common_es.arb) and its language marker is `es`.** Existing translations include wording reviewed by the author. New wording may be awaiting review. The common file includes **Import**, **Back**, **Next**, **Finish**, **Working…**, **Settings**, **Cancel**, **OK**, **Grant**, **Enable**, **Refresh**, **Test**, **Install**, **Save**, **Retry**, **Copy**, **Add**, **Remove** and **Close**. It also includes time picker controls and color presets.

For Spanish, use **panel de control** for dashboard (**paneles de control** in the plural), **kiosko** for kiosk, **protector de pantalla** for screensaver, **Reproduciendo Ahora** for Now Playing and **Lanzador de Inicio** for Home Launcher.

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
| [common_en.arb](../source/common_en.arb) | Shared actions, time picker labels and color presets | Shared buttons and dialogs in setup, Settings and the drawer. Import is under Welcome > Restore backup. |
| [settings_menu_en.arb](../source/settings_menu_en.arb) | Settings menu page names, summaries and group headings | Settings > menu on the device and the remote administration sidebar. Includes remote-only entries such as Overview and File Manager. |
| [settings_search_en.arb](../source/settings_search_en.arb) | Search box hint, clear button, result heading and no-match message | Settings > search box on the device and the remote administration sidebar |
| [drawer_menu_en.arb](../source/drawer_menu_en.arb) | Drawer actions, conditional player and hold labels, confirmations and theme tooltips | Swipe from the left edge of the device screen to open the drawer. Some entries appear only when their feature is configured. Each message explains its condition. |
| [drawer_updates_en.arb](../source/drawer_updates_en.arb) | Version notice, update checks, installation prompts and download progress | Device drawer > version or update notice below the actions |
| [file_manager_en.arb](../source/file_manager_en.arb) | Folders, upload progress, file actions and errors | Remote admin > File Manager. Root names translate, but filenames and paths stay unchanged. `{error}` contains technical details from the device. |
| [kiosk_notices_en.arb](../source/kiosk_notices_en.arb) | Back-button hints, hold-mode notices, downloads and missing WebView guidance | Physical kiosk > notices over the dashboard. The WebView message replaces the dashboard when Android cannot display web pages. |
| [screensaver_playback_notices_en.arb](../source/screensaver_playback_notices_en.arb) | Empty media selections, unreadable folders and Immich playback errors | Physical kiosk > active screensaver using local media or Immich. `{folder}` is a raw path. `{error}` is the reason for an automatic retry. |
| [remote_action_notices_en.arb](../source/remote_action_notices_en.arb) | Remote-management shutdown warning, clipboard guidance and save failures | Remote admin > Device > Remote management, copy controls and setting rows that cannot save. |
| [settings_search_extras_en.arb](../source/settings_search_extras_en.arb) | Search summaries for controls that do not come from a setting definition | Settings search on the device and in remote admin. Each message names its destination in `context`. |
| [android_service_en.arb](../source/android_service_en.arb) | Service notification status and channel description | Android notification shade > Kiosk Satellite Service, plus Android Settings > Notifications. Status phrases are lowercase fragments joined with commas. Keep product names unchanged. The notification follows KS's selected language. |
| [android_accessibility_en.arb](../source/android_accessibility_en.arb) | Accessibility service description | Android Settings > Accessibility > Kiosk Satellite. Android displays this description in its own selected language. |
| [setup_qr_scanner_en.arb](../source/setup_qr_scanner_en.arb) | QR scanner instructions, camera error and flashlight labels | Physical device > first-time setup > Connect > Scan token QR code. Cancel reuses the common action. The scanned token itself must stay unchanged. |
| [remote_login_en.arb](../source/remote_login_en.arb) | Sign-in action and password errors | Remote admin > Log in, before opening the app. The heading and password field reuse Setup and Device messages. This is the kiosk admin password. |
| [remote_connection_en.arb](../source/remote_connection_en.arb) | Reconnecting, browser reload actions and the update countdown | Remote admin > full-page connection and update notices. Keep device names, versions and build numbers unchanged. Reload page reloads the admin browser, not the kiosk dashboard. |
| [offline_notice_en.arb](../source/offline_notice_en.arb) | Dashboard load errors and network lost/restored notifications | On the physical kiosk, over or instead of the dashboard during a connection failure. Retry uses the shared common action. Technical error details remain unchanged. |
| [setup_navigation_en.arb](../source/setup_navigation_en.arb) | Step names such as Welcome and Connect, plus their summaries | The list of steps during first-time setup |
| [setup_welcome_en.arb](../source/setup_welcome_en.arb) | Welcome heading, introduction, device name help, remote password instructions and restore instructions | First-time setup > Welcome |
| [setup_connect_en.arb](../source/setup_connect_en.arb) | Connection instructions, credential labels, QR scanning text and error messages | First-time setup > Connect. QR scanning is on the device. |
| [setup_service_en.arb](../source/setup_service_en.arb) | Service explanation and missing-permission help | First-time setup > Welcome > Recommended Service Permissions, on the device and in remote admin. Shared permission names, status words and ADB guidance reuse Device templates. Keep the ADB commands unchanged. |
| [setup_permissions_en.arb](../source/setup_permissions_en.arb) | Final permission explanations and remote request progress | First-time setup > Permissions, after dashboard and optional Voice Satellite selection. Some explanations depend on the selected recommendations. Remote admin asks you to approve Android prompts on the physical device. Each message lists its applicable interface. |
| [setup_restore_en.arb](../source/setup_restore_en.arb) | Backup validation, restore progress and completion guidance | First-time setup > Welcome > Restore backup. Remote admin also shows a full-page waiting message while permissions are answered on the device. Keep JSON unchanged. Import choices reuse Device configuration templates. |
| [setup_remote_access_en.arb](../source/setup_remote_access_en.arb) | Initial password errors and instructions before restoring a backup | Remote admin > first-time setup > Welcome > Remote administration. These messages concern the kiosk admin password, not the Home Assistant token. |
| [setup_dashboard_en.arb](../source/setup_dashboard_en.arb) | Dashboard heading, instructions and missing-selection error | First-time setup > Dashboard, on the device and in remote admin. This follows Connect. Actual dashboard names, view names and paths come from Home Assistant and stay unchanged. The view picker reuses Home Assistant settings messages. |
| [setup_voice_satellite_en.arb](../source/setup_voice_satellite_en.arb) | Satellite assignment guidance, empty state and recommended settings | First-time setup > Voice Satellite, on the device and in remote admin. This step appears only when the integration is detected. Translate instructions and built-in option labels. Keep satellite names, entity IDs and Voice Satellite unchanged. Most recommended switches reuse their Settings messages. |
| [settings_home_assistant_setup_en.arb](../source/settings_home_assistant_setup_en.arb) | Connection fields, automatic login, validation, secure proxy and dashboard selection | Settings > Home Assistant Setup. In remote administration, open Home Assistant Setup. |
| [settings_home_assistant_user_interface_en.arb](../source/settings_home_assistant_user_interface_en.arb) | Kiosk mode, carousel gestures, vibration and tap sounds | Settings > Home Assistant Setup > User Interface. In remote administration, open Home Assistant Setup > User Interface. |
| [settings_home_assistant_theme_en.arb](../source/settings_home_assistant_theme_en.arb) | Theme choices, synchronization and schedule | Settings > Home Assistant Setup > Theme. In remote administration, open Home Assistant Setup > Theme. |
| [settings_home_assistant_rotation_en.arb](../source/settings_home_assistant_rotation_en.arb) | Rotation timing, view selection, external pages and fade transitions | Settings > Home Assistant Setup > Dashboard View Rotation. In remote administration, open Home Assistant Setup > Dashboard View Rotation. |
| [settings_home_assistant_return_home_en.arb](../source/settings_home_assistant_return_home_en.arb) | Inactivity timeout, destination and disabled explanation | Settings > Home Assistant Setup > Return to home dashboard view. In remote administration, open Home Assistant Setup > Return to home dashboard view. |
| [settings_home_assistant_hold_en.arb](../source/settings_home_assistant_hold_en.arb) | Hold mode, automatic release duration and menu entry | Settings > Home Assistant Setup > Hold mode. In remote administration, open Home Assistant Setup > Hold mode. |
| [settings_home_assistant_optimizations_en.arb](../source/settings_home_assistant_optimizations_en.arb) | Background connection, pausing the dashboard and cameras, update filtering and diagnostic dialogs | Settings > Home Assistant Setup > Optimizations. In remote administration, open Home Assistant Setup > Optimizations. |
| [settings_device_en.arb](../source/settings_device_en.arb) | Device name, mDNS name, renderer options and Device page links | Settings > Device > Device name. In remote administration, open Device. The label also appears during remote setup. |
| [settings_device_user_interface_en.arb](../source/settings_device_user_interface_en.arb) | Language, theme and scale labels, help and theme choices | Settings > Device > User Interface. The language selector also appears first in onboarding > Welcome. Language is the first row. In remote administration, open Device > User Interface. |
| [settings_device_remote_administration_en.arb](../source/settings_device_remote_administration_en.arb) | Remote management, server port, password, fleet discovery and server status | Settings > Device > Remote Administration. In remote administration, open Device > Remote Administration. |
| [settings_device_configuration_en.arb](../source/settings_device_configuration_en.arb) | Backup export, import choices, results and errors | Settings > Device > Configuration. Also Device > Configuration in remote administration. |
| [settings_device_permissions_en.arb](../source/settings_device_permissions_en.arb) | Permission names, explanations, status and actions | Settings > Device > Permissions Manager. Also Device > Permissions Manager in remote administration. |
| [settings_device_service_en.arb](../source/settings_device_service_en.arb) | Service status, reasons it stays active and required permissions | Settings > Device > Kiosk Satellite Service. Also Device > Kiosk Satellite Service in remote administration. |
| [settings_device_updates_en.arb](../source/settings_device_updates_en.arb) | Update source choices, APK uploads, installation progress and failure explanations | Settings > Device > Updates. Also Device > Updates in remote administration. |
| [settings_device_shizuku_en.arb](../source/settings_device_shizuku_en.arb) | Connection status, permission actions, failure explanations and setup guidance | Settings > Device > Shizuku. Also Device > Shizuku in remote administration. |
| [settings_device_update_helper_en.arb](../source/settings_device_update_helper_en.arb) | Helper status and ADB setup instructions | Settings > Device > Optional update helper. Also Device > Optional update helper in remote administration. |
| [settings_device_analytics_en.arb](../source/settings_device_analytics_en.arb) | Analytics choices and explanation | Settings > Device > Kiosk Satellite Analytics. Also Device > Kiosk Satellite Analytics in remote administration. |
| [settings_device_information_en.arb](../source/settings_device_information_en.arb) | Hardware, Home Assistant and WebView status labels | Remote administration only: Device > Hardware, Device > Home Assistant and Device > WebView. |
| [settings_screen_audio_screen_en.arb](../source/settings_screen_audio_screen_en.arb) | Orientation, camera cutout area, brightness and permission notices | Settings > Screen & Audio > Screen. Also Screen & Audio > Screen in remote administration. |
| [settings_screen_audio_adaptive_brightness_en.arb](../source/settings_screen_audio_adaptive_brightness_en.arb) | Brightness limits, room light thresholds and live sensor readings | Settings > Screen & Audio > Adaptive brightness. Also Screen & Audio > Adaptive brightness in remote administration. |
| [settings_screen_audio_volume_en.arb](../source/settings_screen_audio_volume_en.arb) | Master, media, intercom and assistant volume | Settings > Screen & Audio > Audio Volume. Also Screen & Audio > Audio Volume in remote administration. |
| [settings_screen_audio_devices_en.arb](../source/settings_screen_audio_devices_en.arb) | Microphone and speaker choices, including disconnected devices | Settings > Screen & Audio > Audio Devices. Also Screen & Audio > Audio Devices in remote administration. |
| [settings_screen_audio_microphone_en.arb](../source/settings_screen_audio_microphone_en.arb) | Capture mode, channel, processing, gain and the live level meter | Settings > Screen & Audio > Microphone settings. Also Screen & Audio > Microphone settings in remote administration. |
| [settings_screensaver_general_en.arb](../source/settings_screensaver_general_en.arb) | Main controls, mode choices, brightness and screen-off warnings | Settings > Screensaver. Also Screensaver in remote administration. |
| [settings_screensaver_black_en.arb](../source/settings_screensaver_black_en.arb) | Fully black display and extra overlays | Settings > Screensaver > Black screensaver. Also Screensaver > Black screensaver in remote administration. |
| [settings_screensaver_website_en.arb](../source/settings_screensaver_website_en.arb) | Website URL, zoom and touch behavior | Settings > Screensaver > Website screensaver. Also Screensaver > Website screensaver in remote administration. |
| [settings_screensaver_clock_en.arb](../source/settings_screensaver_clock_en.arb) | Clock style, font, colors, night mode and background photo | Settings > Screensaver > Clock screensaver. Also Screensaver > Clock screensaver in remote administration. |
| [settings_screensaver_schedule_en.arb](../source/settings_screensaver_schedule_en.arb) | Scheduled times, mode changes, overrides and summaries | Settings > Screensaver > Scheduled Screensavers. Also Screensaver > Scheduled Screensavers in remote administration. |
| [settings_screensaver_media_home_assistant_en.arb](../source/settings_screensaver_media_home_assistant_en.arb) | Media browser, slideshow timing and display choices | Settings > Screensaver > Home Assistant Media screensaver. Also Screensaver > Home Assistant Media screensaver in remote administration. |
| [settings_screensaver_media_local_en.arb](../source/settings_screensaver_media_local_en.arb) | Local folder, slideshow timing and display choices | Settings > Screensaver > Local Media screensaver. Also Screensaver > Local Media screensaver in remote administration. |
| [settings_screensaver_media_gallery_en.arb](../source/settings_screensaver_media_gallery_en.arb) | Photo selection, copying progress and slideshow choices | Settings > Screensaver > Photo Gallery screensaver. Also Screensaver > Photo Gallery screensaver in remote administration. |
| [settings_screensaver_media_camera_en.arb](../source/settings_screensaver_media_camera_en.arb) | Camera view selection, ordering, timing and sound | Settings > Screensaver > Camera Streams screensaver. Also Screensaver > Camera Streams screensaver in remote administration. |
| [settings_screensaver_media_common_en.arb](../source/settings_screensaver_media_common_en.arb) | Shared transition and fill choices for Home Assistant Media, Local Media, Photo Gallery and Immich slideshows | Settings > Screensaver. Also Screensaver in remote administration. |
| [settings_screensaver_immich_connection_en.arb](../source/settings_screensaver_immich_connection_en.arb) | Server address, API key and validation results | Settings > Screensaver > Immich Media screensaver > Server Connection. Also Screensaver > Immich Media screensaver > Server Connection in remote administration. |
| [settings_screensaver_immich_source_en.arb](../source/settings_screensaver_immich_source_en.arb) | Albums, local caching and media selection | Settings > Screensaver > Immich Media screensaver > Media. Also Screensaver > Immich Media screensaver > Media in remote administration. |
| [settings_screensaver_immich_slideshow_en.arb](../source/settings_screensaver_immich_slideshow_en.arb) | Timing, transitions and portrait pairing | Settings > Screensaver > Immich Media screensaver > Slideshow. Also Screensaver > Immich Media screensaver > Slideshow in remote administration. |
| [settings_screensaver_immich_metadata_en.arb](../source/settings_screensaver_immich_metadata_en.arb) | Photo details, placement, text styling and shading | Settings > Screensaver > Immich Media screensaver > Metadata. Also Screensaver > Immich Media screensaver > Metadata in remote administration. |
| [settings_screensaver_immich_filters_en.arb](../source/settings_screensaver_immich_filters_en.arb) | People, tags, favorites and date filters | Settings > Screensaver > Immich Media screensaver > Filters. Also Screensaver > Immich Media screensaver > Filters in remote administration. |
| [settings_screensaver_widgets_en.arb](../source/settings_screensaver_widgets_en.arb) | Widget list and global size, font, shadow and shading | Settings > Screensaver > Widgets. Also Screensaver > Widgets in remote administration. |
| [settings_screensaver_motion_detection_en.arb](../source/settings_screensaver_motion_detection_en.arb) | Motion wake and postpone controls with camera guidance | Settings > Screensaver > Motion Detection. Also Screensaver > Motion Detection in remote administration. |
| [settings_screensaver_face_detection_en.arb](../source/settings_screensaver_face_detection_en.arb) | Face wake controls, sensitivity and device availability | Settings > Screensaver > Face Detection. Also Screensaver > Face Detection in remote administration. |
| [settings_screensaver_face_preview_en.arb](../source/settings_screensaver_face_preview_en.arb) | Camera preview duration, size and corner | Settings > Screensaver > Face Detection > Camera Preview. Also Screensaver > Face Detection > Camera Preview in remote administration. |
| [settings_screensaver_proximity_detection_en.arb](../source/settings_screensaver_proximity_detection_en.arb) | Proximity wake controls and sensor availability | Settings > Screensaver > Proximity Detection. Also Screensaver > Proximity Detection in remote administration. |
| [settings_screensaver_person_detection_en.arb](../source/settings_screensaver_person_detection_en.arb) | Person wake controls and live occupancy status | Settings > Screensaver > Person Detection. Also Screensaver > Person Detection in remote administration. |
| [settings_screensaver_person_permissions_en.arb](../source/settings_screensaver_person_permissions_en.arb) | Log access status, ADB guidance and restart actions | Settings > Screensaver > Person Detection > Required system permissions. Also Screensaver > Person Detection > Required system permissions in remote administration. |
| [settings_kiosk_general_en.arb](../source/settings_kiosk_general_en.arb) | Kiosk protection, exit gestures, PIN setup and hardware buttons | Settings > Kiosk Mode. Also Kiosk Mode in remote administration. Tap counts and stored gesture values stay unchanged. |
| [settings_lockdown_general_en.arb](../source/settings_lockdown_general_en.arb) | Lockdown controls, exit gesture help and mode explanation | Remote admin > Lockdown Mode. These controls are configured remotely. Device Settings > Search explains where to find them. Exit tap counts reuse the Kiosk Mode options. |
| [settings_esphome_bluetooth_en.arb](../source/settings_esphome_bluetooth_en.arb) | Scan intensity, connections, signal limits and sorting | Settings > ESPHome > Bluetooth Proxy and the same page in remote admin. |
| [settings_esphome_bluetooth_status_en.arb](../source/settings_esphome_bluetooth_status_en.arb) | Nearby-device status, age, counts and connection limits | Settings > ESPHome > Bluetooth Proxy > Nearby devices and the same page in remote admin. |
| [settings_esphome_bluetooth_identity_en.arb](../source/settings_esphome_bluetooth_identity_en.arb) | Inferred device classes. Broadcast names, brands and addresses stay unchanged. | Settings > ESPHome > Bluetooth Proxy > Nearby devices and the same page in remote admin. |
| [settings_esphome_notifications_en.arb](../source/settings_esphome_notifications_en.arb) | Appearance, sound defaults and test notification | Settings > ESPHome > Notifications and the same page in remote admin. |
| [settings_esphome_announcements_en.arb](../source/settings_esphome_announcements_en.arb) | Announcement settings and the text-to-speech engine picker. Engine names and entity IDs stay unchanged. | Settings > ESPHome > Announcements and the same page in remote admin. |
| [settings_esphome_gps_en.arb](../source/settings_esphome_gps_en.arb) | Location settings, coordinates and receiver status. Coordinates stay unchanged. | Settings > ESPHome > GPS Sensor and the same page in remote admin. |
| [settings_esphome_permissions_en.arb](../source/settings_esphome_permissions_en.arb) | Bluetooth and GPS permissions and their status messages | Settings > ESPHome > Bluetooth Proxy and GPS Sensor > Required system permissions and the same page in remote admin. |
| [settings_esphome_setup_en.arb](../source/settings_esphome_setup_en.arb) | Server setup, entity exposure, node name, encryption key and API port | Settings > ESPHome and remote admin > ESPHome, on the main page. Keep ESPHome, Home Assistant, identifiers, keys and port numbers unchanged. |
| [settings_voice_satellite_setup_en.arb](../source/settings_voice_satellite_setup_en.arb) | Connection guidance, installation help and loading messages | Settings > Voice Satellite and remote admin > Voice Satellite, before the integration is ready. Keep Voice Satellite, Home Assistant and HACS unchanged. |
| [settings_voice_satellite_general_en.arb](../source/settings_voice_satellite_general_en.arb) | Engine controls, satellite selection, Assist pipelines, background listening and general options | Settings > Voice Satellite > General and the same group in remote admin. Translate labels and help. Satellite names, pipeline names, entity IDs and version numbers come from Home Assistant and stay unchanged. Wake Word tuning, its tester and Appearance use the separate templates listed below. |
| [settings_voice_satellite_permissions_en.arb](../source/settings_voice_satellite_permissions_en.arb) | Permission status and guidance for voice detection and background listening | Settings > Voice Satellite > Required system permissions and the same group in remote admin. Shared permission names and actions are in the Device templates. |
| [settings_voice_satellite_wake_word_en.arb](../source/settings_voice_satellite_wake_word_en.arb) | Engine and sensitivity choices, noise gate, stop word, cached models and local recovery settings | Settings > Voice Satellite > Wake Word and remote admin > Voice Satellite > Wake Word. Translate built-in labels. Keep spoken wake words, model names, engine names and setWakeWordActive(true) unchanged. |
| [settings_voice_satellite_appearance_en.arb](../source/settings_voice_satellite_appearance_en.arb) | Overlay style, theme, activity bar and text size | Settings > Voice Satellite > Appearance and the same page in remote admin. Skin names come from the integration and stay unchanged. |
| [settings_voice_satellite_tester_en.arb](../source/settings_voice_satellite_tester_en.arb) | Chart labels, detection counts, log labels, stop-word suffix and copy confirmation | On the device only: Settings > Voice Satellite > Wake Word Tester > Open tester. Translate interface labels. Keep decoded phonemes, spoken words, timestamps and measurements unchanged. |
| [esphome_entity_picker_en.arb](../source/esphome_entity_picker_en.arb) | Excluded-entity selection, search, summaries and type labels | Settings > ESPHome > Excluded entities and the same picker in remote admin. Entity names and IDs match Home Assistant and are not translated. |
| [settings_esphome_advanced_en.arb](../source/settings_esphome_advanced_en.arb) | Hardware identity, manual MAC address and status | Settings > ESPHome > Advanced settings and remote admin > ESPHome > Advanced settings. Keep addresses unchanged. The other ESPHome subpages have separate templates listed above. |
| [settings_lockdown_permissions_en.arb](../source/settings_lockdown_permissions_en.arb) | Screen-wide shield permission and search guidance | Remote admin > Lockdown Mode > Required system permissions. Shared permission labels and actions reuse the Kiosk Mode templates. |
| [lockdown_shield_en.arb](../source/lockdown_shield_en.arb) | The brief locked-screen notice | Device > Lockdown Mode > tap the screen. Used by both the Android screen-wide shield and the in-app fallback. |
| [settings_kiosk_allowed_actions_en.arb](../source/settings_kiosk_allowed_actions_en.arb) | Actions available from the restricted menu | Settings > Kiosk Mode > Allowed Actions. Also Kiosk Mode > Allowed Actions in remote administration. |
| [settings_kiosk_permissions_en.arb](../source/settings_kiosk_permissions_en.arb) | Overlay and system UI guard permissions | Settings > Kiosk Mode > Required system permissions. Remote Kiosk Mode and the shared permission rows on Lockdown Mode also use these labels. |
| [kiosk_pin_en.arb](../source/kiosk_pin_en.arb) | PIN prompt, wrong PIN and unlock action | On the device after the configured kiosk exit gesture, including when leaving Lockdown Mode. Never translate or change the PIN entered by the user. |
| [settings_home_launcher_en.arb](../source/settings_home_launcher_en.arb) | Default home screen and screen pinning options | Settings > Home Launcher. Also Home Launcher in remote administration. |
| [settings_home_launcher_status_en.arb](../source/settings_home_launcher_status_en.arb) | Default-home status, system confirmation, unsupported devices and recovery | Settings > Home Launcher > Status. Also Home Launcher > Status in remote administration. Android's own confirmation dialogs are translated by Android. |
| [settings_app_launcher_en.arb](../source/settings_app_launcher_en.arb) | App Launcher switches and automatic return timing | Settings > App Launcher. Also App Launcher in remote administration. |
| [app_launcher_picker_en.arb](../source/app_launcher_picker_en.arb) | App selection, loading and empty states | Settings > App Launcher > Apps. Also App Launcher > Apps > Edit in remote administration. App names and package names come from Android and are not translated. |
| [settings_app_launcher_permissions_en.arb](../source/settings_app_launcher_permissions_en.arb) | Permissions needed for automatic return | Settings > App Launcher > Required system permissions. Also App Launcher in remote administration when Return automatically is on. |
| [fleet_general_en.arb](../source/fleet_general_en.arb) | Fleet setup, followers and documentation | Settings > Fleet Management. Also Fleet Management in remote administration. |
| [fleet_profiles_en.arb](../source/fleet_profiles_en.arb) | Profile names, contents, editing and deletion | Settings > Fleet Management > Profiles > select a profile. Also Fleet Management > select a profile in remote administration. |
| [fleet_sync_selection_en.arb](../source/fleet_sync_selection_en.arb) | Category notes, credentials and excluded settings | Settings > Fleet Management > select a profile > Categories, Credentials or Excluded settings. Same paths in remote administration. |
| [fleet_invitations_en.arb](../source/fleet_invitations_en.arb) | Adding kiosks, invitation prompts and joining | Settings > Fleet Management > Add a kiosk and the invitation prompt on the kiosk. Remote administration can send invitations but confirmation happens on the kiosk. |
| [fleet_status_en.arb](../source/fleet_status_en.arb) | Sync status, progress, leader notices and failures | Settings > Fleet Management > Followers or Leader and notices above managed settings. Also in remote administration. |
| [fleet_updates_en.arb](../source/fleet_updates_en.arb) | Fleet update controls and results | Settings > Fleet Management > Updates. Also Fleet Management > Updates in remote administration. |
| [fleet_switcher_en.arb](../source/fleet_switcher_en.arb) | Choosing another kiosk to administer | Remote administration > click the device name under the logo. This picker only exists in remote administration. |
| [plugins_general_en.arb](../source/plugins_general_en.arb) | Plugin list, enable controls, removal and developer links | Settings > Plugin Manager and its plugin entries. Also Plugin Manager in remote administration. |
| [plugins_install_en.arb](../source/plugins_install_en.arb) | Repository preview, trust notices and ZIP installation | Settings > Plugin Manager > Add plugin or Developer Tools > Install from ZIP. Same controls in remote administration. |
| [plugins_actions_en.arb](../source/plugins_actions_en.arb) | Plugin action placement and built-in control labels | Settings > Plugin Manager > select a plugin > Actions. Also Plugin Manager > select a plugin > Actions in remote administration. Plugin-supplied action names and descriptions are not translated here. |
| [plugins_shizuku_en.arb](../source/plugins_shizuku_en.arb) | Access state and permission guidance | Settings > Plugin Manager > select a plugin that needs Shizuku > Shizuku access. Same section in remote administration. |
| [plugins_output_en.arb](../source/plugins_output_en.arb) | Chart controls and empty or boolean readings | Settings > Plugin Manager > select a plugin > Charts or Readings. Also the same plugin page in remote administration. Names, units and text readings supplied by plugins stay unchanged. |
| [logs_general_en.arb](../source/logs_general_en.arb) | Entry counts, copy and share actions and clipboard notices | Settings > Logs and remote admin > Logs. Translate only app controls, never diagnostic lines. |
| [logs_logcat_en.arb](../source/logs_logcat_en.arb) | Android log filters, empty results and read failures | Settings > Logs > Logcat and remote admin > Logs > Logcat. Keep inserted error details unchanged. |
| [logs_console_en.arb](../source/logs_console_en.arb) | Console labels, JavaScript input hints and app-owned failures | Settings > Logs > Web Console, the docked console and remote admin > Logs > Web Console. Code, results and command history stay unchanged. |
| [remote_overview_health_en.arb](../source/remote_overview_health_en.arb) | Status tiles for Home Assistant, voice detection, ESPHome, the service and updates | Remote admin > Overview > Status. Translate the status wording. Keep wake words, engine names, versions and plugin-provided text unchanged. |
| [remote_overview_attention_en.arb](../source/remote_overview_attention_en.arb) | Notices about missing permissions, connection setup, stopped services, fleet invitations and updates | Remote admin > Overview > Needs attention, shown only when an action is needed. Names of other kiosks and version numbers fill the placeholders. |
| [remote_overview_screen_en.arb](../source/remote_overview_screen_en.arb) | Screenshot modes, capture age, screen state and camera-view badges | Remote admin > Overview > screenshot preview and its toolbar. This is the kiosk screen preview, not the camera snapshot dialog. Camera-view names stay unchanged. |
| [remote_overview_controls_en.arb](../source/remote_overview_controls_en.arb) | Quick-action labels, confirmation dialogs, camera snapshots, brightness and volume | Remote admin > Overview > Quick controls. Includes Restart device, Take snapshot, Show camera view and Check for updates dialogs. Shared actions such as Cancel and Close reuse existing templates. |
| [remote_overview_views_en.arb](../source/remote_overview_views_en.arb) | Loading messages and placeholder choices in the dashboard-view picker | Remote admin > Overview > Quick controls > Go to view. Translate the built-in choices only. Dashboard and view names supplied by Home Assistant stay unchanged. Overview is the remote admin landing page. Dashboard here means the Home Assistant panel displayed on the kiosk. |
| [settings_footer_en.arb](../source/settings_footer_en.arb) | Maker credit and coffee support link | Bottom of every Settings page on the device and every page in remote administration. Keep `{heart}` and `{author}`. They become the icon and linked name. |
| [plugin_windows_en.arb](../source/plugin_windows_en.arb) | Close button with the window title | Physical kiosk > floating window opened by a plugin > Close button tooltip. Keep `{name}` unchanged. |
| [about_identity_en.arb](../source/about_identity_en.arb) | App details, attribution links and license summary | Settings > About and remote admin > About. Keep names, addresses, license identifiers and filenames unchanged. |
| [about_updates_en.arb](../source/about_updates_en.arb) | Update checks, installation and permission guidance | Remote admin > About > Updates. Device update controls reuse existing templates. |
| [app_launcher_overlay_en.arb](../source/app_launcher_overlay_en.arb) | Failure to open a selected app | Device > Menu > Apps > Tap an app. |
| [settings_gestures_en.arb](../source/settings_gestures_en.arb) | Gesture list, deletion and clap detection | Settings > Gestures. Also Gestures in remote administration. |
| [gesture_trigger_editor_en.arb](../source/gesture_trigger_editor_en.arb) | Trigger choices, corners, counts and timing | Settings > Gestures > Add gesture or tap an existing gesture. Also Gestures > Add gesture in remote administration. |
| [gesture_actions_en.arb](../source/gesture_actions_en.arb) | Action choices and target pickers | Settings > Gestures > Add gesture > Choose an action. Also Gestures > Add gesture > Choose in remote administration. Keep URLs, app packages, kiosk names and plugin names unchanged. |
| [gesture_ha_actions_en.arb](../source/gesture_ha_actions_en.arb) | Home Assistant action fields and validation | Settings > Gestures > Add gesture > Choose an action > Home Assistant. Also the corresponding remote gesture action editors. JSON examples, domains and entity IDs are technical values and stay unchanged. |
| [gesture_descriptions_en.arb](../source/gesture_descriptions_en.arb) | Summaries of configured triggers and actions | Settings > Gestures > Configured gesture rows. Also the remote gesture list and the device hand tester. |
| [gesture_outcomes_en.arb](../source/gesture_outcomes_en.arb) | Results after a gesture runs an action | Device > Notification after a Home Assistant or plugin gesture action. |
| [gesture_hand_tester_en.arb](../source/gesture_hand_tester_en.arb) | Hand positioning guidance and live finger readings | Settings > Gestures > Hand Gesture Tester > Open tester, on the device only. |
| [settings_intercom_general_en.arb](../source/settings_intercom_general_en.arb) | Enable Intercom, menu shortcut, key creation and key changes | Settings > Intercom. Also Intercom in remote administration. Never translate the key itself. |
| [settings_intercom_answer_en.arb](../source/settings_intercom_answer_en.arb) | Answer mode, ring duration, ring sound and incoming announcements | Settings > Intercom > Answer. Also Intercom > Answer in remote administration. |
| [settings_intercom_talk_en.arb](../source/settings_intercom_talk_en.arb) | Push to talk and hands free | Settings > Intercom > Talk. Also Intercom > Talk in remote administration. |
| [settings_intercom_kiosks_en.arb](../source/settings_intercom_kiosks_en.arb) | Discovered kiosks and their availability | Settings > Intercom > Kiosks. Also Intercom > Kiosks in remote administration. Preserve kiosk names and addresses. |
| [intercom_calls_en.arb](../source/intercom_calls_en.arb) | Call picker, ringing, active calls and announcement overlays | Kiosk menu > Intercom > Call a kiosk and the on-device call overlay. Remote administration shows call status and End call. Each message lists its applicable interface. Preserve names and announcement text. |
| [intercom_errors_en.arb](../source/intercom_errors_en.arb) | Call failures, key validation and command errors | Intercom settings, the call picker and active calls. Technical details stay unchanged. |
| [sound_picker_en.arb](../source/sound_picker_en.arb) | Built-in sounds, sound files, upload and validation | Intercom > Answer > Ring sound and the shared sound pickers in ESPHome > Notifications and ESPHome > Announcements. Filenames stay unchanged. |
| [settings_dlna_en.arb](../source/settings_dlna_en.arb) | Receiver controls, background audio and server port | Settings > DLNA Renderer. Also DLNA Renderer in remote administration. Port validation is shared with ESPHome and lives in common_en.arb. |
| [dlna_player_en.arb](../source/dlna_player_en.arb) | Playback failures, log guidance and accessibility labels | Full-screen media received on the device from Home Assistant or a DLNA controller. Leave media titles and metadata unchanged. |
| [settings_media_player_floating_en.arb](../source/settings_media_player_floating_en.arb) | Floating player size, dismissal and menu shortcut | Settings > Media Player > Floating Player. Also Media Player > Floating Player in remote administration. |
| [settings_media_player_now_playing_screensaver_en.arb](../source/settings_media_player_now_playing_screensaver_en.arb) | Full-screen player, shared layout, photo filling and brightness | Settings > Media Player > Now Playing > Screensaver. Also the same group under Media Player > Now Playing in remote administration. |
| [settings_media_player_now_playing_interface_en.arb](../source/settings_media_player_now_playing_interface_en.arb) | Playback controls, text and button size, layout and dismissal | Settings > Media Player > Now Playing > User Interface. Also the same group under Media Player > Now Playing in remote administration. |
| [settings_media_player_lyrics_en.arb](../source/settings_media_player_lyrics_en.arb) | Lyrics source, fallback and timing | Settings > Media Player > Lyrics. Also Media Player > Lyrics in remote administration. |
| [player_controls_en.arb](../source/player_controls_en.arb) | Playback button labels, status and Media Player gesture actions | On the kiosk: Floating Player and Now Playing controls. In remote administration: Overview > Now playing. Media actions also appear in Settings > Gestures > Action and the remote Gestures editor. Read each message location for its specific interface. |
| [player_queue_en.arb](../source/player_queue_en.arb) | Queue headings, empty queue and unnamed chapters | On the kiosk: Now Playing > Queue. The Now playing heading also appears on the remote Overview. Translate only generated chapter labels, never titles supplied by an audiobook provider. |
| [player_speaker_groups_en.arb](../source/player_speaker_groups_en.arb) | Speaker selection and grouping notices | On the kiosk: Now Playing > Speaker selection. Room and player names stay unchanged. |
| [settings_media_player_sonos_en.arb](../source/settings_media_player_sonos_en.arb) | Group volume, TV and line-in activity, speaker discovery, adding by address and forgetting speakers | Settings > Media Player > Sonos. Also Media Player > Sonos in remote administration. Keep room names, speaker IDs and network addresses unchanged. |
| [settings_media_player_general_en.arb](../source/settings_media_player_general_en.arb) | Player source, volume controls and the local player notice | Settings > Media Player. Also Media Player in remote administration. |
| [settings_media_player_picker_en.arb](../source/settings_media_player_picker_en.arb) | Player selection, search, availability and setup notices | Settings > Media Player > Player. Also the Player selector under Media Player in remote administration. Keep player names and IDs unchanged. |
| [settings_media_player_sendspin_en.arb](../source/settings_media_player_sendspin_en.arb) | Local player connection, codec and audio synchronization | Settings > Media Player > Sendspin Player. Also Media Player > Sendspin Player in remote administration. |
| [settings_media_player_music_assistant_en.arb](../source/settings_media_player_music_assistant_en.arb) | Server connection, validation and kiosk menu shortcut | Settings > Media Player > Music Assistant. Also Media Player > Music Assistant in remote administration. |
| [settings_media_player_cache_en.arb](../source/settings_media_player_cache_en.arb) | Album art cache usage and clearing | Settings > Media Player > Album art cache, below the voice interaction volume slider. Also the same row under Media Player in remote administration. |
| [settings_web_browsing_navigation_en.arb](../source/settings_web_browsing_navigation_en.arb) | Reload, zoom and scrolling controls plus crash recovery permission notices | Settings > Web Browsing. Also Web Browsing in remote administration. |
| [settings_web_browsing_cache_security_en.arb](../source/settings_web_browsing_cache_security_en.arb) | Disable cache, Allow mixed content and Ignore SSL errors | Settings > Web Browsing. Also Web Browsing in remote administration. |
| [settings_web_browsing_scripts_en.arb](../source/settings_web_browsing_scripts_en.arb) | JavaScript injection labels, help and example comments | Settings > Web Browsing > Inject JavaScript on the HA dashboard or Inject JavaScript on external pages. Also the same rows under Web Browsing in remote administration. Translate the example comments only and keep the executable code unchanged. |
| [camera_view_status_en.arb](../source/camera_view_status_en.arb) | Connection status, retry notices and playback errors | On the kiosk: Drawer > Camera view, Settings > Camera Streams > Views > Show view and the Camera Streams screensaver. These messages appear over camera tiles. |
| [settings_camera_streams_imports_en.arb](../source/settings_camera_streams_imports_en.arb) | Home Assistant camera imports and results | Settings > Camera Streams > Home Assistant. In remote administration, open Camera Streams. |
| [settings_camera_streams_servers_en.arb](../source/settings_camera_streams_servers_en.arb) | Go2RTC server connections, credentials and deletion | Settings > Camera Streams > Go2RTC servers > Add Go2RTC server or select a server. In remote administration, open Camera Streams. |
| [settings_camera_streams_sources_en.arb](../source/settings_camera_streams_sources_en.arb) | Camera types, protocols, stream addresses and deletion | Settings > Camera Streams > Cameras > Add camera manually or select a camera. In remote administration, open Camera Streams. |
| [settings_camera_streams_views_en.arb](../source/settings_camera_streams_views_en.arb) | View editing, camera order, grid size and deletion | Settings > Camera Streams > Views > Create camera view or select a view. In remote administration, open Camera Streams. |
| [settings_camera_streams_playback_en.arb](../source/settings_camera_streams_playback_en.arb) | Codec, audio, zoom and automatic dismissal settings | Settings > Camera Streams > Playback. In remote administration, open Camera Streams. |
| [settings_camera_streams_errors_en.arb](../source/settings_camera_streams_errors_en.arb) | Validation and import errors | Settings > Camera Streams > Server, camera and view editors or import results. In remote administration, open Camera Streams. |
| [settings_camera_general_en.arb](../source/settings_camera_general_en.arb) | Camera selection and automatic snapshots | Settings > Camera. Also Camera in remote administration. |
| [settings_camera_motion_en.arb](../source/settings_camera_motion_en.arb) | Home Assistant motion sensor and shared detection controls | Settings > Camera > Motion Sensor. Also Camera > Motion Sensor in remote administration. |
| [settings_camera_streaming_en.arb](../source/settings_camera_streaming_en.arb) | RTSP and ONVIF configuration, validation and resolution guidance | Settings > Camera > RTSP & ONVIF Streaming. Also Camera > RTSP & ONVIF Streaming in remote administration. |
| [settings_camera_status_en.arb](../source/settings_camera_status_en.arb) | Stream health, URLs and connected clients | Settings > Camera > RTSP & ONVIF Streaming > Stream Status and Connected Clients. Also the same groups under Camera in remote administration. |
| [settings_camera_permissions_en.arb](../source/settings_camera_permissions_en.arb) | Camera availability and permission notices | Settings > Camera > Enable camera. Also Camera > Enable camera in remote administration. |
| [settings_camera_snapshot_en.arb](../source/settings_camera_snapshot_en.arb) | Latest image, capture action and snapshot age | Camera > Latest snapshot in remote administration only. |
| [settings_screensaver_widget_editor_en.arb](../source/settings_screensaver_widget_editor_en.arb) | Corner, widget type and shared appearance controls | Settings > Screensaver > Widgets > Add widget or select a widget. Also Screensaver > Widgets > Add widget or select a widget in remote administration. |
| [settings_screensaver_widget_weather_en.arb](../source/settings_screensaver_widget_weather_en.arb) | Weather entity, location and weather lines | Settings > Screensaver > Widgets > Weather widget. Also Screensaver > Widgets > Weather widget in remote administration. |
| [settings_screensaver_glance_en.arb](../source/settings_screensaver_glance_en.arb) | At a Glance enable switch, entities, unavailable or unknown states and Now Playing | Settings > Screensaver > At a Glance. Also Screensaver > At a Glance in remote administration. |
| [settings_screensaver_glance_appearance_en.arb](../source/settings_screensaver_glance_appearance_en.arb) | Row size, font, icons and text style | Settings > Screensaver > At a Glance > Appearance. Also Screensaver > At a Glance > Appearance in remote administration. |
| [settings_screensaver_entity_picker_en.arb](../source/settings_screensaver_entity_picker_en.arb) | Shared entity search, custom names and displayed attributes | Settings > Screensaver > Widgets > Entity widget and At a Glance > Entities. Also Screensaver > Widgets > Entity widget and At a Glance > Entities in remote administration. |

First-time setup is the wizard shown before a kiosk is configured. Its **Connect** step is separate from the **Home Assistant Setup** settings page. The reference files also contain short explanations and, for shared settings, exact device and remote administration paths in `x-locations`.

These files cover setup, Device, Home Assistant Setup, Screen & Audio, the main Screensaver controls, Clock settings and scheduled screensavers, plus Settings navigation, search and the device drawer. Screensaver media sources, pickers and slideshow settings are also included. Widgets, At a Glance and detection pages will be added in later batches. Other detailed settings pages and screens still use English where they have not been cataloged.

Dashboard names, view names, entity names and saved paths supplied by Home Assistant stay as supplied. Technical scan output also stays as supplied. Names supplied by users or plugins are not translation entries. The drawer formats plugin actions with `{pluginName}` and `{actionTitle}`. Preserve both variables. Plugin-provided wording, technical error details and published release notes remain as supplied.

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

For the German example above, the result includes `de/common_de.arb: 2/43 translated`. That means two of the forty-two messages have translations. It is fine to submit that partial file.

Commit your translation files to your fork and open a PR against this repository. Fill in the PR template with your language, what you translated and your preferred public credit. Copy the `revision` value from [source/manifest.json](../source/manifest.json) into **English source revision**. Include the validation result if you ran it and say whether you checked the text in the app.

After opening the PR, follow the [acceptance guide](PR-ACCEPTANCE.md) to check the agreement box added by the workflow. If you are unsure how to create a file or open a PR, [open an issue](https://github.com/jxlarrea/kiosk-satellite-localization/issues) with your language and the step where you got stuck.

The maintainer reviews translations and includes approved wording in a future app release. Editing a translation file does not immediately change your installed app. If English wording changes later, the affected translations need another review.
