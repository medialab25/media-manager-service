"""
Folder merging service.
"""
import os
from pathlib import Path
from typing import List


class FolderMerger:
    """Handles merging folders with priority-based hard links."""

    def __init__(self, input_folders: List[str], output_folder: str):
        """Initialize merger with input and output paths.

        Args:
            input_folders: List of input folder paths in priority order
            output_folder: Path to output folder for merged content
        """
        self.input_folders = [Path(f) for f in input_folders]
        self.output_folder = Path(output_folder)

    def merge(self) -> None:
        """Merge input folders into output using hard links."""
        # Create output structure
        self.output_folder.mkdir(parents=True, exist_ok=True)

        # Process each input folder in priority order
        for input_folder in self.input_folders:
            if not input_folder.exists():
                continue

            # Walk through input folder
            for root, _, files in os.walk(input_folder):
                rel_path = Path(root).relative_to(input_folder)
                output_path = self.output_folder / rel_path
                output_path.mkdir(parents=True, exist_ok=True)

                # Create hard links for files
                for file in files:
                    source = Path(root) / file
                    target = output_path / file

                    # Skip if file exists (higher priority)
                    if target.exists():
                        continue

                    try:
                        os.link(source, target)
                    except OSError as e:
                        # Handle hard link creation errors
                        print(f"Error creating hard link: {e}")
