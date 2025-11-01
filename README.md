# Product Recommendation System


This is a simple web application that demonstrates and compares two fundamental recommendation algorithms: **Content-Based Filtering** and **Collaborative Filtering**.

The app allows a user to upload product and rating data, trains both models in real-time, and then provides a clean, side-by-side comparison of their recommendations.

### Technologies Used
![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-black?logo=flask)
![scikit-learn](https://img.shields.io/badge/scikit--learn-F7931E?logo=scikit-learn)
![Pandas](https://img.shields.io/badge/Pandas-150458?logo=pandas)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?logo=html5)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?logo=css3)

---

## How It Works

This project is a hands-on tool to understand the practical difference between the two main filtering methods.

### 1. Content-Based Filtering (The "Product Expert")

This model **only reads the `products.csv` file**. It doesn't know anything about users or ratings.
* It uses `TfidfVectorizer` to convert product descriptions and categories into numerical vectors.
* It then uses `cosine_similarity` to find products that are "textually" similar to the product you select.
* **Result:** Recommends items that are objectively similar (e.g., "Laptop" -> "Gaming PC", "Monitor").

### 2. Collaborative Filtering (The "Taste Expert")

This model **only reads the `ratings.csv` file**. It doesn't know what a "laptop" or "jacket" is.
* It creates a "user-item matrix" (who rated what).
* Using `NearestNeighbors`, it finds a cluster of users who have similar taste profiles (i.e., they rated items similarly).
* It then recommends items that those "neighbor" users loved but that the selected user hasn't seen yet.
* **Result:** Recommends items based on shared user behavior (e.g., "People who liked this... also liked...").

---

## Key Features

* **🧪 Live Model Comparison:** Get immediate, side-by-side results from both algorithms to understand their different approaches.
* **⬆️ Dynamic Data Upload:** Use your own `products.csv` and `ratings.csv` files to test the models on different datasets.
* **🤖 Sample Data Generator:** Includes a `generate_datasets.py` script to create perfectly formatted sample data to get you started instantly.
* **🐍 Pure scikit-learn:** Both models are built from the ground up using `pandas` and `scikit-learn`—no extra recommendation libraries needed.

---
