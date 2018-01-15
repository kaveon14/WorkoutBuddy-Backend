from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from WorkoutBuddy.models import Profile
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def android_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                json = {
                    'username':username,
                    'password':password,
                    'id':user.id,
                    'error':False,
                    'message':'Successfully Logged In'
                }
                return JsonResponse(json)
            else:
                json = {
                    'username': None,
                    'password': None,
                    'id': 0,
                    'error': True,
                    'message': 'Wrong Username or Password'
                }
                return JsonResponse(json)
        else:
            json = {
                'username': None,
                'password': None,
                'id': 0,
                'error': True,
                'message': 'Wrong Username or Password'
            }
            return JsonResponse(json)

def signup(request):#need to also create a new profile here
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            profile = Profile(user=user)
            profile.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})
