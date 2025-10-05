#!/usr/bin/env python3
"""
Monthly Pack Agent - Web Interface Launcher
Quick launcher for the interactive web interface
"""

import subprocess
import webbrowser
import time
import os

def start_web_interface():
    print("🚀 Starting Monthly Pack Web Interface...")
    
    # Check if we have recommendations
    if not os.path.exists('recommendations.json'):
        print("📝 No monthly pack found. Generating one first...")
        subprocess.run(['python', 'generate_pack.py'])
    
    print("🌐 Starting web server...")
    print("📂 Opening browser to: http://localhost:8080")
    print("💡 Click the refresh buttons to get new recommendations instantly!")
    print("\n⚡ Features:")
    print("   • 🔄 Refresh individual categories")
    print("   • 📋 Get 3 options for any category") 
    print("   • 🔄 Refresh all categories at once")
    print("   • 💫 No command line needed - just click!")
    print("\n🛑 Press Ctrl+C to stop the server")
    
    # Open browser after a short delay
    def open_browser():
        time.sleep(2)
        webbrowser.open('http://localhost:8080')
    
    import threading
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    # Start the server
    subprocess.run(['python', 'web_server.py'])

if __name__ == "__main__":
    start_web_interface()