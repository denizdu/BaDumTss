# Future Work

## Analysis

- Calibrate drum-classification thresholds against real songs.
- Add section, chord, bass-line, and melody analysis.
- Record confidence for key, tempo, and event classifications.
- Introduce stem separation when full-mix analysis is insufficient.
- Centralize JSON schemas and file I/O helpers.

## Creation

- Fix MIDI delta-time ordering and note-off placement.
- Verify the mapping between seconds, beats, PPQ ticks, and REAPER time.
- Generate separate instrument tracks with explicit channels and velocities.
- Replace direct spectrum-to-EQ mappings with musically meaningful controls.
- Create and save REAPER projects through a tested integration layer.

## Sound design

- Support configurable sample libraries instead of hard-coded paths.
- Add optional swing, velocity variation, fills, and transition effects.
- Use melody contour and harmonic confidence as generation constraints.
- Keep random generation reproducible through explicit seeds.

## Machine learning

- Remove placeholder Rock/Jazz labels.
- Define a real labeled dataset and a leakage-safe evaluation split.
- Compare learned recommendations with deterministic baselines.
- Add human listening and correction to the evaluation workflow.

## Product and engineering

- Provide one command for fetch, analysis, generation, and validation.
- Separate Spotify metadata, YouTube, and local-file input adapters.
- Replace hard-coded machine-specific paths with portable configuration.
- Clean dependencies and resolve librosa/SciPy deprecation warnings.
- Store large audio assets outside normal Git history.
- Document REAPER and `reapy` installation requirements.
