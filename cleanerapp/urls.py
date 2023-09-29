# myapp/urls.py

from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('cleaner_works/', views.cleaner_works, name='cleaner_works'),
    path('staff_works/', views.staff_works, name='staff_works'),
    path('setting_works/', views.setting_works, name='setting_works'),
    path('update_status/<int:work_id>/<str:status>/', views.update_status, name='update_status'),
    path('reset_status/<int:work_id>/<str:status>/', views.reset_status, name='reset_status'),
    path('edit_work/<int:work_id>/', views.edit_work, name='edit_work'),
    path('delete_work/<int:work_id>/', views.delete_work, name='delete_work'),
    path('add_work/', views.add_work, name='add_work'),
    path('workdata-history/', views.get_workdata_history, name='workdata_history'),
    path('submit_verification/<int:work_id>/', views.submit_verification, name='submit_verification'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    # Add other URL patterns as needed
]