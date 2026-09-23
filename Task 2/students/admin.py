from django.contrib import admin
from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        'student_id',
        'first_name',
        'last_name',
        'email',
        'phone',
        'course',
        'year',
        'created_at',
    )
    list_filter = ('year', 'course', 'created_at')
    search_fields = ('student_id', 'first_name', 'last_name', 'email', 'course')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Basic Information', {
            'fields': ('student_id', 'first_name', 'last_name', 'date_of_birth')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone')
        }),
        ('Academic Information', {
            'fields': ('course', 'year')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
