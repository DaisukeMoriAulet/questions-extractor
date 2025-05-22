from pathlib import Path

# Get the absolute path to the directory where this paths.py file is located.
# e.g., /Users/daisukemori/aulet/questions-extractor/utils
_CURRENT_FILE_DIR = Path(__file__).resolve().parent

# Assume the project root is one level up from the 'utils' directory.
# e.g., /Users/daisukemori/aulet/questions-extractor
PROJECT_ROOT = _CURRENT_FILE_DIR.parent

# Define INPUT_DIR relative to the PROJECT_ROOT.
# This makes it easy to reference from anywhere in your project.
INPUT_DIR = PROJECT_ROOT / "input"  # Or "input_data", "data", etc.

# You could also add other common paths here in the future:
# OUTPUT_DIR = PROJECT_ROOT / "output"
# TMP_DIR = PROJECT_ROOT / "tmp" # You recently added 'tmp/' to .gitignore

# To make it runnable for quick checks (optional)
if __name__ == '__main__':
    print(f"Project Root: {PROJECT_ROOT}")
    print(f"Input Directory: {INPUT_DIR}")

    # You might want to ensure the input directory exists when the app starts,
    # or handle its absence gracefully. For now, this just defines the path.
    # Example: INPUT_DIR.mkdir(parents=True, exist_ok=True)