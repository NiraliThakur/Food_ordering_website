from django.shortcuts import render, HttpResponseRedirect
from django.contrib.auth.models import User, auth
from django.contrib import messages

# Create your views here.
def register(request):
    if request.method=='POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1==password2:
            if User.objects.filter(username=username).exists():
                messages.info(request, "Username already exist")
                return HttpResponseRedirect("/accounts/register")
            elif User.objects.filter(email=email).exists():
                messages.info(request, "Email already have account")
                return HttpResponseRedirect('/accounts/register')
            else:
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password1
                    )
                user.save()
                auth.login(request,user, "Account created")
                return HttpResponseRedirect('Food_ordering_app:index')
        else:
            messages.info(request, "Password does not matched")
            return HttpResponseRedirect('/accounts/resigter')
    else:
        return render(request,'register.html')
    

def login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return HttpResponseRedirect('/Food_ordering_app/index')
        else:
            messages.info(request, 'Invalid user name or password')
            return HttpResponseRedirect('/accounts/login')
        
    return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    messages.info(request, 'You have been logged out')
    return HttpResponseRedirect('/accounts/login')

