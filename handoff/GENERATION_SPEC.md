# Synthetic collection implementation specification

Status: implementation contract, not an implemented Blender pipeline. Read DATA_CONTRACT.md for normative output semantics. Initial device: MacBook M5, Claude Code + Blender. Pin actual tested versions after inspection. Proposed parameter values are engineering defaults, not biological estimates or clinical thresholds.

## Research objective

Hold an underlying straight-line-trot movement constant, change acquisition conditions, and estimate how those changes affect landmark recovery and head/pelvis MinDiff/MaxDiff. Separate (1) geometry/measurement calculations using simulator truth, (2) video pose estimation error, and (3) biological realism. Do not let a perfect synthetic result stand in for real validation.

Two collection modes are useful: in-place motion for initial geometry testing and translated straight-line motion for camera experiments. Mark the mode explicitly. In-place animation is not a field recording of forward locomotion. Physical simulation is not required for the first method tests, but procedural animation must be called kinematic rather than mechanically validated.

## Gate 0 — environment, assets and rights

Create a capability report with Blender executable/build, render engines/devices available, host Python, FFmpeg, OS/architecture, RAM and free disk. Benchmark a single frame on available CPU/Metal paths, recording time and settings. Do not download full datasets or train models as part of this audit.

Asset import decision:

| Inspection result | Action |
|---|---|
| `.blend` with mesh, skeleton, skin weights and trot | Work on a copy; audit constraints/actions/materials and root motion |
| FBX/glTF or another rig-capable format | Test imported hierarchy, weights, actions, axes and textures; compare to source previews |
| OBJ/STL or other static geometry | Expect geometry only unless accompanied by other files; do not assume a rig |
| Mesh plus rigid-body physics | Check whether a separate anatomical rig exists; object-level dynamics alone do not articulate limbs |
| Unusable topology or absent rights | Continue with self-created calibration primitives; document the asset blocker |

Produce contact sheets, rest-pose and animated previews, landmark definitions, bounding dimensions, and a rights inventory. Determine whether scaling is physically grounded. A user-supplied measured dimension or documented asset dimension may establish scale; a visually guessed horse height does not establish empirical calibration. Keep original files immutable and external to Git.

Exit: working copy opens, essential textures resolve or are documented, artifact rights are recorded, axis/unit status explicit, and rig/motion suitability classified. Unknown rights prohibit dataset release or work-environment transfer; use self-created fixtures to continue unaffected work.

## Gate 1 — coordinate and timing fixture

Before horse animation, create known noncoplanar points and a calibration board in an empty scene. Export Blender world coordinates, converted CV camera coordinates, camera intrinsics/extrinsics, and pixel coordinates. Test both a centered and shifted camera. Confirm scale and axis conventions with a point forward, left and above the origin. Confirm horse anatomical left using a temporary asymmetric diagnostic marker.

Use a perspective pinhole camera, fixed exposure, no distortion, no motion blur, no rolling shutter and square pixels initially. Record all resolved intrinsics; do not infer calibration from focal length alone. Evaluate final constraints/deformation via Blender's evaluated dependency graph at every sample. Capture full transforms rather than assuming object/bone local coordinates are world coordinates.

Timing: rational frame rate, `frame_index` zero-based, center sample `t = frame_index * fps_denominator / fps_numerator` after warm-up. Retain exactly N samples; clip nominal duration is N/fps, final sample is (N−1)/fps. Decode the encoded MP4 and compare frame presentation timestamps with the reference; encode without frame duplication or interpolation. Keep original PNGs as a lossless reference. Do not derive timestamps from wall-clock rendering duration.

Exit: projection error ≤0.5 px for known points, round-trip transform checks pass, timestamp discrepancy ≤0.01 frame, exact decoded frame count, and no axis/mirror ambiguity. These are software tolerances, not equine accuracy requirements.

## Gate 2 — short horse pilot

Create one 4-second, 640×360, 60 fps clip after 1 second of unexported warm-up. This is 240 retained frames. Adapt the provided pilot config once paths, renderer, landmark mapping, rights and unit status are resolved. Keep the full horse in frame. Select a rear-oblique view for initial pelvis visibility, then test a front-oblique view for head visibility. Do not assume every required landmark is visible from one camera.

Landmarks: poll, withers, sacrum, left/right tuber coxae and four hoof points. A veterinarian/biomechanics adviser should later review anatomical placement. Define whether each point is a surface location, virtual marker center or skeletal proxy; do not silently substitute nose for poll or tail base for sacrum. If the asset cannot support a point, mark it unavailable and constrain the study endpoint accordingly.

Use deforming-surface barycentric attachments or a validated equivalent tied to evaluated skin geometry. Bone attachments may be exported as separate skeletal proxies. Preserve topology/mapping IDs; subdivision/deformation can invalidate naive vertex-index attachments. No diagnostic markers appear in the clean video. Export a separate overlay/skeleton preview with IDs for debugging.

Animation quality checks: intended diagonal limb pairing in trot, limb ordering, contact schedule, root trajectory, visible foot sliding, ground penetration, joint discontinuities, implausible body deformation and repeat-loop discontinuities. A phase schedule is a commanded event, not verified hoof contact: export both commanded phase events and geometric contact events if measured. Rig controls or ground collisions do not establish forces or pain.

Exit: clean video, diagnostic video, per-frame coordinates/visibility, actual camera calibration, events/provenance, checksums, validation report, motion plausibility notes. Review representative frames and the entire short clip before batch rendering. Allow geometric/pose tests with `scene_unit`; disallow physical-unit outputs and IMUs until scale is verified.

## Gate 3 — controlled camera experiment

Start with this illustrative design, adjusting framing to verified asset dimensions:

- Four independently specified base motion sequences, 6 seconds each after warm-up, 60 fps. Preserve the same movement seed/trajectory across all cameras for a motion.
- Two view families: front and rear. For each, local azimuth offset −20°, 0°, +20°; roll −5°, 0°, +5°; two elevations, nominally 0° and 10°. Exactly 36 camera conditions per motion, 144 clips, 51,840 frames at 360 frames/clip.
- Use one fixed focal length and a recorded fixed camera radius per motion for the primary sweep. Choose radius once to frame the entire trajectory for every planned condition. Do not silently auto-reframe each frame. Camera intrinsics/extrinsics accompany each view.
- Preserve a baseline per view family. Compare each changed view with the same movement's baseline and the same reference trajectory. Cameras may share frame evaluations to avoid regenerating motion.

With one horse mesh and one animation, these are technical replicates/variants, not four independent horses. If all four sequences derive from one action, they remain one source motion family for split leakage checks. Report that limitation. A camera-robustness experiment can use shared motion deliberately; a subject-generalization evaluation cannot count views as independent subjects.

Then add nuisance factors one at a time on a small selected subset: 30 versus 60 fps, reduced resolution, encoding quality, lighting/contrast, handler-like occluders, background complexity and controlled tracking errors. Preserve source frame IDs when downsampling; do not interpolate frames to fake higher capture rates. Defer lens distortion, rolling shutter, camera shake and blur until their reference semantics and quality checks exist. Distinguish known mid-exposure position from a blurred pixel distribution; a blurred landmark does not have a uniquely visible point.

Plan output/time before execution: `clips × frames/clip × measured seconds/frame`, plus encoding and validation. Measure bytes/frame for a pilot; include depth/masks separately. Respect a configurable disk budget and write partial results safely. Resume only after hash/schema checks. Use `planned`, `rendering`, `rendered`, `validated`, `failed`, `quarantined` statuses with reasons.

## Gate 4 — injected movement changes

Keep camera experiments separate from movement-change experiments. Start with small, explicitly assumed perturbations of head/pelvis trajectory, timing or joint controls. Store exact operator/parameter and resulting measured reference change. Root body rocking can alter pelvis/head together and is not a valid surrogate for a unilateral clinical condition. Recheck limb contact and anatomical plausibility after every perturbation.

Compute true MinDiff/MaxDiff from exported reference and a frozen event/half-stride convention, not directly from an animation knob. The same knob can alter extrema differently. No labels such as `lame`, `injured`, `pain_score` or `disease_stage`. Use labels such as `injected_vertical_component` and `amplitude_scene_unit`.

## Collection outputs

Required now: clean RGB frames and MP4, static camera intrinsics/extrinsics, world/CV/pixel landmark reference, occlusion/out-of-frame states, event origin, manifest, configuration snapshot, logs/checksums and quality report.

Optional later: segmentation/depth, synthetic mocap with missing markers/noise, and virtual IMUs. In Blender, depth passes have renderer-specific semantics; specify ray distance versus optical-axis depth before use. Synthetic mocap needs noise/soft-tissue assumptions with provenance. Do not add identical Gaussian noise to all instruments and call them independent references.

For an ideal accelerometer at a sensor origin with world position p and world-from-sensor rotation R, use `f_sensor = R.T @ (p_ddot − g_world)` with `g_world = [0, 0, −9.80665] m/s²`. Derive angular velocity from orientation increments on SO(3), not Euler-angle differences. Rigid offsets add rotational acceleration; differentiate the actual offset sensor trajectory. Oversample kinematics at a documented rate (initial candidate 240 Hz), handle endpoint derivatives, test stationary gravity and known rotation, and document filtering/aliasing before resampling. Add bias/drift/noise in a separate observation layer with units and seed. This is an idealized instrument, not a validated commercial IMU or force plate. Do not derive ground reaction forces from animation alone.

## Evaluation

Level A: simulator reference → metrics. Test hand-computed signals, translation/scale behavior, sign conventions, event timing and dropout. Recover known injected changes; distinguish exact finite-sample truth from continuous-time truth.

Level B: projected reference → measurement pipeline. Measures effects of 2D geometry, normalization and segmentation without pose prediction. Raw pixel y or a ground-plane homography cannot generally recover vertical 3D motion under perspective. Keep physical world reference, projected reference and inferred metric separate.

Level C: clean RGB → existing pose model → metrics. Measure landmark pixel error normalized by defined body scale, visible versus occluded performance, usable-stride coverage, metric bias/MAE and paired camera sensitivity. Run model without access to reference labels; no overlay leakage. Rerun on decoded compressed video as well as selected PNGs to isolate encoding effects.

For synthetic study reporting, provide per-motion/per-camera results and condition curves. Seed-bootstrap intervals describe this simulator's stochastic variation only; they do not describe horse populations. Do not count frames/views as independent horses. Future real-video evaluation must use horse-level grouping and independent references, with error limits agreed with veterinary expertise.

Fine-tuning comes after baseline evaluation. Verify mesh/animation/render/label/weight training rights, label anatomy, license of framework and weights, and native Mac backend support. Split by asset and source motion family before augmentation/render derivatives. A one-asset collection cannot support a new-horse generalization claim. Reserve real footage and horses for independent transfer evaluation if legally available. Compare real-only versus synthetic-plus-real training only when both training sets and held-out references exist.

## Required tests and failure conditions

| Test | Expected behavior |
|---|---|
| Known 3D point projection and reconstruction at known depth | Meets stated numeric/pixel tolerance; correct top-left pixel convention |
| Axis, scale, mirror and camera shift | Unambiguous fixture results; physically unverified scale blocks metre outputs |
| Animated surface landmark | Follows evaluated skin location through constraints/deformation |
| Behind camera, occluded, outside image | Explicit states; no zero-filled fake coordinate |
| Render/encode/decode timing | Exact frame count and timestamp checks; failures quarantine the clip |
| Known half-stride extrema and injected change | Correct sign/units; incomplete strides handled explicitly |
| Fixed config/seed rerun | Same reference data within 1e−6 relative numeric tolerance; images may differ across render hardware |
| Interrupted run and resume | Completed validated files reused; incomplete output rewritten in staging |
| Missing texture, action, landmark, rights evidence | Actionable failure/report; no silent fallback labeled as success |
| Split grouping | Every derivative of an asset/source motion family stays in its assigned group |

Deliver `reports/pilot-report.md` with commands, hardware/software versions, all quality checks and failures, asset license status, frame samples/overlays, metric definitions, intended versus measured gait properties, timing/disk benchmarks, and next-batch estimate. Do not report a completed data-generation stage until its required artifacts validate.
