# Rebuild the Nextion status UI

1. Read the rear sticker. Select the exact touchscreen model in Nextion Editor. This specification assumes a 400 × 240 NX4024T032 and touch navigation requires the resistive suffix. Use the editor's simulator while the model is unconfirmed.
2. Add two pages in order, `home` (0) and `diag` (1). Set the listed component names, positions and sizes exactly from `operator_ui.json`. Use a high-contrast background, a readable Latin font, and `txt_maxl` of 32 or more for each text component. Initialize the caption and state fields from the JSON.
3. Put `sendme` in both pages' Postinitialize Event. Add the listed release events. The touchscreen buttons change pages locally. Leave **Send Component ID** unchecked. There is no action on inbound touch events on the controller. The physical panel handles controller actions.
4. Retain 9600 8N1 for the first test. Use Editor Debug to send `sendme` followed by `FF FF FF`. The serial response for Home is `66 00 FF FF FF`; Diagnostics is `66 01 FF FF FF`. Try `camera.txt="CAM2"` with that terminator. If the display reboots, it should return the startup lock screen until the controller refreshes it.
5. Save the native `.HMI` in the revision folder. Compile the matching `.TFT` after suffix confirmation. Verify cable pin order and steady/startup supply at the LCD before loading a unit. Confirm state, camera, speed, diagnostic error and page transitions on bench. The preset field can show local selection, which is separate from camera confirmation.

The JSON and `firmware/display.py` are the reproducible R11 source. Native Editor compilation and physical tests remain open. [Nextion instruction and response reference](https://nextion.ca/nis/).

## R11.1 simulator checklist

- Set page orientation to 400 × 240 landscape. Generate and import a Latin font, assign it to each component, and use text length 32. Use software UART terminal hex mode for the byte tests.
- Set `bkcmd=3` during a debug-only session to capture status frames. An update should show camera and speed on page 0, and `R11.1 BENCH` on page 1. Do not use display acknowledgements as camera status. Input touch frames have no host action.
- After visiting Diagnostics and returning Home, verify the page number response and resend of Home fields. Simulate a display reboot, then verify that the host polls for the page and refreshes the state. Verify the fault text fits using the chosen font.
- Record the owner label, editor version, exact device selected, native file hashes, and simulator result before attaching any compiled files. The current R11.1 package contains the JSON specification and host parser. No physical display result is recorded.
