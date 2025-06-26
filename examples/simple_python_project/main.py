"""
Simple Python project example for Architex demonstration.
"""

from .models import User, Product
from .services import UserService, ProductService
from .database import DatabaseConnection


class Application:
    """Main application class."""
    
    def __init__(self):
        self.db = DatabaseConnection()
        self.user_service = UserService(self.db)
        self.product_service = ProductService(self.db)
    
    def run(self):
        """Run the application."""
        print("Application started")
        
        # Create a user
        user = self.user_service.create_user("john_doe", "john@example.com")
        
        # Create a product
        product = self.product_service.create_product("Sample Product", 29.99)
        
        print(f"Created user: {user.name}")
        print(f"Created product: {product.name}")


if __name__ == "__main__":
    app = Application()
    app.run() 