"""
Service layer for the example project.
"""

from .models import User, Product
from .database import DatabaseConnection


class UserService:
    """Service for user operations."""
    
    def __init__(self, db: DatabaseConnection):
        self.db = db
    
    def create_user(self, name: str, email: str) -> User:
        """Create a new user."""
        user_id = self.db.get_next_id("users")
        user = User(id=user_id, name=name, email=email)
        self.db.save_user(user)
        return user
    
    def get_user(self, user_id: int) -> User:
        """Get user by ID."""
        return self.db.get_user(user_id)
    
    def update_user(self, user: User) -> User:
        """Update user."""
        self.db.save_user(user)
        return user


class ProductService:
    """Service for product operations."""
    
    def __init__(self, db: DatabaseConnection):
        self.db = db
    
    def create_product(self, name: str, price: float) -> Product:
        """Create a new product."""
        product_id = self.db.get_next_id("products")
        product = Product(id=product_id, name=name, price=price)
        self.db.save_product(product)
        return product
    
    def get_product(self, product_id: int) -> Product:
        """Get product by ID."""
        return self.db.get_product(product_id)
    
    def update_product(self, product: Product) -> Product:
        """Update product."""
        self.db.save_product(product)
        return product 