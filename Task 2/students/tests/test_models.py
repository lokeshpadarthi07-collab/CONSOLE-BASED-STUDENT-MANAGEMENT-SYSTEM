from django.test import TestCase
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta, date
from students.models import Student


class StudentModelTest(TestCase):

    def setUp(self):
        self.student = Student.objects.create(
            student_id="STU1001",
            first_name="Alice",
            last_name="Smith",
            email="alice@university.edu",
            phone="+1234567890",
            date_of_birth=date(2002, 5, 15),
            course="Computer Science",
            year=3
        )

    def test_student_creation(self):
        """Test successful creation and retrieval of a Student model instance."""
        self.assertEqual(self.student.student_id, "STU1001")
        self.assertEqual(self.student.first_name, "Alice")
        self.assertEqual(self.student.full_name, "Alice Smith")
        self.assertEqual(str(self.student), "STU1001 - Alice Smith")

    def test_duplicate_student_id(self):
        """Test that duplicate student_id raises ValidationError."""
        duplicate_student = Student(
            student_id="STU1001",
            first_name="Bob",
            last_name="Jones",
            email="bob@university.edu",
            phone="+9876543210",
            date_of_birth=date(2003, 1, 10),
            course="Mathematics",
            year=2
        )
        with self.assertRaises(ValidationError):
            duplicate_student.save()

    def test_duplicate_email(self):
        """Test that duplicate email address raises ValidationError."""
        duplicate_email_student = Student(
            student_id="STU1002",
            first_name="Carol",
            last_name="Danvers",
            email="alice@university.edu",
            phone="+9876543210",
            date_of_birth=date(2001, 8, 20),
            course="Physics",
            year=4
        )
        with self.assertRaises(ValidationError):
            duplicate_email_student.save()

    def test_invalid_future_date_of_birth(self):
        """Test that date of birth in the future raises ValidationError."""
        future_student = Student(
            student_id="STU1003",
            first_name="David",
            last_name="Miller",
            email="david@university.edu",
            phone="+1122334455",
            date_of_birth=timezone.now().date() + timedelta(days=1),
            course="Chemistry",
            year=1
        )
        with self.assertRaises(ValidationError):
            future_student.save()

    def test_invalid_phone_number(self):
        """Test that invalid phone number format raises ValidationError."""
        invalid_phone_student = Student(
            student_id="STU1004",
            first_name="Eve",
            last_name="Adams",
            email="eve@university.edu",
            phone="abc-invalid-phone",
            date_of_birth=date(2002, 3, 12),
            course="Biology",
            year=2
        )
        with self.assertRaises(ValidationError):
            invalid_phone_student.save()
