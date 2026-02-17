from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib import messages

from .models import App
from .forms import SignUpForm, CreateAppForm


def landing(request):
    """Landing page: Launch your own Lovable. Make money. Deploy on KloudBean."""
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
            messages.success(request, 'Account created. Start building.')
            return redirect('core:dashboard')
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = SignUpForm()
    return render(request, 'core/signup.html', {'form': form})


@login_required
def dashboard(request):
    """User dashboard: list of their apps."""
    apps = request.user.apps.all()
    return render(request, 'core/dashboard.html', {'apps': apps})


@login_required
def create_app(request):
    """Create a new app (Lovable-style: name + description)."""
    if request.method == 'POST':
        form = CreateAppForm(request.POST)
        if form.is_valid():
            app = form.save(commit=False)
            app.user = request.user
            app.status = 'building'
            app.save()
            messages.success(request, f'"{app.name}" is being built. You\'re on your way.')
            return redirect('core:app_detail', pk=app.pk)
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = CreateAppForm()
    return render(request, 'core/create_app.html', {'form': form})


@login_required
def app_detail(request, pk):
    """App detail: status, preview placeholder, deploy CTA."""
    app = get_object_or_404(App, pk=pk, user=request.user)
    return render(request, 'core/app_detail.html', {'app': app})


def pricing(request):
    """Pricing page: Free, Pro, Billionaire tiers."""
    return render(request, 'core/pricing.html')


def app_preview(request, pk):
    """Public preview of an app (placeholder / generated page)."""
    app = get_object_or_404(App, pk=pk)
    return render(request, 'core/app_preview.html', {'app': app})
