#!/usr/bin/env python3
"""
Monthly Pack Agent - Quick Setup
One-click setup for Swapna's birthday gift
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install requirements. Please install manually:")
        print("   pip install requests flask")
        return False

def check_api_keys():
    """Check if API keys are configured"""
    try:
        with open('api_keys.env', 'r') as f:
            content = f.read()
            if 'your_tmdb_api_key_here' in content or 'your_google_books_api_key_here' in content:
                print("⚠️  API keys not configured yet!")
                print("📝 Please edit api_keys.env and add your real API keys.")
                print("📋 Instructions: https://www.themoviedb.org/settings/api (for TMDB)")
                print("📋 Instructions: https://console.developers.google.com/ (for Google Books)")
                return False
            else:
                print("✅ API keys are configured!")
                return True
    except FileNotFoundError:
        print("❌ api_keys.env file not found!")
        return False

def generate_first_pack():
    """Generate the first monthly pack"""
    print("🎯 Generating your first monthly pack...")
    try:
        subprocess.check_call([sys.executable, "generate_pack.py"])
        print("✅ First monthly pack generated!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to generate monthly pack. Check your API keys.")
        return False

def main():
    print("🎁 Monthly Pack Agent - Quick Setup")
    print("🎂 Setting up Swapna's birthday gift...")
    print()
    
    success = True
    
    # Step 1: Install requirements
    if not install_requirements():
        success = False
    
    print()
    
    # Step 2: Check API keys
    if not check_api_keys():
        success = False
    
    print()
    
    # Step 3: Generate first pack (if API keys are ready)
    if success:
        if generate_first_pack():
            print()
            print("🎉 Setup complete! Your Monthly Pack Agent is ready!")
            print()
            print("🚀 To start using:")
            print("   python start_web.py")
            print()
            print("💡 This will open an interactive web page where Swapna can:")
            print("   • See her personalized monthly recommendations")
            print("   • Click buttons to refresh any category")
            print("   • Get multiple options with one click")
            print("   • Enjoy a beautiful, user-friendly interface")
            print()
            print("🎁 Perfect birthday gift - ready to go!")
        else:
            print()
            print("⚠️  Setup incomplete. Please fix API keys and try again.")
    else:
        print()
        print("⚠️  Setup incomplete. Please:")
        print("   1. Edit api_keys.env with real API keys")
        print("   2. Run this setup script again")
        print("   3. Then use: python start_web.py")

if __name__ == "__main__":
    main()