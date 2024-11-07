
from login.models import User
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from projects.models import FlowerData  

def lvl_view_1(request):
    # Initialize flower_info as an empty list by default
    flower_info = []
    
    user_data = FlowerData.objects.filter(user=request.user).order_by('-created_at').first()
    
    if user_data and isinstance(user_data.data, list):
        for flower in user_data.data:
            if isinstance(flower, dict):
                flower_info.append({
                    'ID': flower.get('ID', 'N/A'),
                    'Quality': flower.get('Quality', 'N/A'),
                    'Size': f"{flower.get('Sepal.Length', 'N/A')} x {flower.get('Sepal.Width', 'N/A')}"
                })
    
    # Store flower_info in the session
    request.session['flower_info'] = flower_info
    
    return render(request, 'level1.html', {'flower_info': flower_info})

def lvl_view_2(request):
    # Retrieve flower_info from the session
    flower_info = request.session.get('flower_info', [])
    
    return render(request, 'level2.html', {'flower_info': flower_info})