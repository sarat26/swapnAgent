#!/usr/bin/env python3
"""
Monthly Pack Agent - Simple Web Server
Simplified version with better error handling
"""

import json
import os
from datetime import datetime
from flask import Flask, jsonify
from api_services import RecommendationService

app = Flask(__name__)

def load_user_data():
    """Load user preferences from JSON file"""
    try:
        with open('user_data.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("❌ user_data.json not found")
        return None
    except json.JSONDecodeError:
        print("❌ Invalid JSON in user_data.json")
        return None

@app.route('/')
def index():
    """Serve the main monthly pack page"""
    try:
        # Load existing pack or create new one
        if os.path.exists('recommendations.json'):
            with open('recommendations.json', 'r') as f:
                pack = json.load(f)
        else:
            print("📝 No monthly pack found. Creating one...")
            pack = generate_new_pack()
            if not pack:
                return "❌ Failed to generate monthly pack. Check your API keys in api_keys.env"
        
        return create_html_page(pack)
    except Exception as e:
        return f"❌ Error loading page: {str(e)}"

def generate_new_pack():
    """Generate a new monthly pack"""
    try:
        user_data = load_user_data()
        if not user_data:
            return None
        
        rec_service = RecommendationService()
        
        recommendations = {
            'entertainment': rec_service.get_movie_recommendations(user_data.get('tvMovies', {}), 1),
            'book': rec_service.get_book_recommendations(user_data.get('books', {}), 1),
            'podcast': rec_service.get_podcast_recommendations(user_data.get('podcasts', {}), 1),
            'wine': rec_service.get_wine_recommendations(user_data.get('wine', {}), 1),
            'hiking': rec_service.get_hiking_recommendations(user_data.get('hiking', {}), 1),
            'perfume': rec_service.get_perfume_recommendations(user_data.get('perfume', {}), 1)
        }
        
        pack = {
            'date_generated': datetime.now().isoformat(),
            'month_year': datetime.now().strftime('%B %Y'),
            'recommendations': recommendations
        }
        
        # Save the pack
        with open('recommendations.json', 'w') as f:
            json.dump(pack, f, indent=2)
        
        return pack
    except Exception as e:
        print(f"❌ Error generating pack: {e}")
        return None

@app.route('/api/refresh/<category>')
def refresh_category(category):
    """API endpoint to refresh a specific category"""
    try:
        user_data = load_user_data()
        if not user_data:
            return jsonify({'success': False, 'error': 'Failed to load user data'})
        
        rec_service = RecommendationService()
        
        # Get fresh recommendation for the category
        if category == 'entertainment':
            recommendation = rec_service.get_movie_recommendations(user_data.get('tvMovies', {}), 1)
        elif category == 'book':
            recommendation = rec_service.get_book_recommendations(user_data.get('books', {}), 1)
        elif category == 'podcast':
            recommendation = rec_service.get_podcast_recommendations(user_data.get('podcasts', {}), 1)
        elif category == 'wine':
            recommendation = rec_service.get_wine_recommendations(user_data.get('wine', {}), 1)
        elif category == 'hiking':
            recommendation = rec_service.get_hiking_recommendations(user_data.get('hiking', {}), 1)
        elif category == 'perfume':
            recommendation = rec_service.get_perfume_recommendations(user_data.get('perfume', {}), 1)
        else:
            return jsonify({'success': False, 'error': 'Invalid category'})
        
        return jsonify({'success': True, 'recommendation': recommendation})
        
    except Exception as e:
        print(f"❌ Error refreshing {category}: {e}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/more/<category>')
def more_category(category):
    """API endpoint to get multiple options for a specific category"""
    try:
        user_data = load_user_data()
        if not user_data:
            return jsonify({'success': False, 'error': 'Failed to load user data'})
        
        rec_service = RecommendationService()
        
        # Get 3 recommendations for the category
        if category == 'entertainment':
            recommendations = rec_service.get_movie_recommendations(user_data.get('tvMovies', {}), 3)
        elif category == 'book':
            recommendations = rec_service.get_book_recommendations(user_data.get('books', {}), 3)
        elif category == 'podcast':
            recommendations = rec_service.get_podcast_recommendations(user_data.get('podcasts', {}), 3)
        elif category == 'wine':
            recommendations = rec_service.get_wine_recommendations(user_data.get('wine', {}), 3)
        elif category == 'hiking':
            recommendations = rec_service.get_hiking_recommendations(user_data.get('hiking', {}), 3)
        elif category == 'perfume':
            recommendations = rec_service.get_perfume_recommendations(user_data.get('perfume', {}), 3)
        else:
            return jsonify({'success': False, 'error': 'Invalid category'})
        
        return jsonify({'success': True, 'recommendations': recommendations})
        
    except Exception as e:
        print(f"❌ Error getting more {category}: {e}")
        return jsonify({'success': False, 'error': str(e)})

def create_html_page(pack):
    """Create the HTML page with interactive buttons"""
    return f"""
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
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .card-header h3 {{
            margin: 0;
            font-size: 1.3em;
        }}
        .card-buttons {{
            display: flex;
            gap: 8px;
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
        .refresh-btn, .more-btn {{
            background: rgba(255,255,255,0.2);
            color: white;
            border: 1px solid rgba(255,255,255,0.3);
            padding: 6px 10px;
            border-radius: 15px;
            font-size: 0.8em;
            cursor: pointer;
            transition: all 0.3s ease;
        }}
        .refresh-btn:hover, .more-btn:hover {{
            background: rgba(255,255,255,0.3);
        }}
        .refresh-btn:disabled, .more-btn:disabled {{
            opacity: 0.6;
            cursor: not-allowed;
        }}
        .footer {{
            text-align: center;
            margin-top: 40px;
            color: #7f8c8d;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎁 Monthly Pack</h1>
            <p>Personalized recommendations for {pack['month_year']}</p>
            <p style="font-size: 1em; color: #27ae60;">✨ Click the buttons on each card to get new options!</p>
        </div>
        
        <div class="recommendations">
            {generate_cards_html(pack['recommendations'])}
        </div>
        
        <div class="footer">
            <p>Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
            <p>💝 Made with love for Swapna</p>
        </div>
    </div>
    
    <script>
        function updateCard(category, content) {{
            const cardBody = document.querySelector(`[data-category="${{category}}"] .card-body`);
            if (cardBody) {{
                cardBody.innerHTML = content;
            }}
        }}
        
        function formatContent(item, category) {{
            let content = '<div style="padding: 15px; border-left: 3px solid #764ba2;">';
            
            if (category === 'entertainment') {{
                content += `
                    <h4>${{item.title || 'N/A'}}</h4>
                    <p><span class="rating">⭐ ${{item.rating || 'N/A'}}</span> • ${{(item.type || '').charAt(0).toUpperCase() + (item.type || '').slice(1)}}</p>
                    <p>${{item.description || ''}}</p>
                `;
            }} else if (category === 'book') {{
                content += `
                    <h4>${{item.title || 'N/A'}}</h4>
                    <p>by ${{item.author || 'Unknown'}}</p>
                    <p><span class="rating">⭐ ${{item.rating || 'N/A'}}</span></p>
                    <p>${{item.description || ''}}</p>
                `;
            }} else if (category === 'podcast') {{
                content += `
                    <h4>${{item.title || 'N/A'}}</h4>
                    <p>by ${{item.creator || 'Unknown'}}</p>
                    <p>${{item.description || ''}}</p>
                `;
            }} else if (category === 'wine') {{
                content += `
                    <h4>${{item.name || 'N/A'}}</h4>
                    <p><span class="tag">${{item.type || ''}}</span> <span class="tag">${{item.region || ''}}</span></p>
                    <p><span class="price">${{item.price_range || ''}}</span></p>
                    <p>${{item.description || ''}}</p>
                    <p><strong>Where to buy:</strong> ${{item.where_to_buy || ''}}</p>
                `;
            }} else if (category === 'hiking') {{
                let features = item.features || [];
                let featureTags = features.map(f => `<span class="tag">${{f}}</span>`).join('');
                content += `
                    <h4>${{item.name || 'N/A'}}</h4>
                    <p>${{item.location || ''}}</p>
                    <p><strong>${{item.distance || ''}}</strong> • <strong>${{item.elevation || ''}}</strong> • ${{item.difficulty || ''}}</p>
                    <p>${{featureTags}}</p>
                    <p>${{item.description || ''}}</p>
                `;
            }} else if (category === 'perfume') {{
                let scentTags = (item.scent_family || []).map(s => `<span class="tag">${{s}}</span>`).join('');
                content += `
                    <h4>${{item.name || 'N/A'}}</h4>
                    <p>${{item.brand || ''}}</p>
                    <p>${{scentTags}}</p>
                    <p><span class="price">${{item.price_range || ''}}</span></p>
                    <p>${{item.description || ''}}</p>
                    <p><strong>Where to buy:</strong> ${{item.where_to_buy || ''}}</p>
                `;
            }}
            
            content += '</div>';
            return content;
        }}
        
        function refreshCategory(category) {{
            const button = document.querySelector(`[data-category="${{category}}"] .refresh-btn`);
            const originalText = button.textContent;
            button.textContent = '🔄 Loading...';
            button.disabled = true;
            
            fetch(`/api/refresh/${{category}}`)
                .then(response => response.json())
                .then(data => {{
                    if (data.success) {{
                        updateCard(category, formatContent(data.recommendation, category));
                    }} else {{
                        alert('Failed to get new recommendation: ' + (data.error || 'Unknown error'));
                    }}
                }})
                .catch(error => {{
                    console.error('Error:', error);
                    alert('Error getting recommendation. Please try again.');
                }})
                .finally(() => {{
                    button.textContent = originalText;
                    button.disabled = false;
                }});
        }}
        
        function getMoreOptions(category) {{
            const button = document.querySelector(`[data-category="${{category}}"] .more-btn`);
            const originalText = button.textContent;
            button.textContent = '⏳ Loading...';
            button.disabled = true;
            
            fetch(`/api/more/${{category}}`)
                .then(response => response.json())
                .then(data => {{
                    if (data.success) {{
                        let content = '';
                        if (Array.isArray(data.recommendations)) {{
                            data.recommendations.forEach((item, index) => {{
                                if (index > 0) content += '<hr style="margin: 15px 0; border: 1px solid #ecf0f1;">';
                                content += formatContent(item, category);
                            }});
                        }} else {{
                            content = formatContent(data.recommendations, category);
                        }}
                        updateCard(category, content);
                    }} else {{
                        alert('Failed to get more options: ' + (data.error || 'Unknown error'));
                    }}
                }})
                .catch(error => {{
                    console.error('Error:', error);
                    alert('Error getting options. Please try again.');
                }})
                .finally(() => {{
                    button.textContent = originalText;
                    button.disabled = false;
                }});
        }}
    </script>
</body>
</html>
"""

def generate_cards_html(recommendations):
    """Generate HTML for all recommendation cards"""
    cards_html = ""
    categories = [
        ("📺 Entertainment", "entertainment", recommendations.get('entertainment', {})),
        ("📚 Book", "book", recommendations.get('book', {})),
        ("🎧 Podcast", "podcast", recommendations.get('podcast', {})),
        ("🍷 Wine", "wine", recommendations.get('wine', {})),
        ("🥾 Hiking", "hiking", recommendations.get('hiking', {})),
        ("🌸 Perfume", "perfume", recommendations.get('perfume', {}))
    ]
    
    for title, category_type, item in categories:
        # Format content for this category
        content = ""
        
        if category_type == "entertainment":
            content = f"""
                <div style="padding: 15px; border-left: 3px solid #667eea;">
                    <h4>{item.get('title', 'N/A')}</h4>
                    <p><span class="rating">⭐ {item.get('rating', 'N/A')}</span> • {item.get('type', '').title()}</p>
                    <p>{item.get('description', '')}</p>
                </div>"""
        elif category_type == "book":
            content = f"""
                <div style="padding: 15px; border-left: 3px solid #764ba2;">
                    <h4>{item.get('title', 'N/A')}</h4>
                    <p>by {item.get('author', 'Unknown')}</p>
                    <p><span class="rating">⭐ {item.get('rating', 'N/A')}</span></p>
                    <p>{item.get('description', '')}</p>
                </div>"""
        elif category_type == "podcast":
            content = f"""
                <div style="padding: 15px; border-left: 3px solid #764ba2;">
                    <h4>{item.get('title', 'N/A')}</h4>
                    <p>by {item.get('creator', 'Unknown')}</p>
                    <p>{item.get('description', '')}</p>
                </div>"""
        elif category_type == "wine":
            content = f"""
                <div style="padding: 15px; border-left: 3px solid #764ba2;">
                    <h4>{item.get('name', 'N/A')}</h4>
                    <p><span class="tag">{item.get('type', '')}</span> <span class="tag">{item.get('region', '')}</span></p>
                    <p><span class="price">{item.get('price_range', '')}</span></p>
                    <p>{item.get('description', '')}</p>
                    <p><strong>Where to buy:</strong> {item.get('where_to_buy', '')}</p>
                </div>"""
        elif category_type == "hiking":
            features = item.get('features', [])
            feature_tags = ''.join([f'<span class="tag">{f}</span>' for f in features])
            content = f"""
                <div style="padding: 15px; border-left: 3px solid #764ba2;">
                    <h4>{item.get('name', 'N/A')}</h4>
                    <p>{item.get('location', '')}</p>
                    <p><strong>{item.get('distance', '')}</strong> • <strong>{item.get('elevation', '')}</strong> • {item.get('difficulty', '')}</p>
                    <p>{feature_tags}</p>
                    <p>{item.get('description', '')}</p>
                </div>"""
        elif category_type == "perfume":
            scent_tags = ''.join([f'<span class="tag">{s}</span>' for s in item.get('scent_family', [])])
            content = f"""
                <div style="padding: 15px; border-left: 3px solid #764ba2;">
                    <h4>{item.get('name', 'N/A')}</h4>
                    <p>{item.get('brand', '')}</p>
                    <p>{scent_tags}</p>
                    <p><span class="price">{item.get('price_range', '')}</span></p>
                    <p>{item.get('description', '')}</p>
                    <p><strong>Where to buy:</strong> {item.get('where_to_buy', '')}</p>
                </div>"""
        
        cards_html += f"""
            <div class="card" data-category="{category_type}">
                <div class="card-header">
                    <h3>{title}</h3>
                    <div class="card-buttons">
                        <button class="refresh-btn" onclick="refreshCategory('{category_type}')">🔄 Refresh</button>
                        <button class="more-btn" onclick="getMoreOptions('{category_type}')">📋 3 Options</button>
                    </div>
                </div>
                <div class="card-body">
                    {content}
                </div>
            </div>
"""
    
    return cards_html

if __name__ == "__main__":
    print("🌐 Starting Simple Monthly Pack Web Server...")
    print("📂 Open your browser to: http://localhost:8080")
    print("💡 Click the buttons to refresh recommendations!")
    app.run(debug=False, host='0.0.0.0', port=8080)