from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from django.urls import path
from . import views
urlpatterns=[
    path('login/',views.mytoken.as_view()),
    path('login/refresh/',TokenRefreshView.as_view()),
    path('create/',views.CreateUser.as_view()),
    path('verify/<str:uuid>/<str:token>/',views.Verification.as_view()),
    path('employee-create/',views.EmployeeTemperary.as_view()),
    path('password-change/',views.changePassword.as_view()),
    path('password-force-change/<int:pk>/',views.force_password_reset.as_view()),
    path('password-change-Founder/<int:pk>/',views.changePasswordByFounder.as_view()),
    path('employee/<int:pk>/',views.employee_retrieve.as_view()),
    path('employee-all/<int:pk>/',views.employee_list.as_view())
]