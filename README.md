Product Recommendation System

This is a simple web application built with Python, Flask, and scikit-learn that demonstrates and compares two fundamental recommendation algorithms:

Content-Based Filtering: Recommends items based on their properties (e.g., description, category).

Collaborative Filtering: Recommends items based on the behavior of similar users (User-Based k-NN).

The app allows a user to upload product and rating data, trains both models in real-time, and then provides a side-by-side comparison of their recommendations.

Features

Dynamic File Uploads: Upload your own products.csv and ratings.csv files.

Side-by-Side Comparison: A clean UI to select a user and a product and see the different recommendations from both models.

Pure Python/scikit-learn: All models are built using pandas and scikit-learn (no surprise library needed).

Sample Data Generator: Includes a generate_datasets.py script to create perfectly formatted sample data.

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
