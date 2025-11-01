#Product Recommendation System

This is a simple web application that demonstrates and compares two fundamental recommendation algorithms: Content-Based Filtering and Collaborative Filtering.

The app allows a user to upload product and rating data, trains both models in real-time, and then provides a clean, side-by-side comparison of their recommendations.

Technologies Used

How It Works

This project is a hands-on tool to understand the practical difference between the two main filtering methods.

1. Content-Based Filtering (The "Product Expert")

This model only reads the products.csv file. It doesn't know anything about users or ratings.

It uses TfidfVectorizer to convert product descriptions and categories into numerical vectors.

It then uses cosine_similarity to find products that are "textually" similar to the product you select.

Result: Recommends items that are objectively similar (e.g., "Laptop" -> "Gaming PC", "Monitor").

2. Collaborative Filtering (The "Taste Expert")

This model only reads the ratings.csv file. It doesn't know what a "laptop" or "jacket" is.

It creates a "user-item matrix" (who rated what).

Using NearestNeighbors, it finds a cluster of users who have similar taste profiles (i.e., they rated items similarly).

It then recommends items that those "neighbor" users loved but that the selected user hasn't seen yet.

Result: Recommends items based on shared user behavior (e.g., "People who liked this... also liked...").

Key Features

🧪 Live Model Comparison: Get immediate, side-by-side results from both algorithms to understand their different approaches.

⬆️ Dynamic Data Upload: Use your own products.csv and ratings.csv files to test the models on different datasets.

🤖 Sample Data Generator: Includes a generate_datasets.py script to create perfectly formatted sample data to get you started instantly.

🐍 Pure scikit-learn: Both models are built from the ground up using pandas and scikit-learn—no extra recommendation libraries needed.

How to Run This Project Locally

1. Clone the Repository:

git clone [https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git](https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git)
cd YOUR_REPO_NAME


2. Create and Activate a Virtual Environment:

# Windows
python -m venv venv
.\venv\Scripts\Activate.ps1

# macOS/Linux
python3 -m venv venv
source venv/bin/activate


3. Install Dependencies:

pip install -r requirements.txt


4. Generate Sample Data:
The app requires products.csv and ratings.csv. Run the included script to generate them:

python generate_datasets.py


(This will create products.csv and ratings.csv in your project folder. These files are listed in .gitignore and will not be uploaded to the repository).

5. Run the Flask App:

python app.py


6. Open the App:
Open your browser and go to http://127.0.0.1:5000.
