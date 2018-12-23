from flask import request, jsonify, render_template

from app import app, sparql_server


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/recommendations', methods=['GET'])
def get_recommendations():
    course_name = request.args.get('course')

    if not course_name:
        message = "Missing 'course' query param"
        return jsonify({'message': message}), 400

    books = sparql_server.get_course_books(course_name)
    if not books:
        message = 'Invalid course name: {}'.format(course_name)
        return jsonify({'message': message}), 400

    english_books = {book for book in books if book.language == 'en'}
    if english_books:
        book_titles = [book.title for book in english_books]
        recommendations = app.book_recommender.get_recommendations(titles=book_titles)
        books.update(recommendations)

    data = [book.to_json() for book in sorted(books, key=lambda book: book.title)]
    return jsonify({'books': data}), 200
