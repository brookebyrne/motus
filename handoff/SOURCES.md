# Documentation and evidence register

Prepared 17 November 2026. Links are implementation starting points. Pin software versions and consult the matching docs during implementation; web pages may update. The previous project's [phase 1 protocol](../docs/phase-1.md) holds the initial literature review and its limitations.

## Rendering and computation

- [Blender command-line arguments](https://docs.blender.org/manual/en/latest/advanced/command_line/arguments.html): background rendering, Python execution, argument order and Python error exit code. A current development documentation search result was available during preparation; use the manual for the installed stable version.
- [Blender dependency graph API](https://docs.blender.org/api/current/bpy.types.Depsgraph.html): intended reference for evaluated animation/geometry. Direct retrieval was blocked during preparation; Claude must verify API calls against the installed Blender documentation.
- [Blender object utilities](https://docs.blender.org/api/current/bpy_extras.object_utils.html): intended reference for world-to-camera projection. Direct retrieval was blocked; projection semantics must be confirmed with tests, not assumed from this link.
- [FFmpeg documentation](https://ffmpeg.org/ffmpeg.html) and [ffprobe documentation](https://ffmpeg.org/ffprobe.html): encode image sequences and inspect decoded stream/frame timing. Verify installed options before constructing commands.
- [PyTorch MPS backend](https://docs.pytorch.org/docs/stable/notes/mps.html): candidate Apple GPU backend; support of the selected animal-pose framework remains to be tested.
- [NVIDIA Omniverse technical requirements](https://docs.omniverse.nvidia.com/dev-guide/latest/common/technical-requirements.html): check supported operating systems, GPUs, drivers and component licenses before choosing a phase 2 renderer. No assumption of native Mac RTX rendering.

## Databricks — reviewed official pages

- [Unity Catalog volumes](https://docs.databricks.com/aws/en/volumes/): governed file storage, managed/external options and their access/lifecycle differences. Store videos/artifacts as files and structured records in tables.
- [Model lifecycle in Unity Catalog](https://docs.databricks.com/aws/en/machine-learning/manage-model-lifecycle): MLflow-compatible governed model registry; actual workspace/compute requirements must be checked.
- [Declarative Automation Bundles](https://docs.databricks.com/aws/en/dev-tools/bundles): versioned job/app/platform-resource definitions and deployment workflow.
- [Databricks Apps](https://docs.databricks.com/aws/en/dev-tools/databricks-apps/): candidate integrated app hosting with platform authentication/services. Availability, limits, authorization details and costs must be checked in the target workspace.

AWS URLs provide concrete references; the target provider is unknown. Select the corresponding Azure or GCP documentation when appropriate. This package contains a provider-neutral design rather than an untested deployment configuration.

## Scientific motivation and data candidate

- [Järemo Lawin et al., 2023: smartphone versus optical motion capture](https://doi.org/10.3390/ani13030390): supports technical feasibility for the studied system, not accuracy of our implementation.
- [Rhodin et al., 2017: asymmetry in horses perceived free from lameness](https://doi.org/10.1371/journal.pone.0176253): reason to separate movement asymmetry from clinical disease labels.
- [Hardeman et al., 2019: variation in objective gait parameters](https://doi.org/10.1111/evj.13075): motivates repeated-acquisition and biological variation analysis.
- [PFERD publication](https://doi.org/10.1038/s41597-024-03312-1), [repository](https://github.com/Celiali/PFERD), and [dataset](https://doi.org/10.7910/DVN/2EXONE): paired equine video/motion-capture candidate. Dataset terms remain unverified in this project; article, code, model and dataset licenses are separate.

No parameter distribution in the supplied pilot config is asserted to have been estimated from these studies. A later parameter-provenance table must identify each empirical source, variable definition, units, population, estimate, uncertainty and allowed use. Unverified or illustrative parameters stay labeled as assumptions.
