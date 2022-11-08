from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.LoginApi.as_view()),
    path('sendmoney/', views.sendmoney),
    path('sendmoney/<int:pk>/', views.sendoneyDetail),
    path('registration/', views.Regist),
    path('loan/', views.LoanApi.as_view()),
    path('loandetails/<int:pk>/', views.LoanApiDetail.as_view())
]