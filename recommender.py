import argparse
import pickle
import sys

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd

import config


class Book:

    def __init__(self, title, author, language=None):
        self.title = title
        self.author = author
        self.language = language

    def to_json(self):
        return {key: value for key, value in self.__dict__.items() if key != 'language'}


class BookRecommender:

    def __init__(self):
        try:
            with open(config.VECTORIZER_PATH, 'rb') as fp:
                self._vectorizer = pickle.load(fp)

            with open(config.BOOK_VECTORS_PATH, 'rb') as fp:
                self._book_vectors = pickle.load(fp)
        except FileNotFoundError:
            print("TF-IDF model is not trained. Run 'python -m recommender --train'")
            sys.exit(-1)
        self._books_df = load_books()

    def get_recommendations(self, titles, n=5):
        title_vectors = self._vectorizer.transform([title.lower() for title in titles])
        similarities = cosine_similarity(title_vectors, self._book_vectors)
        indices = np.unique(np.argsort(-similarities)[:, :n].flatten())
        recommended_books = {
            Book(title, author)
            for title, author in self._books_df[['Title', 'Author']].iloc[indices].values
        }
        return recommended_books


def load_books(filepath=config.BOOKS_PATH):
    books_df = pd.read_csv(filepath, encoding='utf-8')
    books_df.Title.fillna('', inplace=True)
    books_df.reset_index(inplace=True)
    return books_df


def train():
    print('\n- Loading books')
    books_df = load_books()
    tfidf_vectorizer = TfidfVectorizer(stop_words='english',
                                       ngram_range=(3, 5),
                                       analyzer='char')
    print('- Training TF-IDF vectorizer')
    book_vectors = tfidf_vectorizer.fit_transform(books_df.Title)

    with open(config.VECTORIZER_PATH, 'wb') as fp:
        pickle.dump(tfidf_vectorizer, fp)

    with open(config.BOOK_VECTORS_PATH, 'wb') as fp:
        pickle.dump(book_vectors, fp)
    print("- Models saved to '{}'\n".format(config.MODELS_DIR))


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--train', action='store_true',
                        help='Train recomender system model.')
    parser.add_argument('-b', '--book', type=str,
                        help='Name of book as input for recommender system.')
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()

    if args.train:
        train()

    if args.book:
        recommender = BookRecommender()
        books = recommender.get_recommendations(titles=[args.book])
        for book in books:
            print(book.title, book.author)
