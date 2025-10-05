import requests
import json
import random
from datetime import datetime
from config import *

class RecommendationService:
    def __init__(self):
        self.session = requests.Session()
    
    def get_movie_recommendations(self, user_prefs, count=1):
        """Get movie/TV recommendations from TMDB"""
        try:
            # Search for shows similar to user's favorites
            favorite_shows = ["Virgin River", "Emily in Paris", "The Crown", "Fauda"]
            
            movies = []
            tv_shows = []
            
            # Get trending content
            trending_url = f"{TMDB_BASE_URL}/trending/all/week?api_key={TMDB_API_KEY}"
            response = self.session.get(trending_url)
            
            if response.status_code == 200:
                results = response.json().get('results', [])
                for item in results[:40]:  # Check more items for variety
                    if item.get('media_type') == 'movie':
                        # Filter for drama, comedy, romance
                        genres = item.get('genre_ids', [])
                        if any(g in [18, 35, 10749] for g in genres):  # Drama, Comedy, Romance
                            movies.append({
                                'title': item.get('title', ''),
                                'description': item.get('overview', ''),
                                'rating': item.get('vote_average', 0),
                                'poster': f"https://image.tmdb.org/t/p/w500{item.get('poster_path', '')}" if item.get('poster_path') else '',
                                'type': 'movie'
                            })
                    elif item.get('media_type') == 'tv':
                        genres = item.get('genre_ids', [])
                        if any(g in [18, 35, 10749] for g in genres):
                            tv_shows.append({
                                'title': item.get('name', ''),
                                'description': item.get('overview', ''),
                                'rating': item.get('vote_average', 0),
                                'poster': f"https://image.tmdb.org/t/p/w500{item.get('poster_path', '')}" if item.get('poster_path') else '',
                                'type': 'tv'
                            })
            
            # Return multiple recommendations
            all_content = movies + tv_shows
            if all_content:
                # Sort by rating and return top choices
                all_content.sort(key=lambda x: x['rating'], reverse=True)
                return all_content[:count] if count > 1 else all_content[0]
            
        except Exception as e:
            print(f"Error fetching movies/TV: {e}")
        
        # Fallback recommendations
        fallbacks = [
            {
                'title': 'The Good Place',
                'description': 'A comedy-drama about ethics and personal growth',
                'rating': 8.2,
                'poster': '',
                'type': 'tv'
            },
            {
                'title': 'Bridgerton',
                'description': 'Romantic period drama series with strong characters',
                'rating': 7.3,
                'poster': '',
                'type': 'tv'
            },
            {
                'title': 'Anne with an E',
                'description': 'Coming-of-age story with heart and character development',
                'rating': 8.7,
                'poster': '',
                'type': 'tv'
            }
        ]
        return fallbacks[:count] if count > 1 else fallbacks[0]
    
    def get_book_recommendations(self, user_prefs, count=1):
        """Get book recommendations from Google Books"""
        try:
            # Search terms based on user preferences
            search_terms = ["memoir", "spiritual growth", "mindfulness", "cultural stories", "inspirational", "family stories", "personal growth"]
            
            all_books = []
            
            # Try multiple search terms for variety
            for search_query in search_terms[:3]:  # Use first 3 terms
                url = f"{GOOGLE_BOOKS_BASE_URL}/volumes"
                params = {
                    'q': search_query,
                    'key': GOOGLE_BOOKS_API_KEY,
                    'maxResults': 15,
                    'orderBy': 'relevance'
                }
                
                response = self.session.get(url, params=params)
                
                if response.status_code == 200:
                    books = response.json().get('items', [])
                    for book in books:
                        volume_info = book.get('volumeInfo', {})
                        if volume_info.get('authors') and volume_info.get('description'):
                            all_books.append({
                                'title': volume_info.get('title', ''),
                                'author': ', '.join(volume_info.get('authors', [])),
                                'description': volume_info.get('description', '')[:200] + '...',
                                'rating': volume_info.get('averageRating', 'N/A'),
                                'thumbnail': volume_info.get('imageLinks', {}).get('thumbnail', ''),
                                'link': volume_info.get('previewLink', '')
                            })
            
            if all_books:
                # Remove duplicates and return requested count
                unique_books = []
                seen_titles = set()
                for book in all_books:
                    if book['title'].lower() not in seen_titles:
                        unique_books.append(book)
                        seen_titles.add(book['title'].lower())
                
                return unique_books[:count] if count > 1 else unique_books[0]
                        
        except Exception as e:
            print(f"Error fetching books: {e}")
        
        # Fallback recommendations
        fallbacks = [
            {
                'title': 'The Power of Now',
                'author': 'Eckhart Tolle',
                'description': 'A spiritual guide to enlightenment and living in the present moment',
                'rating': 4.5,
                'thumbnail': '',
                'link': ''
            },
            {
                'title': 'Untamed',
                'author': 'Glennon Doyle',
                'description': 'A memoir about finding courage to live authentically and break free from expectations',
                'rating': 4.3,
                'thumbnail': '',
                'link': ''
            },
            {
                'title': 'The Gifts of Imperfection',
                'author': 'Brené Brown',
                'description': 'Guide to cultivating courage, compassion, and connection',
                'rating': 4.6,
                'thumbnail': '',
                'link': ''
            }
        ]
        return fallbacks[:count] if count > 1 else fallbacks[0]
    
    def get_podcast_recommendations(self, user_prefs, count=1):
        """Get podcast recommendations from iTunes"""
        try:
            # Search terms based on user preferences
            search_terms = ["mindfulness", "parenting", "wellness", "meditation", "self growth", "yoga", "motherhood", "family"]
            
            all_podcasts = []
            
            # Try multiple search terms for variety
            for search_term in search_terms[:4]:  # Use first 4 terms
                url = ITUNES_BASE_URL
                params = {
                    'term': search_term,
                    'media': 'podcast',
                    'limit': 15
                }
                
                response = self.session.get(url, params=params)
                
                if response.status_code == 200:
                    podcasts = response.json().get('results', [])
                    for podcast in podcasts:
                        if podcast.get('artistName') and podcast.get('collectionName'):
                            all_podcasts.append({
                                'title': podcast.get('collectionName', ''),
                                'creator': podcast.get('artistName', ''),
                                'description': podcast.get('description', '')[:200] + '...' if podcast.get('description') else 'Podcast focused on ' + search_term,
                                'artwork': podcast.get('artworkUrl600', ''),
                                'link': podcast.get('collectionViewUrl', '')
                            })
            
            if all_podcasts:
                # Remove duplicates and return requested count
                unique_podcasts = []
                seen_titles = set()
                for podcast in all_podcasts:
                    if podcast['title'].lower() not in seen_titles:
                        unique_podcasts.append(podcast)
                        seen_titles.add(podcast['title'].lower())
                
                return unique_podcasts[:count] if count > 1 else unique_podcasts[0]
                        
        except Exception as e:
            print(f"Error fetching podcasts: {e}")
        
        # Fallback recommendations
        fallbacks = [
            {
                'title': 'The Mindful Mom',
                'creator': 'Various',
                'description': 'A podcast for mindful parenting and personal growth',
                'artwork': '',
                'link': ''
            },
            {
                'title': 'Meditation for Moms',
                'creator': 'Various',
                'description': 'Guided meditations and mindfulness practices for busy mothers',
                'artwork': '',
                'link': ''
            },
            {
                'title': 'Wellness for Women',
                'creator': 'Various',
                'description': 'Health, wellness, and self-care tips for women',
                'artwork': '',
                'link': ''
            }
        ]
        return fallbacks[:count] if count > 1 else fallbacks[0]
    
    def get_wine_recommendations(self, user_prefs, count=1):
        """Get wine recommendations - manual curated list"""
        # Since no free wine API, use curated list based on preferences
        red_wines = [
            {
                'name': 'Catena Malbec',
                'type': 'Malbec',
                'region': 'Argentina',
                'price_range': '$15-25',
                'description': 'Rich, full-bodied Malbec with dark fruit flavors and smooth tannins',
                'where_to_buy': 'Total Wine, BevMo'
            },
            {
                'name': 'Bogle Cabernet Sauvignon',
                'type': 'Cabernet Sauvignon', 
                'region': 'California',
                'price_range': '$12-18',
                'description': 'Classic California Cabernet with blackberry and vanilla notes',
                'where_to_buy': 'Safeway, Total Wine'
            },
            {
                'name': 'Columbia Crest Grand Estates Syrah',
                'type': 'Syrah',
                'region': 'Washington',
                'price_range': '$10-15',
                'description': 'Bold Syrah with spice and dark berry flavors',
                'where_to_buy': 'Most grocery stores'
            },
            {
                'name': 'Seghesio Zinfandel',
                'type': 'Zinfandel',
                'region': 'Sonoma County',
                'price_range': '$20-30',
                'description': 'Robust Zinfandel with jammy fruit and peppery finish',
                'where_to_buy': 'Wine shops, Total Wine'
            },
            {
                'name': 'Decoy Cabernet Sauvignon',
                'type': 'Cabernet Sauvignon',
                'region': 'Sonoma County',
                'price_range': '$18-25',
                'description': 'Elegant Cabernet with cherry and plum notes, smooth finish',
                'where_to_buy': 'BevMo, Whole Foods'
            },
            {
                'name': 'Alamos Malbec',
                'type': 'Malbec',
                'region': 'Argentina',
                'price_range': '$8-12',
                'description': 'Affordable everyday Malbec with ripe berry flavors',
                'where_to_buy': 'Most grocery stores'
            },
            {
                'name': 'La Crema Pinot Noir',
                'type': 'Pinot Noir',
                'region': 'Sonoma Coast',
                'price_range': '$25-35',
                'description': 'Sophisticated Pinot Noir with cherry and earth tones',
                'where_to_buy': 'Wine shops, Total Wine'
            }
        ]
        
        if count == 1:
            return random.choice(red_wines)
        else:
            # Return multiple random choices without duplicates
            shuffled = red_wines.copy()
            random.shuffle(shuffled)
            return shuffled[:min(count, len(shuffled))]
    
    def get_hiking_recommendations(self, user_prefs, count=1):
        """Get hiking recommendations for Bay Area"""
        # Curated list of Bay Area hikes matching preferences
        bay_area_hikes = [
            {
                'name': 'Filoli Gardens Trail',
                'location': 'Woodside, CA',
                'distance': '2 miles',
                'elevation': '100 ft',
                'difficulty': 'Easy',
                'features': ['Gardens', 'Historic mansion', 'Peaceful'],
                'description': 'Beautiful gardens and easy walking paths with stunning views'
            },
            {
                'name': 'Uvas Canyon County Park',
                'location': 'Morgan Hill, CA',
                'distance': '4 miles',
                'elevation': '300 ft',
                'difficulty': 'Moderate',
                'features': ['Waterfalls', 'Creek', 'Shaded'],
                'description': 'Lovely trail with multiple waterfalls and creek crossings'
            },
            {
                'name': 'Rancho San Antonio Preserve',
                'location': 'Cupertino, CA',
                'distance': '6 miles',
                'elevation': '200 ft',
                'difficulty': 'Moderate',
                'features': ['Close to home', 'Wildlife', 'Open space'],
                'description': 'Local favorite with rolling hills and farm animals'
            },
            {
                'name': 'Pescadero Creek Park',
                'location': 'Pescadero, CA',
                'distance': '5 miles',
                'elevation': '250 ft',
                'difficulty': 'Moderate',
                'features': ['Redwoods', 'Creek', 'Peaceful'],
                'description': 'Serene hike through towering redwoods along a gentle creek'
            },
            {
                'name': 'Stevens Creek County Park',
                'location': 'Cupertino, CA',
                'distance': '3 miles',
                'elevation': '150 ft',
                'difficulty': 'Easy-Moderate',
                'features': ['Close to home', 'Lake views', 'Shaded'],
                'description': 'Pleasant loop around Stevens Creek Reservoir'
            },
            {
                'name': 'Castle Rock State Park',
                'location': 'Los Gatos, CA',
                'distance': '5 miles',
                'elevation': '400 ft',
                'difficulty': 'Moderate',
                'features': ['Rock formations', 'Views', 'Forest'],
                'description': 'Stunning rock formations and panoramic views'
            },
            {
                'name': 'Almaden Quicksilver Park',
                'location': 'San Jose, CA',
                'distance': '4 miles',
                'elevation': '300 ft',
                'difficulty': 'Moderate',
                'features': ['Historic mining', 'Wildflowers', 'Open hills'],
                'description': 'Historic mining area with beautiful spring wildflowers'
            }
        ]
        
        if count == 1:
            return random.choice(bay_area_hikes)
        else:
            # Return multiple random choices without duplicates
            shuffled = bay_area_hikes.copy()
            random.shuffle(shuffled)
            return shuffled[:min(count, len(shuffled))]
    
    def get_perfume_recommendations(self, user_prefs, count=1):
        """Get perfume recommendations - curated list"""
        # Curated list based on Jo Malone preferences and scent profile
        perfumes = [
            {
                'name': 'Jo Malone Wood Sage & Sea Salt',
                'brand': 'Jo Malone',
                'scent_family': ['Woody', 'Fresh'],
                'price_range': '$68-134',
                'description': 'Fresh and woody with sea salt minerality - perfect for everyday wear',
                'where_to_buy': 'Sephora, Nordstrom'
            },
            {
                'name': 'Bath & Body Works Eucalyptus Tea',
                'brand': 'Bath & Body Works',
                'scent_family': ['Woody', 'Herbal'],
                'price_range': '$12-25',
                'description': 'Affordable alternative with eucalyptus and warm tea notes',
                'where_to_buy': 'Bath & Body Works'
            },
            {
                'name': 'The Body Shop White Musk',
                'brand': 'The Body Shop',
                'scent_family': ['Woody', 'Floral'],
                'price_range': '$20-35',
                'description': 'Clean, warm musk with subtle floral undertones',
                'where_to_buy': 'The Body Shop, Ulta'
            },
            {
                'name': 'Jo Malone Basil & Neroli',
                'brand': 'Jo Malone',
                'scent_family': ['Herbal', 'Citrus'],
                'price_range': '$68-134',
                'description': 'Uplifting blend of basil and neroli - energizing and sophisticated',
                'where_to_buy': 'Sephora, Jo Malone boutique'
            },
            {
                'name': 'Pacifica Indian Coconut Nectar',
                'brand': 'Pacifica',
                'scent_family': ['Warm', 'Exotic'],
                'price_range': '$22-36',
                'description': 'Warm coconut with vanilla and wood notes - tropical and cozy',
                'where_to_buy': 'Target, Ulta, Whole Foods'
            },
            {
                'name': 'Jo Malone Peony & Blush Suede',
                'brand': 'Jo Malone',
                'scent_family': ['Floral', 'Suede'],
                'price_range': '$68-134',
                'description': 'Soft floral with luxurious suede notes - elegant and feminine',
                'where_to_buy': 'Sephora, Nordstrom'
            },
            {
                'name': 'Nest Cedar Leaf & Lavender',
                'brand': 'Nest',
                'scent_family': ['Woody', 'Herbal'],
                'price_range': '$45-68',
                'description': 'Calming blend of cedar and lavender - perfect for relaxation',
                'where_to_buy': 'Sephora, Nordstrom'
            }
        ]
        
        if count == 1:
            return random.choice(perfumes)
        else:
            # Return multiple random choices without duplicates
            shuffled = perfumes.copy()
            random.shuffle(shuffled)
            return shuffled[:min(count, len(shuffled))]