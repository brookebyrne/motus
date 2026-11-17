# Paste the following into Claude Code

You are implementing a reproducible synthetic equine gait data generator on my MacBook M5, using Blender and Python. My horse model, alternative file formats, and textures are on this computer. I do not know whether the asset has a usable skeleton, skin weights, or gait animation. Read this handoff directory and the existing `docs/phase-1.md` before implementation.

The goal is a documented methods-feasibility research dataset and pipeline. Generate controlled video and synchronized simulator reference data for evaluating markerless movement measurement. Do not produce a clinical lameness classifier or claim the generated movement reproduces disease. The phase 2 design is a future integration target, not permission to provision paid cloud resources or deploy to an employer's account.

## First actions

1. Inspect the project and local instructions. Determine macOS, architecture, available RAM/disk, Blender executable/version/build, FFmpeg availability, Python tooling, and available rendering devices. Record actual values. Use native Apple acceleration only when supported and verified, with CPU fallback. Do not assume CUDA on this Mac.
2. Locate the horse assets only in the directory I provide or clearly identified project directories. If the path is missing, ask me for that one essential input and continue code/design work independent of it. Do not scan unrelated personal files. Never overwrite original assets.
3. Inventory file names, extensions, sizes, hashes, associated textures, license/receipt documents, and import candidates. Prefer an existing `.blend` scene if its provenance is known and safe; otherwise choose the most complete mesh/rig format after inspection. Disable auto-execution of embedded scripts on import/load. Do not execute untrusted asset code.
4. Produce `reports/asset-audit.md`: unit/axis assumptions, object transforms, bounds, materials, missing texture links, skeleton/bone names and hierarchy, skin weights, constraints/drivers, available actions, frame ranges, root-motion behavior, and apparent gait. Include static views and a small skeleton/landmark overlay where possible.
5. Determine which branch applies:
   - Existing rig plus suitable trot: adapt it in a working copy, verify retargeting and timing.
   - Rig without suitable motion: implement a clearly labeled procedural or licensed animation, then review plausibility.
   - Static mesh/rigid-body asset: report that anatomical articulation is absent. Implement inspection/data/export tooling and a simple landmark-motion test immediately. For horse animation, prepare a non-destructive rigging plan; ask for input only if the current asset is unusable or an external paid/licensed asset is necessary.
6. Record rights separately for mesh, rig, animation, textures, and reference data. Missing rights evidence blocks ingestion into a shared/distributed/training dataset; it does not block development using self-created geometric fixtures. Do not invent permissions or apply the article's license to a dataset.

## Build sequence

Implement the gates in GENERATION_SPEC.md in order. Start with a tiny static calibration fixture and one 4-second clip. Prefer deterministic procedural controls and exact exported references over visually impressive unconstrained motion. Save all resolved configuration and random seeds. Create a diagnostic render with visible landmarks and a separate clean video without reference markers.

Suggested project structure (new implementation):

```
generator/
  cli.py
  blender/{inspect_asset.py,build_scene.py,animate.py,export_reference.py,render.py}
  {coordinates.py,schemas.py,quality.py,encode.py,plan.py}
configs/{pilot.json,camera_sweep.json}
tests/{test_projection.py,test_timing.py,test_quality.py,test_metrics.py}
reports/{asset-audit.md,pilot-report.md,quality-report.json}
data/                    # ignored in Git
```

Use the standard host Python environment for planning, validation, encoding, and analysis. Blender runs its own Python scripts in background mode. Avoid installing host packages into Blender unnecessarily. Build a small adapter boundary around Blender APIs. Pin the tested Blender version, renderer/settings, FFmpeg version, and host dependencies. Check version-specific APIs against official docs.

Provide these implemented CLI behaviors, with `--help`:

```
python -m generator.cli inspect --asset-root <path> --output reports/asset-audit.md
python -m generator.cli validate-config --config configs/pilot.json
python -m generator.cli plan --config configs/pilot.json --output reports/render-plan.json
python -m generator.cli generate --config configs/pilot.json --output data/pilot
python -m generator.cli validate-dataset --input data/pilot
python -m generator.cli evaluate --input data/pilot --output reports/pilot-report.md
```

These are required interfaces to create, not existing commands in this handoff. Fail clearly on unresolved asset paths, scale, unknown landmark mappings, missing rights, or invalid configurations. Allow `scene_unit` geometric testing when scale is unresolved, with physical outputs disabled. Include dry-run counts and estimated disk/compute use; start at low resolution and measure throughput before increasing batch size. Resume valid completed artifacts and never silently overwrite a different run/config.

## Acceptance and reporting

- Export DATA_CONTRACT.md v1.0 with machine-readable validation and explicit provenance.
- Verify world-to-camera-to-pixel transforms and decoded-frame timestamps with known geometry before accepting labels.
- Track surface anatomical landmarks after deformation, not just rest-pose bone heads. Document point definitions and mapping uncertainty.
- Reference coordinate truth is exported independently of the pose model. No predicted coordinates may overwrite reference columns.
- A frame with an occluded landmark keeps its reference location but marks visibility explicitly; predictions may be missing.
- Keep source motion families and all derivatives in one data split; no adjacent-frame or multiview leakage.
- Report physiological assumptions, biomechanical defects, failed trials, exclusions, and all unimplemented outputs. Never fabricate results.
- Do not add virtual IMU channels until physical scale, pose trajectories, orientation and derivative tests pass. They are optional for the initial camera study.
- Do not fine-tune a model before the generator/reference tests pass. First evaluate a reviewed existing animal pose model, noting its anatomical mismatch and licenses.
- Record commands, exit status, package/device versions, timings and memory, tests, artifact hashes, and representative images in the final report. Compare CPU and accelerated reference coordinates within stated tolerances; image bytes may differ across platforms.

Continue through reversible implementation and local tests without repeatedly asking permission. Ask only for truly missing information, external rights/purchases, or actions outside my local authorized scope. Do not delete source files, upload assets, publish videos, or provision cloud services without authorization. Do not assume my employer permits personal research data on its systems.

At completion, give me: asset-readiness findings, exact commands to reproduce, pilot artifacts, quality/evaluation report, what is biologically assumed, what remains blocked, and a hashed phase 2 transfer manifest. Update this project's documentation to match actual implementation rather than claiming planned features exist.
