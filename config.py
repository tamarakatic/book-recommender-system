import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(ROOT_DIR, 'data/')
MODELS_DIR = os.path.join(ROOT_DIR, 'models/')

BOOKS_PATH = os.path.join(DATA_DIR, 'books.csv')
VECTORIZER_PATH = os.path.join(MODELS_DIR, 'vectorizer.pkl')
BOOK_VECTORS_PATH = os.path.join(MODELS_DIR, 'book_vectors.pkl')
