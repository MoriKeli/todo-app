from django.urls import path
from todo_app.views import *

urlpatterns = [
    path('', index_page, name='landing_page'),
    path('login/', UserLogin.as_view(), name='login'),
    path('signup/', create_user_account, name='signup'),
    path('homepage/', user_homepage, name='homepage'),
    path('profile/', user_profile_page, name='edit_profile'),
    path('completed-tasks/', completed_tasks, name='tasks_completed'),
    path('pending-tasks/', pending_tasks, name='tasks_pending'),
    path('outdated-tasks/', outdated_tasks, name='outdated_tasks'),
    path('update-task-status/<str:pk>/', mark_as_complete, name='task_complete'),
    path('edit-scheduled-task/<str:pk>/', edit_scheduledTask, name='edit_task'),
    path('delete-task/<str:pk>/', delete_scheduledtask, name='delete'),
    path('logout', LogoutUser.as_view(), name='logout'),    
]