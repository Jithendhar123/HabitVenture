from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns=[
    path("dashboard/", views.dashboard, name="dashboard"),
    path('register/', views.register, name="register"),
    path('login/', views.CustomLoginView.as_view(), name="login"),
    path('logout/', auth_views.LogoutView.as_view(), name="logout"),
    path('create/', views.create_habit, name="create"),
    path('complete/<int:id>', views.complete_habit, name="complete"),
    path('completed_graphs/', views.completed_habits_graph, name="graph"),
    path('update/<int:pk>/', views.update_habit, name='habit_update'),
    path('delete/<int:pk>/', views.delete_habit  , name='habit_delete'),
    path('list/', views.habits_list, name='habit_list')

]