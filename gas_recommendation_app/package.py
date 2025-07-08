#!/usr/bin/env python3
"""
Package script for Gas Station Recommendation App
Creates a standalone executable that launches the web app
"""

import os
import sys
import shutil
import subprocess
import webbrowser
import threading
import time
from pathlib import Path

class AppPackager:
    def __init__(self):
        self.app_name = "Gas Station Recommendation"
        self.version = "1.0.0"
        self.dist_dir = "dist"
        self.build_dir = "build"
        
    def create_launcher_script(self):
        """Create a launcher script that starts the web app"""
        launcher_content = '''#!/usr/bin/env python3
"""
Gas Station Recommendation App Launcher
Automatically starts the web server and opens the browser
"""

import os
import sys
import subprocess
import webbrowser
import threading
import time
import signal
from pathlib import Path

def find_app_directory():
    """Find the app directory relative to this script"""
    script_dir = Path(__file__).parent
    app_dir = script_dir / "gas_recommendation_app"
    if app_dir.exists():
        return app_dir
    
    # Try parent directory
    app_dir = script_dir.parent / "gas_recommendation_app"
    if app_dir.exists():
        return app_dir
    
    # Try current directory
    app_dir = Path.cwd() / "gas_recommendation_app"
    if app_dir.exists():
        return app_dir
    
    raise FileNotFoundError("Could not find gas_recommendation_app directory")

def setup_environment():
    """Setup the Python environment"""
    app_dir = find_app_directory()
    os.chdir(app_dir)
    
    # Add current directory to Python path
    sys.path.insert(0, str(app_dir))
    sys.path.insert(0, str(app_dir / "services"))
    sys.path.insert(0, str(app_dir / "models"))
    sys.path.insert(0, str(app_dir / "utils"))
    
    return app_dir

def start_web_server():
    """Start the Flask web server"""
    try:
        from web_app import app
        print("🚀 Starting Gas Station Recommendation Web App...")
        print("📍 Access the app at: http://localhost:8080")
        print("🔧 API endpoints available at: http://localhost:8080/api/")
        print("Press Ctrl+C to quit")
        
        # Run the Flask app
        app.run(host='0.0.0.0', port=8080, debug=False, use_reloader=False)
        
    except ImportError as e:
        print(f"❌ Error importing web app: {e}")
        print("Make sure all dependencies are installed:")
        print("pip install flask requests anthropic geopy")
        return False
    except Exception as e:
        print(f"❌ Error starting web server: {e}")
        return False

def open_browser():
    """Open the web browser after a short delay"""
    time.sleep(2)  # Wait for server to start
    try:
        webbrowser.open('http://localhost:8080')
        print("🌐 Opened browser to http://localhost:8080")
    except Exception as e:
        print(f"⚠️  Could not open browser automatically: {e}")
        print("Please manually open: http://localhost:8080")

def main():
    """Main launcher function"""
    print("=" * 60)
    print("🚗 Gas Station Recommendation App")
    print("=" * 60)
    
    try:
        # Setup environment
        app_dir = setup_environment()
        print(f"📁 Using app directory: {app_dir}")
        
        # Start browser in a separate thread
        browser_thread = threading.Thread(target=open_browser, daemon=True)
        browser_thread.start()
        
        # Start the web server
        start_web_server()
        
    except KeyboardInterrupt:
        print("\\n👋 Shutting down Gas Station Recommendation App...")
    except Exception as e:
        print(f"❌ Error: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
'''
        
        # Write launcher script
        launcher_path = Path(self.dist_dir) / "launch_gas_app.py"
        launcher_path.parent.mkdir(exist_ok=True)
        
        with open(launcher_path, 'w') as f:
            f.write(launcher_content)
        
        # Make executable on Unix systems
        if os.name != 'nt':  # Not Windows
            os.chmod(launcher_path, 0o755)
        
        return launcher_path
    
    def create_batch_file(self):
        """Create a Windows batch file launcher"""
        batch_content = f'''@echo off
title {self.app_name}
echo ============================================================
echo 🚗 {self.app_name}
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

REM Check if required packages are installed
python -c "import flask, requests, anthropic, geopy" >nul 2>&1
if errorlevel 1 (
    echo 📦 Installing required packages...
    pip install flask requests anthropic geopy
    if errorlevel 1 (
        echo ❌ Failed to install packages
        pause
        exit /b 1
    )
)

echo 🚀 Starting {self.app_name}...
echo 📍 The app will open in your browser at http://localhost:8080
echo.

REM Start the launcher script
python launch_gas_app.py

pause
'''
        
        batch_path = Path(self.dist_dir) / "launch_gas_app.bat"
        with open(batch_path, 'w') as f:
            f.write(batch_content)
        
        return batch_path
    
    def create_shell_script(self):
        """Create a Unix shell script launcher"""
        shell_content = f'''#!/bin/bash

echo "============================================================"
echo "🚗 {self.app_name}"
echo "============================================================"
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    echo "Please install Python 3 from https://python.org"
    exit 1
fi

# Check if required packages are installed
python3 -c "import flask, requests, anthropic, geopy" 2>/dev/null
if [ $? -ne 0 ]; then
    echo "📦 Installing required packages..."
    pip3 install flask requests anthropic geopy
    if [ $? -ne 0 ]; then
        echo "❌ Failed to install packages"
        exit 1
    fi
fi

echo "🚀 Starting {self.app_name}..."
echo "📍 The app will open in your browser at http://localhost:8080"
echo

# Start the launcher script
python3 launch_gas_app.py
'''
        
        shell_path = Path(self.dist_dir) / "launch_gas_app.sh"
        with open(shell_path, 'w') as f:
            f.write(shell_content)
        
        # Make executable
        os.chmod(shell_path, 0o755)
        
        return shell_path
    
    def copy_app_files(self):
        """Copy the app files to the distribution directory"""
        app_dir = Path("gas_recommendation_app")
        dist_app_dir = Path(self.dist_dir) / "gas_recommendation_app"
        
        if not app_dir.exists():
            print(f"❌ App directory not found: {app_dir}")
            return False
        
        # Create dist directory
        dist_app_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy all app files
        print(f"📁 Copying app files to {dist_app_dir}...")
        
        # Files to copy
        files_to_copy = [
            "web_app.py",
            "config.py",
            "main.py",
            "requirements.txt",
            "README.md"
        ]
        
        # Directories to copy
        dirs_to_copy = [
            "services",
            "models", 
            "utils",
            "static",
            "templates"
        ]
        
        # Copy files
        for file_name in files_to_copy:
            src = app_dir / file_name
            dst = dist_app_dir / file_name
            if src.exists():
                shutil.copy2(src, dst)
                print(f"  ✅ Copied {file_name}")
        
        # Copy directories
        for dir_name in dirs_to_copy:
            src = app_dir / dir_name
            dst = dist_app_dir / dir_name
            if src.exists():
                shutil.copytree(src, dst, dirs_exist_ok=True)
                print(f"  ✅ Copied {dir_name}/")
        
        return True
    
    def create_readme(self):
        """Create a README for the packaged app"""
        readme_content = f'''# {self.app_name} - Standalone Package

## 🚀 Quick Start

### Windows Users:
1. Double-click `launch_gas_app.bat`
2. The app will automatically open in your browser
3. If packages are missing, they will be installed automatically

### Mac/Linux Users:
1. Open terminal in this directory
2. Run: `./launch_gas_app.sh`
3. Or run: `python3 launch_gas_app.py`
4. The app will automatically open in your browser

## 📋 Requirements

- Python 3.7 or higher
- Internet connection (for Google Maps API and Claude AI)
- Web browser

## 🔧 Configuration

Before using the app, you need to set up your API keys:

1. **Google Maps API Key** (for gas station locations):
   - Get a key from: https://console.cloud.google.com/
   - Set it in the app when prompted

2. **Claude API Key** (for AI recommendations):
   - Get a key from: https://console.anthropic.com/
   - Set it in the app when prompted

## 🌐 Access the App

Once launched, the app will be available at:
- **Local**: http://localhost:8080
- **Network**: http://[your-ip]:8080

## 🛠️ Troubleshooting

### Port Already in Use
If port 8080 is busy, the app will show an error. You can:
1. Close other applications using port 8080
2. Or modify the port in `gas_recommendation_app/web_app.py`

### Missing Dependencies
If you see import errors:
1. Run: `pip install flask requests anthropic geopy`
2. Or use the launcher scripts which handle this automatically

### API Key Issues
If the app doesn't work properly:
1. Check that your API keys are valid
2. Ensure you have sufficient API credits
3. Check your internet connection

## 📁 Files

- `launch_gas_app.py` - Main launcher script
- `launch_gas_app.bat` - Windows launcher
- `launch_gas_app.sh` - Unix launcher
- `gas_recommendation_app/` - App source code
- `README.md` - This file

## 🎯 Features

- 🚗 Find nearby gas stations
- 💰 Compare prices across different fuel grades (87, 89, 91)
- 🤖 AI-powered recommendations
- 📍 Use current location or enter address
- ⏱️ Real-time travel time calculations
- 💡 Cost analysis including travel expenses

## 📞 Support

If you encounter issues:
1. Check the console output for error messages
2. Ensure all requirements are met
3. Verify your API keys are working

---
Version: {self.version}
'''
        
        readme_path = Path(self.dist_dir) / "README.md"
        with open(readme_path, 'w') as f:
            f.write(readme_content)
        
        return readme_path
    
    def create_requirements_file(self):
        """Create a requirements file for the packaged app"""
        requirements_content = '''flask>=2.0.0
requests>=2.25.0
anthropic>=0.7.0
geopy>=2.0.0
python-dotenv>=0.19.0
'''
        
        req_path = Path(self.dist_dir) / "requirements.txt"
        with open(req_path, 'w') as f:
            f.write(requirements_content)
        
        return req_path
    
    def package(self):
        """Create the complete package"""
        print("🚀 Creating Gas Station Recommendation App Package...")
        print("=" * 60)
        
        # Create distribution directory
        dist_path = Path(self.dist_dir)
        dist_path.mkdir(exist_ok=True)
        
        # Copy app files
        if not self.copy_app_files():
            return False
        
        # Create launchers
        print("\n📝 Creating launcher scripts...")
        launcher_path = self.create_launcher_script()
        print(f"  ✅ Created {launcher_path}")
        
        batch_path = self.create_batch_file()
        print(f"  ✅ Created {batch_path}")
        
        shell_path = self.create_shell_script()
        print(f"  ✅ Created {shell_path}")
        
        # Create documentation
        print("\n📚 Creating documentation...")
        readme_path = self.create_readme()
        print(f"  ✅ Created {readme_path}")
        
        req_path = self.create_requirements_file()
        print(f"  ✅ Created {req_path}")
        
        # Create zip file
        print("\n📦 Creating distribution package...")
        zip_name = f"gas_station_recommendation_v{self.version}.zip"
        shutil.make_archive(
            f"gas_station_recommendation_v{self.version}",
            'zip',
            self.dist_dir
        )
        
        print(f"  ✅ Created {zip_name}")
        
        print("\n🎉 Package created successfully!")
        print(f"📁 Package location: {Path.cwd() / zip_name}")
        print(f"📁 Unpackaged files: {Path.cwd() / self.dist_dir}")
        print("\n🚀 To use the app:")
        print("1. Extract the zip file")
        print("2. Run the appropriate launcher for your OS")
        print("3. The app will open in your browser")
        
        return True

def main():
    """Main function"""
    packager = AppPackager()
    success = packager.package()
    
    if success:
        print("\n✅ Packaging completed successfully!")
    else:
        print("\n❌ Packaging failed!")
        sys.exit(1)

if __name__ == "__main__":
    main() 