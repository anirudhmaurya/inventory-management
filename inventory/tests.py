from rest_framework.test import APITestCase
from rest_framework import status
from .models import Supplier, Product

class ProductAPITest(APITestCase):
    def setUp(self):
        self.supplier = Supplier.objects.create(
            name="Test Supplier", email="test@supplier.com", phone="1234567890", address="Test Address"
        )
    
    def test_create_product(self):
        data = {
            "name": "Test Product",
            "description": "A test product",
            "category": "Electronics",
            "price": 100.00,
            "stock_quantity": 50,
            "supplier": self.supplier.id
        }
        response = self.client.post("/api/products/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["name"], "Test Product")

    def test_list_products(self):
        Product.objects.create(
            name="Product 1", description="Description 1", category="Category 1",
            price=10.00, stock_quantity=20, supplier=self.supplier
        )
        response = self.client.get("/api/products/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
