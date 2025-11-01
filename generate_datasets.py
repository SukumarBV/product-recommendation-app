import pandas as pd
import random

# --- 1. Define Product Catalogs ---

# We'll create 4 distinct categories
products_data = {
    'Electronics': [
        {"title": "Quantum Pro Laptop", "desc": "A high-performance laptop with 16GB RAM and 1TB SSD. Fast processor for all your needs."},
        {"title": "Alpha Wireless Mouse", "desc": "Ergonomic wireless mouse with 5 programmable buttons. Long battery life."},
        {"title": "Noise-Cancelling Headphones", "desc": "Immersive sound quality with active noise cancellation. Perfect for travel and work."},
        {"title": "4K Ultra HD Monitor", "desc": "Stunning 27-inch 4K monitor. Vibrant colors and sharp details. A great computer display."},
        {"title": "Smart Home Hub", "desc": "Control your smart devices with this central hub. Voice-activated assistant."},
    ],
    'Clothing': [
        {"title": "Men's Classic Denim Jacket", "desc": "A timeless denim jacket for all seasons. Comfortable fit and durable fabric."},
        {"title": "Women's Silk Blouse", "desc": "Elegant 100% silk blouse, perfect for formal or casual wear. Available in 5 colors."},
        {"title": "TrailFinder Hiking Boots", "desc": "Waterproof hiking boots with excellent grip. Designed for all-terrain adventure."},
        {"title": "Cozy Knit Scarf", "desc": "A warm and soft knit scarf, perfect for winter. Made from premium wool."},
        {"title": "Performance Running Shorts", "desc": "Lightweight and breathable running shorts for men and women. Wicks moisture away."},
    ],
    'Home & Kitchen': [
        {"title": "Artisan Stand Mixer", "desc": "Powerful stand mixer for all your baking needs. Comes with 3 attachments."},
        {"title": "Stainless Steel Cookware Set", "desc": "10-piece stainless steel pot and pan set. Durable and easy to clean."},
        {"title": "Robotic Vacuum Cleaner", "desc": "Smart robotic vacuum with mapping technology. Cleans your home automatically."},
        {"title": "Espresso Machine", "desc": "Barista-grade espresso machine for home use. Brew the perfect shot every time."},
        {"title": "Memory Foam Mattress", "desc": "Queen size memory foam mattress for ultimate comfort and support. Cooling gel layer."},
    ],
    'Books': [
        {"title": "The Quantum Rift", "desc": "A mind-bending science fiction novel about parallel universes. A must-read sci-fi adventure."},
        {"title": "The Chef's Secret", "desc": "A thrilling mystery set in a 19th-century Parisian kitchen. A great culinary story."},
        {"title":"History of the Ancient World", "desc": "A comprehensive guide to ancient civilizations. Full of facts and illustrations."},
        {"title": "The Minimalist Home", "desc": "A practical guide to decluttering and simplifying your life. Organize your home."},
        {"title": "Python for Data Science", "desc": "Learn Python programming and data analysis from scratch. A great technical book for a programmer."},
    ]
}

# --- 2. Define User Personas ---

# We'll create 4 user types with clear preferences
user_personas = {
    'U1_Techie': {'Electronics': 5, 'Books': 4, 'Home & Kitchen': 3, 'Clothing': 2},
    'U2_Fashionista': {'Clothing': 5, 'Home & Kitchen': 4, 'Books': 2, 'Electronics': 1},
    'U3_Homebody': {'Home & Kitchen': 5, 'Clothing': 4, 'Books': 3, 'Electronics': 2},
    'U4_Bookworm': {'Books': 5, 'Clothing': 3, 'Home & Kitchen': 2, 'Electronics': 1},
    'U5_GadgetFan': {'Electronics': 5, 'Home & Kitchen': 4, 'Books': 3, 'Clothing': 1},
    'U6_Outdoorsy': {'Clothing': 5, 'Books': 4, 'Home & Kitchen': 3, 'Electronics': 1},
}

# --- 3. Generate Products CSV ---

print("Generating products.csv...")
products_list = []
item_id_counter = 101 # Start item IDs from 101

for category, items in products_data.items():
    for item in items:
        products_list.append({
            'item_id': f'P{item_id_counter}',
            'title': item['title'],
            'description': item['desc'],
            'category': category
        })
        item_id_counter += 1

products_df = pd.DataFrame(products_list)
products_df.to_csv('products.csv', index=False)
print("Successfully created products.csv")

# --- 4. Generate Ratings CSV ---

print("Generating ratings.csv...")
ratings_list = []
user_id_counter = 1 # Start user IDs from 1

# Create multiple users for each persona to create "clusters" of similar users
for i in range(50): # We'll create 50 users total
    user_id = f'U{user_id_counter}'
    user_id_counter += 1
    
    # Randomly pick a persona for this user
    persona_name, prefs = random.choice(list(user_personas.items()))
    
    # Each user will rate ~60% of the products
    for _, product in products_df.iterrows():
        if random.random() < 0.6: # 60% chance to rate any given item
            base_rating = prefs[product['category']]
            
            # Add some "noise" to make ratings imperfect
            noise = random.choice([-1, -0.5, 0, 0, 0.5, 1])
            rating = base_rating + noise
            
            # Clamp ratings between 1 and 5
            rating = max(1, min(5, rating))
            
            ratings_list.append({
                'user_id': user_id,
                'item_id': product['item_id'],
                'rating': rating
            })

ratings_df = pd.DataFrame(ratings_list)
# Shuffle the ratings to make it look more real
ratings_df = ratings_df.sample(frac=1).reset_index(drop=True)

ratings_df.to_csv('ratings.csv', index=False)
print("Successfully created ratings.csv")
print("\nDone! You can now run 'python app.py' and use the generated files.")
