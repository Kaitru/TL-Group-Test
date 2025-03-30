from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.http import JsonResponse
from django.db.models import Prefetch
from .models import Department, Employee

# Create your views here.

class DepartmentTreeView(ListView):
    model = Department
    template_name = 'departments/department_tree.html'
    context_object_name = 'departments'

    def get_queryset(self):
        # Загружаем только отделы первого уровня
        return Department.objects.filter(level=1).prefetch_related('employees')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

def get_department_data(request, department_id):
    department = get_object_or_404(Department, id=department_id)
    
    # Получаем данные отдела и его сотрудников
    department_data = {
        'id': department.id,
        'name': department.name,
        'level': department.level,
        'employees': list(department.employees.values('id', 'full_name', 'position', 'hire_date', 'salary')),
        'has_children': department.children.exists()
    }
    
    return JsonResponse(department_data)
