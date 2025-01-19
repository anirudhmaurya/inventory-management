from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .models import Supplier, Product, SaleOrder, StockMovement
from .serializers import SupplierSerializer, ProductSerializer, SaleOrderSerializer, StockMovementSerializer

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    @action(detail=False, methods=['get'])
    def filter_by_category(self, request):
        category = request.query_params.get('category', None)
        if category:
            products = self.queryset.filter(category=category)
            serializer = self.get_serializer(products, many=True)
            return Response(serializer.data)
        return Response({"detail": "Category query parameter is required."}, status=status.HTTP_400_BAD_REQUEST)


class SaleOrderViewSet(viewsets.ModelViewSet):
    queryset = SaleOrder.objects.all()
    serializer_class = SaleOrderSerializer

    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['status', 'sale_date']
    ordering_fields = ['sale_date', 'total_price']

    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        sale_order = self.get_object()
        if sale_order.status != 'Pending':
            return Response({"detail": "Only pending orders can be completed."}, status=status.HTTP_400_BAD_REQUEST)

        sale_order.status = 'Completed'
        sale_order.save()

        sale_order.product.stock_quantity -= sale_order.quantity
        sale_order.product.save()

        return Response({"detail": "Order completed successfully."})

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        sale_order = self.get_object()
        if sale_order.status != 'Pending':
            return Response({"detail": "Only pending orders can be canceled."}, status=status.HTTP_400_BAD_REQUEST)

        sale_order.status = 'Cancelled'
        sale_order.save()

        sale_order.product.stock_quantity += sale_order.quantity
        sale_order.product.save()

        return Response({"detail": "Order canceled successfully."})


class StockMovementViewSet(viewsets.ModelViewSet):
    queryset = StockMovement.objects.all()
    serializer_class = StockMovementSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        stock_movement = serializer.save()

        if stock_movement.movement_type == 'In':
            stock_movement.product.stock_quantity += stock_movement.quantity
        elif stock_movement.movement_type == 'Out':
            if stock_movement.quantity > stock_movement.product.stock_quantity:
                return Response({"detail": "Insufficient stock for outgoing movement."}, status=status.HTTP_400_BAD_REQUEST)
            stock_movement.product.stock_quantity -= stock_movement.quantity

        stock_movement.product.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class StockMovementView(APIView):
    def post(self, request):
        serializer = StockMovementSerializer(data=request.data)
        if serializer.is_valid():
            stock_movement = serializer.save()

            # Update stock levels
            if stock_movement.movement_type == 'In':
                stock_movement.product.stock_quantity += stock_movement.quantity
            elif stock_movement.movement_type == 'Out':
                if stock_movement.quantity > stock_movement.product.stock_quantity:
                    return Response({"detail": "Insufficient stock for outgoing movement."}, status=status.HTTP_400_BAD_REQUEST)
                stock_movement.product.stock_quantity -= stock_movement.quantity

            stock_movement.product.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SaleOrderView(APIView):
    def post(self, request):
        serializer = SaleOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        orders = SaleOrder.objects.all()
        serializer = SaleOrderSerializer(orders, many=True)
        return Response(serializer.data)


class SaleOrderCancelView(APIView):
    def patch(self, request, pk):
        try:
            sale_order = SaleOrder.objects.get(id=pk)
            if sale_order.status == 'Completed':
                return Response({"error": "Completed orders cannot be canceled."}, status=status.HTTP_400_BAD_REQUEST)
            sale_order.status = 'Cancelled'
            sale_order.save()
            return Response(SaleOrderSerializer(sale_order).data, status=status.HTTP_200_OK)
        except SaleOrder.DoesNotExist:
            return Response({"error": "Sale order not found."}, status=status.HTTP_404_NOT_FOUND)

from decimal import Decimal

class SaleOrderCompleteView(APIView):
    def patch(self, request, pk):
        sale_order = SaleOrder.objects.get(id=pk)
        sale_order.status = 'Completed'
        
        # if sale_order.quantity > 0 and sale_order.product.price > 0:
        #     sale_order.total_price = sale_order.product.price * sale_order.quantity

        sale_order.save()
        return Response(SaleOrderSerializer(sale_order).data)

class StockLevelCheckView(APIView):
    def get(self, request):
        products = Product.objects.all()
        data = [{"name": p.name, "stock_quantity": p.stock_quantity} for p in products]
        return Response(data, status=status.HTTP_200_OK)


class ProductListCreateView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SupplierListCreateView(APIView):
    def get(self, request):
        suppliers = Supplier.objects.all()
        serializer = SupplierSerializer(suppliers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = SupplierSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
