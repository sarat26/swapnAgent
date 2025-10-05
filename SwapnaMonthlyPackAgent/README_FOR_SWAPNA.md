# 🎁 Monthly Pack Agent - Happy Birthday Swapna!

## What This Is

Your very own **Monthly Pack Agent** - a personalized recommendation system that creates beautiful monthly packs just for you! Every month, it gives you 6 carefully selected recommendations:

- 📺 **Movies/TV Shows** - Drama, comedy, and character-driven stories you'll love
- 📚 **Books** - Memoirs, spiritual growth, and inspirational reads
- 🎧 **Podcasts** - Mindfulness, parenting, and wellness content
- 🍷 **Wine** - Full-bodied reds like Malbec and Cabernet Sauvignon
- 🥾 **Hiking Trails** - Bay Area trails that match your moderate difficulty preference
- 🌸 **Perfume** - Woody, floral scents in your preferred price ranges

## How to Use Your Monthly Pack Agent

### 🚀 Two Ways to Use Your Monthly Pack Agent:

## **Option 1: Interactive Web Interface (RECOMMENDED)**

**Super easy - just click buttons to refresh!**
```bash
python start_web.py
```

This opens a beautiful web page where you can:
- 🔄 **Click "Refresh"** on any category for instant new options
- 📋 **Click "3 Options"** to get multiple choices for any category
- 🔄 **Click "Refresh All"** to get completely new recommendations
- 💫 **No command line needed** - just click and enjoy!

## **Option 2: Command Line (Traditional)**

**For your regular monthly pack:**
```bash
python generate_pack.py
```

**Want different options? Get fresh alternatives:**
```bash
python generate_pack.py --more
```

**Want multiple choices per category:**
```bash
python generate_pack.py --more --count 3
```

Then open the HTML file in your browser to see your beautiful recommendations!

### 📅 Recommended Usage

**🌟 For the best experience:**
1. **Start the web interface**: `python start_web.py`
2. **Enjoy your monthly pack** with interactive buttons
3. **Click refresh buttons** whenever you want different options
4. **No more command line** - everything is just one click away!

**📱 Traditional command line method still works too** if you prefer it.

## What Makes It Special

✨ **Completely Personalized** - Based on your exact preferences from your user data
✨ **Interactive Web Interface** - Click buttons to refresh any category instantly  
✨ **Always Fresh** - Never repeats recommendations from previous months  
✨ **One-Click Refresh** - Get different options without any commands
✨ **Multiple Options** - Get 3 choices per category with one click
✨ **Beautiful Display** - Elegant cards with descriptions and links
✨ **Zero Cost** - Uses only free APIs, no subscriptions needed
✨ **Privacy First** - All data stays on your computer

## Monthly Pack Features

- **Smart Matching**: Algorithms that understand your taste in Jo Malone scents, Virgin River-style shows, and mindfulness podcasts
- **Bay Area Focus**: Hiking recommendations within driving distance of Cupertino
- **Budget Conscious**: Wine and perfume suggestions across your preferred price ranges
- **Cultural Sensitivity**: Content that respects your Marathi heritage and family values

## Files in Your System

- `generate_pack.py` - The main script you run
- `monthly_pack.html` - Your beautiful monthly pack (opens in browser)
- `user_data.json` - Your preferences (the heart of the system)
- `api_keys.env` - Your API keys (already configured)
- `history.json` - Prevents duplicate recommendations

## Optional: Email Notifications

Want monthly packs delivered to your inbox? 
1. Open `api_keys.env`
2. Set `EMAIL_ENABLED=True`
3. Add your Gmail details
4. Get monthly pack summaries emailed to you!

## Technical Details

Your agent uses:
- **TMDB API** for movies/TV (your key is configured)
- **Google Books API** for book recommendations (your key is configured)
- **iTunes API** for podcasts (free, no key needed)
- **Curated lists** for wine, perfume, and Bay Area hiking trails

## Need Help?

- **Question about recommendations?** The system learns from your user_data.json file
- **Want to update preferences?** Edit the user_data.json file
- **Technical issues?** Check that `requests` is installed: `pip install requests`

---

**💝 Made with love for your birthday! Enjoy discovering new favorites every month!**

*From your Monthly Pack Agent* 🤖✨