"""Fix newline issues in Python files."""
import glob


def fix_file(filepath):
    """Fix newline issues in a single file."""
    with open(filepath, "r") as f:
        content = f.read().rstrip()
    with open(filepath, "w") as f:
        f.write(content + "\n")


if __name__ == "__main__":
    python_files = glob.glob("src/app/**/*.py", recursive=True)
    for file in python_files:
        fix_file(file)
