# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.contrib.auth.models import AbstractUser
from django.db import models


class AppUser(AbstractUser):
    id_user = models.AutoField(db_column='ID_User', primary_key=True)  # Field name made lowercase.
    username = models.CharField(db_column='Username', max_length=100, unique=True)  # Field name made lowercase.
    password = models.CharField(db_column='Password', max_length=100)  # Field name made lowercase.
    id_candidate = models.ForeignKey('Candidate', models.DO_NOTHING, db_column='ID_Candidate', blank=True, null=True)  # Field name made lowercase.
    id_role = models.ForeignKey('Role', models.DO_NOTHING, db_column='ID_Role')  # Field name made lowercase.
    id_worker = models.ForeignKey('Worker', models.DO_NOTHING, db_column='ID_Worker', blank=True, null=True)  # Field name made lowercase.



    def __int__(self):
        return self.id_user

    class Meta:
        db_table = 'App_User'


class Candidate(models.Model):
    id_candidate = models.AutoField(db_column='ID_Candidate', primary_key=True)  # Field name made lowercase.
    id_job_resume = models.ForeignKey('JobResume', models.DO_NOTHING, db_column='ID_Job_Resume', blank=True, null=True)# Field name made lowercase.

    def __int__(self):
        return self.id_candidate


    class Meta:
       
        db_table = 'Candidate'


class Candidateeducation(models.Model):
    id_educational_data = models.OneToOneField('EducationalData', models.DO_NOTHING, db_column='ID_Educational_Data', primary_key=True)  # Field name made lowercase. The composite primary key (ID_Educational_Data, ID_Candidate) found, that is not supported. The first column is selected.
    id_candidate = models.ForeignKey(Candidate, models.DO_NOTHING, db_column='ID_Candidate')  # Field name made lowercase.

    def __int__(self):
        return self.id_educational_data

    class Meta:
       
        db_table = 'CandidateEducation'
        unique_together = (('id_educational_data', 'id_candidate'),)


class Candidateplaceofwork(models.Model):
    id_candidate = models.OneToOneField(Candidate, models.DO_NOTHING, db_column='ID_Candidate', primary_key=True)  # Field name made lowercase. The composite primary key (ID_Candidate, ID_Place_Of_Work, ID_Job_Title, ID_Subdivision) found, that is not supported. The first column is selected.
    id_place_of_work = models.ForeignKey('PlaceOfWork', models.DO_NOTHING, db_column='ID_Place_Of_Work')  # Field name made lowercase.
    id_job_title = models.IntegerField(db_column='ID_Job_Title')  # Field name made lowercase.
    id_subdivision = models.IntegerField(db_column='ID_Subdivision')  # Field name made lowercase.

    def __int__(self):
        return self.id_candidate

    class Meta:
       
        db_table = 'CandidatePlaceOfWork'
        unique_together = (('id_candidate', 'id_place_of_work', 'id_job_title', 'id_subdivision'),)


class Dismissal(models.Model):
    id_dismissal = models.AutoField(db_column='ID_Dismissal', primary_key=True)  # Field name made lowercase. The composite primary key (ID_Dismissal, ID_Contract, ID_Worker, ID_Place_Of_Work, ID_Order, ID_User, ID_Job_Title, ID_Subdivision) found, that is not supported. The first column is selected.
    reason = models.CharField(db_column='Reason', max_length=100)  # Field name made lowercase.
    dismissal_date = models.DateField(db_column='Dismissal_Date')  # Field name made lowercase.
    id_contract = models.ForeignKey('EmploymentContract', models.DO_NOTHING, db_column='ID_Contract')  # Field name made lowercase.
    id_worker = models.IntegerField(db_column='ID_Worker')  # Field name made lowercase.
    id_place_of_work = models.IntegerField(db_column='ID_Place_Of_Work')  # Field name made lowercase.
    id_order = models.ForeignKey('WorkOrder', models.DO_NOTHING, db_column='ID_Order')  # Field name made lowercase.
    id_user = models.IntegerField(db_column='ID_User')  # Field name made lowercase.
    id_job_title = models.IntegerField(db_column='ID_Job_Title')  # Field name made lowercase.
    id_subdivision = models.IntegerField(db_column='ID_Subdivision')  # Field name made lowercase.
    file = models.FileField(db_column='File', null=True, blank=True,upload_to='orders/')
    def __int__(self):
        return self.id_dismissal

    class Meta:
       
        db_table = 'Dismissal'
        unique_together = (('id_dismissal', 'id_contract', 'id_worker', 'id_place_of_work', 'id_order', 'id_user', 'id_job_title', 'id_subdivision'),)


class EducationalData(models.Model):
    id_educational_data = models.AutoField(db_column='ID_Educational_Data', primary_key=True)  # Field name made lowercase.
    educational_institute = models.CharField(db_column='Educational_Institute', max_length=100)  # Field name made lowercase.
    receipt_date = models.DateField(db_column='Receipt_Date')  # Field name made lowercase.
    expiration_date = models.DateField(db_column='Expiration_Date')  # Field name made lowercase.

    def __int__(self):
        return self.id_educational_data

    class Meta:
       
        db_table = 'Educational_Data'


class EmploymentContract(models.Model):
    id_contract = models.AutoField(db_column='ID_Contract', primary_key=True)  # Field name made lowercase. The composite primary key (ID_Contract, ID_Worker, ID_Place_Of_Work, ID_Job_Title, ID_Subdivision) found, that is not supported. The first column is selected.
    receipt_date = models.DateField(db_column='Receipt_Date')  # Field name made lowercase.
    salary = models.BigIntegerField(db_column='Salary')  # Field name made lowercase.
    id_worker = models.ForeignKey('Worker', models.DO_NOTHING, db_column='ID_Worker')  # Field name made lowercase.
    id_place_of_work = models.ForeignKey('PlaceOfWork', models.DO_NOTHING, db_column='ID_Place_Of_Work')  # Field name made lowercase.
    id_job_title = models.ForeignKey('JobTitle',models.DO_NOTHING, db_column='ID_Job_Title')  # Field name made lowercase.
    id_subdivision = models.ForeignKey('StructuralSubdivision', models.DO_NOTHING, db_column='ID_Subdivision')  # Field name made lowercase.

    def __int__(self):
        return self.id_contract

    class Meta:
       
        db_table = 'Employment_Contract'
        unique_together = (('id_contract', 'id_worker', 'id_place_of_work', 'id_job_title', 'id_subdivision'),)


class JobResume(models.Model):
    id_job_resume = models.AutoField(db_column='ID_Job_Resume', primary_key=True)  # Field name made lowercase.
    surname = models.CharField(db_column='Surname', max_length=100)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=100)  # Field name made lowercase.
    patronymic = models.CharField(db_column='Patronymic', max_length=100, blank=True, null=True)  # Field name made lowercase.
    gender = models.CharField(db_column='Gender', max_length=20)  # Field name made lowercase.
    phone_number = models.CharField(db_column='Phone_Number', max_length=20)  # Field name made lowercase.
    adress = models.CharField(db_column='Adress', max_length=200)  # Field name made lowercase.
    birthday = models.DateField(db_column='Birthday')  # Field name made lowercase.
    photo = models.ImageField(db_column='Photo', null=True, blank=True, upload_to='uploads/')  # Field name made lowercase.
    position = models.CharField(db_column='Position', max_length=100)  # Field name made lowercase.
    work_experience = models.IntegerField(db_column='Work_Experience', blank=True, null=True)  # Field name made lowercase.

    def __int__(self):
        return self.id_job_resume


    def __str__(self):
        return f'{self.surname} {self.name} {self.patronymic}'
    class Meta:
       
        db_table = 'Job_Resume'


class JobTitle(models.Model):
    id_job_title = models.AutoField(db_column='ID_Job_Title', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=100)  # Field name made lowercase.

    def __str__(self):
        return self.name

    def __int__(self):
        return self.id_job_title


    class Meta:
       
        db_table = 'Job_Title'


class PlaceOfWork(models.Model):
    id_place_of_work = models.AutoField(db_column='ID_Place_Of_Work', primary_key=True)  # Field name made lowercase. The composite primary key (ID_Place_Of_Work, ID_Job_Title, ID_Subdivision) found, that is not supported. The first column is selected.
    reseipt_date = models.DateField(db_column='Reseipt_Date')  # Field name made lowercase.
    expiration_date = models.DateField(db_column='Expiration_Date', blank=True, null=True)  # Field name made lowercase.
    id_job_title = models.ForeignKey('JobTitle', models.DO_NOTHING, db_column='ID_Job_Title')  # Field name made lowercase.
    id_subdivision = models.ForeignKey('StructuralSubdivision', models.DO_NOTHING, db_column='ID_Subdivision')  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=100)  # Field name made lowercase.

    def __int__(self):
        return self.id_place_of_work

    class Meta:
       
        db_table = 'Place_Of_Work'
        unique_together = (('id_place_of_work', 'id_job_title', 'id_subdivision'),)


class Recruitment(models.Model):
    id_recruitment = models.AutoField(db_column='ID_Recruitment', primary_key=True)  # Field name made lowercase. The composite primary key (ID_Recruitment, ID_Contract, ID_Worker, ID_Place_Of_Work, ID_Order, ID_User, ID_Job_Title, ID_Subdivision) found, that is not supported. The first column is selected.
    recruitment_date = models.DateField(db_column='Recruitment_Date')  # Field name made lowercase.
    id_contract = models.ForeignKey(EmploymentContract, models.DO_NOTHING, db_column='ID_Contract')  # Field name made lowercase.
    id_worker = models.IntegerField(db_column='ID_Worker')  # Field name made lowercase.
    id_place_of_work = models.IntegerField(db_column='ID_Place_Of_Work')  # Field name made lowercase.
    id_order = models.ForeignKey('WorkOrder', models.DO_NOTHING, db_column='ID_Order')  # Field name made lowercase.
    id_user = models.IntegerField(db_column='ID_User')  # Field name made lowercase.
    id_job_title = models.IntegerField(db_column='ID_Job_Title')  # Field name made lowercase.
    id_subdivision = models.IntegerField(db_column='ID_Subdivision')  # Field name made lowercase.
    file = models.FileField(db_column='File', null=True, blank=True, upload_to='orders/')

    def __int__(self):
        return self.id_recruitment

    class Meta:
       
        db_table = 'Recruitment'
        unique_together = (('id_recruitment', 'id_contract', 'id_worker', 'id_place_of_work', 'id_order', 'id_user', 'id_job_title', 'id_subdivision'),)


class Role(models.Model):
    id_role = models.AutoField(db_column='ID_Role', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=100)  # Field name made lowercase.
    canreadworkersdata = models.BooleanField(db_column='CanReadWorkersData')  # Field name made lowercase.
    caneditworkersdata = models.BooleanField(db_column='CanEditWorkersData')  # Field name made lowercase.
    canedituserdata = models.BooleanField(db_column='CanEditUserData')  # Field name made lowercase.
    candoorders = models.BooleanField(db_column='CanDoOrders')  # Field name made lowercase.

    def __int__(self):
        return self.id_role

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Role'


class SickLeave(models.Model):
    id_sick_leave = models.AutoField(db_column='ID_Sick_Leave', primary_key=True)  # Field name made lowercase. The composite primary key (ID_Sick_Leave, ID_Worker) found, that is not supported. The first column is selected.
    receipt_date = models.DateField(db_column='Receipt_Date')  # Field name made lowercase.
    expiration_date = models.DateField(db_column='Expiration_Date')  # Field name made lowercase.
    id_worker = models.ForeignKey('Worker', models.DO_NOTHING, db_column='ID_Worker')  # Field name made lowercase.

    def __int__(self):
        return self.id_sick_leave

    class Meta:
       
        db_table = 'Sick_Leave'
        unique_together = (('id_sick_leave', 'id_worker'),)


class StructuralSubdivision(models.Model):
    id_subdivision = models.AutoField(db_column='ID_Subdivision', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=100)  # Field name made lowercase.

    def __int__(self):
        return self.id_subdivision

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'Structural_Subdivision'


class Vacation(models.Model):
    id_vacation = models.AutoField(db_column='ID_Vacation', primary_key=True)  # Field name made lowercase. The composite primary key (ID_Vacation, ID_VacationType, ID_Worker, ID_Order, ID_User) found, that is not supported. The first column is selected.
    receipt_date = models.DateField(db_column='Receipt_Date')  # Field name made lowercase.
    expiration_date = models.DateField(db_column='Expiration_Date')  # Field name made lowercase.
    id_vacationtype = models.ForeignKey('VacationType', models.DO_NOTHING, db_column='ID_VacationType')  # Field name made lowercase.
    id_worker = models.ForeignKey('Worker', models.DO_NOTHING, db_column='ID_Worker')  # Field name made lowercase.
    id_order = models.ForeignKey('WorkOrder', models.DO_NOTHING, db_column='ID_Order')  # Field name made lowercase.
    id_user = models.IntegerField(db_column='ID_User')  # Field name made lowercase.
    file = models.FileField(db_column='File', null=True, blank=True, upload_to='orders/')

    def __int__(self):
        return self.id_vacation

    class Meta:
       
        db_table = 'Vacation'
        unique_together = (('id_vacation', 'id_vacationtype', 'id_worker', 'id_order', 'id_user'),)


class VacationType(models.Model):
    id_vacation_type = models.AutoField(db_column='ID_Vacation_Type', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=100)  # Field name made lowercase.

    def __int__(self):
        return self.id_vacation_type

    def __str__(self):
        return f'{self.name}'

    class Meta:
       
        db_table = 'Vacation_Type'


class WorkOrder(models.Model):
    id_order = models.AutoField(db_column='ID_Order', primary_key=True)  # Field name made lowercase. The composite primary key (ID_Order, ID_User) found, that is not supported. The first column is selected.
    order_number = models.BigIntegerField(db_column='Order_Number')  # Field name made lowercase.
    receipt_date = models.DateField(db_column='Receipt_Date')  # Field name made lowercase.
    id_user = models.ForeignKey(AppUser, models.DO_NOTHING, db_column='ID_User')  # Field name made lowercase.

    def __int__(self):
        return self.id_order

    class Meta:
       
        db_table = 'Work_Order'
        unique_together = (('id_order', 'id_user'),)


class Worker(models.Model):
    id_worker = models.AutoField(db_column='ID_Worker', primary_key=True)  # Field name made lowercase.
    surname = models.CharField(db_column='Surname', max_length=100)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=100)  # Field name made lowercase.
    patronymic = models.CharField(db_column='Patronymic', max_length=100, blank=True, null=True)  # Field name made lowercase.
    gender = models.CharField(db_column='Gender', max_length=20)  # Field name made lowercase.
    birthday = models.DateField(db_column='Birthday')  # Field name made lowercase.
    work_experience = models.CharField(db_column='Work_Experience', max_length=100)  # Field name made lowercase.
    adress = models.CharField(db_column='Adress', max_length=200)  # Field name made lowercase.
    phone_number = models.CharField(db_column='Phone_Number', max_length=20)  # Field name made lowercase.
    photo = models.ImageField(db_column='Photo', blank=True, null=True, upload_to='uploads/')  # Field name made lowercase.

    def __int__(self):
        return self.id_worker

    def __str__(self):
        return f'{self.surname} {self.name} {self.patronymic}'


    class Meta:
        db_table = 'Worker'
