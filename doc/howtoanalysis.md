# Audio Analysis Guide

## Core measurements

- **Tempo (BPM):** estimated pulse rate. Half-time and double-time ambiguity must be considered.
- **Beat grid:** timestamps of estimated beat positions.
- **Key:** likely tonic and mode derived from harmonic chroma. Always include confidence.
- **Loudness and dynamics:** overall level and variation over time.
- **Chroma:** energy grouped into the twelve pitch classes.
- **MFCCs:** compact descriptors of spectral shape and timbre.
- **Spectral centroid:** an approximate measure of brightness.
- **Spectral roll-off:** the frequency below which a selected proportion of energy lies.
- **Zero-crossing rate:** a rough indicator of noisiness or transient content.
- **Harmonic and percussive components:** separated signals that improve tonal and rhythm analysis.

## Interpretation limits

These measurements describe aspects of a recording but do not contain enough information for an exact recreation. A faithful reconstruction also requires arrangement, instrument identity, articulation, sound design, effects, automation, mixing, and often separated stems.

Do not interpret a single feature in isolation. High spectral centroid may indicate brightness, cymbals, distortion, or noise. A key estimate can be unreliable for atonal, modulating, or strongly percussive material. Tempo confidence should reflect ambiguous pulse levels.

## Recommended pipeline

1. Decode the source once and share the waveform with all analysis modules.
2. Validate sample rate, duration, channels, and numerical values.
3. Separate harmonic and percussive components when useful.
4. Extract time-based, tonal, spectral, and rhythm features.
5. Detect events with timestamps and confidence values.
6. Store structured results using a versioned schema.
7. Review uncertain results before generating MIDI or a DAW project.

## Reconstruction variables

For a practical recreation workflow, capture tempo maps, time signatures, sections, chords, melody, bass, drum events, instrumentation, note timing, velocity, articulation, spatial effects, dynamics, and mix relationships. Use stem separation or manual annotation where full-mix analysis cannot recover these variables reliably.
