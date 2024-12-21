import json
import os
import sys
import re


def sanitize_for_json(data):
    """
    Sanitize data for JSON compatibility.
    """
    if isinstance(data, dict):
        return {key: sanitize_for_json(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [sanitize_for_json(item) for item in data]
    elif isinstance(data, (float, int, str)) or data is None:
        return data
    elif hasattr(data, "tolist"):  # Handle numpy arrays or similar
        return data.tolist()
    else:
        return str(data)  # Fallback to string representation


def validate_json_structure(data):
    """
    Validate JSON structure to ensure compatibility with Lua script.
    """
    for i, item in enumerate(data):
        if not isinstance(item, dict):
            raise ValueError(f"Item at index {i} is not a dictionary: {item}")
        if "tempo" not in item or "energy" not in item or "chroma_mean" not in item:
            raise ValueError(f"Missing required keys in item at index {i}: {item}")


def process_combinations(input_path, output_path):
    """
    Process track combinations, sanitize data, and validate the structure.
    """
    try:
        with open(input_path, "r", encoding="utf-8") as infile:
            data = json.load(infile)

        # Sanitize and validate data
        sanitized_data = sanitize_for_json(data)
        validate_json_structure(sanitized_data)

        with open(output_path, "w", encoding="utf-8") as outfile:
            json.dump(sanitized_data, outfile, ensure_ascii=False, indent=4)

        print(f"Cleaned and validated JSON saved to {output_path}")

    except Exception as e:
        print(f"Error processing combinations: {e}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python track_combinations.py <input_json_path> <output_json_path>")
        sys.exit(1)

    input_json_path = sys.argv[1]
    output_json_path = sys.argv[2]

    if not os.path.exists(input_json_path):
        print(f"Input JSON file not found: {input_json_path}")
        sys.exit(1)

    process_combinations(input_json_path, output_json_path)
