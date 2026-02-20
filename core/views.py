import json
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.urls import reverse_lazy
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from .models import App
from .forms import SignUpForm, CreateAppForm, AppEditForm, PasswordChangeForm
from .defaults import get_default_sections


def landing(request):
    if request.user.is_authenticated:
        return redirect('core:dashboard')
    return render(request, 'core/landing.html')


class CoreLoginView(LoginView):
    template_name = 'core/login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('core:dashboard')


class CoreLogoutView(LogoutView):
    next_page = reverse_lazy('core:landing')


def signup(request):
    if request.user.is_authenticated:
        return redirect('core:dashboard')
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created. Create your first app!')
            return redirect('core:create_app')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = SignUpForm()
    return render(request, 'core/signup.html', {'form': form})


@login_required
def dashboard(request):
    apps = request.user.apps.all()
    return render(request, 'core/dashboard.html', {'apps': apps})


@login_required
def create_app(request):
    if request.method == 'POST':
        form = CreateAppForm(request.POST)
        if form.is_valid():
            app = form.save(commit=False)
            app.user = request.user
            app.status = 'building'
            app.sections = get_default_sections(app.template)
            app.save()
            messages.success(request, f'"{app.name}" created. Edit sections and publish when ready.')
            return redirect('core:app_detail', pk=app.pk)
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = CreateAppForm()
    return render(request, 'core/create_app.html', {'form': form})


@login_required
def app_detail(request, pk):
    app = get_object_or_404(App, pk=pk, user=request.user)
    if request.method == 'POST':
        form = AppEditForm(request.POST, instance=app)
        if form.is_valid():
            form.save()
            messages.success(request, 'App updated.')
            return redirect('core:app_detail', pk=app.pk)
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = AppEditForm(instance=app)
    sections_json = json.dumps(app.sections, indent=2) if app.sections else '[]'
    return render(request, 'core/app_detail.html', {'app': app, 'form': form, 'sections_json': sections_json})


@login_required
@require_http_methods(['POST'])
def app_sections_save(request, pk):
    app = get_object_or_404(App, pk=pk, user=request.user)
    try:
        data = json.loads(request.body)
        if isinstance(data, list):
            app.sections = data
            app.save(update_fields=['sections', 'updated_at'])
            return JsonResponse({'ok': True})
    except (json.JSONDecodeError, TypeError):
        pass
    return JsonResponse({'ok': False}, status=400)


def app_public(request, slug):
    """Public view of an app by slug (published or preview for owner)."""
    app = get_object_or_404(App, slug=slug)
    is_owner = request.user.is_authenticated and app.user_id == request.user.pk
    if not app.published and not is_owner:
        return redirect('core:landing')
    return render(request, 'core/app_public.html', {
        'app': app,
        'is_preview': not app.published and is_owner,
    })


def pricing(request):
    return render(request, 'core/pricing.html')


def app_preview(request, pk):
    app = get_object_or_404(App, pk=pk)
    return redirect('core:app_public', slug=app.slug)


@login_required
def profile(request):
    return render(request, 'core/profile.html')


class CorePasswordChangeView(PasswordChangeView):
    template_name = 'core/password_change.html'
    success_url = reverse_lazy('core:profile')
    form_class = PasswordChangeForm
