from django.urls import path
from .views import DepartmentTreeView, get_department_data

app_name = 'departments'

urlpatterns = [
    path('', DepartmentTreeView.as_view(), name='department_tree'),
    path('department/<int:department_id>/', get_department_data, name='department_data'),
] 