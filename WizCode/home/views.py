from django.shortcuts import render
from projects.models import FlowerData  


# Create your views here.
def home_view(request, *args, **kwargs):
    if request.user.is_authenticated:
        level = FlowerData.objects.filter(user=request.user).first().level
        if level==0:
            FlowerData.objects.filter(user=request.user).update(level=5)
    else:
        level = 0
        
    context = {
        'user_level': level
    }
    

    if(level==0):
        return render(request, 'home.html', context)
    
    elif(level==5):
        FlowerData.objects.filter(user=request.user).update(level=10)
        return render(request, 'L0_dialogue.html', context)
    
    elif(level==10):
        return render(request, 'home.html', context)
    
    else:
        return render(request, 'home.html', context)

