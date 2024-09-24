from django.shortcuts import render
import pyrebase
from django.contrib import auth
# Create your views here.

config = {
  "apiKey": "AIzaSyAWb2L1PEKTXMJQLmQvCrqonhfLLXfE1lI",
  "authDomain": "cpanel-5e873.firebaseapp.com",
  "databaseURL": "https://cpanel-5e873.firebaseio.com",
  "projectId": "cpanel-5e873",
  "storageBucket": "cpanel-5e873.appspot.com",
  "messagingSenderId": "579985583952"
};

firebase = pyrebase.initialize_app(config)
fireauth = firebase.auth()

def login_view(request):
    context = {

    }
    return render(request, 'login.html', context)

def postsign_view(request):
    email = request.POST.get('email')
    passw = request.POST.get('pass')

    try:
        user = fireauth.sign_in_with_email_and_password(email, passw)
    except:
        message = "Invalid Credentials"
        return render (request, 'login.html', {"messg":message})
    
    session_id = user['idToken']
    request.session['uid']=str(session_id)
    context = {
        'email' : email
    }
    return render(request, 'postsign.html', context)

def logout(request):
    auth.logout(request)
    return render(request, 'login.html', )
