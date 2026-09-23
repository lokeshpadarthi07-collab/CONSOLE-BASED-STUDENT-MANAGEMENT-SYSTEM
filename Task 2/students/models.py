from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
import re


class Student(models.Model):
    """
    Student model representing normalized student records in the Database-Driven
    Student Management System.
    """
    YEAR_CHOICES = [
        (1, '1st Year (Freshman)'),
        (2, '2nd Year (Sophomore)'),
        (3, '3rd Year (Junior)'),
        (4, '4th Year (Senior)'),
        (5, '5th Year (Postgraduate/Masters)'),
    ]

    student_id = models.CharField(
        max_length=20,
        unique=True,
        db_index=True,
        verbose_name="Student ID",
        help_text="Unique student identification number (e.g., STU1001)"
    )
    first_name = models.CharField(max_length=50, verbose_name="First Name")
    last_name = models.CharField(max_length=50, verbose_name="Last Name")
    email = models.EmailField(
        max_length=254,
        unique=True,
        db_index=True,
        verbose_name="Email Address"
    )
    phone = models.CharField(max_length=20, verbose_name="Phone Number")
    date_of_birth = models.DateField(verbose_name="Date of Birth")
    course = models.CharField(max_length=100, verbose_name="Course / Major")
    year = models.IntegerField(
        choices=YEAR_CHOICES,
        default=1,
        verbose_name="Academic Year"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Student"
        verbose_name_plural = "Students"

    @property
    def full_name(self):
        """Returns the full name of the student."""
        return f"{self.first_name} {self.last_name}"

    def clean(self):
        """Custom model validation."""
        super().clean()
        
        # Phone validation: numeric digits, optional leading plus, hyphen or space
        if self.phone:
            clean_phone = re.sub(r'[\s\-]', '', self.phone)
            if not re.match(r'^\+?[0-9]{7,15}$', clean_phone):
                raise ValidationError({
                    'phone': 'Enter a valid phone number (7 to 15 digits, optional + prefix).'
                })

        # Year validation
        if self.year and (self.year < 1 or self.year > 6):
            raise ValidationError({
                'year': 'Academic year must be between 1 and 6.'
            })

        # Date of birth validation (cannot be in the future)
        if self.date_of_birth and self.date_of_birth > timezone.now().date():
            raise ValidationError({
                'date_of_birth': 'Date of birth cannot be in the future.'
            })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student_id} - {self.full_name}"
