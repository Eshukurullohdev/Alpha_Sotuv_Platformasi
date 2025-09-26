from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib import messages
from .models import Product
from django.shortcuts import render, get_object_or_404


def home(request):
    product = Product.objects.all()
    context = {'product': product}
    return render(request, 'index.html', context)
def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, username=email, password=password)

        if user is not None:
            auth_login(request, user)
            messages.success(request, f"Welcome back, {user.first_name}!")
            return redirect("home")
        else:
            messages.error(request, "Invalid email or password")
            return render(request, "login.html")

    return render(request, "login.html")

def register(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

      
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "Invalid email address")
            return render(request, "register.html")

      
        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return render(request, "register.html")

        try:
            validate_password(password1)
        except ValidationError as e:
            for err in e:
                messages.error(request, err)
            return render(request, "register.html")

       
        if User.objects.filter(email=email).exists():
            messages.error(request, "This email is already registered")
            return render(request, "register.html")

       
        user = User.objects.create_user(
            username=email,
            first_name=name,
            email=email,
            password=password1,
        )


        auth_login(request, user)
        messages.success(request, "Account created successfully!")
        return redirect("home")

    return render(request, "register.html")

def contact(request):
    return render(request, 'contact.html')


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, "product_detail.html", {"product": product})



