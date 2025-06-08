from django.urls import path

from expense.views import CreateUserView, ExpenseAnalyticsView, ExpenseListCreateView, LoginView

urlpatterns = [
    path("register-user/",CreateUserView.as_view(), name="register_user"),
    path("login/",LoginView.as_view(), name="login"),
    path("expenses/",ExpenseListCreateView.as_view(), name="expenses"),
    path("expenses/analytics/",ExpenseAnalyticsView.as_view(), name="expense_analytics"),
]
