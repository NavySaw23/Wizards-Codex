from login.models import User
from django.shortcuts import render, get_object_or_404,redirect
from django.http import HttpResponseRedirect, JsonResponse
from .forms import RegistrationForm

from django.contrib.auth.models import User
from django.contrib import messages

from django.contrib.auth import login,logout,authenticate, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required

from django.views.decorators.csrf import csrf_exempt
import json
import random

def registrationView(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if cd['password'] == cd['confirm_password']:
                obj = form.save(commit=False)
                obj.set_password(obj.password)
                obj.save()
                messages.success(request, 'You have been registered.')
                return redirect('login')
            else:
                return render(request, "registration.html", {'form': form, 'note': 'password must match'})
    else:
        form = RegistrationForm()

    return render(request, "registration.html", {'form': form})


def loginView(request):
    if request.method == "POST":
        usern = request.POST.get('username')
        passw = request.POST.get('password')
        user = authenticate(request, username=usern, password=passw)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.success(request, 'Invalid username or password!')
            return render(request, "login.html")
    else:
        return render(request, "login.html")


@login_required
def logoutView(request):
    logout(request)
    return redirect('home')

@login_required
def get_user_data(request):
    user_data = FlowerData.objects.filter(user=request.user).order_by('-created_at').first()
    if user_data:
        return JsonResponse({
            'status': 'success',
            'score': user_data.score,
            'flower_data': user_data.data,
            'created_at': user_data.created_at
        })
    else:
        return JsonResponse({'status': 'error', 'message': 'No data found for this user'})

from .models import FlowerData

@csrf_exempt
def update_flower_count(request):
    print("Function called: update_flower_count")
    if request.method == 'POST':
        print("Request method: POST")
        try:
            data = json.loads(request.body)
            print("Received data:", data)
            flower_count = data.get('flowerCount', 0)
            print(f"Flower count: {flower_count}")
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON data'})

        # Generate list with random data
        flower_data = []
        species = ['setosa', 'versicolor', 'virginica']
        good_count = int(flower_count * 0.7)  # 70% good quality

        print("Generating flower data...")
        for i in range(flower_count):
            quality = 'good' if i < good_count else 'bad'
            flower = {
                'ID': i + 1,
                'Sepal.Length': round(random.uniform(4.0, 7.9), 1),
                'Sepal.Width': round(random.uniform(2.0, 4.4), 1),
                'Petal.Length': round(random.uniform(1.0, 6.9), 1),
                'Petal.Width': round(random.uniform(0.1, 2.5), 1),
                'Species': random.choice(species),
                'Petal_Count': random.randint(3, 8),
                'Price': round(random.uniform(5.0, 50.0), 2),
                'Quality': quality
            }
            flower_data.append(flower)
            print(f"Generated flower: {flower}")

        # Calculate a simple score based on the number of flowers
        score = flower_count * 10
        print(f"Calculated score: {score}")

        # Save the data and score for the current user
        if request.user.is_authenticated:
            try:
                flower_data_obj = FlowerData.objects.create(user=request.user, data=flower_data, score=score)
                print(f"Data saved for user: {request.user.username}")
                print(f"Saved object ID: {flower_data_obj.id}")
            except Exception as e:
                print(f"Error saving data: {e}")
                return JsonResponse({'status': 'error', 'message': 'Failed to save data'})
        else:
            print("User not authenticated")
            return JsonResponse({'status': 'error', 'message': 'User not authenticated'})

        print(f"Flower Data for {request.user.username} (Count: {flower_count}):")
        for flower in flower_data:
            print(flower)

        return JsonResponse({'status': 'success', 'message': f'Received {flower_count} flowers'})
    else:
        print(f"Invalid request method: {request.method}")
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})