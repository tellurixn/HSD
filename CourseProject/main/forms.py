from django import forms
from django.forms import DateInput, NumberInput, DateField
from .models import *
from django.forms import ModelForm, TextInput, FileInput


class WorkerForm(ModelForm):
    class Meta:
        model = Worker
        fields = '__all__'
        widgets = {
            'photo': FileInput(attrs={
                'accept': 'image/*',
                'required': 'False',
          }),
            'surname': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите фамилию..',
                'id': 'surname',
                'name': 'surname'
            }),
            'name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите имя..',
                'id': 'name',
                'name': 'name'
            }),
            'patronymic': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите фамилию..',
                'id': 'patronymic',
                'name': 'patronymic'
            }),
            'gender': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите пол..',
                'id': 'gender',
                'name': 'gender'
            }),
            'birthday': DateInput(attrs={
                'class': 'form-control',
                'id': 'birthday',
                'name': 'birthday'
            }),
            'work_experience': NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите опыт работы..',
                'id': 'work_experience',
                'name': 'work_experience'
            }),
            'adress': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите адрес..',
            }),
            'phone_number': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите номер..',
                'id': 'phone_number',
                'name': 'phone_number'
            }),

        }

class ResumeForm(ModelForm):
    class Meta:
        model = Worker
        fields = '__all__'
        widgets = {
            'photo': FileInput(attrs={
                'accept': 'image/*',
                'required': 'False',
          }),
            'surname': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите фамилию..',
                'id': 'surname',
                'name': 'surname'
            }),
            'name': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите имя..',
                'id': 'name',
                'name': 'name'
            }),
            'patronymic': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите фамилию..',
                'id': 'patronymic',
                'name': 'patronymic'
            }),
            'gender': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите пол..',
                'id': 'gender',
                'name': 'gender'
            }),
            'birthday': DateInput(attrs={
                'class': 'form-control',
                'id': 'birthday',
                'name': 'birthday'
            }),
            'work_experience': NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите опыт работы..',
                'id': 'work_experience',
                'name': 'work_experience'
            }),
            'adress': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите адрес..',
            }),
            'phone_number': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите номер..',
                'id': 'phone_number',
                'name': 'phone_number'
            }),
            'position': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите желаемую позицицю..',
                'id': 'position',
                'name': 'position'
            }),
        }




