from django.urls import path
from . import views

urlpatterns = [
    path('hello/', views.hello),
    path('users/', views.users),
    path('write_user/', views.write_user),
    path('update_user/', views.update_user),
    path('delete_user/', views.delete_user),
    path('delete_all/', views.delete_all),
    path('update_user_avatar/<int:id>/', views.update_user_avatar2),
]