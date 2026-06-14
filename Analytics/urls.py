from django.urls import path
from . import views

urlpatterns=[

    path('employee-analytics/<int:pk>/',views.EmployeeAnalytics.as_view()),
    path('organization-analytics/<int:pk>/',views.OrganizationAnalytics.as_view()),

]