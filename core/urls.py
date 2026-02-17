from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.landing, name='landing'),
    path('login/', views.CoreLoginView.as_view(), name='login'),
    path('logout/', views.CoreLogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('pricing/', views.pricing, name='pricing'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('apps/new/', views.create_app, name='create_app'),
    path('apps/<int:pk>/', views.app_detail, name='app_detail'),
    path('apps/<int:pk>/preview/', views.app_preview, name='app_preview'),
]
