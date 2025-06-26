"""
Privacy and data protection module for Architex.
Handles data minimization, consent management, and privacy controls.
"""

import os
import json
import hashlib
from pathlib import Path
from typing import Dict, List, Optional, Set, Any
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)


@dataclass
class PrivacySettings:
    """Privacy configuration settings."""
    # Data handling
    local_only: bool = True
    store_analyzed_code: bool = False
    store_ai_responses: bool = False
    clear_cache_on_exit: bool = True
    
    # AI features
    ai_enabled: bool = False
    require_consent_for_ai: bool = True
    anonymize_code_before_ai: bool = True
    
    # File watching
    file_watching_enabled: bool = True
    respect_gitignore: bool = True
    exclude_sensitive_patterns: Optional[List[str]] = None
    
    # Web interface
    websocket_enabled: bool = False
    require_authentication: bool = True
    
    # Data retention
    max_cache_age_hours: int = 24
    max_log_retention_days: int = 7
    
    def __post_init__(self):
        if self.exclude_sensitive_patterns is None:
            self.exclude_sensitive_patterns = [
                "*.key", "*.pem", "*.p12", "*.pfx",  # Certificates
                "*.env", ".env*", "config.local.*",  # Environment files
                "*.db", "*.sqlite", "*.sqlite3",     # Databases
                "secrets.json", "credentials.json",  # Credential files
                "*.log", "logs/",                    # Log files
                "node_modules/", "venv/", "env/",    # Dependencies
                ".git/", ".svn/", ".hg/"             # Version control
            ]


class PrivacyManager:
    """Manages privacy controls and data protection."""
    
    def __init__(self, config_path: Optional[Path] = None):
        self.config_path = config_path or Path.home() / ".architex" / "privacy.json"
        self.settings = self._load_settings()
        self.consent_given = False
        self.data_hashes: Set[str] = set()
        self._ensure_config_dir()
    
    def _ensure_config_dir(self):
        """Ensure configuration directory exists."""
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
    
    def _load_settings(self) -> PrivacySettings:
        """Load privacy settings from file."""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r') as f:
                    data = json.load(f)
                    return PrivacySettings(**data)
            except Exception as e:
                logger.warning(f"Failed to load privacy settings: {e}")
        
        return PrivacySettings()
    
    def _save_settings(self):
        """Save privacy settings to file."""
        try:
            with open(self.config_path, 'w') as f:
                json.dump(asdict(self.settings), f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save privacy settings: {e}")
    
    def update_settings(self, **kwargs):
        """Update privacy settings."""
        for key, value in kwargs.items():
            if hasattr(self.settings, key):
                setattr(self.settings, key, value)
        self._save_settings()
    
    def get_consent(self, feature: str) -> bool:
        """Get user consent for a specific feature."""
        if not self.settings.require_consent_for_ai:
            return True
        
        if feature == "ai_analysis" and not self.consent_given:
            print("\n" + "="*60)
            print("PRIVACY NOTICE - AI Analysis")
            print("="*60)
            print("Architex can use AI to enhance code analysis with:")
            print("• Component labeling and categorization")
            print("• Code summarization and recommendations")
            print("• Service boundary detection")
            print("\nThis may involve sending code snippets to external AI services.")
            print("Your code will be processed according to the service provider's privacy policy.")
            print("\nData handling:")
            print("• Code snippets are anonymized before transmission")
            print("• No persistent storage of analyzed code")
            print("• AI responses are not stored unless explicitly enabled")
            print("="*60)
            
            response = input("Do you consent to AI-powered analysis? (y/N): ").strip().lower()
            self.consent_given = response in ['y', 'yes']
            
            if self.consent_given:
                print("✓ AI features enabled")
            else:
                print("✓ AI features disabled - using local analysis only")
            
            return self.consent_given
        
        return True
    
    def should_analyze_file(self, file_path: Path) -> bool:
        """Check if a file should be analyzed based on privacy settings."""
        if not self.settings.file_watching_enabled:
            return False
        
        # Check sensitive patterns
        if self.settings.exclude_sensitive_patterns:
            for pattern in self.settings.exclude_sensitive_patterns:
                if self._matches_pattern(file_path, pattern):
                    logger.debug(f"Skipping sensitive file: {file_path}")
                    return False
        
        # Check gitignore if enabled
        if self.settings.respect_gitignore:
            gitignore_path = file_path.parent / ".gitignore"
            if gitignore_path.exists():
                # Simple gitignore check - could be enhanced
                try:
                    with open(gitignore_path, 'r') as f:
                        gitignore_patterns = f.read().splitlines()
                    
                    for pattern in gitignore_patterns:
                        if pattern.strip() and not pattern.startswith('#'):
                            if self._matches_pattern(file_path, pattern):
                                logger.debug(f"Skipping gitignored file: {file_path}")
                                return False
                except Exception as e:
                    logger.warning(f"Error reading .gitignore: {e}")
        
        return True
    
    def _matches_pattern(self, file_path: Path, pattern: str) -> bool:
        """Check if file matches a pattern."""
        # Simple pattern matching - could be enhanced with fnmatch
        if pattern.startswith('*'):
            return file_path.name.endswith(pattern[1:])
        elif pattern.endswith('/'):
            return file_path.is_dir() and file_path.name == pattern[:-1]
        else:
            return file_path.name == pattern
    
    def anonymize_code(self, code: str) -> str:
        """Anonymize code by removing sensitive information."""
        if not self.settings.anonymize_code_before_ai:
            return code
        
        # Remove comments that might contain sensitive info
        lines = code.split('\n')
        anonymized_lines = []
        
        for line in lines:
            # Skip lines with potential sensitive patterns
            sensitive_patterns = [
                'password', 'secret', 'key', 'token', 'api_key',
                'private_key', 'certificate', 'credential'
            ]
            
            if any(pattern in line.lower() for pattern in sensitive_patterns):
                anonymized_lines.append('# [SENSITIVE DATA REMOVED]')
            else:
                anonymized_lines.append(line)
        
        return '\n'.join(anonymized_lines)
    
    def hash_data(self, data: str) -> str:
        """Create a hash of data for tracking without storing content."""
        return hashlib.sha256(data.encode()).hexdigest()[:16]
    
    def should_store_data(self, data_type: str) -> bool:
        """Check if data should be stored based on privacy settings."""
        if data_type == "analyzed_code":
            return self.settings.store_analyzed_code
        elif data_type == "ai_response":
            return self.settings.store_ai_responses
        return False
    
    def cleanup_old_data(self):
        """Clean up old cached data and logs."""
        if not self.settings.clear_cache_on_exit:
            return
        
        cache_dir = Path(".architex_cache")
        if cache_dir.exists():
            cutoff_time = datetime.now() - timedelta(hours=self.settings.max_cache_age_hours)
            
            for file_path in cache_dir.rglob("*"):
                if file_path.is_file():
                    try:
                        if datetime.fromtimestamp(file_path.stat().st_mtime) < cutoff_time:
                            file_path.unlink()
                            logger.debug(f"Cleaned up old cache file: {file_path}")
                    except Exception as e:
                        logger.warning(f"Failed to clean up cache file {file_path}: {e}")
    
    def get_privacy_report(self) -> Dict[str, Any]:
        """Generate a privacy report."""
        return {
            "local_only": self.settings.local_only,
            "ai_enabled": self.settings.ai_enabled and self.consent_given,
            "data_storage": {
                "analyzed_code": self.settings.store_analyzed_code,
                "ai_responses": self.settings.store_ai_responses
            },
            "file_watching": self.settings.file_watching_enabled,
            "websocket_enabled": self.settings.websocket_enabled,
            "sensitive_patterns_excluded": len(self.settings.exclude_sensitive_patterns) if self.settings.exclude_sensitive_patterns else 0,
            "data_hashes_tracked": len(self.data_hashes)
        }
    
    def export_privacy_settings(self, output_path: Path):
        """Export privacy settings for review."""
        report = {
            "timestamp": datetime.now().isoformat(),
            "settings": asdict(self.settings),
            "privacy_report": self.get_privacy_report()
        }
        
        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"Privacy settings exported to: {output_path}")


# Global privacy manager instance
privacy_manager = PrivacyManager()


def require_consent(feature: str):
    """Decorator to require consent for features."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            if privacy_manager.get_consent(feature):
                return func(*args, **kwargs)
            else:
                logger.warning(f"Consent not given for feature: {feature}")
                return None
        return wrapper
    return decorator


def privacy_cleanup():
    """Cleanup function to be called on exit."""
    privacy_manager.cleanup_old_data()
