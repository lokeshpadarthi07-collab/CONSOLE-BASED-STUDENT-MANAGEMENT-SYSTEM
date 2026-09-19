"""
File handling utilities for JSON persistence and CSV export operations.
"""

import csv
import json
import os
from pathlib import Path
from typing import List, Dict, Any


class FileHandler:
    """Handles reading and writing student data to JSON and CSV files safely."""

    @staticmethod
    def ensure_directory_exists(file_path: str | Path) -> None:
        """Ensure that the parent directory for a given file path exists."""
        directory = os.path.dirname(file_path)
        if directory:
            os.makedirs(directory, exist_ok=True)

    @classmethod
    def save_json(cls, file_path: str | Path, data: List[Dict[str, Any]]) -> bool:
        """
        Save student records to a JSON file safely using atomic file replacement
        to prevent accidental data loss or corruption during writing.

        Args:
            file_path: Path to target JSON file.
            data: List of dictionary representations of students.

        Returns:
            bool: True if saving succeeded.

        Raises:
            PermissionError: If write permission is denied.
            IOError: If an error occurs during writing.
        """
        cls.ensure_directory_exists(file_path)
        temp_file_path = f"{file_path}.tmp"

        try:
            # Write to temporary file first using context manager
            with open(temp_file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

            # Atomically replace destination file
            os.replace(temp_file_path, file_path)
            return True
        except PermissionError as pe:
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)
            raise PermissionError(f"Permission denied when saving to '{file_path}': {pe}")
        except Exception as e:
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)
            raise IOError(f"Failed to save JSON data to '{file_path}': {e}")

    @classmethod
    def load_json(cls, file_path: str | Path) -> List[Dict[str, Any]]:
        """
        Load student records from a JSON file.

        Args:
            file_path: Path to target JSON file.

        Returns:
            List[Dict[str, Any]]: Loaded list of student dictionaries. Returns empty list if file doesn't exist.

        Raises:
            json.JSONDecodeError: If JSON structure is corrupted or invalid.
            PermissionError: If read permission is denied.
            IOError: For other read errors.
        """
        if not os.path.exists(file_path):
            return []

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if not isinstance(data, list):
                    raise ValueError("JSON file content is not a valid list of student records.")
                return data
        except FileNotFoundError:
            return []
        except json.JSONDecodeError as jde:
            raise json.JSONDecodeError(
                msg=f"Corrupted or invalid JSON data in file '{file_path}': {jde.msg}",
                doc=jde.doc,
                pos=jde.pos,
            )
        except PermissionError as pe:
            raise PermissionError(f"Permission denied when reading '{file_path}': {pe}")
        except Exception as e:
            raise IOError(f"Failed to load JSON file '{file_path}': {e}")

    @classmethod
    def export_csv(
        cls,
        file_path: str | Path,
        fieldnames: List[str],
        data: List[Dict[str, Any]],
    ) -> bool:
        """
        Export student records to a CSV file.

        Args:
            file_path: Output CSV file path.
            fieldnames: Headers/columns for CSV file.
            data: List of student dictionaries.

        Returns:
            bool: True if export was successful.

        Raises:
            PermissionError: If write permission is denied.
            IOError: For write errors.
        """
        cls.ensure_directory_exists(file_path)

        try:
            with open(file_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(data)
            return True
        except PermissionError as pe:
            raise PermissionError(f"Permission denied when writing to CSV file '{file_path}': {pe}")
        except Exception as e:
            raise IOError(f"Failed to export CSV file '{file_path}': {e}")
