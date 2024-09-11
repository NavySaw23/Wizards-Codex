from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login, logout
from .middlewares import auth, guest 
# Create your views here.

def homepage_view(request):
    return render(request, 'homepage.html')

@guest
def register_view(request):
    if request.method =='POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user= form.save()
            login(request,user)
            return redirect('dashboard')
    else:
        initial_data ={'username':'','password1':'','password2':''}
        form = AuthenticationForm(initial=initial_data)
    return render(request,'auth/register.html',{'form':form})
@guest
def login_view(request):
    if request.method =='POST':
        form = AuthenticationForm(request,data=request.POST)
        
        if form.is_valid():
            user= form.get_user()
            login(request,user)
            return redirect('dashboard')
    else:
        initial_data ={'username':'','password':''}
        form = UserCreationForm(initial=initial_data)
    return render(request,'auth/login.html',{'form':form})
@auth
def dashboard(request):
    return render(request, 'dashboard.html')
def logout_view(request):
    logout(request)
    return  redirect('login')

