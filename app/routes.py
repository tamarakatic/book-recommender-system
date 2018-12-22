from flask import request, jsonify

from app import app, sparql_server


@app.route('/recommendations', methods=['GET'])
def get_recommendations():
    course_name = request.args.get('course')

    if not course_name:
        message = "Missing 'course' query param"
        return jsonify({'message': message}), 400

    books = sparql_server.get_course_books(course_name)
    return jsonify(books), 200
