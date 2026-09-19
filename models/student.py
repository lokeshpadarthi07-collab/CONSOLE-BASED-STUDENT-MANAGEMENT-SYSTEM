"""
Student model representing individual student records.
"""

from typing import Dict, Any


class Student:
    """
    Represents a student in the Student Management System.

    Attributes:
        student_id (str): Unique identifier for the student.
        name (str): Full name of the student.
        age (int): Age of the student.
        email (str): Contact email address.
        phone (str): Contact phone number.
        course (str): Enrolled course or degree program.
        year (str): Academic year (e.g., 1st Year, 2nd Year, etc.).
        department (str): Academic department (e.g., Computer Science).
        gpa (float): Academic Marks or Grade Point Average (0.0 to 4.0 / 100).
    """

    def __init__(
        self,
        student_id: str,
        name: str,
        age: int,
        email: str,
        phone: str,
        course: str,
        year: str,
        department: str,
        gpa: float,
    ) -> None:
        self.student_id = str(student_id).strip()
        self.name = str(name).strip()
        self.age = int(age)
        self.email = str(email).strip()
        self.phone = str(phone).strip()
        self.course = str(course).strip()
        self.year = str(year).strip()
        self.department = str(department).strip()
        self.gpa = float(gpa)

    def to_dict(self) -> Dict[str, Any]:
        """Convert Student object into a dictionary representation."""
        return {
            "student_id": self.student_id,
            "name": self.name,
            "age": self.age,
            "email": self.email,
            "phone": self.phone,
            "course": self.course,
            "year": self.year,
            "department": self.department,
            "gpa": self.gpa,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Student":
        """
        Create a Student instance from a dictionary.

        Raises:
            KeyError: If mandatory keys are missing in the dictionary.
            ValueError: If data types cannot be converted.
        """
        return cls(
            student_id=data["student_id"],
            name=data["name"],
            age=data["age"],
            email=data["email"],
            phone=data["phone"],
            course=data["course"],
            year=data["year"],
            department=data["department"],
            gpa=data["gpa"],
        )

    def __str__(self) -> str:
        return (
            f"ID: {self.student_id:<8} | Name: {self.name:<18} | Age: {self.age:<3} | "
            f"Dept: {self.department:<12} | Course: {self.course:<12} | Year: {self.year:<8} | GPA: {self.gpa:.2f}"
        )

    def __repr__(self) -> str:
        return f"<Student id='{self.student_id}' name='{self.name}'>"
