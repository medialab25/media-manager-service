"""
Folder merging service.
"""
import os
import shutil
from pathlib import Path
from typing import List, Set
from .config import Settings

settings = Settings()

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

    def _get_quality_index(self, quality: str) -> int:
        """Get index of quality in quality_list."""
        try:
            return settings.merge["quality_list"].index(quality.lower())
        except ValueError:
            return -1

    def _get_current_quality(self, target_path: Path) -> str:
        """Get current quality from quality marker files."""
        for q in settings.merge["quality_list"]:
            if (target_path / f".quality-{q}").exists():
                return q
        return None

    def _cleanup_quality_markers(self, target_path: Path) -> None:
        """Remove all quality marker files from target path."""
        for q in settings.merge["quality_list"]:
            marker = target_path / f".quality-{q}"
            if marker.exists():
                marker.unlink()

    def _get_best_available_quality(self, target_path: Path) -> str:
        """Get best available quality from input folders."""
        best_quality = None
        best_idx = len(settings.merge["quality_list"])
        
        for input_folder in self.input_folders:
            if not input_folder.exists():
                continue
                
            quality = input_folder.name.split('-')[-1] if '-' in input_folder.name else ''
            if quality.lower() not in settings.merge["quality_list"]:
                continue
                
            if (input_folder / target_path.name).exists():
                idx = self._get_quality_index(quality)
                if idx < best_idx:
                    best_idx = idx
                    best_quality = quality
                    
        return best_quality

    def _update_quality(self, target_path: Path, new_quality: str) -> None:
        """Update quality marker for a directory."""
        self._cleanup_quality_markers(target_path)
        (target_path / f".quality-{new_quality.lower()}").touch()

    def merge(self) -> None:
        """Merge input folders into output using hard links."""
        self.output_folder.mkdir(parents=True, exist_ok=True)

        # Process each input folder
        for input_folder in self.input_folders:
            if not input_folder.exists():
                continue

            quality = input_folder.name.split('-')[-1] if '-' in input_folder.name else ''
            if quality.lower() not in settings.merge["quality_list"]:
                continue

            for item in input_folder.iterdir():
                if not item.is_dir():
                    continue

                target_path = self.output_folder / item.name
                target_path.mkdir(parents=True, exist_ok=True)

                current_quality = self._get_current_quality(target_path)
                if current_quality:
                    current_idx = self._get_quality_index(current_quality)
                    new_idx = self._get_quality_index(quality)
                    if new_idx >= current_idx:
                        continue

                self._update_quality(target_path, quality)

        # Check for removed higher quality folders
        for item in self.output_folder.iterdir():
            if not item.is_dir():
                continue

            current_quality = self._get_current_quality(item)
            if not current_quality:
                continue

            # Check if current quality still exists
            found = False
            for input_folder in self.input_folders:
                if not input_folder.exists():
                    continue
                    
                quality = input_folder.name.split('-')[-1] if '-' in input_folder.name else ''
                if quality.lower() == current_quality and (input_folder / item.name).exists():
                    found = True
                    break

            if not found:
                best_quality = self._get_best_available_quality(item)
                if best_quality:
                    self._update_quality(item, best_quality)

