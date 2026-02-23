from .views import ProductCreateView, ProductUpdateView, ProductDeleteView
from django.urls import path
from . import views
from .views import (
    WarehouseListView,
    ProductListView,
    StockItemListView,
)

app_name = 'main'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('warehouses/', WarehouseListView.as_view(), name='warehouses'),
    path('products/', ProductListView.as_view(), name='products'),
    path('stock/', StockItemListView.as_view(), name='stock'),
    path('products/add/', ProductCreateView.as_view(), name='product_add'),
    path('products/<int:pk>/edit/', ProductUpdateView.as_view(), name='product_edit'),
    path('products/<int:pk>/delete/', ProductDeleteView.as_view(), name='product_delete'),
    path('register/', views.register, name='register'),
]