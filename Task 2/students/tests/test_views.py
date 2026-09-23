from django.test import TestCase
from django.urls import reverse
from datetime import date
from students.models import Student


class StudentViewsTest(TestCase):

    def setUp(self):
        self.student = Student.objects.create(
            student_id="STU3001",
            first_name="Kevin",
            last_name="Bacon",
            email="kevin@university.edu",
            phone="+1444555666",
            date_of_birth=date(2000, 10, 24),
            course="Drama & Arts",
            year=4
        )

    def test_student_list_view(self):
        """Test student list view renders correctly."""
        response = self.client.get(reverse('student_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'students/student_list.html')
        self.assertContains(response, "Kevin Bacon")
        self.assertContains(response, "STU3001")

    def test_student_list_search_filter(self):
        """Test searching for students in list view."""
        response = self.client.get(reverse('student_list'), {'q': 'STU3001'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Kevin Bacon")

        # Non-matching search query
        response_empty = self.client.get(reverse('student_list'), {'q': 'NONEXISTENT'})
        self.assertContains(response_empty, "No Students Found")

    def test_student_detail_view(self):
        """Test student detail view displays individual student details."""
        url = reverse('student_detail', args=[self.student.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'students/student_detail.html')
        self.assertContains(response, "Kevin Bacon")
        self.assertContains(response, "kevin@university.edu")

    def test_student_create_view_get(self):
        """Test rendering the student creation form page."""
        response = self.client.get(reverse('student_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'students/student_form.html')

    def test_student_create_view_post(self):
        """Test registering a new student via POST."""
        post_data = {
            'student_id': 'STU3002',
            'first_name': 'Laura',
            'last_name': 'Croft',
            'email': 'laura@university.edu',
            'phone': '+1777888999',
            'date_of_birth': '2003-02-14',
            'course': 'Archaeology',
            'year': 2
        }
        response = self.client.post(reverse('student_create'), data=post_data)
        self.assertEqual(response.status_code, 302)  # Redirects to detail view
        self.assertTrue(Student.objects.filter(student_id='STU3002').exists())

    def test_student_update_view(self):
        """Test updating an existing student via POST."""
        url = reverse('student_update', args=[self.student.pk])
        post_data = {
            'student_id': 'STU3001',
            'first_name': 'Kevin',
            'last_name': 'Bacon Updated',
            'email': 'kevin.new@university.edu',
            'phone': '+1444555666',
            'date_of_birth': '2000-10-24',
            'course': 'Film Studies',
            'year': 4
        }
        response = self.client.post(url, data=post_data)
        self.assertEqual(response.status_code, 302)
        self.student.refresh_from_db()
        self.assertEqual(self.student.last_name, 'Bacon Updated')
        self.assertEqual(self.student.email, 'kevin.new@university.edu')
        self.assertEqual(self.student.course, 'Film Studies')

    def test_student_delete_view(self):
        """Test deleting a student record via POST."""
        url = reverse('student_delete', args=[self.student.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Student.objects.filter(pk=self.student.pk).exists())
