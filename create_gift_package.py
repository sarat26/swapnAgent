#!/usr/bin/env python3
"""
Create a gift package for Swapna
Packages the Monthly Pack Agent for easy sharing
"""

import os
import shutil
import zipfile
from datetime import datetime

def create_package():
    """Create a clean package for Swapna"""
    
    # Create package directory
    package_name = "SwapnaMonthlyPackAgent"
    if os.path.exists(package_name):
        shutil.rmtree(package_name)
    os.makedirs(package_name)
    
    # Essential files to include
    essential_files = [
        'user_data.json',
        'user_data.md', 
        'api_keys.env',
        'api_services.py',
        'simple_web.py',
        'start_monthly_pack.py',
        'generate_pack.py',
        'email_service.py',
        'config.py',
        'requirements.txt',
        'SETUP_FOR_SWAPNA.md',
        'README_FOR_SWAPNA.md'
    ]
    
    # Copy essential files
    print("📦 Creating Swapna's Monthly Pack Agent package...")
    for file in essential_files:
        if os.path.exists(file):
            shutil.copy2(file, package_name)
            print(f"✅ Added {file}")
        else:
            print(f"⚠️  Missing {file}")
    
    # Create a simple README for the package
    with open(f"{package_name}/START_HERE.md", 'w') as f:
        f.write("""# 🎁 Happy Birthday Swapna!

## Your Personal Monthly Pack Agent

This is your birthday gift - a personalized AI recommendation system!

### 🚀 Quick Start:
1. **Read**: `SETUP_FOR_SWAPNA.md` for full instructions
2. **Setup**: Edit `api_keys.env` with your free API keys  
3. **Run**: Double-click `start_monthly_pack.py`
4. **Enjoy**: Click refresh buttons for unlimited new recommendations!

### 💝 What This Does:
Creates personalized monthly recommendations for:
- Movies & TV shows you'll love
- Books for spiritual growth  
- Mindfulness podcasts
- Full-bodied red wines
- Bay Area hiking trails
- Woody & floral perfumes

**Made with love just for you!** 🌟
""")
    
    # Create ZIP file
    zip_name = f"SwapnaMonthlyPackAgent_{datetime.now().strftime('%Y%m%d')}.zip"
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(package_name):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, os.path.dirname(package_name))
                zipf.write(file_path, arcname)
    
    print(f"\n🎉 Package created: {zip_name}")
    print(f"📂 Package folder: {package_name}/")
    print("\n📧 How to send to Swapna:")
    print(f"1. Email the ZIP file: {zip_name}")
    print("2. Or share the folder directly")
    print("3. Include the setup instructions from SETUP_FOR_SWAPNA.md")
    
    print("\n💡 What Swapna needs to do:")
    print("1. Extract the ZIP file")
    print("2. Get free API keys (5 minutes)")
    print("3. Run start_monthly_pack.py")
    print("4. Enjoy her personalized recommendations!")
    
    return zip_name, package_name

if __name__ == "__main__":
    create_package()