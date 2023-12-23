from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index ),
    path('candidates/', views.candidates),
    path('workers/', views.workers),
    path('orders/', views.orders),
    path('worker/<int:id>', views.concrete_worker),
    path('candidate/<int:id>', views.concrete_candidate),
    path('edit/<int:id>', views.edit_worker),
    path('profile/<int:id>', views.profile),
    path('candidate_page/<int:id>', views.candidate_page),


]
