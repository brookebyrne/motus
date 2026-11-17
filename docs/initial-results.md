# First engineering experiment

Executed in Linux on Python 3.12.14, 16 November 2026. Reproduce with `python sweep.py` from the project directory. Raw summaries: [synthetic-sweep.csv](synthetic-sweep.csv).

Nine noise/roll conditions, 30 seeds each, 20 strides per run. Seeds change noise only, not independent horses or biological motion. Repeated noiseless runs are identical. Metrics use supplied simulated stride boundaries and arbitrary scene units.

| Noise SD | Roll | Mean stride MaxDiff absolute error |
|---|---|---|
| 0 | 0° | 0.000 |
| 0 | 2° | 1.030 |
| 0 | 10° | 5.129 |
| 0.5 | 0° | 0.519 |
| 2 | 0° | 1.733 |

The identity case recovers the reference. Roll mixes horizontal drift into apparent vertical motion, changing asymmetry estimates even without tracking noise. This motivates a camera-geometry experiment and compensation baseline. It does not estimate the size of this effect in real horses. Noise interacts with extrema selection; errors need not increase monotonically for every combined condition.

Eight numerical unit tests passed. Direct HTML rendering and parameter display checks passed, and a standalone viewer snapshot is in `viewer-preview.html`. Socket creation is restricted in this execution sandbox, so the live HTTP server was not smoke-tested here. Mac hardware, browser appearance, hosted CI, video decoding, inference and deployment remain untested. Run the server locally using the README instructions.
