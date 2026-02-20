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
from .ai import generate_sections_from_prompt


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
            description = (app.description or '').strip()
            sections = generate_sections_from_prompt(description) if description else None
            used_ai = sections is not None
            if not sections:
                sections = get_default_sections(app.template)
            app.sections = sections
            app.save()
            if used_ai:
                messages.success(request, f'"{app.name}" created from your description. Ask for changes with a prompt or publish.')
            else:
                messages.success(request, f'"{app.name}" created. Set DEEPSEEK_API_KEY or OPENAI_API_KEY in env for AI generation, or edit in Settings.')
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
def app_generate(request, pk):
    """Apply AI prompt to update app sections (Lovable-style)."""
    app = get_object_or_404(App, pk=pk, user=request.user)
    try:
        body = json.loads(request.body) if request.body else {}
        prompt = (body.get('prompt') or '').strip()
    except (json.JSONDecodeError, TypeError):
        prompt = ''
    if not prompt:
        return JsonResponse({'ok': False, 'error': 'Prompt required'}, status=400)
    sections, reply = generate_sections_from_prompt(
        prompt, current_sections=app.sections, return_reply=True
    )
    if not sections:
        return JsonResponse({
            'ok': False,
            'error': 'Could not generate. Add DEEPSEEK_API_KEY or OPENAI_API_KEY in your .env or KloudBean env vars, then restart the app.',
        }, status=400)
    app.sections = sections
    app.save(update_fields=['sections', 'updated_at'])
    return JsonResponse({
        'ok': True,
        'sections': sections,
        'message': reply or "I've applied your changes.",
    })


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
