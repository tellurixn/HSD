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


class OrderForm(forms.Form):
    orderNumber = forms.IntegerField(label='Номер приказа', widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Введите номер приказа'}))
    orderType = forms.ChoiceField(label='Выбор типа приказа', choices=[('', 'Выберите тип приказа'), (1, 'Отпуск'), (2, 'Прием на работу'), (3, 'Увольнение')], widget=forms.Select(attrs={'class': 'form-control'}))
    vacationType = forms.ChoiceField(required=False, label='Выбор вида отпуска', choices=[(1, 'Ежегодный обычный'), (2, 'Ежегодный дополнительный'), (3, 'Без сохранения ЗП'), (4, 'Учебный')], widget=forms.Select(attrs={'class': 'form-control'}))
    employee = forms.ModelChoiceField( required=False, queryset=Worker.objects.all(), label='Сотрудник',
                                      widget=forms.Select(attrs={'class': 'form-control'}))
    startDate = forms.DateField(required=False, label='Дата начала отпуска', widget=forms.DateInput(attrs={'class': 'form-control'}))
    endDate = forms.DateField(required=False, label='Дата окончания отпуска', widget=forms.DateInput(attrs={'class': 'form-control'}))
    contractNumber = forms.CharField(required=False, label='Номер трудового договора', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите номер трудового договора'}))
    candidate = forms.CharField(required=False, label='Кандидат', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите имя кандидата'}))
    dismissalContractNumber = forms.CharField(required=False, label='Номер трудового договора', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите номер трудового договора'}))
    dismissalEmployee = forms.CharField(required=False,label='Сотрудник', max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите имя сотрудника'}))
    reason = forms.CharField(required=False, label='Причина увольнения', widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Введите причину увольнения'}))

