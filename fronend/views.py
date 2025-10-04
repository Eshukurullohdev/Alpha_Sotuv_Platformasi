from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib import messages
from .models import Product
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from .forms import ProductForm
from .models import Product
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import logout
from django.contrib.auth.decorators import user_passes_test
def home(request):
    product = Product.objects.all()
    context = {'product': product}
    messages.success(request, f" {request.user.username}, saytga xush kelibsiz!")
    return render(request, 'index.html', context)
def login(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.method == "POST":
        username = request.POST.get("username")  # <-- username olish
        password = request.POST.get("password")  # <-- password olish

        user = authenticate(request, username=username, password=password)  # <-- username to‘g‘rilandi

        if user is not None:
            auth_login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect("home")
        else:
            messages.error(request, "Username yoki parol noto‘g‘ri!")
            return render(request, "login.html")

    # GET request bo‘lsa
    if request.user.is_authenticated:
        messages.info(request, f"{request.user.username}, siz allaqachon tizimdasiz!")
        return redirect("home")
    else:
        messages.info(request, "Login sahifasiga xush kelibsiz!")
        return render(request, "login.html")
def logout_view(request):
    logout(request)  # user sessiyasini tozalaydi
    messages.success(request, "Siz tizimdan chiqdingiz!")
    return redirect("home")
def register(request):
    if request.user.is_authenticated:
        return redirect("home")
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
    messages.success(request, f" {request.user.username}, Register sahifasiga xush kelibsiz!")
    return render(request, "register.html")

def contact(request):
    return render(request, 'contact.html')


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, "product_detail.html", {"product": product})



# faqat staff (admin) foydalanuvchilar kira oladi

def admin_page(request):
    products = Product.objects.all()
    users = User.objects.all()

    # yangi product qo‘shish
    if request.method == "POST" and 'name' in request.POST:
        name = request.POST['name']
        narx = request.POST['narx']
        type = request.POST['type']
        tavsif = request.POST.get('tavsif', '')
        img = request.FILES.get('img')

        Product.objects.create(
            name=name, narx=narx, type=type, tavsif=tavsif, img=img
        )
        return redirect('admin_page')

    return render(request, 'admin_page.html', {
        'products': products,
        'users': users
    })


def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        product.name = request.POST['name']
        product.narx = request.POST['narx']
        product.type = request.POST['type']
        product.tavsif = request.POST.get('tavsif', '')
        if request.FILES.get('img'):
            product.img = request.FILES['img']
        product.save()
        return redirect('admin_page')
    return redirect('admin_page')


def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        product.delete()
        return redirect('admin_page')
    return redirect('admin_page')



def superuser_required(view_func):
    decorated_view_func = login_required(
        user_passes_test(lambda u: u.is_superuser)(view_func)
    )
    return decorated_view_func

@superuser_required
def admin_page(request):
    products = Product.objects.all()
    users = User.objects.all()

    # yangi product qo‘shish
    if request.method == "POST" and 'name' in request.POST:
        name = request.POST['name']
        narx = request.POST['narx']
        type = request.POST['type']
        tavsif = request.POST.get('tavsif', '')
        img = request.FILES.get('img')

        Product.objects.create(
            name=name, narx=narx, type=type, tavsif=tavsif, img=img
        )
        return redirect('admin_page')

    return render(request, 'admin_page.html', {
        'products': products,
        'users': users
    })


@superuser_required
def edit_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        product.name = request.POST['name']
        product.narx = request.POST['narx']
        product.type = request.POST['type']
        product.tavsif = request.POST.get('tavsif', '')
        if request.FILES.get('img'):
            product.img = request.FILES['img']
        product.save()
        return redirect('admin_page')
    return redirect('admin_page')


@superuser_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        product.delete()
        return redirect('admin_page')
    return redirect('admin_page')



def superuser_required(view_func):
    decorated_view_func = login_required(user_passes_test(lambda u: u.is_superuser)(view_func))
    return decorated_view_func


def is_superuser(user):
    return user.is_authenticated and user.is_superuser

@superuser_required
def profile_view(request):
    user = request.user

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        pwd = request.POST.get("password", "")
        pwd2 = request.POST.get("password_confirm", "")

        # Username yangilash (bo'sh bo'lmasa)
        if username and username != user.username:
            user.username = username

        # Agar parol maydonlaridan hech biri bo'sh bo'lsa va ikkalasi ham bo'sh bo'lsa -> faqat username yangilanadi
        if pwd or pwd2:
            # 1) Parollar mosligini tekshirish
            if pwd != pwd2:
                messages.error(request, "❌ Parollar mos emas — iltimos ikkala maydonga ham bir xil parol kiriting.")
                return redirect("profile")

            # 2) Parol kuchliligini tekshirish (Django validators)
            try:
                validate_password(pwd, user=user)
            except ValidationError as e:
                for err in e:
                    messages.error(request, err)
                return redirect("profile")

            # 3) Parolni saqlash va sessiyani yangilash
            user.set_password(pwd)
            user.save()
            update_session_auth_hash(request, user)  # foydalanuvchini logout qilmaydi
            messages.success(request, "✅ Foydalanuvchi va parol muvaffaqiyatli yangilandi.")
            return redirect("profile")

        # Agar parol maydonlari bo'sh bo'lsa — faqat username saqlanadi
        user.save()
        messages.success(request, "✅ Profil muvaffaqiyatli yangilandi.")
        return redirect("profile")

    return render(request, "profile.html", {"user": user})

@user_passes_test(superuser_required)
@user_passes_test(is_superuser, login_url='admin_login')

def dashboard(request):
    product_count = Product.objects.count()
    user_count = User.objects.count()

    return render(request, "dashboard.html", {
        "product_count": product_count,
        "user_count": user_count,
    })

def is_superuser(user):
    return user.is_authenticated and user.is_superuser


def admin_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_superuser:
            auth_login(request, user)
            messages.success(request, f"Xush kelibsiz, {user.username} (Admin)!")
            return redirect("admin_page")  # bu keyin admin panelga olib boradi
        else:
            messages.error(request, "Noto‘g‘ri ma’lumot yoki sizda ruxsat yo‘q")
            return render(request, "admin_login.html")

    return render(request, "admin_login.html")


def admin_logout(request):
    logout(request)
    messages.success(request, "Siz tizimdan chiqdingiz ✅")
    return redirect('admin_login')