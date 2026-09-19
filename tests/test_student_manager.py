"""
Unit tests for StudentManager service and validation utilities.
"""

import json
import os
import tempfile
import unittest
from pathlib import Path

from models.student import Student
from services.student_manager import StudentManager
from utils.file_handler import FileHandler
from utils.validators import Validator


class TestStudentManager(unittest.TestCase):
    """Test suite covering core StudentManager operations and Validator functions."""

    def setUp(self) -> None:
        """Set up temporary directory and fresh StudentManager instance before each test."""
        self.temp_dir = tempfile.TemporaryDirectory()
        self.json_path = Path(self.temp_dir.name) / "test_students.json"
        self.csv_path = Path(self.temp_dir.name) / "test_students.csv"

        self.manager = StudentManager(
            json_file_path=self.json_path,
            csv_file_path=self.csv_path,
        )

        # Sample test student
        self.sample_student = Student(
            student_id="S999",
            name="Alice Smith",
            age=20,
            email="alice@university.edu",
            phone="+1-555-9999",
            course="Computer Science",
            year="2nd Year",
            department="Engineering",
            gpa=3.9,
        )

    def tearDown(self) -> None:
        """Clean up temporary directory after each test."""
        self.temp_dir.cleanup()

    # ------------------ CRUD Tests ------------------

    def test_add_student_success(self) -> None:
        """Test successfully adding a new student."""
        result = self.manager.add_student(self.sample_student)
        self.assertTrue(result)
        self.assertEqual(self.manager.student_count, 1)

        fetched = self.manager.get_student_by_id("S999")
        self.assertIsNotNone(fetched)
        self.assertEqual(fetched.name, "Alice Smith")

    def test_add_duplicate_student_id_raises_error(self) -> None:
        """Test adding duplicate student ID raises ValueError."""
        self.manager.add_student(self.sample_student)
        duplicate_student = Student(
            student_id="S999",
            name="Bob Brown",
            age=22,
            email="bob@university.edu",
            phone="+1-555-8888",
            course="Physics",
            year="3rd Year",
            department="Science",
            gpa=3.5,
        )
        with self.assertRaises(ValueError) as context:
            self.manager.add_student(duplicate_student)
        self.assertIn("already exists", str(context.exception))

    def test_search_students(self) -> None:
        """Test searching students by ID, Name, Course, Department."""
        self.manager.add_student(self.sample_student)
        student2 = Student(
            student_id="S888",
            name="Bob Builder",
            age=21,
            email="bob@build.com",
            phone="+1-555-1234",
            course="Civil Eng.",
            year="3rd Year",
            department="Construction",
            gpa=3.2,
        )
        self.manager.add_student(student2)

        # Search by ID
        res_id = self.manager.search_students("S999", search_by="id")
        self.assertEqual(len(res_id), 1)
        self.assertEqual(res_id[0].name, "Alice Smith")

        # Search by Name
        res_name = self.manager.search_students("Bob", search_by="name")
        self.assertEqual(len(res_name), 1)
        self.assertEqual(res_name[0].student_id, "S888")

        # Search by Course
        res_course = self.manager.search_students("Computer", search_by="course")
        self.assertEqual(len(res_course), 1)

        # Search by Department
        res_dept = self.manager.search_students("Construction", search_by="department")
        self.assertEqual(len(res_dept), 1)

        # Search all
        res_all = self.manager.search_students("Engineering", search_by="all")
        self.assertEqual(len(res_all), 1)

        # Search non-existent
        res_none = self.manager.search_students("NonExistentQuery")
        self.assertEqual(len(res_none), 0)

    def test_update_student_success(self) -> None:
        """Test updating existing student details."""
        self.manager.add_student(self.sample_student)
        update_data = {
            "name": "Alice Johnson",
            "age": 21,
            "gpa": 4.0,
        }
        success = self.manager.update_student("S999", update_data)
        self.assertTrue(success)

        updated_student = self.manager.get_student_by_id("S999")
        self.assertEqual(updated_student.name, "Alice Johnson")
        self.assertEqual(updated_student.age, 21)
        self.assertEqual(updated_student.gpa, 4.0)

    def test_update_non_existent_student_raises_key_error(self) -> None:
        """Test updating a non-existent student raises KeyError."""
        with self.assertRaises(KeyError):
            self.manager.update_student("INVALID_ID", {"name": "Test"})

    def test_delete_student_success(self) -> None:
        """Test deleting a student."""
        self.manager.add_student(self.sample_student)
        self.assertEqual(self.manager.student_count, 1)

        deleted = self.manager.delete_student("S999")
        self.assertTrue(deleted)
        self.assertEqual(self.manager.student_count, 0)

    def test_delete_non_existent_student_raises_key_error(self) -> None:
        """Test deleting non-existent student ID raises KeyError."""
        with self.assertRaises(KeyError):
            self.manager.delete_student("UNKNOWN_ID")

    # ------------------ Persistence & Export Tests ------------------

    def test_json_save_and_load(self) -> None:
        """Test saving students to JSON and reloading them."""
        self.manager.add_student(self.sample_student)
        self.assertTrue(self.manager.save_to_json())

        # Reset manager instance and reload
        new_manager = StudentManager(
            json_file_path=self.json_path,
            csv_file_path=self.csv_path,
        )
        loaded_count = new_manager.load_from_json()
        self.assertEqual(loaded_count, 1)

        loaded_student = new_manager.get_student_by_id("S999")
        self.assertIsNotNone(loaded_student)
        self.assertEqual(loaded_student.email, "alice@university.edu")

    def test_json_load_non_existent_file(self) -> None:
        """Test loading from a non-existent JSON file returns 0 records cleanly."""
        non_existent_path = Path(self.temp_dir.name) / "does_not_exist.json"
        manager = StudentManager(json_file_path=non_existent_path)
        count = manager.load_from_json()
        self.assertEqual(count, 0)

    def test_json_load_corrupted_file(self) -> None:
        """Test loading corrupted JSON file handles JSONDecodeError cleanly."""
        corrupted_path = Path(self.temp_dir.name) / "corrupted.json"
        with open(corrupted_path, "w", encoding="utf-8") as f:
            f.write("{ INVALID JSON CONTENT ---")

        with self.assertRaises(json.JSONDecodeError):
            FileHandler.load_json(corrupted_path)

    def test_export_to_csv(self) -> None:
        """Test exporting student data to CSV file."""
        self.manager.add_student(self.sample_student)
        self.assertTrue(self.manager.export_to_csv())
        self.assertTrue(os.path.exists(self.csv_path))

        with open(self.csv_path, "r", encoding="utf-8") as f:
            content = f.read()
            self.assertIn("S999", content)
            self.assertIn("Alice Smith", content)

    # ------------------ Validator Tests ------------------

    def test_validators(self) -> None:
        """Test input validators for email, age, phone, gpa, and student ID."""
        # Age
        self.assertEqual(Validator.validate_age("25"), 25)
        with self.assertRaises(ValueError):
            Validator.validate_age("abc")
        with self.assertRaises(ValueError):
            Validator.validate_age(12)  # Under min_age

        # Email
        self.assertEqual(Validator.validate_email("user@domain.com"), "user@domain.com")
        with self.assertRaises(ValueError):
            Validator.validate_email("invalid-email-format")

        # Phone
        self.assertEqual(Validator.validate_phone("+1-555-1234"), "+1-555-1234")
        with self.assertRaises(ValueError):
            Validator.validate_phone("123")  # too short

        # GPA
        self.assertEqual(Validator.validate_gpa("3.85"), 3.85)
        with self.assertRaises(ValueError):
            Validator.validate_gpa("105")  # Over max

        # Student ID
        self.assertEqual(Validator.validate_student_id("s101"), "S101")
        with self.assertRaises(ValueError):
            Validator.validate_student_id("S@101#")  # Special invalid chars


if __name__ == "__main__":
    unittest.main()
