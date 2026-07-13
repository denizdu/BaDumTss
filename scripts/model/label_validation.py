from collections import Counter


def validate_training_labels(labels, minimum_per_class=2):
    """Validate verified labels before a stratified train/test split."""
    counts = Counter(labels)
    if not counts:
        raise ValueError(
            "No verified drum-kit labels matched the analysis records. "
            "Add labels to drum_kit_labels.json before training."
        )
    if len(counts) < 2:
        raise ValueError("Training requires at least two distinct drum-kit labels")

    undersized = sorted(
        label for label, count in counts.items() if count < minimum_per_class
    )
    if undersized:
        raise ValueError(
            "Each drum-kit label requires at least "
            f"{minimum_per_class} examples; insufficient labels: {', '.join(undersized)}"
        )
