from django.shortcuts import render

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Product
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .forms import ProductForm
from django.db.models import Sum, F
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from django.http import HttpResponse, HttpResponseForbidden
import csv
from django.core.serializers.json import DjangoJSONEncoder
import json

def export_products_csv(request):
    if not request.user.is_authenticated:
        return redirect('login_user')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="products.csv"'

    writer = csv.writer(response)
    writer.writerow(['ID', 'Name', 'Quantity', 'Price'])  # Adjusted columns

    # ✅ Corrected for loop
    products = Product.objects.all()
    for p in products:
        writer.writerow([p.id, p.name, p.quantity, p.price])

    return response


@login_required
def dashboard(request):
    # profile = request.user.profile
    # if profile.role == 'viewer':
    #     return HttpResponseForbidden("Viewers can access the dashboard. but not change the details")
    user = request.user

    # 🕵️ Search
    query = request.GET.get('q')
    if query:
        products = Product.objects.filter(name__icontains=query, added_by=user)
    else:
        products = Product.objects.filter(added_by=user)

    # ⚠️ Low-stock
    low_stock_products = products.filter(quantity__lt=5)

    # ➕ Add new product
    if request.method == 'POST':
        name = request.POST.get('name')
        quantity = request.POST.get('quantity')
        price = request.POST.get('price')

        if name and quantity and price:
            Product.objects.create(
                name=name,
                quantity=quantity,
                price=price,
                added_by=user
            )
            return redirect('dashboard')

    # 📊 Dashboard stats
    total_products = products.count()
    total_value = products.aggregate(value=Sum(F('quantity') * F('price')))['value'] or 0
    low_stock_count = low_stock_products.count()
    
    product_names = [p.name for p in products]
    product_quantities = [p.quantity for p in products]
    product_values = [p.price * p.quantity for p in products]


    return render(request, 'dashboard.html', {
        'products': products,
        'low_stock_products': low_stock_products,
        'total_products': total_products,
        'total_value': total_value,
        'low_stock_count': low_stock_count,
        'user': user,
        'product_names': json.dumps(product_names, cls=DjangoJSONEncoder),
        'product_quantities': json.dumps(product_quantities, cls=DjangoJSONEncoder),
        'product_values': json.dumps(product_values, cls=DjangoJSONEncoder),
    })


@login_required
def delete_product(request, product_id):
    product = Product.objects.get(id=product_id, added_by=request.user)
    product.delete()
    return redirect('dashboard')



def register_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
        else:
            # ✅ Secure password hashing
            User.objects.create_user(username=username, password=password)
            messages.success(request, 'Registration successful! Please login.')
            return redirect('login_user')

    return render(request, 'register.html')

def login_user(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Basic validation
        if not username or not password:
            messages.error(request, 'Both username and password are required')
            return render(request, 'login.html')
        
        # Check if user exists (without password check)
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.error(request, 'Invalid username')
            return render(request, 'login.html')
        
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You have been logged in successfully!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Incorrect password')
            return render(request, 'login.html')
    
    return render(request, 'login.html')


def logout_user(request):
    logout(request)
    return redirect('login_user')

def edit_product(request, product_id):
    if not request.user.is_authenticated:
        return redirect('login_user')

    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ProductForm(instance=product)

    return render(request, 'edit_product.html', {'form': form, 'product': product})


@login_required
def import_products_csv(request):
    if request.method == 'POST' and request.FILES['csv_file']:
        csv_file = request.FILES['csv_file']
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'File is not CSV type')
            return redirect('dashboard')

        decoded = csv_file.read().decode('utf-8').splitlines()
        reader = csv.reader(decoded)
        next(reader)  # Skip header

        for row in reader:
            try:
                Product.objects.create(
                    name=row[0],
                    quantity=int(row[1]),
                    price=float(row[2]),
                    added_by=request.user
                )
            except Exception as e:
                messages.error(request, f'Error in row: {row} - {e}')

        messages.success(request, 'Products imported successfully.')
        return redirect('dashboard')

    return redirect('dashboard')



@login_required
def export_products_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="products.pdf"'

    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter

    p.setFont("Helvetica-Bold", 14)
    p.drawString(200, height - 50, "Inventory Product List")

    p.setFont("Helvetica", 12)
    y = height - 80

    products = Product.objects.filter(added_by=request.user)

    for product in products:
        line = f"{product.name} - Qty: {product.quantity} - INR {product.price}"
        p.drawString(50, y, line)
        y -= 20
        if y < 50:
            p.showPage()
            p.setFont("Helvetica", 12)
            y = height - 50

    p.save()
    return response
