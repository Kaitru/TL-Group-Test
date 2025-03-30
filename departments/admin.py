from django.contrib import admin
from .models import Department, Employee

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'level', 'created_at')
    list_filter = ('level', 'created_at')
    search_fields = ('name',)
    ordering = ('name',)

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'position', 'department', 'hire_date', 'salary')
    list_filter = ('department', 'position', 'hire_date')
    search_fields = ('full_name', 'position')
    ordering = ('full_name',)
