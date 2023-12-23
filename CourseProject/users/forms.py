from django import forms
from django.contrib.auth import get_user_model

from main.models import *


class LoginForm(forms.Form):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class RegistrationForm(forms.Form):
    username = forms.CharField(label='Имя пользователя', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    role = forms.ChoiceField(label='Роль', choices=[('', 'Выберите роль'), ('candidate', 'Кандидат'), ('employee', 'Сотрудник'),
                                                    ('departmentHead', 'Начальник подразделения')], widget=forms.Select(attrs={'class': 'form-control'}))
    surname = forms.CharField(label='Фамилия', max_length=100,widget=forms.TextInput(attrs={'class': 'form-control'}))
    name = forms.CharField(label='Имя', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    patronymic = forms.CharField(label='Отчество', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    dob = forms.DateField(label='Дата рождения',widget=forms.DateInput(attrs={'class': 'form-control'}))
    gender = forms.ChoiceField(label='Пол', choices=[('male', 'Мужской'), ('female', 'Женский')], widget=forms.Select(attrs={'class': 'form-control'}))
    experience = forms.IntegerField(label='Опыт работы (в годах)', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    address = forms.CharField(label='Адрес', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(label='Номер телефона', max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))
    photo = forms.ImageField(label='Фотография',required=False)
    pow_name = forms.CharField(label='Место работы', max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    edu_name = forms.CharField(label='Место работы', max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    subdivision = forms.CharField(label='Подразделение', max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    job_title = forms.CharField(label='Должность', max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    ljr = forms.DateField(label='Дата начала работы', required=False, widget=forms.DateInput(attrs={'class': 'form-control'}))
    edr = forms.DateField(label='Дата начала обучения', required=False, widget=forms.DateInput(attrs={'class': 'form-control'}))
    ede = forms.DateField(label='Дата окончания', required=False, widget=forms.DateInput(attrs={'class': 'form-control'}))
    position = forms.CharField(label='Желаемая должность', max_length=100, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))