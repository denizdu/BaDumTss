# Audio asset policy

BaDumTss does not store reference songs or third-party sample packs in Git.
Keeping audio outside the repository avoids copyright ambiguity, prevents large
history growth, and lets each user choose their own licensed material.

## Local directory convention

- `sample/raw/`: full reference tracks used for analysis and recreation.
- `sample/drums/`: local drum one-shots used by REAPER.
- `output/` and `export/`: generated analysis, MIDI, projects, and renders.

These directories are ignored. Removing an asset from Git does not grant or
change permission to use it. Process only material you own or are authorized to
use.

## REAPER configuration

Set `BADUMTSS_KICK_SAMPLE`, `BADUMTSS_SNARE_SAMPLE`, and
`BADUMTSS_HIHAT_SAMPLE` to absolute paths on the local machine. The REAPER
script reports missing configuration and skips unavailable audio events instead
of depending on bundled vendor filenames.

## Manifests

Copy `assets.example.json` to an ignored local manifest when reproducibility is
needed. Store metadata, checksums, and acquisition instructions in Git only when
the source and license allow redistribution of that metadata. Never put access
tokens, browser cookies, signed download links, or the media bytes in a
manifest.

Tests should generate short synthetic fixtures at runtime. A real song may be
used for an optional local end-to-end acceptance test, but it must not be
required by the automated test suite.
