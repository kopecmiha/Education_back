from django.urls import path
from . import views

urlpatterns = [
    path('hello/', views.hello),
    path('users/', views.users),
    path('projects/', views.projects),
    path('write_user/', views.write_user),
    path('get_user/<int:id>/', views.get_user),
    path('update_user/', views.update_user),
    path('delete_user/<int:id>', views.delete_user),
    path('delete_all/', views.delete_all),
    path('update_user_avatar/<int:id>/', views.update_user_avatar2),
    path('authorization/', views.authorization),
    path('write_project/', views.write_project),
    path('get_project/<int:id>/', views.get_project),
    path('update_project/', views.update_project),
    path('delete_project/<int:id>', views.delete_project),

]