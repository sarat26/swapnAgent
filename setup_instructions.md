# Monthly Pack Agent - Setup Instructions

## Quick Start (2 minutes)

### Step 1: Get Free API Keys

1. **TMDB (Movies/TV)** - FREE
   - Go to https://www.themoviedb.org/
   - Create account → Settings → API → Create API Key
   - Copy the API key

2. **Google Books** - FREE  
   - Go to https://console.developers.google.com/
   - Create project → Enable Books API → Create credentials
   - Copy the API key

### Step 2: Configure APIs

1. Open `api_keys.env`
2. Replace `your_tmdb_api_key_here` with your TMDB key
3. Replace `your_google_books_api_key_here` with your Google Books key

**Example:**
```
TMDB_API_KEY=a1b2c3d4e5f6g7h8...
GOOGLE_BOOKS_API_KEY=xyz789abc123...
```

### Step 3: Install Requirements

```bash
pip install requests
```

### Step 4: Run the Agent

```bash
python generate_pack.py
```

### Step 5: View Your Monthly Pack

Open `monthly_pack.html` in your browser!

## What Happens

1. Script fetches personalized recommendations from APIs
2. Generates beautiful HTML page with 6 categories:
   - 📺 Movies/TV (from TMDB)
   - 📚 Books (from Google Books)  
   - 🎧 Podcasts (from iTunes)
   - 🍷 Wine (curated list)
   - 🥾 Hiking (Bay Area trails)
   - 🌸 Perfume (curated list)

## Monthly Usage

Run the script once per month:
```bash
python generate_pack.py
```

## Files Created

- `monthly_pack.html` - Your beautiful monthly pack (open in browser)
- `recommendations.json` - Current pack data
- `history.json` - Prevents duplicate recommendations

## Troubleshooting

- **No recommendations showing**: Check API keys in `config.py`
- **Script fails**: Make sure `requests` is installed: `pip install requests`
- **HTML not displaying**: Open file directly in browser, don't double-click

## Optional: Email Notifications

To receive email notifications:
1. Set `EMAIL_ENABLED = True` in `config.py`
2. Add your Gmail credentials (use app password)
3. Recommendations will be emailed to you monthly