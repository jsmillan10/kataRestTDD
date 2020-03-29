from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('addUser/', views.add_user_view, name='addUser'),
    path('login/', views.login_view, name='login'),
    path('updateUser/', views.update_user, name='updateUser'),
    path('updatePermission/', views.update_permission_user, name='updateUser')
]