#!/usr/bin/env python3
"""
Monthly Pack Agent - Main Script
Generates personalized monthly recommendations for Swapna
"""

import json
import argparse
from datetime import datetime
from api_services import RecommendationService
from email_service import send_monthly_pack_email

def load_user_data():
    """Load user preferences from JSON file"""
    try:
        with open('user_data.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Error: user_data.json not found")
        return None

def load_history():
    """Load recommendation history to avoid duplicates"""
    try:
        with open('history.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"recommendations": []}

def save_history(history):
    """Save recommendation history"""
    with open('history.json', 'w') as f:
        json.dump(history, f, indent=2)

def check_duplicate(new_rec, history, category):
    """Check if recommendation was already given recently"""
    for past_pack in history.get('recommendations', []):
        if category in past_pack:
            past_item = past_pack[category]
            if isinstance(past_item, dict):
                # For complex objects, check title/name
                past_title = past_item.get('title') or past_item.get('name', '')
                new_title = new_rec.get('title') or new_rec.get('name', '')
                if past_title.lower() == new_title.lower():
                    return True
    return False

def generate_monthly_pack(refresh_mode=False, count_per_category=1):
    """Generate the monthly recommendation pack"""
    mode_text = "🔄 Refreshing recommendations" if refresh_mode else "🎯 Generating Monthly Pack"
    print(f"{mode_text} for Swapna...")
    
    # Load user data
    user_data = load_user_data()
    if not user_data:
        return None
    
    # Load history
    history = load_history()
    
    # Initialize recommendation service
    rec_service = RecommendationService()
    
    # Generate recommendations for each category
    recommendations = {}
    
    print("📺 Getting movie/TV recommendation...")
    movie_rec = rec_service.get_movie_recommendations(user_data.get('tvMovies', {}), count_per_category)
    recommendations['entertainment'] = movie_rec
    
    print("📚 Getting book recommendation...")
    book_rec = rec_service.get_book_recommendations(user_data.get('books', {}), count_per_category)
    recommendations['book'] = book_rec
    
    print("🎧 Getting podcast recommendation...")
    podcast_rec = rec_service.get_podcast_recommendations(user_data.get('podcasts', {}), count_per_category)
    recommendations['podcast'] = podcast_rec
    
    print("🍷 Getting wine recommendation...")
    wine_rec = rec_service.get_wine_recommendations(user_data.get('wine', {}), count_per_category)
    recommendations['wine'] = wine_rec
    
    print("🥾 Getting hiking recommendation...")
    hiking_rec = rec_service.get_hiking_recommendations(user_data.get('hiking', {}), count_per_category)
    recommendations['hiking'] = hiking_rec
    
    print("🌸 Getting perfume recommendation...")
    perfume_rec = rec_service.get_perfume_recommendations(user_data.get('perfume', {}), count_per_category)
    recommendations['perfume'] = perfume_rec
    
    # Create the monthly pack
    pack_type = "refresh" if refresh_mode else "monthly"
    monthly_pack = {
        'date_generated': datetime.now().isoformat(),
        'month_year': datetime.now().strftime('%B %Y'),
        'pack_type': pack_type,
        'recommendations': recommendations
    }
    
    # Save current pack
    filename = 'recommendations_refresh.json' if refresh_mode else 'recommendations.json'
    with open(filename, 'w') as f:
        json.dump(monthly_pack, f, indent=2)
    
    # Add to history (only for regular monthly packs, not refreshes)
    if not refresh_mode:
        history['recommendations'].insert(0, {
            'date': monthly_pack['date_generated'],
            'month': monthly_pack['month_year'],
            **recommendations
        })
        
        # Keep only last 12 months in history
        history['recommendations'] = history['recommendations'][:12]
        save_history(history)
    
    success_text = "✅ Alternative recommendations generated!" if refresh_mode else "✅ Monthly pack generated successfully!"
    print(success_text)
    return monthly_pack

def generate_html(refresh_mode=False):
    """Generate HTML file for viewing the monthly pack"""
    print("🌐 Generating HTML display...")
    
    # Load current recommendations
    filename = 'recommendations_refresh.json' if refresh_mode else 'recommendations.json'
    try:
        with open(filename, 'r') as f:
            pack = json.load(f)
    except FileNotFoundError:
        print(f"Error: No recommendations found. Run generation first.")
        return
    
    html_template = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Monthly Pack - {pack['month_year']}</title>
    <style>
        body {{
            font-family: 'Georgia', serif;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            margin: 0;
            padding: 20px;
            min-height: 100vh;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        .header {{
            text-align: center;
            margin-bottom: 40px;
            background: white;
            padding: 30px;
            border-radius: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }}
        .header h1 {{
            color: #2c3e50;
            margin: 0;
            font-size: 2.5em;
        }}
        .header p {{
            color: #7f8c8d;
            font-size: 1.2em;
            margin: 10px 0 0 0;
        }}
        .recommendations {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 25px;
        }}
        .card {{
            background: white;
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }}
        .card:hover {{
            transform: translateY(-5px);
        }}
        .card-header {{
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }}
        .card-header h3 {{
            margin: 0;
            font-size: 1.3em;
        }}
        .card-body {{
            padding: 20px;
        }}
        .card-body h4 {{
            margin: 0 0 10px 0;
            color: #2c3e50;
        }}
        .card-body p {{
            color: #7f8c8d;
            line-height: 1.6;
            margin: 10px 0;
        }}
        .tag {{
            display: inline-block;
            background: #ecf0f1;
            color: #2c3e50;
            padding: 5px 10px;
            border-radius: 15px;
            font-size: 0.9em;
            margin: 5px 5px 5px 0;
        }}
        .price {{
            color: #27ae60;
            font-weight: bold;
        }}
        .rating {{
            color: #f39c12;
            font-weight: bold;
        }}
        .footer {{
            text-align: center;
            margin-top: 40px;
            color: #7f8c8d;
        }}
        .refresh-button {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 25px;
            font-size: 1.1em;
            cursor: pointer;
            margin: 20px 10px;
            transition: transform 0.3s ease;
        }}
        .refresh-button:hover {{
            transform: translateY(-2px);
        }}
        .button-container {{
            text-align: center;
            margin: 30px 0;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎁 Monthly Pack</h1>
            <p>Personalized recommendations for {pack['month_year']}</p>
            <div class="button-container">
                <button class="refresh-button" onclick="refreshRecommendations()">🔄 Get More Options</button>
            </div>
        </div>
        
        <div class="recommendations">
"""
    
    recs = pack['recommendations']
    
    # Helper function to handle single or multiple recommendations
    def format_recommendations(items, category_type):
        if not isinstance(items, list):
            items = [items]
        
        content = ""
        for i, item in enumerate(items):
            border_color = "#667eea" if category_type == "entertainment" else "#764ba2"
            margin = "margin-bottom: 20px;" if i < len(items) - 1 else ""
            
            if category_type == "entertainment":
                content += f"""
                    <div style="{margin} padding: 15px; border-left: 3px solid {border_color};">
                        <h4>{item.get('title', 'N/A')}</h4>
                        <p><span class="rating">⭐ {item.get('rating', 'N/A')}</span> • {item.get('type', '').title()}</p>
                        <p>{item.get('description', '')}</p>
                    </div>"""
            elif category_type == "book":
                content += f"""
                    <div style="{margin} padding: 15px; border-left: 3px solid {border_color};">
                        <h4>{item.get('title', 'N/A')}</h4>
                        <p>by {item.get('author', 'Unknown')}</p>
                        <p><span class="rating">⭐ {item.get('rating', 'N/A')}</span></p>
                        <p>{item.get('description', '')}</p>
                    </div>"""
            elif category_type == "podcast":
                content += f"""
                    <div style="{margin} padding: 15px; border-left: 3px solid {border_color};">
                        <h4>{item.get('title', 'N/A')}</h4>
                        <p>by {item.get('creator', 'Unknown')}</p>
                        <p>{item.get('description', '')}</p>
                    </div>"""
            elif category_type == "wine":
                content += f"""
                    <div style="{margin} padding: 15px; border-left: 3px solid {border_color};">
                        <h4>{item.get('name', 'N/A')}</h4>
                        <p><span class="tag">{item.get('type', '')}</span> <span class="tag">{item.get('region', '')}</span></p>
                        <p><span class="price">{item.get('price_range', '')}</span></p>
                        <p>{item.get('description', '')}</p>
                        <p><strong>Where to buy:</strong> {item.get('where_to_buy', '')}</p>
                    </div>"""
            elif category_type == "hiking":
                features = item.get('features', [])
                feature_tags = ''.join([f'<span class="tag">{f}</span>' for f in features])
                content += f"""
                    <div style="{margin} padding: 15px; border-left: 3px solid {border_color};">
                        <h4>{item.get('name', 'N/A')}</h4>
                        <p>{item.get('location', '')}</p>
                        <p><strong>{item.get('distance', '')}</strong> • <strong>{item.get('elevation', '')}</strong> • {item.get('difficulty', '')}</p>
                        <p>{feature_tags}</p>
                        <p>{item.get('description', '')}</p>
                    </div>"""
            elif category_type == "perfume":
                scent_tags = ''.join([f'<span class="tag">{s}</span>' for s in item.get('scent_family', [])])
                content += f"""
                    <div style="{margin} padding: 15px; border-left: 3px solid {border_color};">
                        <h4>{item.get('name', 'N/A')}</h4>
                        <p>{item.get('brand', '')}</p>
                        <p>{scent_tags}</p>
                        <p><span class="price">{item.get('price_range', '')}</span></p>
                        <p>{item.get('description', '')}</p>
                        <p><strong>Where to buy:</strong> {item.get('where_to_buy', '')}</p>
                    </div>"""
        return content
    
    # Generate all category cards
    categories = [
        ("📺 Entertainment", "entertainment", recs.get('entertainment', {})),
        ("📚 Book", "book", recs.get('book', {})),
        ("🎧 Podcast", "podcast", recs.get('podcast', {})),
        ("🍷 Wine", "wine", recs.get('wine', {})),
        ("🥾 Hiking", "hiking", recs.get('hiking', {})),
        ("🌸 Perfume", "perfume", recs.get('perfume', {}))
    ]
    
    for title, category_type, items in categories:
        content = format_recommendations(items, category_type)
        html_template += f"""
            <div class="card">
                <div class="card-header">
                    <h3>{title}</h3>
                </div>
                <div class="card-body">
                    {content}
                </div>
            </div>
"""
    
    html_template += f"""
        </div>
        
        <div class="footer">
            <p>Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
            <p>💝 Made with love for Swapna</p>
            <div class="button-container">
                <button class="refresh-button" onclick="refreshRecommendations()">🔄 Get Different Options</button>
            </div>
        </div>
    </div>
    
    <script>
        function refreshRecommendations() {{
            alert('To get new recommendations, run:\\n\\npython generate_pack.py --more\\n\\nThen refresh this page!');
        }}
    </script>
</body>
</html>
"""
    
    # Save HTML file
    html_filename = 'monthly_pack_refresh.html' if refresh_mode else 'monthly_pack.html'
    with open(html_filename, 'w') as f:
        f.write(html_template)
    
    html_type = "refresh alternatives" if refresh_mode else "monthly pack"
    print(f"✅ HTML file generated: {html_filename}")
    print(f"🌐 Open the file in your browser to view your {html_type}!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Monthly Pack Agent - Personalized Recommendations')
    parser.add_argument('--more', '--refresh', action='store_true', 
                       help='Generate alternative recommendations instead of monthly pack')
    parser.add_argument('--count', type=int, default=1,
                       help='Number of recommendations per category (default: 1)')
    
    args = parser.parse_args()
    
    if args.more:
        print("🔄 Monthly Pack Agent - Refresh Mode...")
        print("Getting alternative recommendations...")
        
        # Generate alternative recommendations
        pack = generate_monthly_pack(refresh_mode=True, count_per_category=args.count)
        
        if pack:
            # Generate HTML display
            generate_html(refresh_mode=True)
            
            print("\\n🎉 Alternative recommendations ready!")
            print("📂 Open 'monthly_pack_refresh.html' in your browser to see new options.")
        else:
            print("❌ Failed to generate alternatives. Check your configuration.")
    else:
        print("🚀 Monthly Pack Agent Starting...")
        
        # Generate regular monthly recommendations
        pack = generate_monthly_pack(count_per_category=args.count)
        
        if pack:
            # Generate HTML display
            generate_html()
            
            # Send email notification (if enabled)
            send_monthly_pack_email()
            
            print("\\n🎉 All done! Your monthly pack is ready.")
            print("📂 Open 'monthly_pack.html' in your browser to see your recommendations.")
            print("\\n💡 Want different options? Run: python generate_pack.py --more")
        else:
            print("❌ Failed to generate monthly pack. Check your configuration.")