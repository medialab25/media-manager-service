"""
Folder merging service.
"""
import os
import shutil
from pathlib import Path
from typing import List, Set


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

    def _create_hard_links(self, source: Path, target: Path) -> None:
        """Recursively create hard links for a folder tree.

        Args:
            source: Source directory path
            target: Target directory path
        """
        target.mkdir(parents=True, exist_ok=True)

        for item in source.iterdir():
            source_path = source / item.name
            target_path = target / item.name

            if source_path.is_file():
                if not target_path.exists():
                    os.link(source_path, target_path)
            elif source_path.is_dir():
                self._create_hard_links(source_path, target_path)

    def _get_source_paths(self) -> Set[Path]:
        """Get all paths from source folders."""
        source_paths = set()
        for input_folder in self.input_folders:
            if not input_folder.exists():
                continue
            for root, _, _ in os.walk(input_folder):
                source_paths.add(Path(root).relative_to(input_folder))
        return source_paths

    def _cleanup_extra_folders(self) -> None:
        """Remove folders in target that aren't in source folders."""
        source_paths = self._get_source_paths()

        for root, dirs, _ in os.walk(self.output_folder, topdown=False):
            rel_path = Path(root).relative_to(self.output_folder)
            if rel_path not in source_paths:
                shutil.rmtree(root)

    def merge(self) -> None:
        """Merge input folders into output using hard links."""
        # Create output structure
        self.output_folder.mkdir(parents=True, exist_ok=True)

        # Process each input folder in priority order
        for input_folder in self.input_folders:
            if not input_folder.exists():
                continue
            self._create_hard_links(input_folder, self.output_folder)

        # Cleanup extra folders
        self._cleanup_extra_folders()
