"""
File watcher using Watchdog for real-time codebase monitoring.
"""

import asyncio
import time
from pathlib import Path
from typing import Callable, List, Optional, Set
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileModifiedEvent, FileCreatedEvent, FileDeletedEvent

from ..core.analyzer import CodebaseAnalyzer
from ..core.models import AnalysisResult


class CodebaseEventHandler(FileSystemEventHandler):
    """Handles file system events for codebase changes."""
    
    def __init__(self, callback: Callable[[Path, str], None], supported_extensions: Set[str]):
        self.callback = callback
        self.supported_extensions = supported_extensions
        self.debounce_timer = None
        self.pending_changes = set()
    
    def on_modified(self, event):
        if not event.is_directory and self._is_supported_file(event.src_path):
            self._schedule_update(event.src_path, "modified")
    
    def on_created(self, event):
        if not event.is_directory and self._is_supported_file(event.src_path):
            self._schedule_update(event.src_path, "created")
    
    def on_deleted(self, event):
        if not event.is_directory and self._is_supported_file(event.src_path):
            self._schedule_update(event.src_path, "deleted")
    
    def _is_supported_file(self, file_path: str) -> bool:
        """Check if the file has a supported extension."""
        return Path(file_path).suffix in self.supported_extensions
    
    def _schedule_update(self, file_path: str, event_type: str):
        """Schedule an update with debouncing."""
        self.pending_changes.add((file_path, event_type))
        
        # Cancel existing timer
        if self.debounce_timer:
            self.debounce_timer.cancel()
        
        # Schedule new timer
        self.debounce_timer = asyncio.create_task(self._debounced_update())
    
    async def _debounced_update(self):
        """Debounced update to avoid too frequent analysis."""
        await asyncio.sleep(2)  # Wait 2 seconds for more changes
        
        # Process all pending changes
        for file_path, event_type in self.pending_changes:
            self.callback(Path(file_path), event_type)
        
        self.pending_changes.clear()


class FileWatcher:
    """Watches codebase files for changes and triggers analysis."""
    
    def __init__(self, codebase_path: str, callback: Callable[[AnalysisResult], None], config: Optional[dict] = None):
        self.codebase_path = Path(codebase_path)
        self.callback = callback
        self.config = config or {}
        
        # Supported file extensions
        self.supported_extensions = {
            '.py', '.js', '.ts', '.java', '.cpp', '.c', '.h', '.go', '.rs', '.php', '.rb'
        }
        
        # Initialize components
        self.observer = Observer()
        self.analyzer = CodebaseAnalyzer(config)
        self.event_handler = CodebaseEventHandler(self._on_file_change, self.supported_extensions)
        
        # State
        self.is_watching = False
        self.last_analysis = None
        self.analysis_lock = asyncio.Lock()
    
    def start(self):
        """Start watching the codebase."""
        if self.is_watching:
            return
        
        # Schedule the observer
        self.observer.schedule(
            self.event_handler,
            str(self.codebase_path),
            recursive=True
        )
        
        # Start the observer
        self.observer.start()
        self.is_watching = True
        
        print(f"🔍 Started watching: {self.codebase_path}")
        print(f"📁 Supported extensions: {', '.join(self.supported_extensions)}")
    
    def stop(self):
        """Stop watching the codebase."""
        if not self.is_watching:
            return
        
        self.observer.stop()
        self.observer.join()
        self.is_watching = False
        
        print("🛑 Stopped watching codebase")
    
    async def _on_file_change(self, file_path: Path, event_type: str):
        """Handle file change events."""
        print(f"📝 File {event_type}: {file_path}")
        
        # Prevent concurrent analysis
        async with self.analysis_lock:
            try:
                # Perform incremental analysis
                result = await self._analyze_incremental(file_path, event_type)
                
                if result:
                    self.last_analysis = result
                    await self.callback(result)
                    
            except Exception as e:
                print(f"❌ Error during incremental analysis: {e}")
    
    async def _analyze_incremental(self, changed_file: Path, event_type: str) -> Optional[AnalysisResult]:
        """Perform incremental analysis based on file changes."""
        try:
            # For now, perform full analysis (can be optimized later)
            result = self.analyzer.analyze(self.codebase_path)
            
            # Add change metadata
            result.metadata['last_change'] = {
                'file': str(changed_file),
                'event_type': event_type,
                'timestamp': time.time()
            }
            
            return result
            
        except Exception as e:
            print(f"Error in incremental analysis: {e}")
            return None
    
    def get_watched_files(self) -> List[Path]:
        """Get list of currently watched files."""
        watched_files = []
        
        for root, dirs, files in self.observer.emitters[0].watch.paths:
            root_path = Path(root)
            for file in files:
                file_path = root_path / file
                if file_path.suffix in self.supported_extensions:
                    watched_files.append(file_path)
        
        return watched_files
    
    def add_extension(self, extension: str):
        """Add a new file extension to watch."""
        if not extension.startswith('.'):
            extension = '.' + extension
        
        self.supported_extensions.add(extension)
        print(f"➕ Added extension to watch: {extension}")
    
    def remove_extension(self, extension: str):
        """Remove a file extension from watching."""
        if not extension.startswith('.'):
            extension = '.' + extension
        
        self.supported_extensions.discard(extension)
        print(f"➖ Removed extension from watch: {extension}")
    
    def get_status(self) -> dict:
        """Get current watcher status."""
        return {
            'is_watching': self.is_watching,
            'codebase_path': str(self.codebase_path),
            'supported_extensions': list(self.supported_extensions),
            'watched_files_count': len(self.get_watched_files()),
            'last_analysis': self.last_analysis is not None
        } 