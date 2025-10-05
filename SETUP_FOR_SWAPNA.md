# 🎁 Monthly Pack Agent - Setup Guide for Swapna

## 🎂 Happy Birthday! Your Personal AI Recommendation System

This is your very own Monthly Pack Agent that creates personalized recommendations just for you!

## 🚀 Quick Start (5 minutes)

### Step 1: Install Python (if needed)
- **Mac**: Python should already be installed
- **Windows**: Download from https://python.org and install
- **Test**: Open Terminal/Command Prompt and type `python --version`

### Step 2: Setup API Keys (Required)
1. **Open the file called `api_keys.env`**
2. **Get your FREE API keys:**

**TMDB API (for movies/TV shows):**
- Go to: https://www.themoviedb.org/
- Create account → Settings → API → Request API Key → Developer
- Application Name: "Monthly Pack Agent"
- Application URL: "http://localhost:8080"
- Copy your API key

**Google Books API (for book recommendations):**
- Go to: https://console.developers.google.com/
- Create project → Enable "Books API" → Create Credentials → API Key
- Copy your API key

3. **Edit `api_keys.env` and replace:**
```
TMDB_API_KEY=your_actual_tmdb_key_here
GOOGLE_BOOKS_API_KEY=your_actual_google_books_key_here
```

### Step 3: Start Your Monthly Pack Agent
**Double-click** `start_monthly_pack.py` 

OR

**Open Terminal/Command Prompt in this folder and type:**
```bash
python start_monthly_pack.py
```

### Step 4: Enjoy! 
Your browser will open automatically with your personalized recommendations!

## 🎯 How to Use

### **Interactive Web Interface**
Once it starts, you'll see a beautiful webpage with:

- 📺 **Entertainment** - Shows and movies you'll love
- 📚 **Books** - Memoirs and spiritual growth books  
- 🎧 **Podcasts** - Mindfulness and parenting content
- 🍷 **Wine** - Full-bodied reds you enjoy
- 🥾 **Hiking** - Bay Area trails perfect for you
- 🌸 **Perfume** - Woody and floral scents

### **Magic Buttons on Each Card:**
- 🔄 **"Refresh"** → Get a completely different recommendation
- 📋 **"3 Options"** → See 3 choices to pick from

**Click as many times as you want!** Every click gives you fresh, personalized options.

## 💡 Tips & Tricks

- **Monthly Routine**: Start it once a month for fresh recommendations
- **Refresh Anytime**: If you've already seen something, just click refresh!
- **Multiple Options**: Use "3 Options" when you want variety
- **Bookmark It**: Keep the page open and refresh categories as needed
- **No Internet Breaks**: The system works even if some APIs are slow

## 🆘 Need Help?

**If something doesn't work:**

1. **API Key Error**: Make sure you added real API keys to `api_keys.env`
2. **Python Error**: Try running: `pip install flask requests`
3. **Can't Open**: Try going directly to: http://localhost:8080
4. **Still Stuck**: The original command line version still works with `python generate_pack.py`

## 🎉 What Makes This Special

✨ **100% Personalized** - Every recommendation is chosen specifically for your tastes
✨ **Always Fresh** - Unlimited new options with the click of a button  
✨ **Zero Cost** - Uses only free APIs, no subscriptions ever
✨ **Private** - All your data stays on your computer
✨ **Beautiful** - Elegant interface designed just for you

## 📱 Alternative Usage

**If you prefer command line:**
- `python generate_pack.py` → Regular monthly pack
- `python generate_pack.py --more` → Alternative options
- Open the generated HTML files in your browser

---

**💝 Made with love for your birthday! Enjoy discovering new favorites every month!**

*Your Monthly Pack Agent* 🤖✨