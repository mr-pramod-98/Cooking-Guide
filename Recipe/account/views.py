from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth


# Create your views here.
def register(request):
    # IF THE REQUEST METHOD IS POST EXECUTE if BLOCK
    if request.method == 'POST':

        # READING THE SENT DATA FROM THE REGISTRATION FORM
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password']
        password2 = request.POST['password_conf']

        if password1 == password2:

            if User.objects.filter(username=username).exist():
                
                # IF THE USERNAME IS TAKEN THEN REDIRECTING THE USER BACK TO THE "register" PAGE
                messages.info(request, "username taken")
                return redirect('register')

            else:
                # CREATING A USER RECORD IN THE "User" TABLE
                user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name, email=email, password=password2)
                
                # SAVING THE CHANGES
                user.save()
                
                # REDIRECTING TO "login" PAGE AFTER SUCCESSFUL REGISTRATION
                return redirect('login')
        else:

            # IF THE PASSWORD DOES NOT MATCH THEN REDIRECTING THE USER BACK TO THE "register" PAGE
            messages.info(request, "password not matching")
            return redirect('register')

    # IF THE REQUEST METHOD IS GET EXECUTE else BLOCK
    else:
        return render(request, 'register.html')


def login(request):
    return render(request, 'login.html')


def logout(request):
    pass
