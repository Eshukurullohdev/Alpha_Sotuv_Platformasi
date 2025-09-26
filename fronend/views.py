from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages

# Create your views here.

def home(request):
    return render(request, 'index.html')
def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Foydalanuvchini tekshirish (username sifatida email ishlatilgan)
        user = authenticate(request, username=email, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect("home")  # login bo‘lsa home sahifaga yo‘naltiramiz
        else:
            messages.error(request, "Email yoki parol xato")
            return render(request, "login.html")

    return render(request, "login.html")

def register(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        # Parollarni tekshirish
        if password1 != password2:
            messages.error(request, "Passwords do not match")
            return render(request, "register.html")

        # Email borligini tekshirish
        if User.objects.filter(email=email).exists():
            messages.error(request, "This email is already registered")
            return render(request, "register.html")

        # Foydalanuvchi yaratish
        user = User.objects.create_user(
            username=email,
            first_name=name,
            email=email,
            password=password1,
        )

        # Sessiyaga kiritish
        auth_login(request, user)

        return redirect("home")

    return render(request, "register.html")

def contact(request):
    return render(request, 'contact.html')