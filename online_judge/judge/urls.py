from django.urls import  path
from . import views

app_name = 'judge'
urlpatterns = [
    path('', views.index , name="index"),
    path('problems/' , views.problems , name="problems"),
    path('problem/<int:problem_id>/' , views.problem , name="problem"),
    path('submit/<int:pid>/' , views.submit , name="submit"),
    path('submit/<str:status>/' , views.result , name="result"),
    path('submissions/' , views.submissions , name="submissions"),
    path('register/', views.register_request, name="register"),
    path('login/', views.login_request, name="login"),
    path('logout/', views.log_out, name="logout"),
    path('login/check/', views.login_check, name="login_check"),
    path('register/verify/', views.register_verify, name="register_verify")
]