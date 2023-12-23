from django.contrib import admin
from .models import *

admin.site.register(AppUser)
admin.site.register(Candidate)
admin.site.register(Candidateeducation)
admin.site.register(Candidateplaceofwork)
admin.site.register(Worker)
admin.site.register(WorkOrder)
admin.site.register(SickLeave)
admin.site.register(Vacation)
admin.site.register(VacationType)
admin.site.register(Recruitment)
admin.site.register(Dismissal)
admin.site.register(EmploymentContract)
admin.site.register(JobTitle)
admin.site.register(JobResume)
admin.site.register(PlaceOfWork)
admin.site.register(Role)
admin.site.register(StructuralSubdivision)
admin.site.register(EducationalData)

