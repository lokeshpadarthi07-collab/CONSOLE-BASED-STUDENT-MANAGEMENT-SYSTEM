from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from .models import Student
from .forms import StudentForm


def student_list(request):
    """
    View to list all students with search and filtering capabilities.
    """
    query = request.GET.get('q', '').strip()
    year_filter = request.GET.get('year', '').strip()
    course_filter = request.GET.get('course', '').strip()

    students = Student.objects.all()

    # Search filter (student_id, first_name, last_name, email, course)
    if query:
        students = students.filter(
            Q(student_id__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(email__icontains=query) |
            Q(course__icontains=query)
        )

    # Academic year filter
    if year_filter and year_filter.isdigit():
        students = students.filter(year=int(year_filter))

    # Course filter
    if course_filter:
        students = students.filter(course__icontains=course_filter)

    # Distinct courses for dropdown filter
    all_courses = Student.objects.values_list('course', flat=True).distinct().order_by('course')

    context = {
        'students': students,
        'query': query,
        'year_filter': year_filter,
        'course_filter': course_filter,
        'all_courses': all_courses,
        'total_count': students.count(),
        'all_students_count': Student.objects.count(),
    }
    return render(request, 'students/student_list.html', context)


def student_detail(request, pk):
    """
    View to display comprehensive details of a single student.
    """
    student = get_object_or_404(Student, pk=pk)
    return render(request, 'students/student_detail.html', {'student': student})


def student_create(request):
    """
    View to register/add a new student record.
    """
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            student = form.save()
            messages.success(
                request,
                f"Student '{student.full_name}' ({student.student_id}) successfully registered!"
            )
            return redirect('student_detail', pk=student.pk)
        else:
            messages.error(request, "Please correct the errors below before submitting.")
    else:
        form = StudentForm()

    return render(request, 'students/student_form.html', {
        'form': form,
        'title': 'Register New Student',
        'button_text': 'Add Student',
        'is_create': True
    })


def student_update(request, pk):
    """
    View to update an existing student record.
    """
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            updated_student = form.save()
            messages.success(
                request,
                f"Student record for '{updated_student.full_name}' successfully updated!"
            )
            return redirect('student_detail', pk=updated_student.pk)
        else:
            messages.error(request, "Please correct the errors below before updating.")
    else:
        form = StudentForm(instance=student)

    return render(request, 'students/student_form.html', {
        'form': form,
        'student': student,
        'title': f'Update Student - {student.student_id}',
        'button_text': 'Save Changes',
        'is_create': False
    })


def student_delete(request, pk):
    """
    View to handle deletion of a student record.
    """
    student = get_object_or_404(Student, pk=pk)
    if request.method == 'POST':
        student_name = student.full_name
        student_id = student.student_id
        student.delete()
        messages.success(
            request,
            f"Student record '{student_name}' ({student_id}) deleted successfully."
        )
        return redirect('student_list')

    return render(request, 'students/student_confirm_delete.html', {'student': student})
