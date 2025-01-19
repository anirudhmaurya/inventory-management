from djongo import models


class AutoIncrementID(models.Model):
    counter = models.IntegerField()

    class Meta:
        abstract = True


class Supplier(AutoIncrementID):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=10, unique=True)
    address = models.TextField()

    def save(self, *args, **kwargs):
        if not self.id:
            last_supplier = Supplier.objects.all().order_by('-id').first()
            self.id = last_supplier.id + 1 if last_supplier else 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(AutoIncrementID):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField()
    category = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField()
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.id:
            last_product = Product.objects.all().order_by('-id').first()
            self.id = last_product.id + 1 if last_product else 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

from decimal import Decimal
from djongo.models import DecimalField

class SaleOrder(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]
    id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total_price = DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00')) 
    sale_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"Order {self.id} - {self.status}"

    def save(self, *args, **kwargs):
        if isinstance(self.total_price, str):
            self.total_price = Decimal(self.total_price)
        super(SaleOrder, self).save(*args, **kwargs)



class StockMovement(AutoIncrementID):
    MOVEMENT_CHOICES = [
        ('In', 'Incoming'),
        ('Out', 'Outgoing'),
    ]
    id = models.IntegerField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    movement_type = models.CharField(max_length=10, choices=MOVEMENT_CHOICES)
    movement_date = models.DateField(auto_now_add=True)
    notes = models.TextField()

    def save(self, *args, **kwargs):
        if not self.id:
            last_movement = StockMovement.objects.all().order_by('-id').first()
            self.id = last_movement.id + 1 if last_movement else 1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.movement_type} - {self.quantity} {self.product.name}"
