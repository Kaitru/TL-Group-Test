from django.core.management.base import BaseCommand
from django.utils import timezone
from departments.models import Department, Employee
from faker import Faker
import random
from datetime import timedelta

fake = Faker('ru_RU')

class Command(BaseCommand):
    help = 'Генерирует тестовые данные для отделов и сотрудников'

    def handle(self, *args, **kwargs):
        self.stdout.write('Начинаем генерацию тестовых данных...')
        
        # Создаем корневые отделы
        root_departments = [
            'Управление',
            'Производство',
            'Разработка',
            'Маркетинг',
            'Финансы'
        ]
        
        departments_dict = {}
        for root_name in root_departments:
            root_dept = Department.objects.create(name=root_name)
            departments_dict[root_dept.id] = root_dept
            self.stdout.write(f'Создан отдел: {root_name}')
            
            # Создаем подотделы для каждого корневого отдела
            for i in range(5):
                sub_dept = Department.objects.create(
                    name=fake.company_suffix(),
                    parent=root_dept
                )
                departments_dict[sub_dept.id] = sub_dept
                self.stdout.write(f'Создан подотдел: {sub_dept.name} в {root_name}')
                
                # Создаем подотделы третьего уровня
                for j in range(5):
                    sub_sub_dept = Department.objects.create(
                        name=fake.company_suffix(),
                        parent=sub_dept
                    )
                    departments_dict[sub_sub_dept.id] = sub_sub_dept
                    self.stdout.write(f'Создан подотдел: {sub_sub_dept.name} в {sub_dept.name}')
                    
                    # Создаем подотделы четвертого уровня
                    for k in range(5):
                        sub_sub_sub_dept = Department.objects.create(
                            name=fake.company_suffix(),
                            parent=sub_sub_dept
                        )
                        departments_dict[sub_sub_sub_dept.id] = sub_sub_sub_dept
                        self.stdout.write(f'Создан подотдел: {sub_sub_sub_dept.name} в {sub_sub_dept.name}')
                        
                        # Создаем подотделы пятого уровня
                        for l in range(5):
                            sub_sub_sub_sub_dept = Department.objects.create(
                                name=fake.company_suffix(),
                                parent=sub_sub_sub_dept
                            )
                            departments_dict[sub_sub_sub_sub_dept.id] = sub_sub_sub_sub_dept
                            self.stdout.write(f'Создан подотдел: {sub_sub_sub_sub_dept.name} в {sub_sub_sub_dept.name}')
        
        # Создаем сотрудников
        positions = [
            'Менеджер', 'Разработчик', 'Дизайнер', 'Аналитик', 'Бухгалтер',
            'Юрист', 'HR-специалист', 'Маркетолог', 'Продавец', 'Оператор'
        ]
        
        for _ in range(50000):
            department = random.choice(list(departments_dict.values()))
            hire_date = fake.date_between(start_date='-5y', end_date='today')
            
            Employee.objects.create(
                full_name=fake.name(),
                position=random.choice(positions),
                hire_date=hire_date,
                salary=random.randint(30000, 150000),
                department=department
            )
            
        self.stdout.write(self.style.SUCCESS('Тестовые данные успешно сгенерированы!')) 