# Handoff package checks

Prepared in the available Linux workspace on 17 November 2026.

- Existing numerical sandbox: eight unit tests passed after adding this handoff.
- Relative links in the initial seven handoff Markdown documents checked successfully.
- Pilot JSON parsed; duration, rational fps and frame count agree (4 seconds × 60 fps = 240 frames).
- Asset path and physical scale intentionally unresolved; optional virtual IMU export disabled.
- Both CSV templates checked for consistent field counts.
- The transfer archive is accompanied by a per-file SHA-256 manifest; archive entry contents verified against source bytes during packaging.

These checks establish package consistency only. No Blender installation, horse asset, Mac device, animation, rendering, pose inference, new data export, Databricks workspace, deployment or cloud permissions were tested here. CLI names in the handoff describe interfaces Claude must implement. The acceptance checklist remains unchecked until the actual generator passes its gates.
