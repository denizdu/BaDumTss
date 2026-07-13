# Model Development Guide

## Data preparation

Extract consistent features such as tempo, chroma, MFCCs, spectral centroid, roll-off, loudness, rhythm stability, and drum-event density. Validate the source labels and split data by song or artist to reduce leakage.

## Baselines

Start with transparent baselines such as nearest-neighbor retrieval, logistic regression, or a random forest. The current tempo-based Rock/Jazz label is only a placeholder and must not be treated as a trained recommendation system.

## Evaluation

Use task-specific metrics and retain a human listening stage. Report dataset size, class balance, split strategy, and confidence. Compare every learned model with a simple deterministic baseline.

## Generation

Generate an intermediate symbolic representation before rendering audio. MIDI makes timing, pitch, velocity, and track structure easy to inspect in a DAW. More complex sequence models should be considered only after the dataset and evaluation procedure are reliable.
