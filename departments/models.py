from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from datetime import date

# Create your models here.

class Department(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название отдела')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children', verbose_name='Родительский отдел')
    level = models.IntegerField(default=1, verbose_name='Уровень в иерархии')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Отдел'
        verbose_name_plural = 'Отделы'
        ordering = ['name']

    def __str__(self):
        return self.name

    def clean(self):
        if self.parent and self.parent.level >= 5:
            raise ValidationError('Максимальная глубина иерархии отделов - 5 уровней')

    def save(self, *args, **kwargs):
        if self.parent:
            self.level = self.parent.level + 1
            if self.level > 5:
                raise ValidationError('Максимальная глубина иерархии отделов - 5 уровней')
        else:
            self.level = 1
        super().save(*args, **kwargs)

class Employee(models.Model):
    full_name = models.CharField(max_length=200, verbose_name='ФИО')
    position = models.CharField(max_length=200, verbose_name='Должность')
    hire_date = models.DateField(verbose_name='Дата приема на работу')
    salary = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Заработная плата', validators=[MinValueValidator(0)])
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='employees', verbose_name='Подразделение')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'
        ordering = ['full_name']

    def __str__(self):
        return f"{self.full_name} - {self.position}"

    def clean(self):
        if self.hire_date > date.today():
            raise ValidationError('Дата приема на работу не может быть в будущем')
