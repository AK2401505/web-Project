from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views
from .views import (
    TaskList, TaskDetail, TaskCreate, TaskUpdate, 
    DeleteView, CustomLoginView, RegisterView
)

urlpatterns = [
    # Authentication URLs
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    
    # Task URLs
    path('', TaskList.as_view(), name='tasks'),
    path('task/<int:pk>/', TaskDetail.as_view(), name='task'),
    path('task-create/', TaskCreate.as_view(), name='task-create'),
    path('task-update/<int:pk>/', TaskUpdate.as_view(), name='task-update'),
    path('task-delete/<int:pk>/', DeleteView.as_view(), name='task-delete'),
    
    # Feature URLs
    path('toggle-theme/', views.toggle_theme, name='toggle_theme'),
    path('toggle-complete/<int:pk>/', views.toggle_complete, name='toggle-complete'),

    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('reset-password/<int:user_id>/', views.reset_password, name='reset_password'),
]
