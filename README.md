# Equine gait methods sandbox

Phase 1 starter: a research protocol and runnable synthetic measurement experiment. This is **not a clinical lameness detector**, an implemented pose estimator, or a production deployment. No animal data or pretrained weights are included.

Read [the protocol](docs/phase-1.md) for the question, evidence, licensing gate, experimental design, architecture, and phase 2 handoff.

For Claude Code + Blender data generation and the detailed Databricks solution design, start with the [handoff package](handoff/README.md). It contains an execution prompt, generation specification, data contract, pilot config and phase 2 architecture. These specify the next implementation; the Blender renderer is not implemented in this starter.

## Run on a Mac or Linux with Python 3.11+

```sh
python -m unittest discover -s tests -v
python experiment.py --output results.json
python app.py
```

Open http://127.0.0.1:8000. The local app changes noise and camera roll and plots a generated signal against its known reference. Stop with Ctrl-C. It uses only Python's standard library. It has no video upload, inference, authentication, or external service. Keep it bound to loopback.

`results.json` records parameters, seed, errors, exclusions, and software provenance. Numerical units are **synthetic scene units**, never calibrated millimetres. Ground-truth stride boundaries are supplied by the simulator: real stride detection remains unimplemented. An ideal camera roll mixes vertical movement and horizontal drift; this is only one component of camera sensitivity, not a full optical simulation.

The initial signal parameters are illustrative engineering choices, not estimated biological distributions. Literature motivates the metrics and nuisance factors. Future empirical parameter fitting must record sources and permissions separately.

## Transfer

Copy this directory excluding caches to the next environment. Include a Git commit/hash manifest, dependency lock once external packages are introduced, source/license inventory, dataset hashes, model cards, experiment configuration, and reports. Never assume copying to an employer's environment is permitted by a research-only dataset license. No Databricks or NVIDIA services are provisioned here.
