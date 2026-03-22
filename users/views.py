from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .models import User, UserSession, Address
import requests
from datetime import datetime, timedelta, timezone
import json

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'users/login.html')

@csrf_exempt
def create_session(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    data = json.loads(request.body)
    session_id = data.get('session_id')
    
    if not session_id:
        return JsonResponse({'error': 'session_id required'}, status=400)
    
    try:
        response = requests.get(
            'https://demobackend.emergentagent.com/auth/v1/env/oauth/session-data',
            headers={'X-Session-ID': session_id}
        )
        
        if response.status_code != 200:
            return JsonResponse({'error': 'Invalid session'}, status=400)
        
        user_data = response.json()
        
        user, created = User.objects.get_or_create(
            email=user_data['email'],
            defaults={
                'username': user_data['email'].split('@')[0],
                'profile_picture': user_data.get('picture', ''),
            }
        )
        
        if not created:
            user.profile_picture = user_data.get('picture', '')
            user.save()
        
        session_token = user_data['session_token']
        expires_at = datetime.now(timezone.utc) + timedelta(days=7)
        
        UserSession.objects.create(
            user=user,
            session_token=session_token,
            expires_at=expires_at
        )
        
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        
        response = JsonResponse({
            'user_id': user.user_id,
            'email': user.email,
            'name': user.get_full_name() or user.username,
            'picture': user.profile_picture
        })
        
        response.set_cookie(
            'session_token',
            session_token,
            max_age=7*24*60*60,
            httponly=True,
            secure=True,
            samesite='None'
        )
        
        return response
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

def auth_callback(request):
    return render(request, 'users/auth_callback.html')

def get_user(request):
    session_token = request.COOKIES.get('session_token')
    
    if not session_token:
        return JsonResponse({'error': 'Not authenticated'}, status=401)
    
    try:
        session = UserSession.objects.select_related('user').get(session_token=session_token)
        
        expires_at = session.expires_at
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)
        
        if expires_at < datetime.now(timezone.utc):
            session.delete()
            return JsonResponse({'error': 'Session expired'}, status=401)
        
        user = session.user
        return JsonResponse({
            'user_id': user.user_id,
            'email': user.email,
            'name': user.get_full_name() or user.username,
            'picture': user.profile_picture
        })
        
    except UserSession.DoesNotExist:
        return JsonResponse({'error': 'Invalid session'}, status=401)

@login_required
def logout_view(request):
    session_token = request.COOKIES.get('session_token')
    if session_token:
        UserSession.objects.filter(session_token=session_token).delete()
    
    logout(request)
    response = redirect('home')
    response.delete_cookie('session_token')
    messages.success(request, 'Logged out successfully!')
    return response

@login_required
def profile_view(request):
    addresses = Address.objects.filter(user=request.user)
    
    context = {
        'addresses': addresses,
    }
    return render(request, 'users/profile.html', context)

@login_required
def add_address(request):
    if request.method == 'POST':
        Address.objects.create(
            user=request.user,
            full_name=request.POST.get('full_name'),
            phone=request.POST.get('phone'),
            address_line1=request.POST.get('address_line1'),
            
            city=request.POST.get('city'),
            state=request.POST.get('state'),
            pincode=request.POST.get('pincode'),
            is_default=request.POST.get('is_default') == 'on'
        )
        messages.success(request, 'Address added successfully!')
        return redirect('users:profile')
    
    return render(request, 'users/add_address.html')
