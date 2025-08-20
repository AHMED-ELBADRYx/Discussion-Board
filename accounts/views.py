from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.views.decorators.csrf import csrf_protect
from django.middleware.csrf import get_token
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.views.decorators.cache import never_cache
from django.utils.http import url_has_allowed_host_and_scheme
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

# @never_cache
# def login_view(request):
#     """Handle user login with proper redirects and caching headers"""
#     if request.user.is_authenticated:
#         messages.info(request, "You are already logged in!")
#         return redirect('board_list')
    
#     get_token(request)
    
#     if request.method == "POST":
#         form = AuthenticationForm(request, data=request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             login(request, user)
#             messages.success(request, f"Welcome back, {user.username}!")
            
#             # Get next parameter for proper redirect
#             next_url = request.GET.get('next') or request.POST.get('next')
#             redirect_url = next_url if next_url else 'board_list'
            
#             response = HttpResponseRedirect(reverse(redirect_url) if next_url == 'board_list' else next_url)
#             response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
#             response['Pragma'] = 'no-cache'
#             response['Expires'] = '0'
#             return response
#         else:
#             messages.error(request, "Invalid username or password.")
#     else:
#         form = AuthenticationForm()
    
#     return render(request, 'accounts/login.html', {'form': form})

@never_cache
def login_view(request):
    """Handle user login with proper redirects and caching headers"""
    if request.user.is_authenticated:
        messages.info(request, "You are already logged in!")
        return redirect('board_list')
    
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            
            next_url = request.GET.get('next')
            if next_url and url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
                return redirect(next_url)
            return redirect('board_list')
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    
    response = render(request, 'accounts/login.html', {'form': form})
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

@csrf_protect
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
    
    # GET request - show logout confirmation page
    response = render(request, 'accounts/logout.html')
    response['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
    response['Pragma'] = 'no-cache'
    response['Expires'] = '0'
    return response

@csrf_protect
@never_cache
def register_view(request):
    """Handle user registration with proper validation"""
    if request.user.is_authenticated:
        messages.info(request, "You are already logged in!")
        return redirect('board_list')

    get_token(request)
    
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                login(request, user)
                messages.success(request, f"Welcome {user.username}! Registration successful!")
                response = HttpResponseRedirect(reverse('board_list'))
                response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
                response['Pragma'] = 'no-cache'
                response['Expires'] = '0'
                return response
            except Exception as e:
                logger.error(f"Registration error: {e}")
                messages.error(request, "Registration failed. Please try again.")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'accounts/register.html', {'form': form})