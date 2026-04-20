import os
import webbrowser
import pyautogui
import psutil
import subprocess
import platform
import socket
import datetime
import pyperclip
import random
import re
import shutil
import json
import time
import math
import textwrap
from datetime import datetime as dt
from PIL import ImageGrab, Image, ImageDraw, ImageFont
import win32com.client  # For more advanced Windows operations
import sys
import uuid
import hashlib

class VoiceAssistant:
    def __init__(self):
        self.user_preferences = {}
        self.command_history = []
        self.load_preferences()
        
    def load_preferences(self):
        """Load user preferences from file"""
        prefs_file = "assistant_preferences.json"
        if os.path.exists(prefs_file):
            try:
                with open(prefs_file, 'r') as f:
                    self.user_preferences = json.load(f)
            except:
                self.user_preferences = {}
    
    def save_preferences(self):
        """Save user preferences to file"""
        prefs_file = "assistant_preferences.json"
        with open(prefs_file, 'w') as f:
            json.dump(self.user_preferences, f)
    
    def add_to_history(self, command, response):
        """Add command to history"""
        self.command_history.append({
            'timestamp': datetime.datetime.now().isoformat(),
            'command': command,
            'response': response[:100] if response else ""
        })
        # Keep only last 100 commands
        if len(self.command_history) > 100:
            self.command_history = self.command_history[-100:]
    
    def format_response(self, title, content, emoji="ℹ️"):
        """Format response with consistent styling"""
        return f"{emoji} {title}\n{'-'*40}\n{content}"
    
    def execute_command(self, command):
        command_lower = command.lower().strip()
        if " and " in command_lower:
            commands = command_lower.split(" and ")
            responses = []
            for cmd in commands:
                if cmd.strip():
                    # Add delay between chained commands for UI stability
                    if len(responses) > 0:
                        time.sleep(1.0)
                        
                    res = self.execute_command(cmd)
                    if res:
                        responses.append(res)
            
            return "\n➕ ".join(responses) if responses else None
            
        self.command_history.append({
            'timestamp': datetime.datetime.now().isoformat(),
            'command': command
        })
        
        try:
            # Enhanced file operations
            response = self.handle_file_operations(command_lower)
            if response: 
                self.add_to_history(command, response)
                return response
            
            # Enhanced folder operations
            response = self.handle_folder_operations(command_lower)
            if response: 
                self.add_to_history(command, response)
                return response
            
            # System operations
            response = self.handle_system_operations(command_lower)
            if response: 
                self.add_to_history(command, response)
                return response
            
            # Network operations
            response = self.handle_network_operations(command_lower)
            if response: 
                self.add_to_history(command, response)
                return response
            
            # Media operations
            response = self.handle_media_operations(command_lower)
            if response: 
                self.add_to_history(command, response)
                return response
            
            # Productivity operations
            response = self.handle_productivity_operations(command_lower)
            if response: 
                self.add_to_history(command, response)
                return response
            
            # Utility operations
            response = self.handle_utility_operations(command_lower)
            if response: 
                self.add_to_history(command, response)
                return response
            # Shell/Terminal operations (Voice CLI)
            response = self.handle_shell_operations(command_lower)
            if response:
                self.add_to_history(command, response)
                return response
            
            # Keyboard/Macro operations
            response = self.handle_keyboard_operations(command_lower)
            if response:
                self.add_to_history(command, response)
                return response

            # Application operations (Universal Open)
            response = self.handle_app_operations(command_lower)
            if response:
                self.add_to_history(command, response)
                return response

            # Web operations
            response = self.handle_web_operations(command_lower)
            if response: 
                self.add_to_history(command, response)
                return response
            
            # Conversation
            response = self.handle_conversation(command_lower)
            if response: 
                self.add_to_history(command, response)
                return response
            
            # Advanced operations
            response = self.handle_advanced_operations(command_lower)
            if response: 
                self.add_to_history(command, response)
                return response
            
            # Help
            if any(word in command_lower for word in ["help", "what can you do", "commands"]):
                response = self.get_help_text()
                self.add_to_history(command, response)
                return response
            
            # Exit
            if any(word in command_lower for word in ["exit", "quit", "goodbye", "shutdown assistant"]):
                return "EXIT_ASSISTANT"
            
            # Default fallback
            suggestions = [
                "I didn't understand that command. Try saying 'help' to see all available commands. 🆘",
                f"Command not recognized. I can help with files, folders, system tasks, and more. Say 'help' for details. 💡",
                f"Sorry, I don't know how to '{command}' yet. Need assistance? Say 'help'! 📋"
            ]
            return random.choice(suggestions)
            
        except Exception as e:
            error_msg = f"❌ Error executing command: {str(e)}"
            self.add_to_history(command, error_msg)
            return error_msg
    
    def handle_file_operations(self, command):
        """Handle all file-related operations"""
        # Create file with content
        if "create file" in command or "make file" in command:
            return self.create_file(command)
        
        # Delete file
        elif "delete file" in command or "remove file" in command:
            return self.delete_file(command)
        
        # Rename file
        elif "rename file" in command:
            return self.rename_file(command)
        
        # Copy file
        elif "copy file" in command:
            return self.copy_file(command)
        
        # Move file
        elif "move file" in command:
            return self.move_file(command)
        
        # Search file
        elif "search for file" in command or "find file" in command:
            return self.search_file(command)
        
        # File info
        elif "file info" in command or "file details" in command:
            return self.get_file_info(command)
        
        # List files with details
        elif "list files" in command or "show files" in command:
            return self.list_files(command)
        
        # Sort files
        elif "sort files" in command:
            return self.sort_files(command)
        
        # File compression
        elif "compress file" in command:
            return self.compress_file(command)
        
        return None
    
    def create_file(self, command):
        """Create a file with optional content"""
        try:
            # Extract filename and content
            filename = None
            content = ""
            
            # Pattern matching
            if "named" in command:
                parts = command.split("named")
                filename = parts[1].split("with")[0].strip() if "with" in parts[1] else parts[1].strip()
                if "with content" in command or "containing" in command:
                    content_parts = command.split("with content" if "with content" in command else "containing")
                    if len(content_parts) > 1:
                        content = content_parts[1].strip()
            elif "called" in command:
                parts = command.split("called")
                filename = parts[1].split("with")[0].strip() if "with" in parts[1] else parts[1].strip()
            else:
                # Extract from command pattern
                match = re.search(r'create file (.+?)(?: with content (.+))?$', command)
                if match:
                    filename = match.group(1).strip()
                    if match.group(2):
                        content = match.group(2).strip()
            
            if not filename:
                filename = f"document_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            
            # Ensure extension
            if '.' not in filename:
                filename += ".txt"
            
            # Create directory if needed
            os.makedirs(os.path.dirname(filename) if os.path.dirname(filename) else '.', exist_ok=True)
            
            # Write file
            with open(filename, 'w', encoding='utf-8') as f:
                if content:
                    f.write(content)
                else:
                    f.write(f"Created: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write(f"Created by Voice Assistant\n")
            
            size = os.path.getsize(filename)
            return f"✅ Created file: {os.path.abspath(filename)}\n📏 Size: {self.format_size(size)}"
            
        except Exception as e:
            return f"❌ Failed to create file: {str(e)}"
    
    def delete_file(self, command):
        """Delete file with confirmation check"""
        try:
            filename = self.extract_filename(command)
            
            if not filename:
                return "❌ Please specify a filename"
            
            # Check if file exists
            if not os.path.exists(filename):
                # Search for similar files
                similar = self.find_similar_files(filename)
                if similar:
                    return f"❌ File not found. Similar files: {', '.join(similar[:3])}"
                return f"❌ File '{filename}' not found"
            
            # Get file info before deletion
            file_info = f"Size: {self.format_size(os.path.getsize(filename))}, "
            file_info += f"Created: {datetime.datetime.fromtimestamp(os.path.getctime(filename)).strftime('%Y-%m-%d %H:%M:%S')}"
            
            # Delete
            os.remove(filename)
            return f"✅ Deleted: {filename}\n📊 {file_info}"
            
        except Exception as e:
            return f"❌ Failed to delete file: {str(e)}"
    
    def rename_file(self, command):
        """Rename file with pattern matching"""
        try:
            # Extract old and new names
            patterns = [
                r'rename file (.+?) to (.+)',
                r'rename (.+?) to (.+)',
                r'rename file (.+?) as (.+)'
            ]
            
            old_name = None
            new_name = None
            
            for pattern in patterns:
                match = re.search(pattern, command)
                if match:
                    old_name = match.group(1).strip()
                    new_name = match.group(2).strip()
                    break
            
            if not old_name or not new_name:
                return "❌ Usage: rename file oldname.txt to newname.txt"
            
            if not os.path.exists(old_name):
                return f"❌ File '{old_name}' not found"
            
            os.rename(old_name, new_name)
            return f"✅ Renamed '{old_name}' → '{new_name}'"
            
        except Exception as e:
            return f"❌ Failed to rename: {str(e)}"
    
    def copy_file(self, command):
        """Copy file to destination"""
        try:
            match = re.search(r'copy file (.+?) to (.+)', command)
            if match:
                source = match.group(1).strip()
                dest = match.group(2).strip()
                
                if not os.path.exists(source):
                    return f"❌ Source file '{source}' not found"
                
                shutil.copy2(source, dest)
                return f"✅ Copied '{source}' to '{dest}'"
            
            return "❌ Usage: copy file source.txt to destination/"
            
        except Exception as e:
            return f"❌ Failed to copy: {str(e)}"
    
    def move_file(self, command):
        """Move file to new location"""
        try:
            match = re.search(r'move file (.+?) to (.+)', command)
            if match:
                source = match.group(1).strip()
                dest = match.group(2).strip()
                
                if not os.path.exists(source):
                    return f"❌ Source file '{source}' not found"
                
                shutil.move(source, dest)
                return f"✅ Moved '{source}' to '{dest}'"
            
            return "❌ Usage: move file source.txt to destination/"
            
        except Exception as e:
            return f"❌ Failed to move: {str(e)}"
    
    def search_file(self, command):
        """Search for files by name or content"""
        try:
            search_term = command.replace("search for file", "").replace("find file", "").strip()
            
            if not search_term:
                return "❌ Please specify search term"
            
            results = []
            current_dir = os.getcwd()
            
            for root, dirs, files in os.walk(current_dir):
                for file in files:
                    if search_term.lower() in file.lower():
                        full_path = os.path.join(root, file)
                        rel_path = os.path.relpath(full_path, current_dir)
                        size = os.path.getsize(full_path)
                        results.append(f"📄 {rel_path} ({self.format_size(size)})")
                
                # Limit results
                if len(results) >= 20:
                    results.append("... and more")
                    break
            
            if results:
                return f"🔍 Search results for '{search_term}':\n" + "\n".join(results[:10])
            else:
                return f"🔍 No files found containing '{search_term}'"
                
        except Exception as e:
            return f"❌ Search failed: {str(e)}"
    
    def get_file_info(self, command):
        """Get detailed file information"""
        try:
            filename = self.extract_filename(command)
            
            if not filename or not os.path.exists(filename):
                return f"❌ File '{filename}' not found"
            
            stat = os.stat(filename)
            info = [
                f"📄 File: {filename}",
                f"📏 Size: {self.format_size(stat.st_size)}",
                f"📅 Created: {datetime.datetime.fromtimestamp(stat.st_ctime).strftime('%Y-%m-%d %H:%M:%S')}",
                f"📅 Modified: {datetime.datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')}",
                f"📅 Accessed: {datetime.datetime.fromtimestamp(stat.st_atime).strftime('%Y-%m-%d %H:%M:%S')}",
                f"🔒 Permissions: {oct(stat.st_mode)[-3:]}",
                f"📁 Location: {os.path.abspath(filename)}"
            ]
            
            # File type detection
            if filename.endswith(('.txt', '.md', '.csv', '.json', '.xml')):
                try:
                    with open(filename, 'r', encoding='utf-8') as f:
                        lines = sum(1 for _ in f)
                    info.append(f"📝 Lines: {lines}")
                except:
                    pass
            
            return "\n".join(info)
            
        except Exception as e:
            return f"❌ Failed to get file info: {str(e)}"
    
    def list_files(self, command):
        """List files with advanced options"""
        try:
            path = os.getcwd()
            
            # Check for specific path
            if "in" in command:
                path_part = command.split("in")[-1].strip()
                if os.path.isdir(path_part):
                    path = path_part
            
            files = os.listdir(path)
            
            # Filter options
            if "only" in command:
                if "folders" in command:
                    files = [f for f in files if os.path.isdir(os.path.join(path, f))]
                elif "files" in command:
                    files = [f for f in files if os.path.isfile(os.path.join(path, f))]
            
            # Sort options
            sort_by = "name"
            reverse = False
            
            if "sort by" in command:
                if "size" in command:
                    sort_by = "size"
                elif "date" in command or "time" in command:
                    sort_by = "date"
                elif "type" in command:
                    sort_by = "type"
            
            if "reverse" in command or "descending" in command:
                reverse = True
            
            # Sort files
            files = self.sort_file_list(files, path, sort_by, reverse)
            
            # Format output
            output = [f"📁 Directory: {os.path.basename(path)} [{len(files)} items]"]
            output.append("=" * 50)
            
            for item in files[:25]:  # Limit to 25 items
                full_path = os.path.join(path, item)
                if os.path.isdir(full_path):
                    item_count = len(os.listdir(full_path))
                    output.append(f"📁 {item}/ ({item_count} items)")
                else:
                    size = os.path.getsize(full_path)
                    ext = os.path.splitext(item)[1]
                    output.append(f"📄 {item} [{ext[1:] if ext else 'file'}] - {self.format_size(size)}")
            
            if len(files) > 25:
                output.append(f"... and {len(files) - 25} more items")
            
            return "\n".join(output)
            
        except Exception as e:
            return f"❌ Failed to list files: {str(e)}"
    
    def sort_file_list(self, files, path, sort_by="name", reverse=False):
        """Sort files based on criteria"""
        if sort_by == "name":
            files.sort(key=lambda x: x.lower(), reverse=reverse)
        elif sort_by == "size":
            files.sort(key=lambda x: os.path.getsize(os.path.join(path, x)) if os.path.isfile(os.path.join(path, x)) else 0, reverse=reverse)
        elif sort_by == "date":
            files.sort(key=lambda x: os.path.getmtime(os.path.join(path, x)), reverse=reverse)
        elif sort_by == "type":
            files.sort(key=lambda x: os.path.splitext(x)[1].lower(), reverse=reverse)
        
        # Always put folders first unless specified
        if not reverse:
            files.sort(key=lambda x: not os.path.isdir(os.path.join(path, x)))
        
        return files
    
    def compress_file(self, command):
        """Compress files or folders"""
        try:
            import zipfile
            
            # Extract source and destination
            if "compress" in command:
                parts = command.split("compress")[1].strip()
                if "to" in parts:
                    source = parts.split("to")[0].strip()
                    dest = parts.split("to")[1].strip()
                else:
                    source = parts
                    dest = source + ".zip"
            
            if not os.path.exists(source):
                return f"❌ Source '{source}' not found"
            
            with zipfile.ZipFile(dest, 'w', zipfile.ZIP_DEFLATED) as zipf:
                if os.path.isfile(source):
                    zipf.write(source, os.path.basename(source))
                else:
                    for root, dirs, files in os.walk(source):
                        for file in files:
                            file_path = os.path.join(root, file)
                            arcname = os.path.relpath(file_path, os.path.dirname(source))
                            zipf.write(file_path, arcname)
            
            original_size = self.get_total_size(source)
            compressed_size = os.path.getsize(dest)
            ratio = (compressed_size / original_size * 100) if original_size > 0 else 0
            
            return (f"✅ Compressed '{source}' to '{dest}'\n"
                   f"📊 Original: {self.format_size(original_size)}\n"
                   f"📊 Compressed: {self.format_size(compressed_size)}\n"
                   f"📈 Ratio: {ratio:.1f}%")
            
        except Exception as e:
            return f"❌ Compression failed: {str(e)}"
    
    def handle_folder_operations(self, command):
        """Handle folder operations"""
        # Create folder
        if "create folder" in command or "make folder" in command:
            return self.create_folder(command)
        
        # Delete folder
        elif "delete folder" in command or "remove folder" in command:
            return self.delete_folder(command)
        
        # Rename folder
        elif "rename folder" in command:
            return self.rename_folder(command)
        
        # Change directory
        elif "change directory" in command or "cd" in command or "go to" in command:
            return self.change_directory(command)
        
        # Current directory
        elif "current directory" in command or "pwd" in command or "where am i" in command:
            return self.show_current_directory()
        
        # Folder size
        elif "folder size" in command or "directory size" in command:
            return self.calculate_folder_size(command)
        
        # Clean folder
        elif "clean folder" in command or "tidy up" in command:
            return self.clean_folder(command)
        
        # Compare folders
        elif "compare folders" in command:
            return self.compare_folders(command)
        
        return None
    
    def create_folder(self, command):
        """Create folder with subdirectories"""
        try:
            # Extract folder name
            patterns = [
                r'create folder (.+?)(?: at (.+))?',
                r'make folder (.+?)(?: in (.+))?'
            ]
            
            folder_name = None
            location = "."
            
            for pattern in patterns:
                match = re.search(pattern, command)
                if match:
                    folder_name = match.group(1).strip()
                    if match.group(2):
                        location = match.group(2).strip()
                    break
            
            if not folder_name:
                folder_name = f"New_Folder_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            # Create full path
            full_path = os.path.join(location, folder_name)
            
            # Create folder and parents if needed
            os.makedirs(full_path, exist_ok=True)
            
            return f"✅ Created folder: {os.path.abspath(full_path)}"
            
        except Exception as e:
            return f"❌ Failed to create folder: {str(e)}"
    
    def delete_folder(self, command):
        """Delete folder with options"""
        try:
            folder_name = self.extract_filename(command)
            
            if not folder_name:
                return "❌ Please specify folder name"
            
            if not os.path.exists(folder_name):
                return f"❌ Folder '{folder_name}' not found"
            
            if not os.path.isdir(folder_name):
                return f"❌ '{folder_name}' is not a folder"
            
            # Check if folder is empty
            if len(os.listdir(folder_name)) == 0:
                os.rmdir(folder_name)
                return f"✅ Deleted empty folder: {folder_name}"
            else:
                if "force" in command or "recursive" in command:
                    shutil.rmtree(folder_name)
                    return f"✅ Force deleted folder: {folder_name}"
                else:
                    item_count = len(os.listdir(folder_name))
                    return (f"⚠️ Folder '{folder_name}' is not empty ({item_count} items)\n"
                           f"Use 'force delete folder {folder_name}' to delete with contents")
            
        except Exception as e:
            return f"❌ Failed to delete folder: {str(e)}"
    
    def change_directory(self, command):
        """Change directory with path completion"""
        try:
            # Extract path
            patterns = [
                r'change directory to (.+)',
                r'cd (.+)',
                r'go to (.+)',
                r'open folder (.+)'
            ]
            
            path = None
            for pattern in patterns:
                match = re.search(pattern, command)
                if match:
                    path = match.group(1).strip()
                    break
            
            if not path:
                return "❌ Please specify path"
            
            # Special paths
            special_paths = {
                "desktop": os.path.join(os.path.expanduser("~"), "Desktop"),
                "documents": os.path.join(os.path.expanduser("~"), "Documents"),
                "downloads": os.path.join(os.path.expanduser("~"), "Downloads"),
                "pictures": os.path.join(os.path.expanduser("~"), "Pictures"),
                "music": os.path.join(os.path.expanduser("~"), "Music"),
                "videos": os.path.join(os.path.expanduser("~"), "Videos"),
                "home": os.path.expanduser("~"),
                "root": "/" if platform.system() != "Windows" else "C:\\",
                "parent": "..",
                "previous": "-"
            }
            
            if path.lower() in special_paths:
                path = special_paths[path.lower()]
            
            # Change directory
            os.chdir(path)
            
            # Show new directory info
            return self.show_current_directory()
            
        except Exception as e:
            return f"❌ Failed to change directory: {str(e)}"
    
    def show_current_directory(self):
        """Show current directory with details"""
        current_dir = os.getcwd()
        items = os.listdir(current_dir)
        
        file_count = sum(1 for item in items if os.path.isfile(item))
        folder_count = sum(1 for item in items if os.path.isdir(item))
        hidden_count = sum(1 for item in items if item.startswith('.'))
        
        total_size = sum(os.path.getsize(f) for f in items if os.path.isfile(f))
        
        info = [
            f"📁 Current Directory: {os.path.basename(current_dir)}",
            f"📍 Path: {current_dir}",
            f"📊 Contents: {file_count} files, {folder_count} folders",
            f"📏 Total Size: {self.format_size(total_size)}",
            f"👁️ Hidden Items: {hidden_count}"
        ]
        
        # Disk space info
        try:
            disk = psutil.disk_usage(current_dir)
            info.append(f"💾 Disk: {disk.percent}% used ({self.format_size(disk.free)} free)")
        except:
            pass
        
        return "\n".join(info)
    
    def calculate_folder_size(self, command):
        """Calculate folder size with detailed breakdown"""
        try:
            # Extract folder path
            path = "."
            if "size of" in command:
                path = command.split("size of")[-1].strip()
            elif "folder size" in command:
                path = command.replace("folder size", "").strip()
            
            if not path or path == command:
                path = "."
            
            if not os.path.exists(path):
                return f"❌ Path '{path}' not found"
            
            if not os.path.isdir(path):
                # It's a file
                size = os.path.getsize(path)
                return f"📄 {os.path.basename(path)}: {self.format_size(size)}"
            
            # Calculate folder size
            total_size = 0
            file_count = 0
            folder_count = 0
            extension_stats = {}
            
            for dirpath, dirnames, filenames in os.walk(path):
                folder_count += len(dirnames)
                for filename in filenames:
                    filepath = os.path.join(dirpath, filename)
                    if os.path.exists(filepath):
                        try:
                            size = os.path.getsize(filepath)
                            total_size += size
                            file_count += 1
                            
                            # Track extensions
                            ext = os.path.splitext(filename)[1].lower()
                            if ext:
                                extension_stats[ext] = extension_stats.get(ext, 0) + size
                        except:
                            pass
            
            # Format results
            result = [
                f"📊 Folder Analysis: {os.path.basename(path)}",
                f"📁 Path: {os.path.abspath(path)}",
                f"📈 Total Size: {self.format_size(total_size)}",
                f"📄 Files: {file_count}",
                f"📁 Subfolders: {folder_count}",
                ""
            ]
            
            # Show largest extensions
            if extension_stats:
                result.append("📊 File Types (by size):")
                sorted_exts = sorted(extension_stats.items(), key=lambda x: x[1], reverse=True)
                for ext, size in sorted_exts[:5]:
                    percent = (size / total_size * 100) if total_size > 0 else 0
                    result.append(f"  {ext or 'no ext'}: {self.format_size(size)} ({percent:.1f}%)")
            
            return "\n".join(result)
            
        except Exception as e:
            return f"❌ Failed to calculate size: {str(e)}"
    
    def clean_folder(self, command):
        """Clean folder by removing temporary files"""
        try:
            path = "."
            if "clean" in command:
                path_part = command.split("clean")[1].strip()
                if path_part and not any(word in path_part for word in ["folder", "directory"]):
                    path = path_part
            
            temp_extensions = ['.tmp', '.temp', '.log', '.bak', '.old']
            removed = []
            total_freed = 0
            
            for root, dirs, files in os.walk(path):
                for file in files:
                    if any(file.lower().endswith(ext) for ext in temp_extensions):
                        filepath = os.path.join(root, file)
                        try:
                            size = os.path.getsize(filepath)
                            os.remove(filepath)
                            removed.append(file)
                            total_freed += size
                        except:
                            pass
            
            if removed:
                return (f"✅ Cleaned {len(removed)} temporary files\n"
                       f"🗑️ Files removed: {', '.join(removed[:5])}{'...' if len(removed) > 5 else ''}\n"
                       f"💾 Space freed: {self.format_size(total_freed)}")
            else:
                return "✅ No temporary files found to clean"
            
        except Exception as e:
            return f"❌ Clean failed: {str(e)}"
    
    def compare_folders(self, command):
        """Compare two folders"""
        try:
            # Extract two folder paths
            if "compare" in command:
                parts = command.split("compare")[1].strip()
                if "and" in parts:
                    folder1, folder2 = parts.split("and")
                    folder1 = folder1.strip()
                    folder2 = folder2.strip()
                else:
                    return "❌ Usage: compare folders /path1 and /path2"
            
            if not os.path.exists(folder1) or not os.path.exists(folder2):
                return "❌ One or both folders don't exist"
            
            # Get file lists
            files1 = set()
            files2 = set()
            
            for root, dirs, files in os.walk(folder1):
                for file in files:
                    rel_path = os.path.relpath(os.path.join(root, file), folder1)
                    files1.add(rel_path)
            
            for root, dirs, files in os.walk(folder2):
                for file in files:
                    rel_path = os.path.relpath(os.path.join(root, file), folder2)
                    files2.add(rel_path)
            
            # Compare
            only_in_1 = files1 - files2
            only_in_2 = files2 - files1
            common = files1 & files2
            
            result = [
                f"📊 Folder Comparison",
                f"📁 Folder A: {folder1}",
                f"📁 Folder B: {folder2}",
                "=" * 40,
                f"📈 Folder A only: {len(only_in_1)} files",
                f"📈 Folder B only: {len(only_in_2)} files",
                f"📈 Common files: {len(common)} files",
                ""
            ]
            
            if only_in_1:
                result.append("📁 Only in A (first 5):")
                for file in list(only_in_1)[:5]:
                    result.append(f"  • {file}")
            
            if only_in_2:
                result.append("\n📁 Only in B (first 5):")
                for file in list(only_in_2)[:5]:
                    result.append(f"  • {file}")
            
            return "\n".join(result)
            
        except Exception as e:
            return f"❌ Comparison failed: {str(e)}"
    
    def handle_system_operations(self, command):
        """Handle system-related operations"""
        # System info
        if "system info" in command or "system information" in command:
            return self.get_system_info()
        
        # CPU info
        elif "cpu" in command or "processor" in command:
            return self.get_cpu_info()
        
        # Memory info
        elif "memory" in command or "ram" in command:
            return self.get_memory_info()
        
        # Disk info
        elif "disk" in command or "storage" in command:
            return self.get_disk_info()
        
        # Battery
        elif "battery" in command:
            return self.get_battery_info()
        
        # Processes
        elif "processes" in command or "running apps" in command:
            return self.get_processes(command)
        
        # Services
        elif "services" in command:
            return self.get_services()
        
        # Uptime
        elif "uptime" in command or "how long running" in command:
            return self.get_uptime()
        
        # System control
        elif any(word in command for word in ["shutdown", "restart", "reboot", "sleep", "hibernate"]):
            return self.system_control(command)
        
        # Lock
        elif "lock" in command:
            return self.lock_system()
        
        # Screenshot
        elif "screenshot" in command or "capture screen" in command:
            return self.take_screenshot(command)
        
        # Volume control
        elif any(word in command for word in ["volume", "mute", "unmute"]):
            return self.control_volume(command)
        
        # Brightness control
        elif "brightness" in command:
            return self.control_brightness(command)
        
        return None
    
    def get_system_info(self):
        """Get detailed system information"""
        try:
            info = [
                "🖥️ SYSTEM INFORMATION",
                "=" * 40
            ]
            
            # Basic system info
            basic_info = {
                "System": platform.system(),
                "Node Name": platform.node(),
                "Release": platform.release(),
                "Version": platform.version(),
                "Machine": platform.machine(),
                "Processor": platform.processor(),
                "Architecture": platform.architecture()[0],
                "Python": platform.python_version()
            }
            
            for key, value in basic_info.items():
                info.append(f"{key:20}: {value}")
            
            info.append("")
            
            # CPU info
            cpu_info = {
                "Physical Cores": psutil.cpu_count(logical=False),
                "Logical Cores": psutil.cpu_count(logical=True),
                "CPU Usage": f"{psutil.cpu_percent(interval=0.1)}%",
                "Max Frequency": f"{psutil.cpu_freq().max:.0f} MHz" if psutil.cpu_freq() else "N/A"
            }
            
            info.append("💻 CPU INFORMATION")
            for key, value in cpu_info.items():
                info.append(f"{key:20}: {value}")
            
            info.append("")
            
            # Boot time
            boot_time = datetime.datetime.fromtimestamp(psutil.boot_time())
            uptime = datetime.datetime.now() - boot_time
            info.append(f"⏰ System Uptime: {str(uptime).split('.')[0]}")
            info.append(f"🕒 Boot Time: {boot_time.strftime('%Y-%m-%d %H:%M:%S')}")
            
            return "\n".join(info)
            
        except Exception as e:
            return f"❌ Failed to get system info: {str(e)}"
    
    def get_cpu_info(self):
        """Get detailed CPU information"""
        try:
            cpu_percent = psutil.cpu_percent(interval=1, percpu=True)
            avg_cpu = psutil.cpu_percent(interval=1)
            
            info = [
                "💻 CPU INFORMATION",
                "=" * 40,
                f"Total Usage: {avg_cpu}%",
                f"Cores: {psutil.cpu_count(logical=False)} physical, {psutil.cpu_count(logical=True)} logical",
                ""
            ]
            
            # Per-core usage
            if len(cpu_percent) <= 8:  # Show all if 8 or fewer cores
                for i, usage in enumerate(cpu_percent):
                    bar = "█" * int(usage / 5) + "░" * (20 - int(usage / 5))
                    info.append(f"Core {i:2}: {bar} {usage:5.1f}%")
            else:
                # Show first 4 and last 4
                for i in range(4):
                    usage = cpu_percent[i]
                    bar = "█" * int(usage / 5) + "░" * (20 - int(usage / 5))
                    info.append(f"Core {i:2}: {bar} {usage:5.1f}%")
                
                info.append(f"... {len(cpu_percent) - 8} cores hidden ...")
                
                for i in range(-4, 0):
                    usage = cpu_percent[i]
                    bar = "█" * int(usage / 5) + "░" * (20 - int(usage / 5))
                    info.append(f"Core {len(cpu_percent)+i:2}: {bar} {usage:5.1f}%")
            
            # Frequency info
            freq = psutil.cpu_freq()
            if freq:
                info.append("")
                info.append(f"Current Frequency: {freq.current:.0f} MHz")
                info.append(f"Min Frequency: {freq.min:.0f} MHz")
                info.append(f"Max Frequency: {freq.max:.0f} MHz")
            
            return "\n".join(info)
            
        except Exception as e:
            return f"❌ Failed to get CPU info: {str(e)}"
    
    def get_memory_info(self):
        """Get detailed memory information"""
        try:
            memory = psutil.virtual_memory()
            swap = psutil.swap_memory()
            
            info = [
                "💾 MEMORY INFORMATION",
                "=" * 40,
                f"Total RAM: {self.format_size(memory.total)}",
                f"Available: {self.format_size(memory.available)}",
                f"Used: {self.format_size(memory.used)} ({memory.percent}%)",
                f"Free: {self.format_size(memory.free)}",
                ""
            ]
            
            # Memory usage bar
            used_percent = memory.percent
            bar_length = 30
            used_bars = int(used_percent / 100 * bar_length)
            free_bars = bar_length - used_bars
            
            bar = "█" * used_bars + "░" * free_bars
            info.append(f"Usage: [{bar}] {used_percent:.1f}%")
            info.append("")
            
            # Swap memory
            info.append("💽 SWAP MEMORY")
            info.append(f"Total Swap: {self.format_size(swap.total)}")
            info.append(f"Used Swap: {self.format_size(swap.used)} ({swap.percent}%)")
            info.append(f"Free Swap: {self.format_size(swap.free)}")
            
            return "\n".join(info)
            
        except Exception as e:
            return f"❌ Failed to get memory info: {str(e)}"
    
    def get_disk_info(self):
        """Get detailed disk information"""
        try:
            partitions = psutil.disk_partitions()
            info = ["💿 DISK INFORMATION", "=" * 40]
            
            for partition in partitions:
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    
                    # Create usage bar
                    used_percent = usage.percent
                    bar_length = 20
                    used_bars = int(used_percent / 100 * bar_length)
                    free_bars = bar_length - used_bars
                    bar = "█" * used_bars + "░" * free_bars
                    
                    partition_info = [
                        f"📀 Device: {partition.device}",
                        f"📁 Mount: {partition.mountpoint}",
                        f"📊 Type: {partition.fstype}",
                        f"💾 Total: {self.format_size(usage.total)}",
                        f"📈 Used: {self.format_size(usage.used)} ({usage.percent}%)",
                        f"📉 Free: {self.format_size(usage.free)}",
                        f"📊 Usage: [{bar}]"
                    ]
                    
                    info.append("\n".join(partition_info))
                    info.append("-" * 40)
                    
                except:
                    continue
            
            return "\n".join(info)
            
        except Exception as e:
            return f"❌ Failed to get disk info: {str(e)}"
    
    def get_battery_info(self):
        """Get battery information"""
        try:
            battery = psutil.sensors_battery()
            
            if not battery:
                return "🔌 No battery detected (desktop computer?)"
            
            info = [
                "🔋 BATTERY INFORMATION",
                "=" * 40,
                f"Charge: {battery.percent}%",
                f"Status: {'Charging' if battery.power_plugged else 'Discharging'}",
            ]
            
            # Time remaining
            if battery.secsleft != psutil.POWER_TIME_UNLIMITED and battery.secsleft > 0:
                hours = battery.secsleft // 3600
                minutes = (battery.secsleft % 3600) // 60
                info.append(f"Time Left: {hours}h {minutes}m")
            
            # Create battery visualization
            battery_level = battery.percent
            if battery_level > 75:
                battery_icon = "🟢"
            elif battery_level > 25:
                battery_icon = "🟡"
            else:
                battery_icon = "🔴"
            
            bar_length = 10
            filled = int(battery_level / 100 * bar_length)
            empty = bar_length - filled
            battery_bar = "█" * filled + "░" * empty
            
            info.append(f"Visual: {battery_icon} [{battery_bar}]")
            
            return "\n".join(info)
            
        except Exception as e:
            return f"❌ Failed to get battery info: {str(e)}"
    
    def get_processes(self, command):
        """Get running processes with filtering"""
        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'status']):
                try:
                    processes.append(proc.info)
                except:
                    continue
            
            # Sort by CPU or Memory
            sort_by = "cpu"
            if "memory" in command:
                sort_by = "memory"
            elif "name" in command:
                sort_by = "name"
            
            if sort_by == "cpu":
                processes.sort(key=lambda x: x['cpu_percent'] or 0, reverse=True)
            elif sort_by == "memory":
                processes.sort(key=lambda x: x['memory_percent'] or 0, reverse=True)
            elif sort_by == "name":
                processes.sort(key=lambda x: x['name'].lower())
            
            # Filter if requested
            filter_term = None
            if "named" in command:
                filter_term = command.split("named")[-1].strip().lower()
            
            info = ["📊 RUNNING PROCESSES", "=" * 40]
            
            count = 0
            for proc in processes:
                if filter_term and filter_term not in proc['name'].lower():
                    continue
                
                if count >= 15:
                    info.append(f"... and {len(processes) - count} more processes")
                    break
                
                cpu_bar = "█" * min(int((proc['cpu_percent'] or 0) / 5), 20) + "░" * (20 - min(int((proc['cpu_percent'] or 0) / 5), 20))
                mem_bar = "█" * min(int((proc['memory_percent'] or 0) / 5), 20) + "░" * (20 - min(int((proc['memory_percent'] or 0) / 5), 20))
                
                info.append(f"📝 {proc['name'][:20]:20} PID:{proc['pid']:6}")
                info.append(f"     CPU: {cpu_bar} {proc['cpu_percent'] or 0:5.1f}%")
                info.append(f"     MEM: {mem_bar} {proc['memory_percent'] or 0:5.1f}%")
                info.append("")
                count += 1
            
            return "\n".join(info)
            
        except Exception as e:
            return f"❌ Failed to get processes: {str(e)}"
    
    def system_control(self, command):
        """Control system power states"""
        try:
            if "shutdown" in command:
                if platform.system() == "Windows":
                    os.system("shutdown /s /t 30")
                    return "⏹️ System will shutdown in 30 seconds. Cancel with: shutdown /a"
                else:
                    return "❌ Shutdown command not supported on this OS"
            
            elif "restart" in command or "reboot" in command:
                if platform.system() == "Windows":
                    os.system("shutdown /r /t 30")
                    return "🔄 System will restart in 30 seconds. Cancel with: shutdown /a"
                else:
                    return "❌ Restart command not supported on this OS"
            
            elif "sleep" in command:
                if platform.system() == "Windows":
                    os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
                    return "😴 Putting system to sleep"
                else:
                    return "❌ Sleep command not supported on this OS"
            
            elif "hibernate" in command:
                if platform.system() == "Windows":
                    os.system("shutdown /h")
                    return "💤 Hibernating system"
                else:
                    return "❌ Hibernate command not supported on this OS"
            
            return "❌ Unknown system control command"
            
        except Exception as e:
            return f"❌ System control failed: {str(e)}"
    
    def take_screenshot(self, command):
        """Take screenshot with options"""
        try:
            from PIL import ImageGrab
            
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"
            
            # Check for region
            region = None
            if "region" in command or "area" in command:
                # Extract coordinates like "region 100 200 300 400"
                coords = re.findall(r'\d+', command)
                if len(coords) >= 4:
                    region = tuple(map(int, coords[:4]))
            
            # Take screenshot
            if region:
                screenshot = ImageGrab.grab(bbox=region)
            else:
                screenshot = ImageGrab.grab()
            
            # Add timestamp
            if "timestamp" not in command or "notime" not in command:
                draw = ImageDraw.Draw(screenshot)
                # Simple text for now - would need font for better version
                timestamp_text = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                draw.text((10, 10), timestamp_text, fill=(255, 0, 0))
            
            screenshot.save(filename, 'PNG')
            
            # Get file info
            size = os.path.getsize(filename)
            dimensions = screenshot.size
            
            return (f"📸 Screenshot saved: {filename}\n"
                   f"📏 Size: {dimensions[0]}x{dimensions[1]}\n"
                   f"💾 File: {self.format_size(size)}\n"
                   f"📍 Path: {os.path.abspath(filename)}")
            
        except Exception as e:
            return f"❌ Failed to take screenshot: {str(e)}"
    
    def control_volume(self, command):
        """Control system volume"""
        try:
            if "mute" in command:
                for _ in range(3):
                    pyautogui.press("volumemute")
                return "🔇 Volume muted"
            
            elif "unmute" in command:
                for _ in range(3):
                    pyautogui.press("volumemute")
                return "🔊 Volume unmuted"
            
            elif "up" in command or "increase" in command:
                steps = 5
                if "a lot" in command or "maximum" in command:
                    steps = 20
                
                for _ in range(steps):
                    pyautogui.press("volumeup")
                return f"🔊 Volume increased ({steps} steps)"
            
            elif "down" in command or "decrease" in command or "lower" in command:
                steps = 5
                if "a lot" in command or "minimum" in command:
                    steps = 20
                
                for _ in range(steps):
                    pyautogui.press("volumedown")
                return f"🔉 Volume decreased ({steps} steps)"
            
            elif "set" in command or "to" in command:
                # Try to extract percentage
                percentages = re.findall(r'\d+', command)
                if percentages:
                    target = int(percentages[0])
                    # This is a simplified version - actual implementation would need
                    # platform-specific code or additional libraries
                    return f"🔊 Volume set to {target}% (simulated)"
            
            return "❌ Volume command not recognized"
            
        except Exception as e:
            return f"❌ Failed to control volume: {str(e)}"
    
    def handle_network_operations(self, command):
        """Handle network-related operations"""
        # IP address
        if "ip address" in command or "ip" in command:
            return self.get_ip_address()
        
        # Network speed
        elif "network speed" in command or "internet speed" in command:
            return self.test_network_speed()
        
        # Ping
        elif "ping" in command:
            return self.ping_host(command)
        
        # Port check
        elif "port" in command:
            return self.check_port(command)
        
        # DNS
        elif "dns" in command:
            return self.get_dns_info()
        
        # Network info
        elif "network info" in command:
            return self.get_network_info()
        
        return None
    
    def get_ip_address(self):
        """Get IP addresses (local and public)"""
        try:
            info = ["🌐 NETWORK ADDRESSES", "=" * 40]
            
            # Local IP
            hostname = socket.gethostname()
            local_ip = socket.gethostbyname(hostname)
            info.append(f"Local IP: {local_ip}")
            info.append(f"Hostname: {hostname}")
            
            # Get all network interfaces
            try:
                interfaces = psutil.net_if_addrs()
                for interface, addresses in interfaces.items():
                    for addr in addresses:
                        if addr.family == socket.AF_INET:  # IPv4
                            info.append(f"{interface}: {addr.address}")
            except:
                pass
            
            # Try to get public IP (optional)
            try:
                import urllib.request
                public_ip = urllib.request.urlopen('https://api.ipify.org').read().decode('utf8')
                info.append(f"Public IP: {public_ip}")
            except:
                info.append("Public IP: Could not determine")
            
            return "\n".join(info)
            
        except Exception as e:
            return f"❌ Failed to get IP address: {str(e)}"
    
    def test_network_speed(self):
        """Test network speed (simplified)"""
        try:
            import speedtest  # Would need to install speedtest-cli
            
            info = ["🚀 NETWORK SPEED TEST", "=" * 40]
            info.append("Testing... This may take a moment.")
            
            st = speedtest.Speedtest()
            st.get_best_server()
            
            download = st.download() / 1_000_000  # Convert to Mbps
            upload = st.upload() / 1_000_000  # Convert to Mbps
            
            info.append(f"Download: {download:.2f} Mbps")
            info.append(f"Upload: {upload:.2f} Mbps")
            info.append(f"Ping: {st.results.ping:.0f} ms")
            
            return "\n".join(info)
            
        except ImportError:
            return "❌ Install speedtest-cli: pip install speedtest-cli"
        except Exception as e:
            return f"❌ Speed test failed: {str(e)}"
    
    def ping_host(self, command):
        """Ping a host"""
        try:
            # Extract host from command
            host = command.replace("ping", "").strip()
            if not host:
                host = "google.com"
            
            info = [f"📡 PINGING {host}", "=" * 40]
            
            # Platform-specific ping command
            param = '-n' if platform.system().lower() == 'windows' else '-c'
            count = 4
            
            result = subprocess.run(
                ['ping', param, str(count), host],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                # Parse ping results
                lines = result.stdout.split('\n')
                for line in lines[-5:]:
                    if line.strip():
                        info.append(line.strip())
                info.append(f"✅ {host} is reachable")
            else:
                info.append(f"❌ {host} is not reachable")
            
            return "\n".join(info)
            
        except subprocess.TimeoutExpired:
            return f"⏰ Ping to {host} timed out"
        except Exception as e:
            return f"❌ Ping failed: {str(e)}"
    
    def handle_media_operations(self, command):
        """Handle media playback operations"""
        # Play/Pause (specific content check)
        if "play" in command:
            # Check if it's a specific "play [content]" command
            # Filter out simple "play", "play music", "play resume"
            cleaned = command.replace("play", "").strip()
            if cleaned and cleaned not in ["music", "resume", "pause", "stop"]:
                 return self.play_specific_content(command)
            else:
                 return self.control_media(command)

        elif any(word in command for word in ["pause", "stop", "next", "previous"]):
            return self.control_media(command)
        
        # Media info
        elif "what's playing" in command:
            return self.get_media_info()
        
        return None
    
    def control_media(self, command):
        """Control media playback"""
        try:
            if "play" in command:
                pyautogui.press("playpause")
                return "▶️ Media playback started/resumed"
            
            elif "pause" in command:
                pyautogui.press("playpause")
                return "⏸️ Media playback paused"
            
            elif "stop" in command:
                # Some media players use stop key
                pyautogui.press("stop")
                return "⏹️ Media playback stopped"
            
            elif "next" in command:
                pyautogui.press("nexttrack")
                return "⏭️ Next track"
            
            elif "previous" in command or "prev" in command:
                pyautogui.press("prevtrack")
                return "⏮️ Previous track"
            
            elif "volume" in command:
                return self.control_volume(command)
            
            return "❌ Media command not recognized"
            
        except Exception as e:
            return f"❌ Failed to control media: {str(e)}"
    
    def handle_productivity_operations(self, command):
        """Handle productivity tools"""
        # Calculator
        if any(word in command for word in ["calculate", "plus", "minus", "times", "divide", "multiply"]):
            return self.calculate(command)
        
        # Timer
        elif "timer" in command:
            return self.set_timer(command)
        
        # Alarm
        elif "alarm" in command:
            return self.set_alarm(command)
        
        # Reminder
        elif "remind" in command or "reminder" in command:
            return self.set_reminder(command)
        
        # Notes
        elif "note" in command:
            return self.take_note(command)
        
        # Clipboard
        elif "clipboard" in command:
            return self.manage_clipboard(command)
        
        return None
    
    def calculate(self, command):
        """Enhanced calculator with more operations"""
        try:
            # Clean the command
            calc_text = command.lower()
            
            # Replace words with operators
            replacements = {
                "plus": "+", "add": "+", "and": "+",
                "minus": "-", "subtract": "-", "less": "-",
                "times": "*", "multiply": "*", "multiplied by": "*", "x": "*",
                "divided by": "/", "divide": "/", "over": "/",
                "modulo": "%", "mod": "%",
                "to the power of": "**", "power": "**", "^": "**",
                "square root of": "math.sqrt(",
                "squared": "**2",
                "cubed": "**3"
            }
            
            for word, symbol in replacements.items():
                calc_text = calc_text.replace(word, symbol)
            
            # Extract mathematical expression
            # Remove non-math characters but keep numbers, operators, parentheses, and math functions
            import math
            
            # Try to find calculation pattern
            patterns = [
                r'calculate (.+)',
                r'what is (.+)',
                r'compute (.+)',
                r'(.+) equals'
            ]
            
            expression = None
            for pattern in patterns:
                match = re.search(pattern, calc_text)
                if match:
                    expression = match.group(1).strip()
                    break
            
            if not expression:
                # Try to extract just the math part
                expression = re.sub(r'[^0-9+\-*/().%^ ]', '', calc_text).strip()
            
            if not expression:
                return "❌ Please provide a calculation"
            
            # Handle special functions
            if "math.sqrt" in expression:
                # Close the parenthesis if missing
                if expression.count("(") > expression.count(")"):
                    expression += ")"
            
            # Add missing multiplication symbols (e.g., "2(3+4)" -> "2*(3+4)")
            expression = re.sub(r'(\d)(\()', r'\1*\2', expression)
            expression = re.sub(r'(\))(\d)', r'\1*\2', expression)
            
            # Safe evaluation
            allowed_names = {
                'math': math,
                'sqrt': math.sqrt,
                'sin': math.sin,
                'cos': math.cos,
                'tan': math.tan,
                'log': math.log,
                'log10': math.log10,
                'pi': math.pi,
                'e': math.e
            }
            
            # Evaluate
            result = eval(expression, {"__builtins__": {}}, allowed_names)
            
            # Format result
            if isinstance(result, float):
                if result.is_integer():
                    result = int(result)
                else:
                    # Round to reasonable precision
                    result = round(result, 10)
                    # Remove trailing zeros
                    result = format(result, 'f').rstrip('0').rstrip('.')
            
            return f"🧮 Calculation: {expression} = {result}"
            
        except ZeroDivisionError:
            return "❌ Cannot divide by zero"
        except Exception as e:
            return f"❌ Calculation error: {str(e)}"
    
    def set_timer(self, command):
        """Set a timer"""
        try:
            # Extract time
            time_pattern = r'(\d+)\s*(seconds?|minutes?|hours?|secs?|mins?|hrs?)'
            matches = re.findall(time_pattern, command, re.IGNORECASE)
            
            if not matches:
                return "❌ Usage: set timer for 5 minutes"
            
            total_seconds = 0
            time_units = []
            
            for amount, unit in matches:
                amount = int(amount)
                unit = unit.lower()
                
                if unit.startswith('hour') or unit.startswith('hr'):
                    total_seconds += amount * 3600
                    time_units.append(f"{amount} hour{'s' if amount != 1 else ''}")
                elif unit.startswith('min'):
                    total_seconds += amount * 60
                    time_units.append(f"{amount} minute{'s' if amount != 1 else ''}")
                elif unit.startswith('sec'):
                    total_seconds += amount
                    time_units.append(f"{amount} second{'s' if amount != 1 else ''}")
            
            time_str = " and ".join(time_units)
            end_time = datetime.datetime.now() + datetime.timedelta(seconds=total_seconds)
            
            # Store timer (simplified - would need background thread in real implementation)
            timer_file = "assistant_timers.json"
            timers = []
            
            if os.path.exists(timer_file):
                with open(timer_file, 'r') as f:
                    timers = json.load(f)
            
            timer_id = str(uuid.uuid4())[:8]
            timers.append({
                'id': timer_id,
                'duration': total_seconds,
                'end_time': end_time.isoformat(),
                'command': command,
                'active': True
            })
            
            with open(timer_file, 'w') as f:
                json.dump(timers, f)
            
            return f"⏰ Timer set for {time_str}\n🕒 Will end at: {end_time.strftime('%H:%M:%S')}"
            
        except Exception as e:
            return f"❌ Failed to set timer: {str(e)}"
    
    def manage_clipboard(self, command):
        """Manage clipboard operations"""
        try:
            if "show" in command or "what" in command or "get" in command:
                content = pyperclip.paste()
                if content:
                    # Truncate if too long
                    if len(content) > 200:
                        preview = content[:200] + "..."
                    else:
                        preview = content
                    
                    lines = len(content.split('\n'))
                    words = len(content.split())
                    
                    return (f"📋 Clipboard Contents:\n"
                           f"📝 Preview: {preview}\n"
                           f"📊 Stats: {len(content)} chars, {lines} lines, {words} words")
                else:
                    return "📋 Clipboard is empty"
            
            elif "clear" in command or "empty" in command:
                pyperclip.copy("")
                return "✅ Clipboard cleared"
            
            elif "copy" in command and "to" in command:
                # Extract text to copy
                if "text" in command:
                    text_start = command.find("text") + 4
                    text = command[text_start:].strip()
                    if text:
                        pyperclip.copy(text)
                        return f"✅ Copied to clipboard: {text[:50]}..."
                
                return "❌ Please specify text to copy"
            
            elif "save" in command:
                # Save clipboard to file
                content = pyperclip.paste()
                if content:
                    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                    filename = f"clipboard_{timestamp}.txt"
                    
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(content)
                    
                    return f"💾 Clipboard saved to: {filename}"
                else:
                    return "📋 Clipboard is empty"
            
            elif "history" in command:
                # Show clipboard history (simplified)
                return "📋 Clipboard history feature would require additional setup"
            
            return "❌ Clipboard command not recognized"
            
        except Exception as e:
            return f"❌ Clipboard operation failed: {str(e)}"
    
    def handle_utility_operations(self, command):
        """Handle utility operations"""
        # Time and date
        if any(word in command for word in ["time", "date", "day", "clock"]):
            return self.get_time_info(command)
        
        # Weather
        elif "weather" in command:
            return self.get_weather(command)
        
        # Convert units
        elif "convert" in command or any(word in command for word in ["inches", " cm ", " kg ", "pounds"]):
            return self.convert_units(command)
        
        # Random
        elif any(word in command for word in ["random", "choose", "pick", "dice", "coin"]):
            return self.random_operations(command)
        
        # Encode/Decode
        elif any(word in command for word in ["encode", "decode", "encrypt", "decrypt"]):
            return self.encode_decode(command)
        
        # Hash
        elif "hash" in command:
            return self.calculate_hash(command)
        
        return None
    
    def get_time_info(self, command):
        """Get time and date information"""
        now = datetime.datetime.now()
        
        if "time" in command:
            time_str = now.strftime("%I:%M:%S %p")
            timezone = time.tzname[0] if time.daylight else time.tzname[1]
            
            return f"🕒 Current Time: {time_str} ({timezone})"
        
        elif "date" in command:
            date_str = now.strftime("%A, %B %d, %Y")
            day_of_year = now.timetuple().tm_yday
            week_number = now.isocalendar()[1]
            
            return (f"📅 Today is: {date_str}\n"
                   f"📆 Day of year: {day_of_year}\n"
                   f"📆 Week number: {week_number}")
        
        elif "day" in command:
            day_str = now.strftime("%A")
            return f"📆 Today is {day_str}"
        
        elif "full" in command or "detailed" in command:
            info = [
                "🕒 TIME & DATE INFORMATION",
                "=" * 40,
                f"Date: {now.strftime('%A, %B %d, %Y')}",
                f"Time: {now.strftime('%I:%M:%S %p')}",
                f"Timezone: {time.tzname[0] if time.daylight else time.tzname[1]}",
                f"ISO Format: {now.isoformat()}",
                f"Unix Timestamp: {int(now.timestamp())}",
                f"Day of Year: {now.timetuple().tm_yday}",
                f"Week Number: {now.isocalendar()[1]}",
                f"Quarter: {(now.month - 1) // 3 + 1}",
                ""
            ]
            
            # Time in other timezones (example)
            info.append("🌍 Other Timezones:")
            info.append(f"  UTC: {datetime.datetime.utcnow().strftime('%H:%M:%S')}")
            
            return "\n".join(info)
        
        return None
    
    def convert_units(self, command):
        """Convert between different units"""
        try:
            # Extract numbers and units
            numbers = re.findall(r'\d+\.?\d*', command)
            if not numbers:
                return "❌ Please specify a value to convert"
            
            value = float(numbers[0])
            
            # Temperature
            if "celsius" in command and "fahrenheit" in command:
                if "to fahrenheit" in command or "fahrenheit" in command:
                    result = (value * 9/5) + 32
                    return f"🌡️ {value}°C = {result:.1f}°F"
                else:
                    result = (value - 32) * 5/9
                    return f"🌡️ {value}°F = {result:.1f}°C"
            
            # Length
            elif any(word in command for word in ["meter", "foot", "inch", "cm", "mm", "yard", "mile", "kilometer"]):
                conversions = {
                    'meter': 1,
                    'foot': 3.28084,
                    'inch': 39.3701,
                    'cm': 100,
                    'mm': 1000,
                    'yard': 1.09361,
                    'mile': 0.000621371,
                    'kilometer': 0.001
                }
                
                # Find from and to units
                from_unit = None
                to_unit = None
                
                for unit in conversions:
                    if unit in command:
                        if not from_unit:
                            from_unit = unit
                        elif not to_unit:
                            to_unit = unit
                
                if from_unit and to_unit:
                    # Convert to meters first
                    in_meters = value / conversions[from_unit]
                    # Convert to target unit
                    result = in_meters * conversions[to_unit]
                    return f"📏 {value} {from_unit} = {result:.4f} {to_unit}"
            
            # Weight
            elif any(word in command for word in ["kg", "pound", "ounce", "gram"]):
                if "kg" in command and "pound" in command:
                    if "to pound" in command:
                        result = value * 2.20462
                        return f"⚖️ {value} kg = {result:.2f} pounds"
                    else:
                        result = value / 2.20462
                        return f"⚖️ {value} pounds = {result:.2f} kg"
            
            # Digital storage
            elif any(word in command for word in ["byte", "kb", "mb", "gb", "tb"]):
                units = ['B', 'KB', 'MB', 'GB', 'TB']
                idx = 0
                
                # Find source unit
                for i, unit in enumerate(units):
                    if unit.lower() in command.replace('byte', 'b'):
                        idx = i
                        break
                
                # Convert through bytes
                bytes_value = value * (1024 ** idx)
                
                # Convert to other units
                results = []
                for i, unit in enumerate(units):
                    converted = bytes_value / (1024 ** i)
                    results.append(f"{converted:.2f} {unit}")
                
                return f"💾 Storage Conversion:\n" + "\n".join(results)
            
            return "❌ Conversion type not supported"
            
        except Exception as e:
            return f"❌ Conversion failed: {str(e)}"
    
    def random_operations(self, command):
        """Generate random values"""
        try:
            if "number" in command:
                # Extract range
                numbers = re.findall(r'\d+', command)
                if len(numbers) >= 2:
                    start, end = map(int, numbers[:2])
                elif len(numbers) == 1:
                    start, end = 1, int(numbers[0])
                else:
                    start, end = 1, 100
                
                result = random.randint(start, end)
                return f"🔢 Random number between {start} and {end}: {result}"
            
            elif "dice" in command:
                # Check for different dice
                numbers = re.findall(r'\d+', command)
                if numbers:
                    sides = int(numbers[0])
                else:
                    sides = 6
                
                result = random.randint(1, sides)
                return f"🎲 {sides}-sided dice roll: {result}"
            
            elif "coin" in command or "flip" in command:
                result = random.choice(["Heads", "Tails"])
                return f"🪙 Coin flip: {result}"
            
            elif "choose" in command or "pick" in command:
                # Extract options (simplified)
                if "between" in command:
                    options_text = command.split("between")[-1].strip()
                    # Split by "and" or commas
                    if "and" in options_text:
                        options = options_text.split("and")
                    else:
                        options = options_text.split(",")
                    
                    options = [opt.strip() for opt in options if opt.strip()]
                    
                    if len(options) >= 2:
                        result = random.choice(options)
                        return f"🎯 I choose: {result}"
                
                return "❌ Please specify options to choose from"
            
            elif "password" in command:
                # Generate password
                length = 12
                numbers = re.findall(r'\d+', command)
                if numbers:
                    length = min(max(int(numbers[0]), 8), 32)
                
                chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*"
                password = ''.join(random.choice(chars) for _ in range(length))
                
                return f"🔐 Generated password ({length} chars): {password}"
            
            elif "uuid" in command:
                uuid_str = str(uuid.uuid4())
                return f"🆔 Generated UUID: {uuid_str}"
            
            return "❌ Random operation not recognized"
            
        except Exception as e:
            return f"❌ Random operation failed: {str(e)}"
        except Exception as e:
            return f"❌ Random operation failed: {str(e)}"

    def play_specific_content(self, command):
        """Play specific content on YouTube or other platforms"""
        try:
            # Extract content and platform
            # specific play command: "play [content] on [platform]"
            import urllib.parse
            
            platform_name = "youtube" # Default
            content = command
            
            if " on " in command:
                parts = command.split(" on ")
                content = parts[0]
                platform_name = parts[1].strip()
            
            content = content.replace("play", "").strip()
            encoded_content = urllib.parse.quote(content)
            
            if "spotify" in platform_name:
                # Open spotify web or app protocol
                # spotify:search:query
                # But windows 'start spotify:...' is flaky without app logic
                # Let's fallback to web for reliability or try protocol
                try:
                    os.system(f"start spotify:search:{encoded_content}")
                    return f"🎵 Searching '{content}' on Spotify"
                except:
                    url = f"https://open.spotify.com/search/{encoded_content}"
                    webbrowser.open(url)
                    return f"🎵 Opening Spotify Web for: {content}"
            
            else:
                # Default to YouTube
                url = f"https://www.youtube.com/results?search_query={encoded_content}"
                # If the user literally said "play video of..." 
                # We could try a "I'm feeling lucky" approach but search results is safer
                webbrowser.open(url)
                return f"📺 Playing/Searching '{content}' on YouTube"
                
        except Exception as e:
            return f"❌ Failed to play content: {str(e)}"

    def handle_keyboard_operations(self, command):
        """Handle keyboard typing and pressing"""
        if command.startswith("type "):
            text = command.replace("type ", "").strip()
            if text:
                # Type with small delay to look natural and work better
                pyautogui.write(text, interval=0.01)
                return f"⌨️ Typed: '{text}'"
        
        elif command.startswith("press ") or command.startswith("hit "):
            keys = command.replace("press ", "").replace("hit ", "").strip().split()
            # Handle combo (e.g. ctrl+c) logic if needed, but pyautogui handles 'ctrl', 'c' sequence
            # For combos like "press ctrl+c", we need hotkey
            if "+" in keys[0]:
                combo = keys[0].split("+")
                pyautogui.hotkey(*combo)
                return f"⌨️ Pressed Combo: {keys[0]}"
            else:
                pyautogui.press(keys)
                return f"⌨️ Pressed: {', '.join(keys)}"
                
        elif command == "enter" or command == "return":
             pyautogui.press("enter")
             return "⌨️ Pressed Enter"
             
        return None

    def handle_app_operations(self, command):
        """Handle application opening (Universal Opener)"""
        if any(w in command for w in ["open", "launch", "start", "go to"]):
            # Extract target
            target = command.replace("open", "").replace("launch", "").replace("start", "").replace("go to", "").strip()
            
            # Skip if empty or if it's likely a web search/command meant for other handlers
            if not target or "google" in target or "search" in target or "youtube" in target or "email" in target or "directory" in target or "folder" in target:
                return None
            
            # List of known common Windows apps to map nicely
            common_apps = {
                "notepad": "notepad",
                "calculator": "calc",
                "paint": "mspaint",
                "cmd": "cmd",
                "terminal": "wt",
                "explorer": "explorer",
                "word": "winword",
                "excel": "excel",
                "powerpoint": "powerpnt",
                "settings": "ms-settings:",
                "store": "ms-windows-store:",
                "edge": "msedge",
                "chrome": "chrome",
                "firefox": "firefox",
                "spotify": "spotify",
                "discord": "discord"
            }
            
            # Check for direct match or partial match
            app_cmd = target
            for name, cmd in common_apps.items():
                if name in target:
                    app_cmd = cmd
                    break
            
            
            try:
                # Use Windows 'start' command which is versatile (opens apps, files, directories, URLs)
                # shell=True is needed for 'start'
                os.system(f"start {app_cmd}")
                return f"🚀 Opening: {target}"
            except Exception as e:
                return f"❌ Failed to open '{target}': {str(e)}"
                
        return None

    def handle_shell_operations(self, command):
        """Handle shell command execution via voice"""
        triggers = ["run command", "execute command", "run terminal", "system command"]
        prefix = ""
        
        # Check for explicitly longer triggers first
        for t in triggers:
            if t in command:
                prefix = t
                break
        
        # Fallback to simple "run" or "execute" if followed by something
        if not prefix:
            if command.startswith("run ") or command.startswith("execute "):
                prefix = command.split()[0]
        
        if prefix:
            cmd = command.replace(prefix, "").strip()
            if not cmd:
                return "❌ What command should I run?"
                
            # Dangerous commands blocklist
            dangerous = ["rm -rf", "format", "del /s", "rd /s"]
            if any(d in cmd for d in dangerous):
                return "❌ I cannot execute that command for safety reasons."
            
            try:
                # Execute synchronously to get output
                print(f"💻 EXECUTING SHELL: {cmd}")
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
                
                output = result.stdout.strip() or result.stderr.strip()
                
                if not output:
                    return f"✅ Command '{cmd}' executed (no output)"
                
                # Truncate for speech, assume full output in terminal
                preview = output[:100].replace("\n", " ") + "..." if len(output) > 100 else output
                print(f"📄 OUTPUT:\n{output}")
                
                return f"💻 executed '{cmd}'. Output: {preview}"
            except Exception as e:
                return f"❌ Command execution failed: {str(e)}"
        
        return None
    def handle_web_operations(self, command):
        """Handle web and browser operations"""
        # Explicitly handle "open google" to prevent it from being treated as an empty search
        if command.strip() in ["open google", "google", "open google com"]:
            return self.open_website("open google")

        # Search
        if any(word in command for word in ["search", "google", "look up"]):
            return self.web_search(command)

        # Explicit Web Open (specific to websites list)
        elif "open" in command and any(site in command for site in ["youtube", "email", "gmail", "facebook", "twitter", "reddit", "instagram"]):
             return self.open_website(command)
        
        # Download
        elif "download" in command:
            return self.download_file(command)
        
        # Bookmarks
        elif "bookmark" in command:
            return self.manage_bookmarks(command)
        
        return None
    
    def web_search(self, command):
        """Perform web search"""
        try:
            # Extract search query
            query = None
            if "search for" in command:
                query = command.split("search for")[-1].strip()
            elif "google" in command:
                query = command.split("google")[-1].strip()
            elif "look up" in command:
                query = command.split("look up")[-1].strip()
            
            if not query:
                return "❌ What would you like me to search for?"
            
            # Choose search engine
            search_engine = "https://www.google.com/search?q="
            if "bing" in command:
                search_engine = "https://www.bing.com/search?q="
            elif "duckduckgo" in command or "ddg" in command:
                search_engine = "https://duckduckgo.com/?q="
            elif "youtube" in command:
                search_engine = "https://www.youtube.com/results?search_query="
            
            # Open browser
            webbrowser.open(search_engine + query.replace(" ", "+"))
            
            return f"🔍 Searching for: {query}"
            
        except Exception as e:
            return f"❌ Search failed: {str(e)}"
    
    def open_website(self, command):
        """Open specific websites"""
        try:
            websites = {
                "youtube": "https://youtube.com",
                "gmail": "https://gmail.com",
                "google": "https://google.com",
                "github": "https://github.com",
                "facebook": "https://facebook.com",
                "twitter": "https://twitter.com",
                "linkedin": "https://linkedin.com",
                "wikipedia": "https://wikipedia.org",
                "amazon": "https://amazon.com",
                "netflix": "https://netflix.com",
                "stackoverflow": "https://stackoverflow.com",
                "reddit": "https://reddit.com",
                "instagram": "https://instagram.com",
                "whatsapp": "https://web.whatsapp.com",
                "outlook": "https://outlook.com",
                "drive": "https://drive.google.com",
                "docs": "https://docs.google.com",
                "sheets": "https://sheets.google.com",
                "calendar": "https://calendar.google.com",
                "maps": "https://maps.google.com",
                "weather": "https://weather.com",
                "news": "https://news.google.com",
                "bbc": "https://bbc.com/news",
                "cnn": "https://cnn.com",
                "email": "https://gmail.com"  # Default email to gmail
            }
            
            for site, url in websites.items():
                if site in command:
                    webbrowser.open(url)
                    return f"🌐 Opening {site.capitalize()}"
            
            # Try to extract URL directly
            if "http" in command or "www" in command:
                # Extract URL
                url_match = re.search(r'(https?://\S+|www\.\S+)', command)
                if url_match:
                    url = url_match.group(0)
                    if not url.startswith('http'):
                        url = 'https://' + url
                    webbrowser.open(url)
                    return f"🌐 Opening: {url}"
            
            # Try to infer website name from command if it starts with "open"
            if command.startswith("open "):
                site_name = command.replace("open ", "").strip().split()[0]
                if site_name:
                    # Heuristic: assume .com
                    url = f"https://{site_name}.com"
                    webbrowser.open(url)
                    return f"🌐 Opening: {site_name}.com (inferred)"

            return "❌ Website not recognized. Try: open youtube, open google, etc."
            
        except Exception as e:
            return f"❌ Failed to open website: {str(e)}"
    
    def handle_conversation(self, command):
        """Handle conversation and interaction"""
        responses = {
            "hello": ["Hello! 👋", "Hi there! 😊", "Hey! How can I help? 🎯"],
            "hi": ["Hello! 👋", "Hi there! 😊", "Hey! 🚀"],
            "how are you": ["I'm doing great, thanks! 😄", "All systems operational! ⚡", "Ready to assist! 🤖"],
            "your name": ["I'm your Voice Assistant! 🤖", "You can call me VA! 💫", "I'm Assistant, at your service! 🎩"],
            "thank you": ["You're welcome! 😊", "My pleasure! 👍", "Happy to help! 🤗"],
            "good morning": ["Good morning! ☀️", "Morning! Hope you have a great day! 🌅"],
            "good night": ["Good night! 🌙", "Sleep well! 💤", "Sweet dreams! 🌠"],
            "who made you": ["I was created by an AI developer to help you! 💻", "I'm the product of creative programming! 🎨"],
            "what are you": ["I'm a voice assistant designed to help with computer tasks! 🤖", "I'm your digital assistant! 💻"],
            "joke": self.get_joke(),
            "fact": self.get_fact(),
            "quote": self.get_quote(),
            "advice": ["Always backup your important files! 💾", "Take regular breaks when working! ☕", "Keep learning new things! 📚"]
        }
        
        for key, response in responses.items():
            if key in command:
                if callable(response):
                    return response()
                return random.choice(response) if isinstance(response, list) else response
        
        return None
    
    def get_joke(self):
        """Get a random joke"""
        jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "Why did the scarecrow win an award? He was outstanding in his field!",
            "What do you call a fish wearing a bowtie? Sofishticated!",
            "Why don't eggs tell jokes? They'd crack each other up!",
            "What do you call a factory that makes okay products? A satisfactory!",
            "Why did the math book look so sad? Because it had too many problems!",
            "What do you call a bear with no teeth? A gummy bear!",
            "Why can't you give Elsa a balloon? Because she will let it go!",
            "What do you call cheese that isn't yours? Nacho cheese!",
            "Why did the computer go to the doctor? Because it had a virus!"
        ]
        return f"😂 {random.choice(jokes)}"
    
    def get_fact(self):
        """Get a random fact"""
        facts = [
            "Honey never spoils. Archaeologists have found honey in ancient Egyptian tombs that's over 3,000 years old!",
            "Octopuses have three hearts. Two pump blood to the gills, while the third pumps it to the rest of the body.",
            "Bananas are berries, but strawberries aren't.",
            "A day on Venus is longer than a year on Venus.",
            "The shortest war in history was between Britain and Zanzibar on August 27, 1896. Zanzibar surrendered after 38 minutes.",
            "There are more possible iterations of a game of chess than there are atoms in the known universe.",
            "A group of flamingos is called a 'flamboyance'.",
            "The inventor of the frisbee was turned into a frisbee after he died.",
            "A cloud can weigh more than a million pounds.",
            "The Eiffel Tower can be 15 cm taller during the summer due to thermal expansion."
        ]
        return f"📚 {random.choice(facts)}"
    
    def get_quote(self):
        """Get a random quote"""
        quotes = [
            "The only way to do great work is to love what you do. - Steve Jobs",
            "Innovation distinguishes between a leader and a follower. - Steve Jobs",
            "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt",
            "Don't watch the clock; do what it does. Keep going. - Sam Levenson",
            "Believe you can and you're halfway there. - Theodore Roosevelt",
            "It always seems impossible until it's done. - Nelson Mandela",
            "Success is not final, failure is not fatal: it is the courage to continue that counts. - Winston Churchill",
            "The only limit to our realization of tomorrow will be our doubts of today. - Franklin D. Roosevelt"
        ]
        return f"💭 {random.choice(quotes)}"
    
    def handle_advanced_operations(self, command):
        """Handle advanced operations"""
        # Schedule tasks
        if "schedule" in command:
            return self.schedule_task(command)
        
        # Monitor system
        elif "monitor" in command:
            return self.monitor_system(command)
        
        # Backup
        elif "backup" in command:
            return self.create_backup(command)
        
        # System cleanup
        elif "cleanup" in command or "optimize" in command:
            return self.system_cleanup(command)
        
        # Security scan
        elif "scan" in command or "virus" in command:
            return self.security_scan(command)
        
        return None
    
    def schedule_task(self, command):
        """Schedule a task (simplified)"""
        return "📅 Task scheduling would require additional setup with task scheduler integration"
    
    def monitor_system(self, command):
        """Monitor system resources"""
        try:
            cpu = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            info = [
                "📊 SYSTEM MONITOR",
                "=" * 40,
                f"CPU Usage: {cpu}%",
                f"Memory: {memory.percent}% used ({self.format_size(memory.used)} of {self.format_size(memory.total)})",
                f"Disk: {disk.percent}% used ({self.format_size(disk.used)} of {self.format_size(disk.total)})",
                ""
            ]
            
            # Add warnings if thresholds exceeded
            if cpu > 80:
                info.append("⚠️  High CPU usage!")
            if memory.percent > 85:
                info.append("⚠️  High memory usage!")
            if disk.percent > 90:
                info.append("⚠️  Low disk space!")
            
            return "\n".join(info)
            
        except Exception as e:
            return f"❌ Monitoring failed: {str(e)}"
    
    def create_backup(self, command):
        """Create backup of files/folders"""
        try:
            # Extract source and destination
            source = "."
            dest = f"backup_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
            
            if "backup" in command:
                parts = command.split("backup")[1].strip()
                if "to" in parts:
                    source = parts.split("to")[0].strip()
                    dest = parts.split("to")[1].strip()
                else:
                    source = parts
            
            if not os.path.exists(source):
                return f"❌ Source '{source}' not found"
            
            import zipfile
            
            with zipfile.ZipFile(dest, 'w', zipfile.ZIP_DEFLATED) as zipf:
                if os.path.isfile(source):
                    zipf.write(source, os.path.basename(source))
                else:
                    for root, dirs, files in os.walk(source):
                        for file in files:
                            file_path = os.path.join(root, file)
                            arcname = os.path.relpath(file_path, os.path.dirname(source))
                            zipf.write(file_path, arcname)
            
            size = os.path.getsize(dest)
            return f"✅ Backup created: {dest}\n📏 Size: {self.format_size(size)}"
            
        except Exception as e:
            return f"❌ Backup failed: {str(e)}"
    
    def system_cleanup(self, command):
        """Clean up system temporary files"""
        try:
            temp_dirs = []
            if platform.system() == "Windows":
                temp_dirs = [
                    os.environ.get('TEMP', ''),
                    os.environ.get('TMP', ''),
                    os.path.join(os.environ.get('USERPROFILE', ''), 'AppData', 'Local', 'Temp')
                ]
            else:
                temp_dirs = ['/tmp', '/var/tmp']
            
            total_freed = 0
            removed_files = []
            
            for temp_dir in temp_dirs:
                if os.path.exists(temp_dir):
                    for root, dirs, files in os.walk(temp_dir):
                        for file in files:
                            if file.endswith(('.tmp', '.temp', '.log', '.bak')):
                                try:
                                    filepath = os.path.join(root, file)
                                    size = os.path.getsize(filepath)
                                    os.remove(filepath)
                                    total_freed += size
                                    removed_files.append(file)
                                except:
                                    pass
            
            if removed_files:
                return (f"✅ Cleaned {len(removed_files)} temporary files\n"
                       f"🗑️ Space freed: {self.format_size(total_freed)}")
            else:
                return "✅ No temporary files found to clean"
            
        except Exception as e:
            return f"❌ Cleanup failed: {str(e)}"
    
    # Utility methods
    def extract_filename(self, command):
        """Extract filename from command"""
        patterns = [
            r'named (.+?)(?: with| containing|$)',
            r'called (.+?)(?: with| containing|$)',
            r'file (.+?)(?: with| containing|$)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, command)
            if match:
                return match.group(1).strip()
        
        # Fallback: get last word
        words = command.split()
        if len(words) > 1:
            return words[-1]
        
        return None
    
    def find_similar_files(self, filename):
        """Find files with similar names"""
        similar = []
        current_dir = os.getcwd()
        
        for item in os.listdir(current_dir):
            if filename.lower() in item.lower() or item.lower() in filename.lower():
                similar.append(item)
        
        return similar
    
    def format_size(self, size_bytes):
        """Format size in human-readable format"""
        if size_bytes == 0:
            return "0 bytes"
        
        size_names = ("bytes", "KB", "MB", "GB", "TB")
        i = 0
        
        while size_bytes >= 1024 and i < len(size_names) - 1:
            size_bytes /= 1024.0
            i += 1
        
        if i == 0:
            return f"{size_bytes:.0f} {size_names[i]}"
        else:
            return f"{size_bytes:.2f} {size_names[i]}"
    
    def get_total_size(self, path):
        """Get total size of file or folder"""
        if os.path.isfile(path):
            return os.path.getsize(path)
        elif os.path.isdir(path):
            total = 0
            for dirpath, dirnames, filenames in os.walk(path):
                for f in filenames:
                    fp = os.path.join(dirpath, f)
                    if os.path.exists(fp):
                        total += os.path.getsize(fp)
            return total
        return 0
    
    def get_help_text(self):
        """Generate comprehensive help text"""
        help_text = """
        🎯 **VOICE ASSISTANT COMMANDS**
        ======================================
        
        📁 **FILE OPERATIONS:**
        • "create file [name] with content [text]" - Create file with content
        • "delete file [name]" - Delete a file
        • "rename file [old] to [new]" - Rename file
        • "copy file [source] to [destination]" - Copy file
        • "move file [source] to [destination]" - Move file
        • "search for file [name]" - Search files
        • "file info [name]" - Get file details
        • "list files [in folder]" - List files with details
        • "compress file [name] to [archive.zip]" - Compress file
        
        📂 **FOLDER OPERATIONS:**
        • "create folder [name] at [path]" - Create folder
        • "delete folder [name]" - Delete folder
        • "rename folder [old] to [new]" - Rename folder
        • "change directory to [path]" - Change folder
        • "current directory" - Show current location
        • "folder size [path]" - Calculate folder size
        • "clean folder [path]" - Clean temporary files
        • "compare folders [path1] and [path2]" - Compare folders
        
        🖥️ **SYSTEM OPERATIONS:**
        • "system info" - Detailed system information
        • "cpu info" - CPU details and usage
        • "memory info" - Memory usage details
        • "disk info" - Disk space information
        • "battery info" - Battery status
        • "list processes" - Running applications
        • "take screenshot" - Capture screen
        • "shutdown/restart/sleep" - System control
        • "lock screen" - Lock computer
        
        🔊 **MEDIA & AUDIO:**
        • "play/pause/stop" - Control media playback
        • "next/previous track" - Media navigation
        • "volume up/down" - Adjust volume
        • "mute/unmute" - Toggle mute
        
        🌐 **NETWORK OPERATIONS:**
        • "ip address" - Show network addresses
        • "network speed" - Test internet speed
        • "ping [host]" - Ping a server
        • "check port [port]" - Check if port is open
        
        🧮 **PRODUCTIVITY TOOLS:**
        • "calculate [expression]" - Advanced calculator
        • "timer for [time]" - Set timer
        • "remind me to [task]" - Set reminder
        • "note [text]" - Take note
        • "clipboard show/clear/save" - Manage clipboard
        
        🔧 **UTILITIES:**
        • "current time/date" - Time information
        • "convert [value] [unit] to [unit]" - Unit conversion
        • "random number/choice/password" - Random generators
        • "encode/decode [text]" - Text encoding
        
        🌐 **WEB & BROWSING:**
        • "search for [query]" - Web search
        • "open [website]" - Open specific site
        • "download [url]" - Download file
        
        💬 **CONVERSATION:**
        • "hello/hi" - Greetings
        • "how are you" - Check status
        • "tell me a joke/fact/quote" - Entertainment
        • "thank you" - Politeness
        
        ⚡ **ADVANCED FEATURES:**
        • "monitor system" - Resource monitoring
        • "create backup [folder]" - Backup files
        • "system cleanup" - Clean temporary files
        • "schedule task" - Task scheduling
        
        ❓ **HELP:**
        • "help" - Show this help
        • "what can you do" - List capabilities
        
        🚪 **EXIT:**
        • "exit/quit/goodbye" - Close assistant
        
        ======================================
        💡 **Tip:** Speak clearly and use natural language!
        """
        
        return help_text

# Global instance
assistant = VoiceAssistant()

def execute_command(command):
    """Main command execution function"""
    return assistant.execute_command(command)