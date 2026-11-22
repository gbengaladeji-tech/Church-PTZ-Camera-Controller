# Rebuild the Nextion status UI

1. Read the rear sticker. Select the exact touchscreen model in Nextion Editor. This specification assumes a 400 × 240 NX4024T032 and touch navigation requires the resistive suffix. Use the editor's simulator while the model is unconfirmed.
2. Add two pages in order, `home` (0) and `diag` (1). Set the listed component names, positions and sizes exactly from `operator_ui.json`. Use a high-contrast background, a readable Latin font, and `txt_maxl` of 32 or more for each text component. Initialize the caption and state fields from the JSON.
3. Put `sendme` in both pages' Postinitialize Event. Add the listed release events. The touchscreen buttons change pages locally. Leave **Send Component ID** unchecked. There is no action on inbound touch events on the controller. The physical panel handles controller actions.
4. Retain 9600 8N1 for the first test. Use Editor Debug to send `sendme` followed by `FF FF FF`. The serial response for Home is `66 00 FF FF FF`; Diagnostics is `66 01 FF FF FF`. Try `camera.txt="CAM2"` with that terminator. If the display reboots, it should return the startup lock screen until the controller refreshes it.
5. Save the native `.HMI` in the revision folder. Compile the matching `.TFT` after suffix confirmation. Verify cable pin order and steady/startup supply at the LCD before loading a unit. Confirm state, camera, speed, diagnostic error and page transitions on bench. The preset field can show local selection, which is separate from camera confirmation.

The JSON and `firmware/display.py` are the reproducible R11 source. Native Editor compilation and physical tests remain open. [Nextion instruction and response reference](https://nextion.ca/nis/).
