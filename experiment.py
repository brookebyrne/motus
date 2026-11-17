"""Deterministic engineering simulation; no clinical or biological validation."""
import argparse
import hashlib
import json
import math
from pathlib import Path
import platform
import random
import statistics


def simulate(noise=0.5, roll=0.0, seed=17, strides=20, samples=60,
             asymmetry=4.0, dropout=0.0):
    if not (0 <= noise <= 20 and -30 <= roll <= 30):
        raise ValueError("noise must be 0–20 and roll -30–30")
    if not (2 <= strides <= 1000 and 20 <= samples <= 1000):
        raise ValueError("invalid simulation size")
    if not (0 <= dropout < 1 and math.isfinite(asymmetry)):
        raise ValueError("invalid dropout or asymmetry")
    rng = random.Random(seed)
    truth, observed = [], []
    theta = math.radians(roll)
    for i in range(strides * samples):
        phase = 2 * math.pi * (i % samples) / samples
        # Two vertical oscillations/stride plus an alternating component.
        y = 20 * math.cos(2 * phase) + asymmetry / 2 * math.cos(phase)
        x = 30 * i / samples
        measurement = y * math.cos(theta) + x * math.sin(theta) + rng.gauss(0, noise)
        truth.append(y)
        observed.append(None if rng.random() < dropout else measurement)
    return truth, observed


def stride_metrics(signal, samples):
    """Fixed simulated half-strides. Signed first-half minus second-half extrema.

    Drop incomplete strides rather than silently imputing occlusion. These
    boundaries must be independently estimated and validated for real video.
    """
    output = []
    for start in range(0, len(signal) - samples + 1, samples):
        stride = signal[start:start + samples]
        if any(v is None or not math.isfinite(v) for v in stride):
            continue
        a, b = stride[:samples // 2], stride[samples // 2:]
        output.append({"stride": start // samples,
                       "min_diff": min(a) - min(b),
                       "max_diff": max(a) - max(b)})
    return output


def evaluate(noise=0.5, roll=0.0, seed=17, dropout=0.0):
    config = dict(noise=noise, roll=roll, seed=seed, dropout=dropout,
                  strides=20, samples=60, asymmetry=4.0)
    truth, observed = simulate(**config)
    reference = {m["stride"]: m for m in stride_metrics(truth, config["samples"])}
    measured = stride_metrics(observed, config["samples"])
    metrics = {}
    for name in ("min_diff", "max_diff"):
        errors = [m[name] - reference[m["stride"]][name] for m in measured]
        metrics[name] = {"bias": statistics.mean(errors) if errors else None,
                         "mae": statistics.mean(map(abs, errors)) if errors else None,
                         "error_sd": statistics.stdev(errors) if len(errors) > 1 else None}
    return {"status": "synthetic_only" if measured else "insufficient_data",
            "units": "synthetic_scene_units", "config": config,
            "valid_strides": len(measured), "excluded_strides": 20 - len(measured),
            "metrics": metrics, "truth": truth, "observed": observed,
            "provenance": {"python": platform.python_version(),
                           "source_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                           "reference": "analytical simulator; same supplied stride boundaries"}}


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--noise", type=float, default=0.5)
    parser.add_argument("--roll", type=float, default=0)
    parser.add_argument("--seed", type=int, default=17)
    parser.add_argument("--dropout", type=float, default=0)
    parser.add_argument("--output", default="results.json")
    args = parser.parse_args()
    result = evaluate(args.noise, args.roll, args.seed, args.dropout)
    Path(args.output).write_text(json.dumps(result, indent=2, allow_nan=False) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k not in ("truth", "observed")}, indent=2))
