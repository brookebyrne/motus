# Review checklist for Claude's delivery

This checklist is intentionally unchecked: the handoff does not implement or validate rendering.

## Asset and environment

- [ ] Original assets preserved; asset directory supplied locally.
- [ ] Mesh/rig/animation/texture inventory and hashes produced.
- [ ] Rig and trot availability established; missing rig/motion explicitly addressed.
- [ ] Source rights reviewed per use; unresolved restrictions block affected release/transfer/training only.
- [ ] Actual Mac/Blender/FFmpeg/device versions and pilot benchmarks recorded.
- [ ] Scale verified with evidence or `scene_unit` retained; anatomy mapped/review status recorded.

## Generator

- [ ] Required CLI commands implemented, documented and tested.
- [ ] Placeholder config resolved; strict validation reports all missing inputs.
- [ ] Calibration fixture passes projection/axis/mirror/timing tests.
- [ ] Evaluated surface landmark positions exported correctly through deformation.
- [ ] Short clean video and separate diagnostic overlay produced and reviewed.
- [ ] Decoded MP4 frame count/timestamps agree with reference labels.
- [ ] Visibility distinguishes occluded/out-of-frame/behind-camera states.
- [ ] Source motion, event origin and motion plausibility limitations documented.
- [ ] Dry-run plan estimates batch count/disk/time; pilot/resume/failed outputs handled safely.

## Research and data

- [ ] Reference, predicted and optional noisy observation tables remain distinct.
- [ ] Contract validators cover keys, units, timestamps, transforms, finite values and artifact hashes.
- [ ] Motion/asset derivative grouping prevents leakage; one-asset scope is explicit.
- [ ] Camera experiment holds movement fixed and reports paired errors plus coverage.
- [ ] Parameters have provenance or explicit assumption labels.
- [ ] No disease/injury labels inferred from animation; no physical forces inferred from kinematics alone.
- [ ] Optional virtual IMUs remain disabled unless scale/derivative/orientation tests pass.
- [ ] Fine-tuning follows a documented baseline and independent split plan, if attempted.

## Transfer and phase 2

- [ ] Pilot report lists actual passing/failing checks and unimplemented components.
- [ ] Resolved configs, environment lock, code/source hashes and commands included.
- [ ] Restricted assets/secrets/private paths excluded from transfer unless explicitly permitted.
- [ ] Destination employer/data authorization and cloud/runtime inventory confirmed before upload/deploy.
- [ ] Dataset revalidated after transfer; phase 2 implementation tracked against P2-01 through P2-08.
