
from login.models import User
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from projects.models import FlowerData  

def lvl_view_1(request):
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
    
    request.session['flower_info'] = flower_info
    
    return render(request, 'level1_Page.html', {'flower_info': flower_info})

def lvl_view_2(request):
    if not request.user.is_authenticated:
        return render(request, 'level2.html', {'flower_info': []})
    
    try:
        latest_flower_data = FlowerData.objects.filter(user=request.user).latest('created_at')
        flower_info = latest_flower_data.data

        processed_flower_info = []
        for flower in flower_info:
            processed_flower = {
                'ID': flower.get('ID'),
                'Quality': flower.get('Quality'),
                'Size': flower.get('Petal.Length', 'N/A') 
            }
            processed_flower_info.append(processed_flower)
        
        return render(request, 'level2_Page.html', {'flower_info': processed_flower_info})
    
    except FlowerData.DoesNotExist:
        return render(request, 'level2_Page.html', {'flower_info': []})