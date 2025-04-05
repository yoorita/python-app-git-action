import unittest
from unittest.mock import patch
from app import app, ProductModel, create_product, get_product_by_id, update_product, delete_product

class FlaskAppTests(unittest.TestCase):
    # Set up the Flask test client
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    # Test case for GET /api/products (list all products)
    @patch('app.ProductModel.select')
    def test_get_products(self, mock_select):
        # Mock the response from the database
        mock_select.return_value = [ProductModel(id=1, name="Product1", price=100.0),
                                    ProductModel(id=2, name="Product2", price=150.0)]
        
        response = self.app.get('/api/products')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Product1', response.get_data(as_text=True))
        self.assertIn('Product2', response.get_data(as_text=True))

    # Test case for POST /api/products (create a new product)
    @patch('app.create_product')
    def test_create_product(self, mock_create_product):
        # Mock the response of create_product function
        mock_create_product.return_value = ProductModel(id=1, name="Product1", price=100.0)
        
        response = self.app.post('/api/products', json={"name": "Product1", "price": 100.0})
        self.assertEqual(response.status_code, 201)
        self.assertIn("Product added successfully.", response.get_data(as_text=True))

    # Test case for GET /api/products/<int:product_id> (get a specific product by ID)
    @patch('app.get_product_by_id')
    def test_get_product_by_id(self, mock_get_product_by_id):
        # Mock the response of get_product_by_id
        mock_get_product_by_id.return_value = ProductModel(id=1, name="Product1", price=100.0)

        response = self.app.get('/api/products/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Product1', response.get_data(as_text=True))

    # Test case for GET /api/products/<int:product_id> when the product doesn't exist
    @patch('app.get_product_by_id')
    def test_get_product_not_found(self, mock_get_product_by_id):
        # Mock the response of get_product_by_id for a non-existent product
        mock_get_product_by_id.return_value = None

        response = self.app.get('/api/products/999')
        self.assertEqual(response.status_code, 404)
        self.assertIn("Product not found.", response.get_data(as_text=True))

    # Test case for PATCH /api/products/<int:product_id> (update product details)
    @patch('app.get_product_by_id')
    @patch('app.update_product')
    def test_update_product(self, mock_update_product, mock_get_product_by_id):
        # Mock the response of get_product_by_id and update_product
        mock_get_product_by_id.return_value = ProductModel(id=1, name="Product1", price=100.0)
        mock_update_product.return_value = None  # Nothing to return, we just need the function to be called
        
        response = self.app.patch('/api/products/1', json={"name": "Updated Product", "price": 120.0})
        self.assertEqual(response.status_code, 200)
        self.assertIn("Product updated successfully.", response.get_data(as_text=True))

    # Test case for DELETE /api/products/<int:product_id> (delete product)
    @patch('app.get_product_by_id')
    @patch('app.delete_product')
    def test_delete_product(self, mock_delete_product, mock_get_product_by_id):
        # Mock the response of get_product_by_id
        mock_get_product_by_id.return_value = ProductModel(id=1, name="Product1", price=100.0)
        
        response = self.app.delete('/api/products/1')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Product deleted.", response.get_data(as_text=True))

    # Test case for DELETE /api/products/<int:product_id> when the product doesn't exist
    @patch('app.get_product_by_id')
    def test_delete_product_not_found(self, mock_get_product_by_id):
        # Mock the response of get_product_by_id for a non-existent product
        mock_get_product_by_id.return_value = None
        
        response = self.app.delete('/api/products/999')
        self.assertEqual(response.status_code, 404)
        self.assertIn("Product not found.", response.get_data(as_text=True))

if __name__ == '__main__':
    unittest.main()
