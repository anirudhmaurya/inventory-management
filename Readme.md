# Inventory Management System (Backend)

## Overview

This project is a backend implementation for an Inventory Management System using Django and MongoDB. It provides REST APIs for managing products, suppliers, stock movements, and sales orders.

## Features
- CRUD operations for products and suppliers
- Stock management with incoming and outgoing movements
- Sales order management with status updates
- Filtering and sorting options for products and sales orders

## Tech Stack
- **Backend:** Django, Django REST Framework
- **Database:** MongoDB (remote)

## Installation

### Prerequisites
- Python 3.9 or above
- MongoDB running remotely (MongoDB Atlas)
- pip package manager

### Steps
1. Download the repository.
2. Run the following command to install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. To run the app locally, execute:
   ```bash
   python manage.py runserver
   ```

## API Endpoints

### 1. Add a Product
- **Method:** POST
- **URL:** `{{base_url}}/api/products/`
- **Headers:**
  ```json
  {
    "Content-Type": "application/json"
  }
  ```
- **Body:**
  ```json
  {
    "name": "Product 2r",
    "description": "Description of Product A",
    "category": "Category1",
    "price": 100.50,
    "stock_quantity": 50,
    "supplier": 3
  }
  ```

### 2. List All Products
- **Method:** GET
- **URL:** `{{base_url}}/api/products/`

### 3. Add a Supplier
- **Method:** POST
- **URL:** `{{base_url}}/api/suppliers/`
- **Headers:**
  ```json
  {
    "Content-Type": "application/json"
  }
  ```
- **Body:**
  ```json
  {
    "name": "Supplier w",
    "email": "suppliwerE8811@example.com",
    "phone": "1233567800",
    "address": "123 Supplier Street"
  }
  ```

### 4. List All Suppliers
- **Method:** GET
- **URL:** `{{base_url}}/api/suppliers/`

### 5. Add Stock Movement
- **Method:** POST
- **URL:** `{{base_url}}/api/stock_movements/`
- **Headers:**
  ```json
  {
    "Content-Type": "application/json"
  }
  ```
- **Body:**
  ```json
  {
    "product": 1,
    "quantity": 20,
    "movement_type": "In",
    "notes": "Restocking new items"
  }
  ```

### 6. Create a Sale Order
- **Method:** POST
- **URL:** `{{base_url}}/api/sale_orders/`
- **Headers:**
  ```json
  {
    "Content-Type": "application/json"
  }
  ```
- **Body:**
  ```json
  {
    "product": 2,
    "quantity": 5,
    "status": "Pending"
  }
  ```

### 7. Cancel a Sale Order
- **Method:** PATCH
- **URL:** `{{base_url}}/api/sale_orders/1/cancel/`

### 8. Complete a Sale Order
- **Method:** PATCH
- **URL:** `{{base_url}}/api/sale_orders/1/complete/`

### 9. List Sale Orders
- **Method:** GET
- **URL:** `{{base_url}}/api/sale_orders/`

### 10. Check Stock Levels
- **Method:** GET
- **URL:** `{{base_url}}/api/products/stock_levels/`
