from flask import request, jsonify

from app import app, sparql_server


@app.route('/recommendations', methods=['GET'])
def get_recommendations():
    course_name = request.args.get('course')

    if not course_name:
        message = "Missing 'course' query param"
        return jsonify({'message': message}), 400

    books = sparql_server.get_course_books(course_name)
    if not books:
        message = 'Invalid course name.'
        return jsonify({'message': message}), 400

    book_titles = [book['title'] for book in books]
    recommendations = app.book_recommender.get_recommendations(titles=book_titles)
    return jsonify(recommendations), 200
