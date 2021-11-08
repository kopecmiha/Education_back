from django.urls import path
from . import views

urlpatterns = [
    path('hello/', views.hello),
    path('users/', views.users),
    path('projects/', views.projects),
    path('status/', views.status),
    path('tags/', views.tags),
    path('comments/', views.comments),
    path('events/', views.events),
    path('activities/', views.activities),
    path('cards/', views.cards),

    path('write_user/', views.write_user),
    path('get_user/<int:id>/', views.get_user),
    path('user/get_email/', views.get_user_email),
    path('update_user/', views.update_user),
    path('delete_user/<int:id>', views.delete_user),
    path('update_user_avatar/<int:id>/', views.update_user_avatar2),

    path('delete_all/', views.delete_all),

    path('authorization/', views.authorization),

    path('write_project/', views.write_project),
    path('get_project/<int:id>/', views.get_project),
    path('update_project/', views.update_project),
    path('update_project_image/<int:id>/', views.update_project_image),
    path('delete_project/<int:id>', views.delete_project),

    path('write_status/', views.write_status),
    path('get_user_status/<int:id>/', views.get_user_status),
    path('update_status/', views.update_status),
    path('get_project_status/<int:id>/', views.get_project_status),
    path('delete_status/<int:user>/<int:project>/', views.delete_status),

    path('write_tag/', views.write_tag),path('write_status/', views.write_status),

    path('write_comment/', views.write_comment),
    path('get_project_comment/<int:id>/', views.get_project_comment),
    path('update_comment/', views.update_comment),
    path('delete_comment/<int:user>/<int:project>/', views.delete_comment),

    path('write_event/', views.write_event),
    path('get_project_event/<int:id>/', views.get_project_event),
    path('get_user_event/<int:id>/', views.get_user_event),
    path('update_event/', views.update_event),
    path('delete_event/<int:user>/<int:project>/', views.delete_event),

    path('write_active/', views.write_active),
    path('get_project_active/<int:id>/', views.get_project_active),
    path('get_user_active/<int:id>/', views.get_user_active),
    path('update_active_file/<int:id>/', views.update_active_file),

    path('board/writecolumn/', views.writecolumn),
    path('board/writecard/', views.writecard),
    path('board/getboard/<int:id>/', views.getboard),
    path('board/switch/', views.switch)
]

'''urlpatterns = [
    path('hello/', views.hello),
    path('users/all/', views.users),
    path('projects/all/', views.projects),
    path('status/all/', views.status),
    path('tags/all/', views.tags),
    path('users/write/', views.write_user),
    path('users/get/<int:id>/', views.get_user),
    path('users/update/', views.update_user),
    path('users/delete/<int:id>/', views.delete_user),
    path('users/delete_all/', views.delete_all),
    path('users/update_user_avatar/<int:id>/', views.update_user_avatar2),
    path('users/authorization/', views.authorization),
    path('projects/write_project/', views.write_project),
    path('projects/get_project/<int:id>/', views.get_project),
    path('projects/update_project/', views.update_project),
    path('projects/update_project_image/<int:id>/', views.update_project_image),
    path('projects/delete_project/<int:id>/', views.delete_project),
    path('status/write_status/', views.write_status),
    path('users/get_user_status/<int:id>/', views.get_user_status),
    path('status/update_status/', views.update_status),
    path('project/get_project_status/<int:id>/', views.get_project_status),
    path('status/delete_status/<int:user>/<int:project>/', views.delete_status),
    path('tag/write_tag/', views.write_tag),
]'''