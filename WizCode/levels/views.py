
from login.models import User
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.

def lvl_view_1(request):
    sizex = 5
    context = {
       's1'  : sizex

    }
    return render(request, 'level1_Page.html', context)