from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.landing, name='landing'),
    path('login/', views.CoreLoginView.as_view(), name='login'),
    path('logout/', views.CoreLogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('pricing/', views.pricing, name='pricing'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('profile/password/', views.CorePasswordChangeView.as_view(), name='password_change'),
    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='core/password_reset.html',
        email_template_name='core/email/password_reset_body.txt',
        subject_template_name='core/email/password_reset_subject.txt',
        success_url=reverse_lazy('core:password_reset_done'),
    ), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='core/password_reset_done.html',
    ), name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='core/password_reset_confirm.html',
        success_url=reverse_lazy('core:password_reset_complete'),
    ), name='password_reset_confirm'),
    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='core/password_reset_complete.html',
    ), name='password_reset_complete'),
    path('apps/new/', views.create_app, name='create_app'),
    path('apps/<int:pk>/', views.app_detail, name='app_detail'),
    path('apps/<int:pk>/sections/', views.app_sections_save, name='app_sections_save'),
    path('apps/<int:pk>/preview/', views.app_preview, name='app_preview'),
    path('a/<slug:slug>/', views.app_public, name='app_public'),
]
