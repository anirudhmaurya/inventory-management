from rest_framework import serializers
from .models import Supplier, Product, SaleOrder, StockMovement

class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ['id', 'name', 'email', 'phone', 'address']
        read_only_fields = ['id']

    def validate_phone(self, value):
        if len(value) != 10 or not value.isdigit():
            raise serializers.ValidationError("Phone number must be exactly 10 digits.")
        return value


class ProductSerializer(serializers.ModelSerializer):
    supplier = serializers.PrimaryKeyRelatedField(queryset=Supplier.objects.all())

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'category', 'price', 'stock_quantity', 'supplier']
        read_only_fields = ['id']

    def validate_stock_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError("Stock quantity cannot be negative.")
        return value

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than zero.")
        return value


class SaleOrderSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(source='product.id', read_only=True)

    class Meta:
        model = SaleOrder
        fields = ['id', 'product_id', 'quantity', 'total_price', 'sale_date', 'status']
        read_only_fields = ['id', 'total_price']

    def validate(self, data):
        if data.get('quantity') <= 0:
            raise serializers.ValidationError("Quantity must be greater than zero.")
        if data.get('quantity') > data.get('product').stock_quantity:
            raise serializers.ValidationError("Insufficient stock for this product.")
        return data
    

    
class StockMovementSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = StockMovement
        fields = ['id', 'product', 'quantity', 'movement_type', 'movement_date', 'notes']
        read_only_fields = ['id']

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be greater than zero.")
        return value
