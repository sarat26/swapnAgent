#!/usr/bin/env python3
"""
Monthly Pack Agent - Simple Launcher
Easy way to start the interactive monthly pack
"""

import subprocess
import webbrowser
import time
import os
import sys

def check_requirements():
    """Check if all required files exist"""
    required_files = [
        'user_data.json',
        'api_keys.env', 
        'api_services.py',
        'simple_web.py'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("❌ Missing required files:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    
    return True

def check_api_keys():
    """Check if API keys are configured"""
    try:
        with open('api_keys.env', 'r') as f:
            content = f.read()
            if 'your_tmdb_api_key_here' in content or 'your_google_books_api_key_here' in content:
                print("⚠️  API keys not configured!")
                print("📝 Please edit api_keys.env with your real API keys first.")
                return False
            return True
    except:
        print("❌ Could not read api_keys.env")
        return False

def install_requirements():
    """Install Flask if needed"""
    try:
        import flask
        return True
    except ImportError:
        print("📦 Installing Flask...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "flask"])
            print("✅ Flask installed successfully!")
            return True
        except:
            print("❌ Failed to install Flask. Please run: pip install flask")
            return False

def start_server():
    """Start the web server"""
    print("🌐 Starting Monthly Pack Web Interface...")
    print("📂 Opening browser to: http://localhost:8080")
    print("💡 Click the refresh buttons to get new recommendations!")
    print("\n🛑 Press Ctrl+C to stop")
    
    # Open browser after a short delay
    def open_browser():
        time.sleep(3)
        try:
            webbrowser.open('http://localhost:8080')
        except:
            print("💡 Manually open: http://localhost:8080")
    
    import threading
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    # Start the server
    try:
        subprocess.run([sys.executable, 'simple_web.py'])
    except KeyboardInterrupt:
        print("\n👋 Monthly Pack Agent stopped. Thanks for using it!")

def main():
    print("🎁 Monthly Pack Agent - Starting...")
    print()
    
    # Check requirements
    if not check_requirements():
        print("\n❌ Setup incomplete. Please ensure all files are present.")
        return
    
    # Check API keys
    if not check_api_keys():
        print("\n📋 Setup instructions:")
        print("1. Edit api_keys.env file")
        print("2. Replace placeholder API keys with real ones")
        print("3. Run this script again")
        return
    
    # Install requirements
    if not install_requirements():
        return
    
    print("✅ Everything ready!")
    print()
    
    # Start the server
    start_server()

if __name__ == "__main__":
    main()