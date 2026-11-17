# Claude Code handoff and phase 2 solution design

Prepared 17 November 2026. User-confirmed target: Claude Code controlling Blender on a MacBook M5. Horse files/textures exist on the user's Mac. Rig, animations, formats, rights, and anatomical suitability are not yet inspected. This package specifies work to implement; it does not contain a renderer or claim that the user's assets have been opened.

## Start here

1. Copy this project to the Mac. Keep horse assets outside Git. Open Claude Code in the copied project directory.
2. Paste [CLAUDE_START_HERE.md](CLAUDE_START_HERE.md) into Claude Code. Supply the local asset directory when Claude needs it. No upload is required for local rendering.
3. Claude must first create an asset/capability report and a static preview. A rigid body or static mesh may not have an anatomical skeleton or gait animation.
4. Read [GENERATION_SPEC.md](GENERATION_SPEC.md) for the implementation contract and staged acceptance gates. Start with a short pilot, then a controlled camera experiment; avoid a large render batch before geometry/timing checks pass.
5. Use [DATA_CONTRACT.md](DATA_CONTRACT.md) for all exported labels and manifests. The starter config and inventory template have intentional unresolved fields; they are not ready-to-render inputs.
6. Use [PHASE2_SOLUTION_DESIGN.md](PHASE2_SOLUTION_DESIGN.md) to build the Databricks-backed research application in the work environment. It includes the delivery backlog and environment decisions still needed.

## Files

| File | Purpose |
|---|---|
| CLAUDE_START_HERE.md | Copy/paste execution prompt, autonomy boundaries, required reports |
| GENERATION_SPEC.md | Rendering, motion, virtual collection methods, experiments, quality gates |
| DATA_CONTRACT.md | Coordinate/time conventions, tables, schema examples, validation rules |
| PHASE2_SOLUTION_DESIGN.md | Full-stack/data/ML architecture, security, deployment, tests, operations |
| config/pilot.json | Conservative smoke-test configuration; scientific parameters remain assumptions |
| templates/asset_inventory.csv | Local inventory and rights review template |
| templates/parameter_provenance.csv | Separates evidence-based parameters from engineering assumptions |
| ACCEPTANCE_CHECKLIST.md | Review checklist for Claude's eventual implementation |
| SOURCES.md | Official implementation documentation and scientific references |

## Scope and scientific boundary

Primary phase 1 experiment: hold one movement fixed, vary camera conditions, and quantify errors in recovered landmarks and head/pelvis asymmetry. All outputs are labeled synthetic. Exact simulator coordinates validate software against that simulator, not against living horses. The same simulator coordinates used to create a motion are not an independent biological reference.

Physical metres are allowed only after asset scale is explicitly verified against a documented dimension; otherwise use `scene_unit`, disable physical sensor claims, and do not relabel output as millimetres. No clinical disease, injury, pain, or performance labels are generated from animation parameters.

The original numerical sandbox remains usable from the project root. Its synthetic scene units and known stride boundaries are distinct from this new proposed 3D collection pipeline.
