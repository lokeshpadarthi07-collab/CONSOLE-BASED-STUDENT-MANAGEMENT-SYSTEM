from django import forms
from django.core.exceptions import ValidationError
from django.utils import timezone
import re
from .models import Student


class StudentForm(forms.ModelForm):
    """
    Form for registering and updating Student records with comprehensive validation.
    """
    class Meta:
        model = Student
        fields = [
            'student_id',
            'first_name',
            'last_name',
            'email',
            'phone',
            'date_of_birth',
            'course',
            'year',
        ]
        widgets = {
            'student_id': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g. STU1001',
                'autocomplete': 'off'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter first name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter last name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g. student@university.edu'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g. +1234567890'
            }),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-input',
                'type': 'date'
            }),
            'course': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g. Computer Science & Engineering'
            }),
            'year': forms.Select(attrs={
                'class': 'form-select'
            }),
        }

    def clean_student_id(self):
        student_id = self.cleaned_data.get('student_id', '').strip().upper()
        if not student_id:
            raise ValidationError("Student ID is required.")
        
        # Check uniqueness excluding self on update
        query = Student.objects.filter(student_id=student_id)
        if self.instance and self.instance.pk:
            query = query.exclude(pk=self.instance.pk)
            
        if query.exists():
            raise ValidationError(f"A student with Student ID '{student_id}' already exists.")
            
        return student_id

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip().lower()
        if not email:
            raise ValidationError("Email address is required.")
            
        # Check uniqueness excluding self on update
        query = Student.objects.filter(email=email)
        if self.instance and self.instance.pk:
            query = query.exclude(pk=self.instance.pk)
            
        if query.exists():
            raise ValidationError(f"A student with Email '{email}' already exists.")
            
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '').strip()
        if not phone:
            raise ValidationError("Phone number is required.")
            
        clean_phone = re.sub(r'[\s\-]', '', phone)
        if not re.match(r'^\+?[0-9]{7,15}$', clean_phone):
            raise ValidationError("Invalid phone number format. Please provide 7 to 15 digits.")
            
        return phone

    def clean_date_of_birth(self):
        dob = self.cleaned_data.get('date_of_birth')
        if not dob:
            raise ValidationError("Date of birth is required.")
            
        if dob > timezone.now().date():
            raise ValidationError("Date of birth cannot be in the future.")
            
        return dob

    def clean_year(self):
        year = self.cleaned_data.get('year')
        if year is None or year < 1 or year > 5:
            raise ValidationError("Please select a valid academic year (1 to 5).")
        return year
