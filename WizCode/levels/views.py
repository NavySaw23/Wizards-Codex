
from login.models import User
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from projects.models import FlowerData  
@login_required
def lvl_view_1(request):
    # Get the latest flower data for the current user
    user_data = FlowerData.objects.filter(user=request.user).order_by('-created_at').first()
    
    if user_data and isinstance(user_data.data, list):
        # Extract the required information
        flower_info = []
        for flower in user_data.data:
            if isinstance(flower, dict):
                flower_info.append({
                    'ID': flower.get('ID', 'N/A'),
                    'Quality': flower.get('Quality', 'N/A'),
                    'Size': f"{flower.get('Sepal.Length', 'N/A')} x {flower.get('Sepal.Width', 'N/A')}"
                })
        
        context = {
            'flower_info': flower_info
        }
    else:
        context = {
            'flower_info': []
        }
    
    return render(request, 'level1.html', context)

def lvl_view_2(request):
   context = {
   }
  