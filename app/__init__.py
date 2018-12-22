from flask import Flask
from recommender import BookRecommender

app = Flask(__name__)
app.book_recommender = BookRecommender()

from app import routes
