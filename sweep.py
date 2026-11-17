"""Run the nine-condition synthetic sensitivity experiment: python sweep.py."""
import csv
from pathlib import Path
import statistics
from experiment import evaluate


def main():
    rows = []
    for noise in (0, 0.5, 2):
        for roll in (0, 2, 10):
            runs = [evaluate(noise=noise, roll=roll, seed=s) for s in range(30)]
            rows.append(dict(noise=noise, roll_degrees=roll, seeds=30,
                             min_diff_mae=statistics.mean(r['metrics']['min_diff']['mae'] for r in runs),
                             max_diff_mae=statistics.mean(r['metrics']['max_diff']['mae'] for r in runs)))
    destination = Path(__file__).parent / 'docs' / 'synthetic-sweep.csv'
    with destination.open('w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print(destination)


if __name__ == '__main__':
    main()
