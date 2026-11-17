# Dataset contract v1.0

Normative specification for the future generator and phase 2 ingestion. CSV and JSON are acceptable for the pilot. Use typed Parquet for large frame/landmark tables and Delta after ingestion. JSON numbers must be finite; missing values are null, never NaN or sentinel zero. UUIDs or stable content-derived strings are acceptable identifiers. All timestamps recording software execution use UTC ISO-8601; simulation time is separate.

## Coordinates, units and time

- World: right-handed; +X nominal forward heading, +Y anatomical left at initial heading, +Z up. A moving body frame is separate from world when heading changes. Store the world-from-body transform when relevant.
- Length: `m` only with verified physical scale and evidence; otherwise `scene_unit`. Store `meters_per_scene_unit` only when verified. Derived metric units must match their coordinate domain: world length, pixels or a named dimensionless normalization.
- Camera CV coordinates: +x right, +y down, +z forward. Convert explicitly from Blender camera coordinates (+x right, +y up, −z forward). Export a world-to-CV 4×4 matrix for each static camera or each frame for moving cameras.
- Projection: `p_cv = R_world_to_cv @ p_world + t_world_to_cv`, column-vector convention; `q = K @ p_cv`; `u = q_x/q_z`, `v = q_y/q_z` only for positive depth. World length and translation share units.
- Pixel coordinates: continuous top-left origin at the upper-left image boundary, pixel centers at (0.5, 0.5), right/down positive. Bounds are `0 <= u < width`, `0 <= v < height`. Implement the half-pixel convention consistently when converting Blender normalized device coordinates and labels from CV frameworks; verify with a rendered fixture.
- Temporal reference: retained `frame_index` starts at 0; `t_seconds = frame_index * fps_den / fps_num`. Warm-up samples are excluded, and original Blender frame/subframe mapping is stored. Nominal clip duration N/fps differs from the last sample time. MP4 decoded presentation timestamps must be checked relative to the first retained frame.
- Occlusion does not erase simulator truth. Out-of-frame points may have valid projections outside image bounds. Behind-camera points have null u/v. These states remain distinct.

## Directory layout

```
dataset/
  dataset.json
  licenses/                 # evidence or references; redact personal receipts
  configs/<config_hash>.json
  asset_inventory.csv
  landmark_definitions.json
  split_assignments.csv
  trials/<trial_id>/
    manifest.json
    events.csv
    landmarks_world.parquet # or pilot CSV
    observations_mocap.parquet  # optional
    observations_imu.parquet    # optional
    views/<camera_id>/
      camera.json
      frames/000000.png
      video.mp4
      landmarks_2d.parquet
      diagnostic_overlay.mp4
      frame_timestamps.csv
    quality.json
  runs/<run_id>/{environment.json,commands.jsonl,logs/}
  checksums.sha256
```

Use relative paths in manifests. Resolve within the dataset root; reject path traversal, unsafe symlinks and references outside approved storage. Avoid copying local usernames, absolute paths, tokens or private receipts into a distribution archive.

## Required entities

| Entity | Required fields and meaning |
|---|---|
| Dataset | schema_version, dataset_id, created_at_utc, synthetic=true, purpose, provenance_status, unit policy, allowed_use, generator revision, inventory/config/split paths |
| Asset | asset_id, content SHA-256, asset type, source, license evidence/status, permissions per use, topology/rig identity |
| Motion | motion_id, source_motion_family_id, asset_id, method, source/provenance, seed, parameters, plausibility_review_status |
| Trial | trial_id, motion_id, run_id, config_hash, split_group_id, frame count/rational fps, warm-up, units/scale status, requested/actual outputs, validation status |
| Camera | camera_id, width/height, fps, K, world_to_cv transform, distortion model/coefficients, clipping planes, lens/sensor settings, shutter/exposure, pixel convention |
| Landmark definition | landmark_id, anatomical description, surface/skeletal/proxy type, object/mesh identity, attachment method and coordinates, mapping version, reviewer/status |
| World landmark row | trial_id, frame_index, t_seconds, landmark_id, x/y/z, unit, reference_type, mapping_version |
| Projected landmark row | trial_id, camera_id, frame_index, landmark_id, u/v, depth_cv, occluded, in_frame, behind_camera, visibility_method |
| Event row | trial_id, event_id, event_type, limb, t_seconds, origin, uncertainty_seconds, method_version |
| Run | run_id, generator revision/source hash, dirty-state hash if needed, config hash, seeds, runtime versions, renderer/device/settings, started/ended UTC, exit status |
| Quality | trial/view ID, check name, value, tolerance, pass/fail/not_applicable, reason, validation software revision |

Keys: `(trial_id,frame_index,landmark_id)` for world landmarks; add camera_id for projected landmarks; `(trial_id,event_id)` for events. No duplicate keys. World data is not duplicated per camera. Predicted keypoints use separate tables with model/run IDs, confidence and coordinate-domain metadata. Pose-model confidence is not visibility or calibrated uncertainty.

`reference_type` examples: `simulator_surface`, `simulator_skeletal_proxy`, `simulator_marker_center`. Do not name simulated references `clinical_ground_truth`. Dataset truth is exact relative to the modeled scene, subject to numeric and attachment correctness.

Visibility: estimate line-of-sight from the camera to evaluated landmark using scene occlusion/ray/depth tests. Define tolerance and whether the point is a surface point or lies inside the mesh. A skeletal point inside the body is not directly visible; optionally link it to a named surface proxy rather than ray-casting it as if it were a marker. Check occlusion by all relevant scene objects, including the horse itself. Export diagnostic validation images.

Events must distinguish `commanded_animation_phase`, `geometric_contact` and future `independent_reference`. A commanded phase label cannot be presented as measured contact. Store subframe event times; derived frame indices are optional. Geometric contact should document height/velocity thresholds in appropriate units and their assumptions.

## Example manifest shape

This is a documentation example with illustrative IDs, not an accepted output: placeholder hashes must be replaced by actual SHA-256 values.

```json
{
  "schema_version": "1.0",
  "trial_id": "trial-001",
  "synthetic": true,
  "run_id": "run-001",
  "asset_id": "horse-001",
  "motion_id": "motion-001",
  "source_motion_family_id": "source-action-001",
  "split_group_id": "horse-001/source-action-001",
  "config_hash": "REPLACE_WITH_SHA256",
  "unit": "scene_unit",
  "scale_status": "unverified",
  "meters_per_scene_unit": null,
  "frame_count": 240,
  "fps_num": 60,
  "fps_den": 1,
  "warmup_seconds": 1,
  "motion_mode": "in_place_pilot",
  "motion_validity": "engineering_animation_not_biologically_validated",
  "status": "planned",
  "artifacts": []
}
```

Actual artifact entries require relative path, byte size, SHA-256, content type, role, license reference and validation status. A manifest cannot be `validated` while required outputs are missing. Use explicit `not_requested` for IMU/mocap observations rather than empty files interpreted as successful collection.

## Measurement results and uncertainty

Each result row: `run_id, trial_id, camera_id, landmark_id, coordinate_domain, metric_name, value, unit, reference_result_id, stride_count_total, stride_count_valid, exclusion_reason_counts, event_method, preprocessing_config_hash, model_version, method_version`.

Use world Z for world vertical. For projected image motion, define the sign and normalization; do not equate raw v with physical height. Freeze half-stride/event ordering before signed MinDiff/MaxDiff comparisons. Keep per-stride values and trial summaries separately. No automatic limb diagnosis based on metric sign.

Uncertainty metadata must name the quantity and method: numerical tolerance, assumed annotation error, calibration uncertainty, repeated-trial variation, seed variation or population interval. A simulator's zero reference noise is not zero real-world uncertainty. Missing/insufficient strides produce a structured unavailable result with reasons, never a score of zero.

## Split policy

All views, clips, crops, encodings, perturbations and frame derivatives of a source family inherit a common group. For training intended to generalize across assets and motions, group connected assets/source motion families to avoid either crossing splits. Keep a separate deliberate paired-view protocol for camera sensitivity. With only one asset/family, record `evaluation_scope=within_asset_camera_sensitivity`; a generalization test split may be unavailable rather than fabricated.

## Validation and transfer acceptance

Validate JSON schemas, supported major version, enums, finite values, key uniqueness, referential integrity, time monotonicity, fps/frame alignment, calibrated projection, visibility semantics, units, split grouping, hashes and artifact existence. Reject a physical-unit claim with unverified scale, zero depth treated as a normal projection, inference predictions in reference columns or inconsistent timestamps.

Transfer archive includes code/revision and source hashes, tested dependency lock, documentation, resolved configs, permitted asset/data manifests, license evidence, quality/evaluation reports and checksums. Raw assets/media are included only where their permissions allow. Run checksum and schema validation after copying. Never silently convert `scene_unit` to metres during ingestion. Unsupported versions go to quarantine for explicit migration.
