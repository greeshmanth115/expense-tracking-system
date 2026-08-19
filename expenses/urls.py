from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("expenses/", views.expense_list, name="expense_list"),
    path("expenses/add/", views.expense_add, name="expense_add"),
    path("expenses/edit/<int:pk>/", views.expense_edit, name="expense_edit"),
    path("expenses/delete/<int:pk>/", views.expense_delete, name="expense_delete"),
    path("income/", views.income_list, name="income_list"),
    path("income/add/", views.income_add, name="income_add"),
    path("income/edit/<int:pk>/", views.income_edit, name="income_edit"),
    path("income/delete/<int:pk>/", views.income_delete, name="income_delete"),
    path("report/", views.report, name="report"),
    path("signup/", views.signup, name="signup"),
    path("login/", auth_views.LoginView.as_view(template_name="expenses/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]
