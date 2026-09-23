from django.test import TestCase
from datetime import date
from students.models import Student
from students.forms import StudentForm


class StudentFormTest(TestCase):

    def setUp(self):
        Student.objects.create(
            student_id="STU2001",
            first_name="Frank",
            last_name="Wright",
            email="frank@university.edu",
            phone="+1999888777",
            date_of_birth=date(2001, 4, 18),
            course="Engineering",
            year=3
        )

    def test_valid_form(self):
        """Test form with valid data."""
        data = {
            'student_id': 'STU2002',
            'first_name': 'Grace',
            'last_name': 'Hopper',
            'email': 'grace@university.edu',
            'phone': '+1555666777',
            'date_of_birth': '2002-12-09',
            'course': 'Computer Science',
            'year': 2
        }
        form = StudentForm(data=data)
        self.assertTrue(form.is_valid())

    def test_missing_required_fields(self):
        """Test form submission with missing required fields."""
        form = StudentForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('student_id', form.errors)
        self.assertIn('first_name', form.errors)
        self.assertIn('last_name', form.errors)
        self.assertIn('email', form.errors)

    def test_duplicate_student_id_validation(self):
        """Test form validation prevents duplicate student_id."""
        data = {
            'student_id': 'STU2001',
            'first_name': 'Henry',
            'last_name': 'Ford',
            'email': 'henry@university.edu',
            'phone': '+1222333444',
            'date_of_birth': '2003-01-01',
            'course': 'Business',
            'year': 1
        }
        form = StudentForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('student_id', form.errors)

    def test_invalid_email_format(self):
        """Test form validation catches invalid email format."""
        data = {
            'student_id': 'STU2003',
            'first_name': 'Ian',
            'last_name': 'Fleming',
            'email': 'not-an-email',
            'phone': '+1222333444',
            'date_of_birth': '2002-05-05',
            'course': 'Literature',
            'year': 4
        }
        form = StudentForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_invalid_year_validation(self):
        """Test form validation rejects invalid academic year."""
        data = {
            'student_id': 'STU2004',
            'first_name': 'Jane',
            'last_name': 'Austin',
            'email': 'jane@university.edu',
            'phone': '+1222333444',
            'date_of_birth': '2001-07-07',
            'course': 'History',
            'year': 10
        }
        form = StudentForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn('year', form.errors)
