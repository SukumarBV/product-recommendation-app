import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.neighbors import NearestNeighbors
from scipy.sparse import csr_matrix

# --- This class is UNCHANGED ---
class ContentBasedRecommender:
    """
    This class builds a Content-Based recommendation model
    based on item features.
    """
    def __init__(self):
        self.item_profiles = None
        self.tfidf_matrix = None
        self.cosine_sim = None
        self.indices = None

    def fit(self, products_csv_path):
        """
        Trains the model on the product data.
        Assumes CSV has columns: 'item_id', 'title', 'description', 'category'
        """
        df = pd.read_csv(products_csv_path)
        df['item_id'] = df['item_id'].astype(str)
        
        # Handle potential missing values in text fields
        df['title'] = df['title'].fillna('')
        df['description'] = df['description'].fillna('')
        df['category'] = df['category'].fillna('')
        
        # Create a 'soup' of features to vectorize
        df['soup'] = df['title'] + ' ' + df['description'] + ' ' + df['category']
        
        # Create TF-IDF matrix
        tfidf = TfidfVectorizer(stop_words='english')
        self.tfidf_matrix = tfidf.fit_transform(df['soup'])
        
        # Create cosine similarity matrix
        self.cosine_sim = cosine_similarity(self.tfidf_matrix, self.tfidf_matrix)
        
        # Create a mapping from item_id to dataframe index
        self.indices = pd.Series(df.index, index=df['item_id']).drop_duplicates()
        self.item_profiles = df

    def get_recommendations(self, item_id, n=10):
        """
        Gets top N similar items for a given item_id.
        """
        item_id = str(item_id)
        if item_id not in self.indices:
            return []  # Item not found

        idx = self.indices[item_id]
        
        # Get pairwise similarity scores
        sim_scores = list(enumerate(self.cosine_sim[idx]))
        
        # Sort by similarity
        sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
        
        # Get top N, skipping the first one (itself)
        sim_scores = sim_scores[1:n + 1]
        
        # Get item indices
        item_indices = [i[0] for i in sim_scores]
        
        # Return item titles and IDs
        results = self.item_profiles.iloc[item_indices][['item_id', 'title']]
        return results.to_dict('records')


# --- This class is NEW (replaces the surprise-based one) ---
class CollaborativeRecommender:
    """
    This class builds a User-Based k-NN Collaborative Filtering model
    using scikit-learn.
    """
    def __init__(self, k_neighbors=11):
        self.k_neighbors = k_neighbors # k=11 to get 10 neighbors + self
        self.nn_model = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=self.k_neighbors)
        self.user_item_matrix_sparse = None
        self.user_item_matrix_df = None
        self.user_id_map = None # maps user_id to matrix row index

    def fit(self, ratings_csv_path):
        """
        Trains the model on the ratings data.
        Assumes CSV has columns: 'user_id', 'item_id', 'rating'
        """
        df = pd.read_csv(ratings_csv_path)
        
        # Standardize types to string to avoid mismatches
        df['user_id'] = df['user_id'].astype(str)
        df['item_id'] = df['item_id'].astype(str)

        # Create pivot table: users as rows, items as columns
        user_item_matrix_df = df.pivot_table(index='user_id', columns='item_id', values='rating').fillna(0)
        
        # Store mappings from user_id to matrix row index
        self.user_id_map = {user_id: i for i, user_id in enumerate(user_item_matrix_df.index)}

        # Store the df and a sparse matrix for fast KNN
        self.user_item_matrix_df = user_item_matrix_df
        self.user_item_matrix_sparse = csr_matrix(self.user_item_matrix_df.values)

        # Fit the NearestNeighbors model
        self.nn_model.fit(self.user_item_matrix_sparse)

    def get_recommendations(self, user_id, n=10, product_profiles_df=None):
        """
        Gets top N recommendations for a given user_id.
        """
        user_id = str(user_id) # Ensure incoming ID is a string

        # Try to find the user in our map
        if user_id not in self.user_id_map:
            print(f"Warning: User {user_id} not in training data.")
            return []
        
        user_index = self.user_id_map[user_id]
        user_vector = self.user_item_matrix_sparse[user_index]
        
        # Find neighbors
        distances, indices = self.nn_model.kneighbors(user_vector)
        
        # Get neighbor indices (skip the first one, which is the user itself)
        neighbor_indices = indices.flatten()[1:]
        
        # Get the ratings from these neighbors
        neighbor_ratings = self.user_item_matrix_df.iloc[neighbor_indices]
        
        # Calculate mean rating for each item across all neighbors
        avg_neighbor_ratings = neighbor_ratings.mean(axis=0)
        
        # Get items the original user has *already* rated (rating > 0)
        user_ratings_series = self.user_item_matrix_df.iloc[user_index]
        rated_items = user_ratings_series[user_ratings_series > 0].index
        
        # Filter out already-rated items
        recommendations_series = avg_neighbor_ratings.drop(rated_items, errors='ignore').sort_values(ascending=False)
        
        # Get top N item IDs
        top_n_item_ids_str = recommendations_series.head(n).index.tolist()
        
        # Map back to titles
        if product_profiles_df is not None:
            # Ensure product_data item_id is also string
            product_profiles_df['item_id'] = product_profiles_df['item_id'].astype(str)
            
            results_df = product_profiles_df[product_profiles_df['item_id'].isin(top_n_item_ids_str)]
            
            # Re-order results to match prediction order
            if not results_df.empty:
                results_df = results_df.set_index('item_id').loc[top_n_item_ids_str].reset_index()
            
            return results_df.to_dict('records')
        else:
            return [{'item_id': item_id, 'title': 'N/A'} for item_id in top_n_item_ids_str]