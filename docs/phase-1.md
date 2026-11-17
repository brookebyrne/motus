# Phase 1: scientific protocol and engineering plan

Prepared 16 November 2026. Status: focused initial literature review, proposed protocol, and tested synthetic signal starter. Real-video extraction, independent reference evaluation, Mac hardware benchmarks, and deployment have not been completed. No research permission has been obtained. This is a feasibility study, not a clinical detector.

## 1. Observation and research question

Low-cost equine video analysis is plausible and has published precedents. The useful unanswered question for this project is where a reproducible implementation succeeds or fails, rather than whether AI can detect lameness in principle.

**Primary question:** In straight-line trot, how closely can a Python markerless pipeline estimate selected head and pelvis vertical movement asymmetry measures against synchronized reference trajectories, and how do camera geometry and image quality change agreement and usable-data coverage?

Separate three claims: (a) mathematical measurement recovery on known synthetic signals; (b) landmark localization and trajectory agreement on licensed real data; (c) clinical validity. Phase 1 addresses (a), and attempts (b) if usable licensed data exist. It cannot establish (c).

Published population summaries can inform plausible simulation settings and interpretation. They cannot serve as paired ground truth for a particular video. Manual annotation validates visible 2D landmarks; it does not establish true 3D displacement, pain, or a diagnosis.

## 2. Focused literature review

This is an initial narrative review, not an exhaustive systematic review or meta-analysis. Searches used combinations of equine gait asymmetry, objective lameness, smartphone markerless validation, horse pose dataset, repeatability, and camera viewpoint. Public publisher pages, PubMed/PMC search records, official repositories, and vendor documentation were consulted. Some full texts and dataset terms were blocked. Do not treat search abstracts as full risk-of-bias appraisal.

| Source | Evidence and relevance | Implication for this study |
|---|---|---|
| Rhodin et al., 2017, PLOS ONE, DOI [10.1371/journal.pone.0176253](https://doi.org/10.1371/journal.pone.0176253) | Owner-perceived soundness did not imply symmetric movement in a riding-horse cohort. | Do not equate asymmetry with disease or use owner reports as diagnostic labels. |
| Rhodin et al., 2016, EVJ, DOI [10.1111/evj.12446](https://doi.org/10.1111/evj.12446) | Circular exercise changes head/pelvis symmetry even in horses symmetric on the straight. | Restrict the first experiment to straight-line trot; analyze circles separately later. |
| Hardeman et al., 2019, EVJ, DOI [10.1111/evj.13075](https://doi.org/10.1111/evj.13075) | Evaluates variation across repeated measurements, paths, and days. | Distinguish algorithm repeatability from biological and acquisition variation. |
| Järemo Lawin et al., 2023, Animals, DOI [10.3390/ani13030390](https://doi.org/10.3390/ani13030390) | Paired smartphone and optical-motion-capture study supports the technical premise. | Its results belong to that specific system and protocol; our implementation must earn its own agreement estimates. Commercial affiliations require noting in appraisal. |
| [Comparing IMUs to markerless video in Quarter Horses, 2023](https://pubmed.ncbi.nlm.nih.gov/37896509/) | Field comparison of different measurement systems in a specific horse population. | Reference systems and populations are not interchangeable; document acquisition and metric definitions. |
| Li et al., 2024, Scientific Data, DOI [10.1038/s41597-024-03312-1](https://doi.org/10.1038/s41597-024-03312-1) | PFERD supplies synchronized multi-view video, dense skin-marker motion, and camera information from five horses. | Useful for paired geometry experiments, but five horses limit generalization. Visible markers and laboratory acquisition differ from consumer field video. |
| [Reliability, agreement and variability under field conditions](https://pubmed.ncbi.nlm.nih.gov/41185610/) | Compares automated 2D landmarks with manual annotation. | Useful annotation baseline; annotation is a different reference from independent 3D capture. Record commercial conflicts. |
| [Handheld smartphone validation against optical capture](https://doi.org/10.1002/evj.70149) | Recent work explicitly evaluates groundline estimation and optical-capture agreement. | Ground/camera compensation is a separate measurable component; extracting raw image y is insufficient. |

Before preregistration, expand backwards/forwards citation searching, include foundational inertial-sensor validation and subjective-assessment reliability work, retrieve full texts, and record exact search strings, dates, inclusion decisions, populations, sample sizes, camera setups, reference standards, exclusions, uncertainty, funding, and limitations in an evidence CSV. Include negative findings and reject irrelevant human-gait extrapolation. A veterinary supervisor should review anatomical definitions and interpretation.

## 3. Hypotheses, outcomes, and decision rules

H1: Under the prespecified acquisition envelope, video-derived trial asymmetry agrees with synchronized reference within an engineering tolerance fixed before the held-out evaluation.

H2: Increasing obliquity, roll, occlusion, blur, or reducing effective frame rate increases error and/or reduces retained coverage. Treat each nuisance factor as an experiment, not an undocumented augmentation.

H3: Repeated independent acquisitions yield greater variation than rerunning the deterministic pipeline on the same file. Repeated identical computation only tests reproducibility.

Primary endpoints: signed bias and MAE of trial-mean MinDiff and MaxDiff for each landmark, with horse-level uncertainty. Define coordinate axes, event ordering, units, filtering, and positive direction before evaluation. Do not map positive/negative values to a limb without validated event timing and orientation.

Secondary endpoints: stride duration error, normalized landmark error, accepted-stride coverage, failures by condition, processing time, memory, and inter/intra-annotator agreement. Normalized image-space displacement is a different endpoint from calibrated physical displacement. A known object or a ground-plane homography alone does not recover arbitrary out-of-plane vertical millimetres.

Gate A (software): noiseless simulator reproduces reference; hand-computed extrema, unit/coordinate transformations, missing-data policy, and repeatability checks pass. This is an engineering gate only.

Gate B (data): archive explicit dataset/file/model terms and confirm permitted use, including transfer to a work environment; confirm landmarks, stride events, timing, calibration, and enough trot are available. Otherwise stop the real-data claim and document the access limitation.

Gate C (real-data feasibility): set a smallest scientifically useful difference and acceptable error with a veterinary/biomechanics adviser, checking reference uncertainty. If no defensible physical tolerance is available, preregister a descriptive estimation study rather than invent a clinical pass threshold. Set coverage and latency targets separately as product requirements. Do not tune any target after seeing held-out performance.

## 4. Data and licensing

**Preferred candidate:** PFERD, [dataset DOI 10.7910/DVN/2EXONE](https://doi.org/10.7910/DVN/2EXONE), [official repository](https://github.com/Celiali/PFERD). Dataset access terms could not be read through the Dataverse verification page during this review, so its license is **unverified here**. The article's CC BY license does not automatically license videos, code, or hSMAL assets. The repository explicitly assigns its code CC BY-NC-SA 4.0 and directs users to separate dataset and model terms. Do not copy that code into an intended proprietary product without resolving its conditions. Prefer independently written analysis and minimal data readers.

No horse dataset has been approved for ingestion in this starter. Public visibility, a download button, or a model hub label is not sufficient proof of underlying video rights. Do not use scraped social-media footage. Inspect a small permitted demo before planning a large download; confirm trotting sequences, subject IDs, marker definitions and reference quality. Skin markers are reference measurements with soft-tissue and visibility errors, not error-free bone motion. Ensure visible markers are not giving the pose estimator an artificial shortcut.

Maintain a manifest with dataset version, original URL/DOI, retrieval date, exact terms snapshot/hash, attribution, permitted purpose, redistribution/derivative restrictions, employer-environment eligibility, file SHA-256, subject/session/trial/view IDs, frame timestamps, calibration, units, and any preprocessing. Track code, pretrained weights, meshes, textures, motions, and videos separately. Exclude restricted raw data from Git and distribution archives.

Fallback collection: obtain owner and venue permission plus veterinary/institutional advice on applicable ethical review before research collection. Use normal comfortable exercise; do not induce lameness. Define stop rules with the supervising professional. Obtain handler consent, remove identifying metadata, restrict access, and define retention/deletion. Written permission must cover research, annotation, storage, model training if intended, and separately any public demonstration. Synchronized reference collection requires suitable equipment and expertise; unsynchronized published averages are not a substitute.

## 5. Synthetic data: what to generate and what it proves

Start with analytical two-oscillation-per-stride vertical signals plus an alternating component. Vary amplitude, timing, phase, asymmetry, and stride variability independently. Add pixel noise, temporally correlated tracking error, missing segments, frame timing variation, camera movement, and incorrect stride boundaries in later experiments. A perfect sinusoid alone makes the task unrealistically easy.

The included simulator uses illustrative values, not literature-fitted horse distributions. It tests extrema extraction, exclusions, and simple roll mixing. It does not model 3D horse biomechanics, true stance events, perspective, realistic tracker confidence, or a learned pose model. Its extrema differ according to waveform shape; the injected harmonic coefficient is not automatically equal to both MinDiff and MaxDiff. The analytical sampled trajectory is the reference.

Next create a parameter provenance table: parameter, anatomical meaning, units, empirical source, population, estimated distribution, uncertainty, and whether assumed or measured. Only fit biological distributions from licensed source data or reported estimates with adequate definitions. Keep synthetic and empirical datasets and metrics visibly separate.

For 3D, use an independently licensed rigged horse in Blender, with documented animation/mesh rights. A controlled scene can provide exact 3D landmarks, camera parameters, render timestamps, masks, and projected 2D landmarks. Factorially vary azimuth/elevation/roll, distance, focal length, camera height, speed, lighting, background, texture, occlusion, and blur. Use a small fractional design initially. Rendered realism does not validate biological realism or transfer to live horses. Synthetic training improvements must be tested on independent real subjects.

## 6. Experimental procedure

1. Freeze protocol version, endpoints, candidate tolerances, and exclusion rules before held-out evaluation. Preserve an exploratory notebook separately.
2. Audit permitted files and timing; select straight-line trot; record exclusions and missing references before modeling. Preserve original timestamps and videos immutable.
3. Create a blinded double-annotated subset covering views, horses, coat patterns, and occlusions. Record annotation instructions and disagreements. Human raters should not see model output while annotating the reference subset.
4. Baseline: manually annotated 2D head/pelvis trajectories plus a documented signal-processing pipeline. This separates pose errors from metric/geometry errors. Define anatomical points consistently; nose or generic torso keypoints are not automatically poll or sacrum.
5. Add a Python pose adapter using a reviewed animal-pose framework such as DeepLabCut or SLEAP. Verify current framework, weight license, anatomical coverage, and Mac backend support before selection. A generic horse checkpoint may lack precise head/pelvis landmarks; fine-tuning may be necessary. Compare CPU first, then MPS where supported.
6. Estimate stride boundaries from video-visible events; validate separately against independently measured events. Audit smoothing, minimum segment length, interpolation gaps, event swaps and edge effects. Do not filter away true asymmetry.
7. Synchronize reference and video using recorded triggers/timestamps if available. Estimate any residual alignment on development data, constrain permitted shifts, and report alignment uncertainty. Avoid optimizing alignment to minimize test errors.
8. Split by horse, grouping every session, clip, view, augmentation and synthetic derivative with its source. With five horses, consider nested leave-one-horse-out exploration, report every horse, and emphasize wide uncertainty. Never split frames randomly. Keep view generalization distinct from subject generalization.
9. Compare calibrated trajectories and derived trial metrics to independent reference; also report image-space endpoints where physical reconstruction is unsupported. Publish usable-data rates over all eligible trials, not just successful clips.
10. Repeat physical acquisition if permission/equipment permit. Compare within-session, between-day, inter-rater and inter-device variation separately. For paired multiview data vary view while holding motion constant; for field repeats acknowledge changed motion.

Statistical analysis: report horse/trial counts and stride counts distinctly. Use Bland–Altman bias/limits with a method accounting for repeated measurements, plus cluster bootstrap intervals at horse level when sample size permits; naive stride-independent intervals are inappropriate. With very few horses, show individual results and call interval estimates unstable. ICC is optional with its model and agreement definition specified; correlation alone is insufficient. Propagate annotation, calibration, synchronization, and model uncertainty through sensitivity analysis. Keypoint confidence scores are not calibrated error bars. Conduct a pilot to estimate variance, then plan sample size for agreement-interval precision at the horse level; thousands of frames do not replace independent horses.

Bias audit: breed/conformation, age if known, coat/contrast, equipment, handler occlusion, camera hardware, surface, speed, direction, clinical selection and exclusion patterns. Unknown metadata remain unknown. Do not infer subgroup fairness from tiny cells. No lame/sound classification from surrogate asymmetry labels.

## 7. Portable full-stack architecture

| Concern | Phase 1 on MacBook M5 | Phase 2 work environment |
|---|---|---|
| Compute | Native arm64 Python, CPU reference; benchmark PyTorch MPS on chosen packages | CPU or NVIDIA CUDA workers after capability check; batch first |
| Data | Immutable local files plus Parquet tables and DuckDB when dependencies are added | Approved cloud object storage/Unity Catalog Volumes for videos; Delta tables for metadata, keypoints and metrics |
| AI | Versioned pose adapter; independent measurement library; local MLflow tracking | Databricks training/evaluation jobs, MLflow tracking and Unity Catalog model versions |
| Orchestration | Reproducible CLI/configs; small sample fixtures | Databricks Declarative Automation Bundles, jobs, environments, retry and idempotency policies |
| Backend | Starter loopback viewer; next FastAPI with typed job/result contracts | Separate authenticated API and workers; Databricks batch results behind API |
| Frontend | Starter synthetic controls; next React/TypeScript accessible review UI | Same UI, authorized uploads or approved object-store references, role-based access |
| 3D | Blender with licensed assets, optional USD export | Optional Omniverse Kit/Replicator on supported RTX compute |

Databricks runs in the target cloud/workspace; it is not a local Mac application. Its value here is governed data, reproducible jobs, experiment lineage, and a portable deployment definition. Avoid forcing single-video inference into Spark transformations; distribute independent clips/jobs where beneficial and keep large video payloads in object storage. Store keys and timestamps in tables.

Suggested tables: assets(asset_id, source_hash, license_id, subject_id, session_id, trial_id, view_id, fps/timebase, calibration_id); keypoints(asset_id, frame_id, timestamp, landmark, x, y, confidence, model_version); references(reference_id, trial_id, timestamp, landmark, coordinates, units, uncertainty); results(run_id, trial_id, landmark, metric, value, units, exclusions, config_hash). Every derived row points to a run and source version. Keep license records and synthetic scenario metadata first-class.

PyTorch supports Apple GPU acceleration via MPS, but package/operation compatibility must be measured. CUDA, TensorRT and RAPIDS do not run natively on an Apple GPU. Docker on a Mac does not supply CUDA. NVIDIA documents supported Windows/Linux GPU environments for Omniverse rendering; a Mac can be a development or remote client. Omniverse is a platform with component-specific terms, not a blanket open-source product. OpenUSD is an interchange ecosystem, not a biomechanical validation method. Keep Blender/3D optional until it answers a measured scientific need.

Hardware audit to run on the actual Mac: OS, architecture, Python version, RAM, available disk, `torch.backends.mps.is_available()` after installing the selected PyTorch version, video decode correctness, sustained memory/latency on a short permitted clip, and CPU/MPS numerical agreement. This workspace is Linux; it cannot certify the user's M5. A planning preference is 24–32 GB memory and ample external SSD storage, not a measured minimum. Benchmark before buying or downloading full multi-view archives.

## 8. UX, tests, evals, and operations

Research UI workflow: choose a clearly labeled synthetic scenario or licensed clip → inspect acquisition metadata → review landmark overlay and missingness → inspect stride/event traces → view agreement and uncertainty → export provenance and results. Keep reference and model outputs distinguishable. Show processing failures and rejected strides explicitly. Never display a health score or lame/sound traffic light. Avoid millimetre labels without valid calibration and geometry. Include keyboard-accessible controls, readable plots, units, and downloadable tabular data.

Tests: analytical signals, signed coordinate conventions, translation/scaling, missing-data behavior, boundary timing, decode/timestamp integrity, calibration projection, split leakage, deterministic reruns, and schema migrations. Integration: a tiny lawfully redistributable fixture through decode → pose → metrics → export. Evals: independent landmark annotations, paired-reference agreement, horse-level holdouts, nuisance-factor curves, missingness/coverage, and CPU versus accelerated numeric tolerances. End-to-end tests should verify job failure and result provenance as well as the successful UI path.

CI should lint/type-check as dependencies grow, run numerical and integration tests, scan dependencies/secrets, and build versioned artifacts. The starter includes a small Python test matrix for macOS/Linux; hosted CI has not been run. Add dependency locks and multiarchitecture images only after selecting external packages. Local tests do not establish clinical performance.

Before network deployment: authentication/authorization, upload size/duration/type checks, untrusted decoder isolation and time/resource limits, private storage, signed links, encryption, secrets management, audit trails, retention, backups and restore test. Use separate dev/test environments, infrastructure definitions, immutable model/config versions, deployment health checks and rollback. Monitor queue depth, latency, failed decoding, data-quality rejection, keypoint drift and reference-eval regressions. No automatic clinical decisions. No employer account/storage use is assumed authorized merely because the laptop is available.

## 9. Phased execution and deliverables

Indicative 6–8 week sequence, dependent on permissions and mentoring:

1. Week 1: expand and appraise review; choose endpoints; obtain veterinary review; audit Mac and license candidates. Deliver evidence matrix and preregistration draft.
2. Week 2: expand synthetic tests and nuisance sweeps; establish data contracts. Deliver known-answer report and documented assumptions. Starter code provided now covers only the first signal experiment.
3. Weeks 3–4: if data gate passes, ingest a small synchronized subset, annotate, implement baseline and pose adapter, validate timing and geometry. Deliver data card, annotation guide, reproducible pipeline.
4. Weeks 5–6: freeze configuration; run horse-held-out evaluation, sensitivity and repeatability analyses. Deliver per-horse results, failures, uncertainty and honest negative findings.
5. Weeks 7–8: package research UI, run operational checks, prepare demo and phase 2 manifest. Deliver a concise methods report and application portfolio narrative.

Phase 2 entry requires: confirmed employer and data-use permissions; actual OS/GPU/storage/cloud inventory; frozen portable contracts; passing software checks; documented real-data feasibility results or explicit synthetic-only scope; reviewed access/security requirements. Deploy approved Databricks bundles, data paths, job workers and UI into a sandbox, then verify a restore/rollback and repeat a frozen reference experiment. Treat production readiness as an engineering checklist separate from scientific validation.

For the veterinary application, preserve a lab notebook, supervisor feedback, transparent personal contribution versus AI assistance, annotated bibliography, protocol deviations, data/ethics decisions, a short demo, and a two-page methods/results/limitations summary. A failed hypothesis with careful measurement can still be a strong outcome. Never present this starter's synthetic accuracy as results from horses.

## Technical sources

- [PyTorch MPS backend](https://docs.pytorch.org/docs/stable/notes/mps.html): verify installed-version requirements and operation support.
- [NVIDIA Omniverse technical requirements](https://docs.omniverse.nvidia.com/dev-guide/latest/common/technical-requirements.html): inspect component and GPU requirements in the target environment.
- [Databricks model lifecycle in Unity Catalog](https://docs.databricks.com/aws/en/machine-learning/manage-model-lifecycle): governance and model lifecycle design.
- [Databricks Declarative Automation Bundles](https://learn.microsoft.com/en-us/azure/databricks/dev-tools/bundles/): versioned resource/deployment definitions; select matching cloud docs at implementation.

Next concrete milestone: validate the Mac setup and resolve a small paired-data sample's license and anatomical/timing suitability. Until then, proceed with software and simulation work while leaving real-world accuracy unanswered.
