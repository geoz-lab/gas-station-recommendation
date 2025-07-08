#!/usr/bin/env python3
"""
One-Click Launcher for Gas Station Recommendation App
This script can be run from anywhere to start the app
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
    """Find the gas_recommendation_app directory"""
    # Try multiple possible locations
    possible_paths = [
        Path(__file__).parent / "gas_recommendation_app",  # Same directory as this script
        Path(__file__).parent.parent / "gas_recommendation_app",  # Parent directory
        Path.cwd() / "gas_recommendation_app",  # Current working directory
        Path.home() / "gas_station_recommendation" / "gas_recommendation_app",  # Home directory
    ]
    
    for path in possible_paths:
        if path.exists():
            return path
    
    # If not found, ask user to locate it
    print("❌ Could not find gas_recommendation_app directory automatically.")
    print("Please enter the path to your gas_recommendation_app directory:")
    user_path = input("Path: ").strip()
    
    if user_path:
        path = Path(user_path)
        if path.exists():
            return path
    
    raise FileNotFoundError("Could not find gas_recommendation_app directory")

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = ['flask', 'requests', 'anthropic', 'geopy']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"📦 Installing missing packages: {', '.join(missing_packages)}")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing_packages)
            print("✅ Packages installed successfully!")
        except subprocess.CalledProcessError:
            print("❌ Failed to install packages. Please install manually:")
            print(f"pip install {' '.join(missing_packages)}")
            return False
    
    return True

def setup_environment(app_dir):
    """Setup the Python environment"""
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
    time.sleep(3)  # Wait for server to start
    try:
        webbrowser.open('http://localhost:8080')
        print("🌐 Opened browser to http://localhost:8080")
    except Exception as e:
        print(f"⚠️  Could not open browser automatically: {e}")
        print("Please manually open: http://localhost:8080")

def signal_handler(signum, frame):
    """Handle shutdown signals"""
    print("\n👋 Shutting down Gas Station Recommendation App...")
    sys.exit(0)

def main():
    """Main launcher function"""
    print("=" * 60)
    print("🚗 Gas Station Recommendation App - One-Click Launcher")
    print("=" * 60)
    
    try:
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        # Find app directory
        print("🔍 Looking for app directory...")
        app_dir = find_app_directory()
        print(f"✅ Found app at: {app_dir}")
        
        # Check dependencies
        print("🔧 Checking dependencies...")
        if not check_dependencies():
            input("Press Enter to exit...")
            return
        
        # Setup environment
        print("⚙️  Setting up environment...")
        setup_environment(app_dir)
        
        # Start browser in a separate thread
        print("🌐 Preparing to open browser...")
        browser_thread = threading.Thread(target=open_browser, daemon=True)
        browser_thread.start()
        
        # Start the web server
        print("🚀 Starting web server...")
        start_web_server()
        
    except KeyboardInterrupt:
        print("\n👋 Shutting down Gas Station Recommendation App...")
    except Exception as e:
        print(f"❌ Error: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main() 