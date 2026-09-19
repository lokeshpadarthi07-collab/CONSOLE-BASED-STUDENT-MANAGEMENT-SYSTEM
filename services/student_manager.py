"""
StudentManager service managing core business logic and student CRUD operations.
"""

from pathlib import Path
from typing import List, Optional, Dict, Any

from models.student import Student
from utils.file_handler import FileHandler
from utils.validators import Validator


class StudentManager:
    """
    Manages in-memory student records and coordinates persistence & export operations.
    """

    CSV_HEADERS = [
        "student_id",
        "name",
        "age",
        "email",
        "phone",
        "course",
        "year",
        "department",
        "gpa",
    ]

    def __init__(
        self,
        json_file_path: str | Path = "data/students.json",
        csv_file_path: str | Path = "data/students.csv",
    ) -> None:
        self._students: List[Student] = []
        self.json_file_path = Path(json_file_path)
        self.csv_file_path = Path(csv_file_path)

    @property
    def student_count(self) -> int:
        """Return the current number of registered students."""
        return len(self._students)

    def get_existing_ids(self) -> set[str]:
        """Return a set of all currently registered student IDs."""
        return {student.student_id.upper() for student in self._students}

    def add_student(self, student: Student) -> bool:
        """
        Add a new student to the records.

        Args:
            student: Student instance to add.

        Returns:
            bool: True if successfully added.

        Raises:
            ValueError: If student ID is duplicate.
        """
        if student.student_id.upper() in self.get_existing_ids():
            raise ValueError(f"Student with ID '{student.student_id}' already exists.")

        self._students.append(student)
        return True

    def get_student_by_id(self, student_id: str) -> Optional[Student]:
        """
        Search and return a student by their unique Student ID.

        Args:
            student_id: The ID of the student to retrieve.

        Returns:
            Optional[Student]: Student object if found, otherwise None.
        """
        clean_id = str(student_id).strip().upper()
        for student in self._students:
            if student.student_id.upper() == clean_id:
                return student
        return None

    def update_student(self, student_id: str, updated_fields: Dict[str, Any]) -> bool:
        """
        Update an existing student's attributes.

        Args:
            student_id: ID of the student to update.
            updated_fields: Dictionary of field names and new values.

        Returns:
            bool: True if student was successfully updated.

        Raises:
            KeyError: If student with given ID is not found.
            ValueError: If validation fails for updated values.
        """
        student = self.get_student_by_id(student_id)
        if not student:
            raise KeyError(f"Student with ID '{student_id}' not found.")

        # Validate provided updated fields before mutating
        if "name" in updated_fields:
            student.name = Validator.validate_name(updated_fields["name"])
        if "age" in updated_fields:
            student.age = Validator.validate_age(updated_fields["age"])
        if "email" in updated_fields:
            student.email = Validator.validate_email(updated_fields["email"])
        if "phone" in updated_fields:
            student.phone = Validator.validate_phone(updated_fields["phone"])
        if "course" in updated_fields:
            student.course = Validator.validate_non_empty(updated_fields["course"], "Course")
        if "year" in updated_fields:
            student.year = Validator.validate_year(updated_fields["year"])
        if "department" in updated_fields:
            student.department = Validator.validate_non_empty(updated_fields["department"], "Department")
        if "gpa" in updated_fields:
            student.gpa = Validator.validate_gpa(updated_fields["gpa"])

        return True

    def delete_student(self, student_id: str) -> bool:
        """
        Delete a student record by ID.

        Args:
            student_id: ID of student to delete.

        Returns:
            bool: True if student was deleted.

        Raises:
            KeyError: If student ID does not exist.
        """
        student = self.get_student_by_id(student_id)
        if not student:
            raise KeyError(f"Student with ID '{student_id}' does not exist.")

        self._students.remove(student)
        return True

    def search_students(self, query: str, search_by: str = "all") -> List[Student]:
        """
        Search students by Student ID, Name, Course, Department, or all fields.

        Args:
            query: The search text query.
            search_by: Field to filter by ('id', 'name', 'course', 'department', or 'all').

        Returns:
            List[Student]: List of matching student objects.
        """
        query_clean = str(query).strip().lower()
        if not query_clean:
            return self.get_all_students()

        results: List[Student] = []
        search_by_lower = search_by.strip().lower()

        for student in self._students:
            if search_by_lower in ("id", "student_id") and query_clean in student.student_id.lower():
                results.append(student)
            elif search_by_lower == "name" and query_clean in student.name.lower():
                results.append(student)
            elif search_by_lower == "course" and query_clean in student.course.lower():
                results.append(student)
            elif search_by_lower == "department" and query_clean in student.department.lower():
                results.append(student)
            elif search_by_lower == "all":
                if (
                    query_clean in student.student_id.lower()
                    or query_clean in student.name.lower()
                    or query_clean in student.course.lower()
                    or query_clean in student.department.lower()
                    or query_clean in student.email.lower()
                ):
                    results.append(student)

        return results

    def get_all_students(self) -> List[Student]:
        """Get copy of all student records."""
        return list(self._students)

    def load_from_json(self, file_path: Optional[str | Path] = None) -> int:
        """
        Load student records from JSON persistence file.

        Args:
            file_path: Custom file path (optional).

        Returns:
            int: Total count of loaded records.
        """
        target_path = Path(file_path) if file_path else self.json_file_path
        data = FileHandler.load_json(target_path)

        loaded_students: List[Student] = []
        for index, item in enumerate(data, start=1):
            try:
                student = Student.from_dict(item)
                loaded_students.append(student)
            except (KeyError, ValueError, TypeError) as e:
                raise ValueError(f"Error parsing record #{index} in JSON file '{target_path}': {e}")

        self._students = loaded_students
        return len(self._students)

    def save_to_json(self, file_path: Optional[str | Path] = None) -> bool:
        """
        Save current student records to JSON persistence file.

        Args:
            file_path: Custom target path (optional).

        Returns:
            bool: True if saving succeeded.
        """
        target_path = Path(file_path) if file_path else self.json_file_path
        data = [student.to_dict() for student in self._students]
        return FileHandler.save_json(target_path, data)

    def export_to_csv(self, file_path: Optional[str | Path] = None) -> bool:
        """
        Export all current student records to a CSV file.

        Args:
            file_path: Custom output file path (optional).

        Returns:
            bool: True if export succeeded.
        """
        target_path = Path(file_path) if file_path else self.csv_file_path
        data = [student.to_dict() for student in self._students]
        return FileHandler.export_csv(target_path, self.CSV_HEADERS, data)
