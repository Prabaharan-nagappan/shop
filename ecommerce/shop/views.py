from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from .forms import ProductForm
from django.contrib import messages  # For flash messages

# Home View - Displays products and handles adding new products
def home(request):
    products = Product.objects.all()  # Get all products
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Product added successfully!")
            return redirect('home')
        else:
            messages.error(request, "Error adding product. Please check the form.")
    else:
        form = ProductForm()
    return render(request, 'shop/home.html', {'products': products, 'form': form})

# Product List View - Displays all products
def product_list(request):
    products = Product.objects.all()
    return render(request, 'shop/product_list.html', {'products': products})

# Cart View - Displays items in the cart
def cart(request):
    # Assuming a Cart model is used and linked to the user
    cart_items = Cart.objects.filter(user=request.user)
    return render(request, 'shop/cart.html', {'cart_items': cart_items})

# Product Edit View - Handles editing an existing product
def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product updated successfully!")
            return redirect('home')
        else:
            messages.error(request, "Error updating product. Please check the form.")
    else:
        form = ProductForm(instance=product)
    return render(request, 'shop/product_edit.html', {'form': form, 'product': product})

# Product Delete View - Handles deleting a product
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, f"Product '{product.name}' deleted successfully!")
        return redirect('home')
    return render(request, 'shop/product_delete.html', {'product': product})
