from django.urls import include , path
from . import views

app_name = 'contestApp'

urlpatterns = [
    path('', views.index , name='index'),
    path('leaderboard/', views.leaderboard , name='leaderboard'),
    path('<int:contestId>/', views.contest,name='contest'),
    path('submit/<int:problemid>/' , views.contestSubmission , name="submit")
]
