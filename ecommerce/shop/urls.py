from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('cart/', views.cart, name='cart'),
    path('product/<int:pk>/edit/', views.product_edit, name='product_edit'),  # URL for editing a product
    path('product/<int:pk>/delete/', views.product_delete, name='product_delete'),  # URL for deleting a product
]

# urlpatterns = [
#     path('', views.home, name='home'),
#     path('products/', views.product_list, name='product_list'),
#     path('cart/', views.cart, name='cart'),
#     path('edit/<int:pk>/', views.product_edit, name='product_edit'),  # Ensure this matches the view
# ]
