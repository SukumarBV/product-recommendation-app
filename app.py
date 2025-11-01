import os
from flask import Flask, request, render_template, jsonify
from recommender import ContentBasedRecommender, CollaborativeRecommender
import pandas as pd
import atexit

# Initialize Flask app
app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# --- In-Memory "Database" ---
# For a demo, we'll train and hold models in memory.
# For production, you'd save/load (pickle) models.
cb_recommender = ContentBasedRecommender()
cf_recommender = CollaborativeRecommender()
product_data = None
models_trained = False
uploaded_files = [] # Keep track of files to delete later

# --- Helper Function to Clean Up Uploads ---
def cleanup_files():
    """Remove uploaded files on app exit."""
    for f in uploaded_files:
        if os.path.exists(f):
            os.remove(f)
atexit.register(cleanup_files) # Register cleanup to run on exit

# --- Routes ---

@app.route('/')
def index():
    """Serves the main HTML page."""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    """Handles file uploads and model training."""
    global cb_recommender, cf_recommender, product_data, models_trained, uploaded_files
    
    if 'ratings_file' not in request.files or 'products_file' not in request.files:
        return jsonify({'error': 'Missing one or both files'}), 400
        
    ratings_file = request.files['ratings_file']
    products_file = request.files['products_file']

    if ratings_file.filename == '' or products_file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Save files
    ratings_path = os.path.join(app.config['UPLOAD_FOLDER'], ratings_file.filename)
    products_path = os.path.join(app.config['UPLOAD_FOLDER'], products_file.filename)
    ratings_file.save(ratings_path)
    products_file.save(products_path)
    
    # Add to cleanup list
    uploaded_files.extend([ratings_path, products_path])

    try:
        # Load product data
        product_data = pd.read_csv(products_path)
        product_data['item_id'] = product_data['item_id'].astype(str)
        
        # Load ratings data for user list
        ratings_data = pd.read_csv(ratings_path)
        
        # Get lists for dropdowns
        all_users = sorted(list(ratings_data['user_id'].unique()))
        all_items = product_data[['item_id', 'title']].to_dict('records')

        # --- Train Models ---
        print("Training Content-Based model...")
        cb_recommender.fit(products_path)
        print("Training Collaborative model...")
        cf_recommender.fit(ratings_path)
        print("Models trained successfully.")
        
        models_trained = True

        return jsonify({
            'message': 'Files uploaded and models trained!',
            'users': all_users,
            'items': all_items
        })

    except Exception as e:
        models_trained = False
        return jsonify({'error': f'Error processing files: {str(e)}'}), 500

@app.route('/recommend', methods=['POST'])
def get_recommendations():
    """Generates and returns recommendations."""
    if not models_trained:
        return jsonify({'error': 'Models not trained. Please upload files first.'}), 400
        
    data = request.get_json()
    if not data or 'user_id' not in data or 'item_id' not in data:
        return jsonify({'error': 'Missing user_id or item_id'}), 400

    user_id = data['user_id'] # Note: user_id from CSV might be int or string
    item_id = str(data['item_id']) # Ensure item_id is a string

    try:
        # Get Content-Based recommendations
        cb_recs = cb_recommender.get_recommendations(item_id, n=10)
        
        # Get Collaborative recommendations
        cf_recs = cf_recommender.get_recommendations(user_id, n=10, product_profiles_df=product_data)
        
        return jsonify({
            'collaborative': cf_recs,
            'content_based': cb_recs
        })

    except Exception as e:
        return jsonify({'error': f'Error generating recommendations: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)