"""
Demo project for Architex extension showcase.
This project demonstrates various architectural patterns and code structures.
"""

from typing import List, Dict, Optional
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class User:
    """User entity representing a system user."""
    id: int
    username: str
    email: str
    is_active: bool = True
    created_at: datetime = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()


class DatabaseInterface(ABC):
    """Abstract interface for database operations."""
    
    @abstractmethod
    def connect(self) -> bool:
        """Establish database connection."""
        pass
    
    @abstractmethod
    def disconnect(self) -> bool:
        """Close database connection."""
        pass
    
    @abstractmethod
    def execute_query(self, query: str) -> List[Dict]:
        """Execute a database query."""
        pass


class PostgreSQLDatabase(DatabaseInterface):
    """PostgreSQL database implementation."""
    
    def __init__(self, host: str, port: int, database: str, username: str, password: str):
        self.host = host
        self.port = port
        self.database = database
        self.username = username
        self.password = password
        self.connection = None
    
    def connect(self) -> bool:
        """Connect to PostgreSQL database."""
        try:
            # Simulate connection
            logger.info(f"Connecting to PostgreSQL at {self.host}:{self.port}")
            self.connection = True
            return True
        except Exception as e:
            logger.error(f"Failed to connect to database: {e}")
            return False
    
    def disconnect(self) -> bool:
        """Disconnect from PostgreSQL database."""
        if self.connection:
            logger.info("Disconnecting from PostgreSQL")
            self.connection = None
        return True
    
    def execute_query(self, query: str) -> List[Dict]:
        """Execute a PostgreSQL query."""
        if not self.connection:
            raise ConnectionError("Not connected to database")
        
        logger.info(f"Executing query: {query}")
        # Simulate query execution
        return [{"result": "demo_data"}]


class UserRepository:
    """Repository pattern for user data operations."""
    
    def __init__(self, database: DatabaseInterface):
        self.database = database
    
    def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Retrieve user by ID."""
        query = f"SELECT * FROM users WHERE id = {user_id}"
        results = self.database.execute_query(query)
        
        if results:
            data = results[0]
            return User(
                id=data.get("id"),
                username=data.get("username"),
                email=data.get("email"),
                is_active=data.get("is_active", True)
            )
        return None
    
    def get_all_users(self) -> List[User]:
        """Retrieve all users."""
        query = "SELECT * FROM users"
        results = self.database.execute_query(query)
        
        users = []
        for data in results:
            user = User(
                id=data.get("id"),
                username=data.get("username"),
                email=data.get("email"),
                is_active=data.get("is_active", True)
            )
            users.append(user)
        
        return users
    
    def create_user(self, username: str, email: str) -> User:
        """Create a new user."""
        query = f"INSERT INTO users (username, email) VALUES ('{username}', '{email}')"
        self.database.execute_query(query)
        
        # Simulate getting the created user
        return User(id=1, username=username, email=email)


class UserService:
    """Service layer for user business logic."""
    
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
    
    def get_user_profile(self, user_id: int) -> Optional[Dict]:
        """Get user profile with additional business logic."""
        user = self.user_repository.get_user_by_id(user_id)
        
        if not user:
            return None
        
        if not user.is_active:
            logger.warning(f"Attempted to access inactive user: {user_id}")
            return None
        
        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "status": "active" if user.is_active else "inactive",
            "member_since": user.created_at.isoformat()
        }
    
    def register_user(self, username: str, email: str) -> Dict:
        """Register a new user with validation."""
        # Business logic validation
        if not username or len(username) < 3:
            raise ValueError("Username must be at least 3 characters long")
        
        if not email or "@" not in email:
            raise ValueError("Invalid email address")
        
        # Check if user already exists
        all_users = self.user_repository.get_all_users()
        for user in all_users:
            if user.username == username or user.email == email:
                raise ValueError("User already exists")
        
        # Create new user
        new_user = self.user_repository.create_user(username, email)
        
        logger.info(f"New user registered: {new_user.username}")
        
        return {
            "id": new_user.id,
            "username": new_user.username,
            "email": new_user.email,
            "status": "registered"
        }


class AuthenticationService:
    """Service for user authentication."""
    
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        self.active_sessions = {}
    
    def authenticate(self, username: str, password: str) -> Optional[str]:
        """Authenticate user and return session token."""
        user = self._find_user_by_username(username)
        
        if not user:
            logger.warning(f"Authentication failed: user not found - {username}")
            return None
        
        if not user.is_active:
            logger.warning(f"Authentication failed: inactive user - {username}")
            return None
        
        # Simulate password verification
        if self._verify_password(password):
            session_token = self._generate_session_token(user.id)
            self.active_sessions[session_token] = user.id
            logger.info(f"User authenticated successfully: {username}")
            return session_token
        
        logger.warning(f"Authentication failed: invalid password - {username}")
        return None
    
    def _find_user_by_username(self, username: str) -> Optional[User]:
        """Find user by username."""
        all_users = self.user_repository.get_all_users()
        for user in all_users:
            if user.username == username:
                return user
        return None
    
    def _verify_password(self, password: str) -> bool:
        """Verify user password (simplified)."""
        # In real implementation, this would hash and compare passwords
        return password == "demo_password"
    
    def _generate_session_token(self, user_id: int) -> str:
        """Generate a session token."""
        return f"session_{user_id}_{datetime.now().timestamp()}"


class APIHandler:
    """HTTP API handler for user operations."""
    
    def __init__(self, user_service: UserService, auth_service: AuthenticationService):
        self.user_service = user_service
        self.auth_service = auth_service
    
    def handle_get_user_profile(self, user_id: int, session_token: str) -> Dict:
        """Handle GET /users/{id}/profile request."""
        # Validate session
        if not self._validate_session(session_token):
            return {"error": "Invalid session", "status": 401}
        
        try:
            profile = self.user_service.get_user_profile(user_id)
            if profile:
                return {"data": profile, "status": 200}
            else:
                return {"error": "User not found", "status": 404}
        except Exception as e:
            logger.error(f"Error getting user profile: {e}")
            return {"error": "Internal server error", "status": 500}
    
    def handle_register_user(self, username: str, email: str) -> Dict:
        """Handle POST /users/register request."""
        try:
            result = self.user_service.register_user(username, email)
            return {"data": result, "status": 201}
        except ValueError as e:
            return {"error": str(e), "status": 400}
        except Exception as e:
            logger.error(f"Error registering user: {e}")
            return {"error": "Internal server error", "status": 500}
    
    def handle_login(self, username: str, password: str) -> Dict:
        """Handle POST /auth/login request."""
        session_token = self.auth_service.authenticate(username, password)
        
        if session_token:
            return {
                "data": {"session_token": session_token},
                "status": 200
            }
        else:
            return {"error": "Invalid credentials", "status": 401}
    
    def _validate_session(self, session_token: str) -> bool:
        """Validate session token."""
        return session_token in self.auth_service.active_sessions


def main():
    """Main function demonstrating the application."""
    # Initialize components
    database = PostgreSQLDatabase("localhost", 5432, "demo_db", "user", "password")
    database.connect()
    
    user_repository = UserRepository(database)
    user_service = UserService(user_repository)
    auth_service = AuthenticationService(user_repository)
    api_handler = APIHandler(user_service, auth_service)
    
    # Demo operations
    print("=== Architex Demo Application ===")
    
    # Register a user
    print("\n1. Registering a new user...")
    result = api_handler.handle_register_user("demo_user", "demo@example.com")
    print(f"Result: {result}")
    
    # Login
    print("\n2. Logging in...")
    login_result = api_handler.handle_login("demo_user", "demo_password")
    print(f"Result: {login_result}")
    
    # Get user profile
    if login_result["status"] == 200:
        session_token = login_result["data"]["session_token"]
        print("\n3. Getting user profile...")
        profile_result = api_handler.handle_get_user_profile(1, session_token)
        print(f"Result: {profile_result}")
    
    # Cleanup
    database.disconnect()
    print("\n=== Demo completed ===")


if __name__ == "__main__":
    main() 