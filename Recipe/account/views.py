from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
import mysql.connector


class CreateAccount:

    def __init__(self):
        self.create_connection()

    def create_connection(self):
        self.mydatabase = mysql.connector.connect(host='localhost', user='root', passwd='password', database='recipe_test')
        self.mycursor = self.mydatabase.cursor()

    # "create_table_by_username" METHOD CREATES A TABLE BY THE "username" OF THE USER IN THE SPECIFIED DATABASE
    def create_table_by_username(self, table_name):
        self.mycursor.execute(''' 
                                    CREATE TABLE ''' + table_name + '''(
                                    TITLE VARCHAR(200) PRIMARY KEY,
                                    INGREDIENTS LONGTEXT,
                                    DIRECTIONS LONGTEXT);
                                ''')


# Create your views here.

# "register" METHOD IS CALLED WHET THE USER REQUEST FOR "register" PAGE
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

            if User.objects.filter(username=username).exists():

                # IF THE USERNAME IS TAKEN THEN REDIRECTING THE USER BACK TO THE "register" PAGE
                messages.info(request, "username taken")
                return redirect('register')

            else:
                # CREATE AN ACCOUNT BY THE "username" OF USER
                new_account = CreateAccount()
                new_account.create_table_by_username(username)

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


# "login" METHOD IS CALLED WHET THE USER REQUEST FOR "login" PAGE
def login(request):

    # IF THE REQUEST METHOD IS POST EXECUTE if BLOCK
    if request.method == "POST":

        # FETCHING "username" AND "password" FROM THE LOGIN PAGE
        username = request.POST['username']
        password = request.POST['password']

        # AUTHENTICATING THE USER
        # "user" EQUALS "None" IF THE "username" DOES NOT MATCH WITH IT'S THE CORRESPONDING "password"
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)

            # REDIRECTING TO "cook_guide/<username>" PAGE AFTER SUCCESSFUL LOGIN
            # EXAMPLE: /cook_guide/pramod
            return redirect('/cook_guide/' + username)
        else:
            messages.info(request, "invalid username or password")

            # REDIRECTING BACK TO "login" IF THE "username" DOES NOT MATCH WITH IT'S THE CORRESPONDING "password"
            return redirect('login')

    # IF THE REQUEST METHOD IS GET EXECUTE else BLOCK
    else:
        return render(request, 'login.html')


# "logout" METHOD IS CALLED WHET THE USER LOGOUT'S OF HIS ACCOUNT
def logout(request):

    # LOGGING-OUT THE USER
    auth.logout(request)

    # REDIRECTING THE USER TO THE HOME PAGE
    return redirect('/')
