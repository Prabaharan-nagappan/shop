from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from .forms import ProductForm
from django.contrib import messages
from django.db.models import Q  # For advanced search


def product_edit(request, pk):
    """
    View to edit an existing product.
    """
    product = get_object_or_404(Product, pk=pk)  # Fetch the product to edit
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()  # Save the updated product
            return redirect('home')  # Redirect to home or product list
    else:
        form = ProductForm(instance=product)  # Pre-fill the form with the product data
    return render(request, 'shop/product_edit.html', {'form': form, 'product': product})

def product_list(request):
    """
    View to display a list of products.
    """
    products = Product.objects.all()
    query = request.GET.get('search', '')
    if query:
        products = products.filter(name__icontains=query)

    return render(request, 'shop/product_list.html', {'products': products})



def home(request):
    # Get query parameters for filtering and searching
    query = request.GET.get('search', '')
    category = request.GET.get('category', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')

    # Start with all products
    products = Product.objects.all()

    # Filter by search query
    if query:
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )

    # Filter by category
    if category:
        products = products.filter(category__iexact=category)

    # Filter by price range
    if min_price and max_price:
        products = products.filter(price__gte=min_price, price__lte=max_price)

    # Handle adding new products
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

    return render(
        request,
        'shop/home.html',
        {
            'products': products,
            'form': form,
            'query': query,
            'category': category,
            'min_price': min_price,
            'max_price': max_price,
        },
    )



def cart(request):
    """
    View to display items in the cart.
    """
    # Example: Simulating a cart stored in the session
    cart = request.session.get('cart', {})  # Retrieve cart from session or use an empty dict
    cart_items = []
    total_price = 0

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, pk=product_id)
        cart_items.append({
            'product': product,
            'quantity': quantity,
            'total_price': product.price * quantity
        })
        total_price += product.price * quantity

    return render(request, 'shop/cart.html', {'cart_items': cart_items, 'total_price': total_price})

def add_to_cart(request, product_id):
    """
    Add a product to the cart.
    """
    cart = request.session.get('cart', {})
    cart[product_id] = cart.get(product_id, 0) + 1  # Increment quantity
    request.session['cart'] = cart  # Save cart back to session
    return redirect('cart')

# Product Delete View - Handles deleting a product
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, f"Product '{product.name}' deleted successfully!")
        return redirect('home')
    return render(request, 'shop/product_delete.html', {'product': product})
