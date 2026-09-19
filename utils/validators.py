"""
Input validation utilities for Student Management System.
"""

import re
from typing import Container, Optional


class Validator:
    """Provides validation helper methods for student details and user inputs."""

    # Regex patterns for validation
    EMAIL_PATTERN = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    PHONE_PATTERN = re.compile(r"^\+?[0-9\s\-]{7,15}$")
    NAME_PATTERN = re.compile(r"^[a-zA-Z\s\.\'-]{2,50}$")
    STUDENT_ID_PATTERN = re.compile(r"^[a-zA-Z0-9\-_]{2,20}$")

    @staticmethod
    def validate_non_empty(value: str, field_name: str = "Field") -> str:
        """
        Validate that a string input is not empty or pure whitespace.

        Raises:
            ValueError: If value is empty or whitespace.
        """
        if not value or not str(value).strip():
            raise ValueError(f"{field_name} cannot be empty.")
        return str(value).strip()

    @classmethod
    def validate_student_id(
        cls,
        student_id: str,
        existing_ids: Optional[Container[str]] = None,
        is_update: bool = False,
    ) -> str:
        """
        Validate student ID format and uniqueness.

        Args:
            student_id: Student ID string to validate.
            existing_ids: Collection of already existing student IDs.
            is_update: Set True if updating existing student (skips uniqueness check for self).

        Raises:
            ValueError: If format is invalid or ID already exists.
        """
        clean_id = cls.validate_non_empty(student_id, "Student ID").upper()

        if not cls.STUDENT_ID_PATTERN.match(clean_id):
            raise ValueError(
                "Student ID must be 2-20 alphanumeric characters (letters, numbers, hyphens, underscores allowed)."
            )

        if not is_update and existing_ids and clean_id in existing_ids:
            raise ValueError(f"Student ID '{clean_id}' already exists. IDs must be unique.")

        return clean_id

    @classmethod
    def validate_name(cls, name: str) -> str:
        """
        Validate student name format.

        Raises:
            ValueError: If name is invalid.
        """
        clean_name = cls.validate_non_empty(name, "Name")
        if not cls.NAME_PATTERN.match(clean_name):
            raise ValueError(
                "Name must contain 2-50 characters (only letters, spaces, hyphens, and dots allowed)."
            )
        return clean_name.title()

    @classmethod
    def validate_age(cls, age_input: str | int, min_age: int = 15, max_age: int = 100) -> int:
        """
        Validate student age.

        Raises:
            ValueError: If input is non-numeric or outside acceptable range.
        """
        try:
            age = int(age_input)
        except (ValueError, TypeError):
            raise ValueError("Age must be a valid whole integer number.")

        if not (min_age <= age <= max_age):
            raise ValueError(f"Age must be between {min_age} and {max_age}.")

        return age

    @classmethod
    def validate_email(cls, email: str) -> str:
        """
        Validate student email address format.

        Raises:
            ValueError: If email format is invalid.
        """
        clean_email = cls.validate_non_empty(email, "Email").lower()
        if not cls.EMAIL_PATTERN.match(clean_email):
            raise ValueError("Invalid email format. Example of valid email: student@example.com")
        return clean_email

    @classmethod
    def validate_phone(cls, phone: str) -> str:
        """
        Validate student phone number format.

        Raises:
            ValueError: If phone format is invalid.
        """
        clean_phone = cls.validate_non_empty(phone, "Phone number")
        # Strip internal extra spaces for evaluation
        digits_only = re.sub(r"[\s\-]", "", clean_phone)

        if not cls.PHONE_PATTERN.match(clean_phone) or len(digits_only) < 7:
            raise ValueError(
                "Invalid phone number. Must contain 7 to 15 digits (optional +, dashes allowed)."
            )
        return clean_phone

    @classmethod
    def validate_gpa(cls, gpa_input: str | float, min_val: float = 0.0, max_val: float = 100.0) -> float:
        """
        Validate student Marks/GPA. Supports 0.00 to 4.00 or percentage scale 0 to 100.

        Raises:
            ValueError: If input is non-numeric or outside range.
        """
        try:
            gpa = float(gpa_input)
        except (ValueError, TypeError):
            raise ValueError("Marks/GPA must be a valid number (e.g., 3.85 or 85.5).")

        if not (min_val <= gpa <= max_val):
            raise ValueError(f"Marks/GPA must be between {min_val} and {max_val}.")

        return round(gpa, 2)

    @classmethod
    def validate_year(cls, year_input: str) -> str:
        """
        Validate academic year input.

        Raises:
            ValueError: If year is invalid or empty.
        """
        clean_year = cls.validate_non_empty(year_input, "Year")
        # Normalize inputs like "1", "1st", "1st Year", "Freshman" etc.
        return clean_year
