from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'platform'

urlpatterns = [
    path('', views.landing, name='landing'),
    path('login/', views.PlatformLoginView.as_view(), name='login'),
    path('logout/', views.PlatformLogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('pricing/', views.pricing, name='pricing'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('apps/new/', views.create_app, name='create_app'),
    path('apps/<int:pk>/', views.app_detail, name='app_detail'),
    path('apps/<int:pk>/preview/', views.app_preview, name='app_preview'),
]
