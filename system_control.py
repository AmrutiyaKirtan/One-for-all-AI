#!/usr/bin/env python3
"""
System Control APIs for Phase 1 completion
Basic phone/PC control functionality
"""

import subprocess
import os
import platform
import psutil
import shutil
from pathlib import Path

class SystemController:
    """Handles basic system control operations"""
    
    def __init__(self):
        self.os_type = platform.system()
        
    def open_application(self, app_name):
        """Open applications by name"""
        app_name = app_name.lower()
        
        if self.os_type == "Windows":
            apps = {
                'notepad': 'notepad.exe',
                'calculator': 'calc.exe',
                'paint': 'mspaint.exe',
                'browser': 'start chrome',
                'chrome': 'start chrome',
                'firefox': 'start firefox',
                'edge': 'start msedge',
                'file explorer': 'explorer.exe',
                'explorer': 'explorer.exe',
                'cmd': 'cmd.exe',
                'powershell': 'powershell.exe'
            }
            
            if app_name in apps:
                try:
                    if apps[app_name].startswith('start '):
                        os.system(apps[app_name])
                    else:
                        subprocess.Popen(apps[app_name])
                    return f"Opening {app_name}"
                except Exception as e:
                    return f"Failed to open {app_name}: {e}"
            else:
                return f"Application '{app_name}' not recognized"
        
        return f"Application control not implemented for {self.os_type}"
    
    def close_application(self, app_name):
        """Close applications by name"""
        app_name = app_name.lower()
        
        try:
            for proc in psutil.process_iter(['pid', 'name']):
                if app_name in proc.info['name'].lower():
                    proc.terminate()
                    return f"Closed {app_name}"
            return f"Application '{app_name}' not found running"
        except Exception as e:
            return f"Failed to close {app_name}: {e}"
    
    def set_volume(self, level):
        """Set system volume (Windows only for now)"""
        if self.os_type == "Windows":
            try:
                # Use nircmd for volume control (would need to be installed)
                # For now, use a simple approach
                level = max(0, min(100, int(level)))
                # This is a placeholder - would need actual volume control library
                return f"Volume set to {level}% (placeholder - needs volume control library)"
            except Exception as e:
                return f"Failed to set volume: {e}"
        
        return f"Volume control not implemented for {self.os_type}"
    
    def lock_computer(self):
        """Lock the computer"""
        if self.os_type == "Windows":
            try:
                os.system('rundll32.exe user32.dll,LockWorkStation')
                return "Computer locked"
            except Exception as e:
                return f"Failed to lock computer: {e}"
        
        return f"Lock function not implemented for {self.os_type}"
    
    def shutdown_computer(self, delay=60):
        """Shutdown computer with delay"""
        if self.os_type == "Windows":
            try:
                os.system(f'shutdown /s /t {delay}')
                return f"Computer will shutdown in {delay} seconds"
            except Exception as e:
                return f"Failed to schedule shutdown: {e}"
        
        return f"Shutdown not implemented for {self.os_type}"
    
    def create_folder(self, folder_name, path=None):
        """Create a new folder"""
        try:
            # Use Desktop as default location for user folders
            if path is None:
                desktop = Path.home() / "Desktop"
                if desktop.exists():
                    path = desktop
                else:
                    path = Path.home()
            
            folder_path = Path(path) / folder_name
            folder_path.mkdir(exist_ok=True)
            return f"Created folder '{folder_name}' on {path}"
        except Exception as e:
            return f"Failed to create folder: {e}"
    
    def create_folder_in_location(self, folder_name, location):
        """Create a folder in a specific location"""
        try:
            # Handle common location names
            location_lower = location.lower()
            
            if location_lower in ['desktop']:
                base_path = Path.home() / "Desktop"
            elif location_lower in ['documents']:
                base_path = Path.home() / "Documents"
            elif location_lower in ['downloads']:
                base_path = Path.home() / "Downloads"
            else:
                # Try to find the folder on Desktop first (case-insensitive)
                desktop = Path.home() / "Desktop"
                
                # Look for existing folder (case-insensitive)
                found_folder = None
                if desktop.exists():
                    for item in desktop.iterdir():
                        if item.is_dir() and item.name.lower() == location.lower():
                            found_folder = item
                            break
                
                if found_folder:
                    base_path = found_folder
                else:
                    # Create the parent folder if it doesn't exist
                    base_path = desktop / location
                    base_path.mkdir(exist_ok=True)
            
            # Create the target folder
            folder_path = base_path / folder_name
            folder_path.mkdir(exist_ok=True)
            
            return f"Created folder '{folder_name}' in {base_path}"
        except Exception as e:
            return f"Failed to create folder in location: {e}"
    
    def delete_file(self, file_path):
        """Delete a file safely"""
        try:
            file_path = Path(file_path)
            if file_path.exists():
                if file_path.is_file():
                    file_path.unlink()
                    return f"Deleted file: {file_path}"
                else:
                    return f"'{file_path}' is not a file"
            else:
                return f"File '{file_path}' not found"
        except Exception as e:
            return f"Failed to delete file: {e}"
    
    def get_running_apps(self):
        """Get list of running applications"""
        try:
            apps = []
            for proc in psutil.process_iter(['pid', 'name']):
                if proc.info['name'] and not proc.info['name'].startswith('System'):
                    apps.append(proc.info['name'])
            
            # Remove duplicates and system processes
            unique_apps = list(set(apps))
            user_apps = [app for app in unique_apps if not app.endswith('.exe') or 
                        app.lower() in ['notepad.exe', 'calc.exe', 'chrome.exe', 'firefox.exe']]
            
            return f"Running applications: {', '.join(user_apps[:10])}"  # Limit to 10
        except Exception as e:
            return f"Failed to get running apps: {e}"
    
    def adjust_volume(self, adjustment):
        """Adjust volume by relative amount"""
        if self.os_type == "Windows":
            try:
                if adjustment.startswith('+'):
                    return f"Volume increased by {adjustment[1:]}% (placeholder - needs volume control library)"
                elif adjustment.startswith('-'):
                    return f"Volume decreased by {adjustment[1:]}% (placeholder - needs volume control library)"
                else:
                    return f"Volume adjusted by {adjustment}% (placeholder - needs volume control library)"
            except Exception as e:
                return f"Failed to adjust volume: {e}"
        
        return f"Volume control not implemented for {self.os_type}"