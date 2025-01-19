from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import SupplierViewSet, ProductViewSet, SaleOrderViewSet, StockMovementViewSet

router = DefaultRouter()
router.register(r'suppliers', SupplierViewSet)
router.register(r'products', ProductViewSet)
router.register(r'sale-orders', SaleOrderViewSet)
router.register(r'stock-movements', StockMovementViewSet)

urlpatterns = [
    path('', include(router.urls)),

    path("products/", views.ProductListCreateView.as_view(), name="product-list-create"),
    path("suppliers/", views.SupplierListCreateView.as_view(), name="supplier-list-create"),

    path("stock_movements/", views.StockMovementView.as_view(), name="stock-movement"),
    path("sale_orders/", views.SaleOrderView.as_view(), name="sale-order-list-create"),

    path("sale_orders/<int:pk>/cancel/", views.SaleOrderCancelView.as_view(), name="sale-order-cancel"),
    path("sale_orders/<int:pk>/complete/", views.SaleOrderCompleteView.as_view(), name="sale-order-complete"),

    path("products/stock_levels/", views.StockLevelCheckView.as_view(), name="stock-level-check"),
]
