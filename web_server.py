#!/usr/bin/env python3
"""
Monthly Pack Agent - Web Server
Provides web interface for interactive recommendations
"""

import json
import os
from datetime import datetime
from flask import Flask, render_template_string, jsonify, send_from_directory
from api_services import RecommendationService

app = Flask(__name__)

def load_user_data():
    """Load user preferences from JSON file"""
    try:
        with open('user_data.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return None

def get_fresh_recommendations(category=None, count=1):
    """Get fresh recommendations for a specific category or all categories"""
    user_data = load_user_data()
    if not user_data:
        return None
    
    rec_service = RecommendationService()
    
    if category:
        # Get recommendations for specific category
        if category == 'entertainment':
            return rec_service.get_movie_recommendations(user_data.get('tvMovies', {}), count)
        elif category == 'book':
            return rec_service.get_book_recommendations(user_data.get('books', {}), count)
        elif category == 'podcast':
            return rec_service.get_podcast_recommendations(user_data.get('podcasts', {}), count)
        elif category == 'wine':
            return rec_service.get_wine_recommendations(user_data.get('wine', {}), count)
        elif category == 'hiking':
            return rec_service.get_hiking_recommendations(user_data.get('hiking', {}), count)
        elif category == 'perfume':
            return rec_service.get_perfume_recommendations(user_data.get('perfume', {}), count)
    else:
        # Get all categories
        return {
            'entertainment': rec_service.get_movie_recommendations(user_data.get('tvMovies', {}), count),
            'book': rec_service.get_book_recommendations(user_data.get('books', {}), count),
            'podcast': rec_service.get_podcast_recommendations(user_data.get('podcasts', {}), count),
            'wine': rec_service.get_wine_recommendations(user_data.get('wine', {}), count),
            'hiking': rec_service.get_hiking_recommendations(user_data.get('hiking', {}), count),
            'perfume': rec_service.get_perfume_recommendations(user_data.get('perfume', {}), count)
        }

@app.route('/')
def index():
    """Serve the main monthly pack page"""
    try:
        with open('recommendations.json', 'r') as f:
            pack = json.load(f)
    except FileNotFoundError:
        return "No monthly pack found. Please run 'python generate_pack.py' first."
    
    return create_interactive_html(pack)

@app.route('/api/refresh/<category>')
def refresh_category(category):
    """API endpoint to refresh a specific category"""
    recommendations = get_fresh_recommendations(category, count=1)
    if recommendations:
        return jsonify({'success': True, 'recommendations': recommendations})
    else:
        return jsonify({'success': False, 'error': 'Failed to get recommendations'})

@app.route('/api/refresh/all')
def refresh_all():
    """API endpoint to refresh all categories"""
    recommendations = get_fresh_recommendations(count=1)
    if recommendations:
        return jsonify({'success': True, 'recommendations': recommendations})
    else:
        return jsonify({'success': False, 'error': 'Failed to get recommendations'})

@app.route('/api/more/<category>')
def more_category(category):
    """API endpoint to get multiple options for a specific category"""
    recommendations = get_fresh_recommendations(category, count=3)
    if recommendations:
        return jsonify({'success': True, 'recommendations': recommendations})
    else:
        return jsonify({'success': False, 'error': 'Failed to get recommendations'})

def create_interactive_html(pack):
    """Create interactive HTML with working refresh buttons"""
    
    # JavaScript helper functions
    js_functions = """
    function formatRecommendation(item, categoryType) {
        let content = `<div style="margin-bottom: 20px; padding: 15px; border-left: 3px solid #764ba2;">`;
        
        if (categoryType === 'entertainment') {
            content += `
                <h4>${item.title || 'N/A'}</h4>
                <p><span class="rating">⭐ ${item.rating || 'N/A'}</span> • ${(item.type || '').charAt(0).toUpperCase() + (item.type || '').slice(1)}</p>
                <p>${item.description || ''}</p>
            `;
        } else if (categoryType === 'book') {
            content += `
                <h4>${item.title || 'N/A'}</h4>
                <p>by ${item.author || 'Unknown'}</p>
                <p><span class="rating">⭐ ${item.rating || 'N/A'}</span></p>
                <p>${item.description || ''}</p>
            `;
        } else if (categoryType === 'podcast') {
            content += `
                <h4>${item.title || 'N/A'}</h4>
                <p>by ${item.creator || 'Unknown'}</p>
                <p>${item.description || ''}</p>
            `;
        } else if (categoryType === 'wine') {
            content += `
                <h4>${item.name || 'N/A'}</h4>
                <p><span class="tag">${item.type || ''}</span> <span class="tag">${item.region || ''}</span></p>
                <p><span class="price">${item.price_range || ''}</span></p>
                <p>${item.description || ''}</p>
                <p><strong>Where to buy:</strong> ${item.where_to_buy || ''}</p>
            `;
        } else if (categoryType === 'hiking') {
            let features = item.features || [];
            let featureTags = features.map(f => `<span class="tag">${f}</span>`).join('');
            content += `
                <h4>${item.name || 'N/A'}</h4>
                <p>${item.location || ''}</p>
                <p><strong>${item.distance || ''}</strong> • <strong>${item.elevation || ''}</strong> • ${item.difficulty || ''}</p>
                <p>${featureTags}</p>
                <p>${item.description || ''}</p>
            `;
        } else if (categoryType === 'perfume') {
            let scentTags = (item.scent_family || []).map(s => `<span class="tag">${s}</span>`).join('');
            content += `
                <h4>${item.name || 'N/A'}</h4>
                <p>${item.brand || ''}</p>
                <p>${scentTags}</p>
                <p><span class="price">${item.price_range || ''}</span></p>
                <p>${item.description || ''}</p>
                <p><strong>Where to buy:</strong> ${item.where_to_buy || ''}</p>
            `;
        }
        
        content += `</div>`;
        return content;
    }
    
    function updateCategoryContent(category, recommendations) {
        const cardBody = document.querySelector(`[data-category="${category}"] .card-body`);
        if (!cardBody) return;
        
        let content = '';
        if (Array.isArray(recommendations)) {
            recommendations.forEach(item => {
                content += formatRecommendation(item, category);
            });
        } else {
            content = formatRecommendation(recommendations, category);
        }
        
        cardBody.innerHTML = content;
    }
    
    function refreshCategory(category) {
        const button = document.querySelector(`[data-category="${category}"] .refresh-btn`);
        const originalText = button.textContent;
        button.textContent = '🔄 Loading...';
        button.disabled = true;
        
        fetch(`/api/refresh/${category}`)
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    updateCategoryContent(category, data.recommendations);
                } else {
                    alert('Failed to get new recommendations. Please try again.');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error getting recommendations. Please try again.');
            })
            .finally(() => {
                button.textContent = originalText;
                button.disabled = false;
            });
    }
    
    function getMoreOptions(category) {
        const button = document.querySelector(`[data-category="${category}"] .more-btn`);
        const originalText = button.textContent;
        button.textContent = '⏳ Loading...';
        button.disabled = true;
        
        fetch(`/api/more/${category}`)
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    updateCategoryContent(category, data.recommendations);
                } else {
                    alert('Failed to get more options. Please try again.');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error getting options. Please try again.');
            })
            .finally(() => {
                button.textContent = originalText;
                button.disabled = false;
            });
    }
    
    function refreshAllCategories() {
        const button = document.querySelector('.refresh-all-btn');
        const originalText = button.textContent;
        button.textContent = '🔄 Refreshing All...';
        button.disabled = true;
        
        fetch('/api/refresh/all')
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    Object.keys(data.recommendations).forEach(category => {
                        updateCategoryContent(category, data.recommendations[category]);
                    });
                } else {
                    alert('Failed to refresh recommendations. Please try again.');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Error refreshing recommendations. Please try again.');
            })
            .finally(() => {
                button.textContent = originalText;
                button.disabled = false;
            });
    }
    """
    
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
            gap: 10px;
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
        .refresh-btn, .more-btn, .refresh-all-btn {{
            background: rgba(255,255,255,0.2);
            color: white;
            border: 1px solid rgba(255,255,255,0.3);
            padding: 8px 12px;
            border-radius: 20px;
            font-size: 0.9em;
            cursor: pointer;
            transition: all 0.3s ease;
        }}
        .refresh-btn:hover, .more-btn:hover, .refresh-all-btn:hover {{
            background: rgba(255,255,255,0.3);
            transform: translateY(-1px);
        }}
        .refresh-btn:disabled, .more-btn:disabled, .refresh-all-btn:disabled {{
            opacity: 0.6;
            cursor: not-allowed;
        }}
        .button-container {{
            text-align: center;
            margin: 30px 0;
        }}
        .refresh-all-btn {{
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
            <div class="button-container">
                <button class="refresh-all-btn" onclick="refreshAllCategories()">🔄 Refresh All Categories</button>
            </div>
        </div>
        
        <div class="recommendations">
"""
    
    # Generate category cards with interactive buttons
    recs = pack['recommendations']
    categories = [
        ("📺 Entertainment", "entertainment", recs.get('entertainment', {})),
        ("📚 Book", "book", recs.get('book', {})),
        ("🎧 Podcast", "podcast", recs.get('podcast', {})),
        ("🍷 Wine", "wine", recs.get('wine', {})),
        ("🥾 Hiking", "hiking", recs.get('hiking', {})),
        ("🌸 Perfume", "perfume", recs.get('perfume', {}))
    ]
    
    for title, category_type, items in categories:
        # Format content for this category
        content = ""
        if not isinstance(items, list):
            items = [items]
        
        for i, item in enumerate(items):
            margin = "margin-bottom: 20px;" if i < len(items) - 1 else ""
            
            if category_type == "entertainment":
                content += f"""
                    <div style="{margin} padding: 15px; border-left: 3px solid #667eea;">
                        <h4>{item.get('title', 'N/A')}</h4>
                        <p><span class="rating">⭐ {item.get('rating', 'N/A')}</span> • {item.get('type', '').title()}</p>
                        <p>{item.get('description', '')}</p>
                    </div>"""
            elif category_type == "book":
                content += f"""
                    <div style="{margin} padding: 15px; border-left: 3px solid #764ba2;">
                        <h4>{item.get('title', 'N/A')}</h4>
                        <p>by {item.get('author', 'Unknown')}</p>
                        <p><span class="rating">⭐ {item.get('rating', 'N/A')}</span></p>
                        <p>{item.get('description', '')}</p>
                    </div>"""
            elif category_type == "podcast":
                content += f"""
                    <div style="{margin} padding: 15px; border-left: 3px solid #764ba2;">
                        <h4>{item.get('title', 'N/A')}</h4>
                        <p>by {item.get('creator', 'Unknown')}</p>
                        <p>{item.get('description', '')}</p>
                    </div>"""
            elif category_type == "wine":
                content += f"""
                    <div style="{margin} padding: 15px; border-left: 3px solid #764ba2;">
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
                    <div style="{margin} padding: 15px; border-left: 3px solid #764ba2;">
                        <h4>{item.get('name', 'N/A')}</h4>
                        <p>{item.get('location', '')}</p>
                        <p><strong>{item.get('distance', '')}</strong> • <strong>{item.get('elevation', '')}</strong> • {item.get('difficulty', '')}</p>
                        <p>{feature_tags}</p>
                        <p>{item.get('description', '')}</p>
                    </div>"""
            elif category_type == "perfume":
                scent_tags = ''.join([f'<span class="tag">{s}</span>' for s in item.get('scent_family', [])])
                content += f"""
                    <div style="{margin} padding: 15px; border-left: 3px solid #764ba2;">
                        <h4>{item.get('name', 'N/A')}</h4>
                        <p>{item.get('brand', '')}</p>
                        <p>{scent_tags}</p>
                        <p><span class="price">{item.get('price_range', '')}</span></p>
                        <p>{item.get('description', '')}</p>
                        <p><strong>Where to buy:</strong> {item.get('where_to_buy', '')}</p>
                    </div>"""
        
        html_template += f"""
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
    
    html_template += f"""
        </div>
        
        <div class="footer">
            <p>Generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')}</p>
            <p>💝 Made with love for Swapna</p>
        </div>
    </div>
    
    <script>
        {js_functions}
    </script>
</body>
</html>
"""
    
    return html_template

if __name__ == "__main__":
    print("🌐 Starting Monthly Pack Web Server...")
    print("📂 Open your browser to: http://localhost:8080")
    print("💡 Interactive refresh buttons will work in the web version!")
    app.run(debug=True, host='0.0.0.0', port=8080)