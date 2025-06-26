"""
Data models for the example project.
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class User:
    """User model."""
    id: int
    name: str
    email: str
    is_active: bool = True


@dataclass
class Product:
    """Product model."""
    id: int
    name: str
    price: float
    description: Optional[str] = None
    in_stock: bool = True 