from login.models import User
import logging
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

logger = logging.getLogger(__name__)

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


@login_required
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
                # Check if a FlowerData object already exists for the user
                flower_data_obj = FlowerData.objects.filter(user=request.user).first()
                
                if flower_data_obj:
                    # If level is 1, update it to 2
                    if flower_data_obj.level == 10:
                        flower_data_obj.level = 20
                        flower_data_obj.save()
                        print(f"Updated level for user: {request.user.username} to 2")

                    # Optionally, update other fields or just save the new flower data
                    flower_data_obj.data = flower_data  # Update with new flower data
                    flower_data_obj.score = score  # Update score
                    flower_data_obj.save()  # Save the updated object
                    print(f"Data updated for user: {request.user.username}")
                else:
                    # Create a new FlowerData object if none exists
                    flower_data_obj = FlowerData.objects.create(user=request.user, data=flower_data, score=score)
                    print(f"New data created for user: {request.user.username}")

            except Exception as e:
                print(f"Error saving data: {e}")
                return JsonResponse({'status': 'error', 'message': 'Failed to save data'})
        else:
            print("User  not authenticated")
            return JsonResponse({'status': 'error', 'message': 'User  not authenticated'})

        print(f"Flower Data for {request.user.username} (Count: {flower_count}):")
        for flower in flower_data:
            print(flower)

        return JsonResponse({'status': 'success', 'message': f'Received {flower_count} flowers'})
    else:
        print(f"Invalid request method: {request.method}")
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

@login_required
@csrf_exempt
def clean_flower_data(request):
    try:
        # Log the raw request body for debugging
        logger.info(f"Raw request body: {request.body}")

        # Parse the JSON body
        try:
            body_data = json.loads(request.body)
            logger.info(f"Parsed body data type: {type(body_data)}")
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {e}")
            return JsonResponse({
                'status': 'error',
                'message': f'Could not parse JSON: {str(e)}'
            }, status=400)

        # Extract flower data
        frontend_flower_data = body_data.get('flower_data', [])
        # logger.info(f"Frontend flower data type: {type(frontend_flower_data)}")
        # logger.info(f"Frontend flower data length: {len(frontend_flower_data)}")
        
        # Validate frontend flower data
        if not isinstance(frontend_flower_data, list):
            logger.error(f"Invalid frontend flower data type: {type(frontend_flower_data)}")
            return JsonResponse({
                'status': 'error',
                'message': 'Frontend flower data must be a list'
            }, status=400)

        # Get the latest FlowerData for the user
        flower_data_obj = FlowerData.objects.filter(user=request.user).first()
        
        if not flower_data_obj or not flower_data_obj.data:
            return JsonResponse({
                'status': 'success', 
                'message': 'No data to clean',
                'original_count': 0,
                'cleaned_count': 0
            })

        # Ensure data is a list
        if isinstance(flower_data_obj.data, str):
            try:
                flower_data_obj.data = json.loads(flower_data_obj.data)
            except json.JSONDecodeError:
                logger.error("Could not parse stored flower data")
                return JsonResponse({
                    'status': 'error',
                    'message': 'Invalid stored data format'
                }, status=400)

        # Extract frontend flower IDs
        frontend_flower_ids = [
            int(flower.get('id')) 
            for flower in frontend_flower_data 
            if flower.get('id') is not None
        ]
        logger.info(f"Extracted frontend flower IDs: {frontend_flower_ids}")

        # If no IDs found, return error
        if not frontend_flower_ids:
            logger.warning("No valid flower IDs found")
            return JsonResponse({
                'status': 'error',
                'message': 'No valid flower IDs found'
            }, status=400)

        # Filter the data
        cleaned_data = []
        removed_data = []

        for item in flower_data_obj.data:
            item_id = item.get('id') or item.get('ID')
            
            if item_id is not None and int(item_id) in frontend_flower_ids:
                cleaned_data.append(item)
            else:
                removed_data.append(item)

        logger.info(f"Cleaned data length: {len(cleaned_data)}")
        logger.info(f"Removed data length: {len(removed_data)}")

        # Save the cleaned data
        if cleaned_data:
            flower_data_obj.data = cleaned_data
            flower_data_obj.save()

            return JsonResponse({
                'status': 'success', 
                'message': 'Flower data cleaned successfully',
                'original_count': len(flower_data_obj.data),
                'cleaned_count': len(cleaned_data),
                'removed_count': len(removed_data),
                'frontend_flower_ids': frontend_flower_ids,
                'details': {
                    'first_item_type': type(cleaned_data[0]).__name__,
                    'first_item_keys': list(cleaned_data[0].keys())
                }
            })
        else:
            logger.warning("No data remained after cleaning")
            return JsonResponse({
                'status': 'error',
                'message': 'All data was removed during cleaning',
                'original_count': len(flower_data_obj.data),
                'cleaned_count': 0
            }, status=400)
    
    except Exception as e:
        logger.error(f"Unexpected error cleaning flower data: {e}", exc_info=True)
        return JsonResponse({
            'status': 'error', 
            'message': f'Unexpected error: {str(e)}'
        }, status=500)