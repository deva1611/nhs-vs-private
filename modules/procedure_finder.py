"""
procedure_finder.py
-------------------
Takes what the user typed (e.g. "knee" or "mri scan")
and finds the best matching procedure from our database.
"""

import json        # json lets us read .json files
import os          # os helps us find file paths


def load_procedures():
    """
    Reads the procedures.json file and returns all procedures as a list.
    """
    # Find the path to procedures.json relative to this file
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    json_path = os.path.join(base_dir, "data", "procedures.json")

    with open(json_path, "r") as f:
        data = json.load(f)   # Convert JSON file into a Python dictionary

    return data["procedures"]  # Return just the list of procedures


def find_procedure(user_input):
    """
    Takes user input like "knee" or "mri scan"
    Returns the best matching procedure dict, or None if no match.

    How it works:
    - Converts user input to lowercase
    - Checks if any keyword for each procedure is in the user's input
    - Returns the first match found
    """
    user_input = user_input.strip().lower()
    procedures = load_procedures()

    for procedure in procedures:
        for keyword in procedure["keywords"]:
            if keyword in user_input or user_input in keyword:
                return procedure  # Return as soon as we find a match

    return None  # No match found


def list_all_procedures():
    """
    Returns a simple list of all procedure names.
    Used to show the user what's available.
    """
    procedures = load_procedures()
    return [p["name"] for p in procedures]


# ── Quick test ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("=== All available procedures ===")
    for name in list_all_procedures():
        print(f"  - {name}")

    print("\n=== Testing procedure finder ===")
    tests = ["knee", "mri scan", "hip replacement", "eye", "something random"]
    for t in tests:
        result = find_procedure(t)
        if result:
            print(f"  '{t}' → Found: {result['name']}")
        else:
            print(f"  '{t}' → No match found")
