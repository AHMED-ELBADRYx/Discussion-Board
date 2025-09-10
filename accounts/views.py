from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.views.decorators.cache import never_cache
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import UpdateView
from django.urls import reverse_lazy
from .forms import UserUpdateForm
from django.contrib.auth.models import User

@never_cache
def login_view(request):
    """Handle user login with proper redirects and caching headers"""
    if request.user.is_authenticated:
        messages.info(request, "You are already logged in!")
        return redirect('board_list')
    
    next_page = request.GET.get('next') or request.POST.get('next') or 'board_list'

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            update_session_auth_hash(request, user)  # Important for password change
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect(next_page)
        
        else:
            messages.error(request, "Invalid username or password.")
            return render(request, 'accounts/login.html', {'form': form, 'next': next_page})
    else:
        form = AuthenticationForm()

    return render(request, 'accounts/login.html', {'form': form, 'next': next_page})

@login_required
@require_http_methods(["GET", "POST"])
@never_cache
def logout_view(request):
    """Handle user logout with proper CSRF protection"""
    if request.method == "POST":
        username = request.user.username
        logout(request)
        messages.success(request, f"Goodbye {username}! You have been logged out successfully.")
        return redirect('login')
    return render(request, 'accounts/logout.html')

@never_cache
def register_view(request):
    """Handle user registration with proper validation"""
    if request.user.is_authenticated:
        messages.info(request, "You are already logged in!")
        return redirect('board_list')
    
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
                user = form.save()
                if user.is_active:
                    login(request, user)
                    messages.success(request, f"Welcome {user.username}! Registration successful!")
                else:
                    messages.info(request, "Registration successful! Please wait for activation.")
                return redirect('board_list')

        else:
            messages.error(request, "Please correct the errors below.")
            return render(request, 'accounts/register.html', {'form': form})
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form})

class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'accounts/profile_update.html'
    success_message = "Your profile has been updated successfully!"
    success_url = reverse_lazy('board_list')
    
    def get_object(self):
        return self.request.user