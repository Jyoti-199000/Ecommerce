from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('callback/', views.auth_callback, name='auth_callback'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('address/add/', views.add_address, name='add_address'),
    path('api/session/', views.create_session, name='create_session'),
    path('api/me/', views.get_user, name='get_user'),
]
