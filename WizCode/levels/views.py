
from login.models import User
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.

def lvl_view_1(request):
    context = {

    }
    return render(request, 'level1_Page.html', context)