"""
Database connection and operations for the example project.
"""

from typing import Dict, Any, Optional
from .models import User, Product


class DatabaseConnection:
    """Simple in-memory database connection."""
    
    def __init__(self):
        self.users: Dict[int, User] = {}
        self.products: Dict[int, Product] = {}
        self.counters = {"users": 0, "products": 0}
    
    def get_next_id(self, table: str) -> int:
        """Get next available ID for a table."""
        self.counters[table] += 1
        return self.counters[table]
    
    def save_user(self, user: User) -> None:
        """Save user to database."""
        self.users[user.id] = user
    
    def get_user(self, user_id: int) -> Optional[User]:
        """Get user from database."""
        return self.users.get(user_id)
    
    def save_product(self, product: Product) -> None:
        """Save product to database."""
        self.products[product.id] = product
    
    def get_product(self, product_id: int) -> Optional[Product]:
        """Get product from database."""
        return self.products.get(product_id)
    
    def execute_query(self, query: str, params: Optional[Dict[str, Any]] = None) -> Any:
        """Execute a database query."""
        # This is a mock implementation
        print(f"Executing query: {query}")
        return None 