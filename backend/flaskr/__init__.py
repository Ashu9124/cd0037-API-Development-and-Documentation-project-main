# import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    
    """
    # CORS(app, resources={r"/api/*": {"origins": "*"}})
    CORS(app)
    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Headers', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    # """
    # @TODO:
    # Create an endpoint to handle GET requests
    # for all available categories.
    # """

    @app.route('/categories', methods=['GET'])
    def get_categories():
        # Implement pagination
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * 3
        end = start + 3

        categories = Category.query.all()
        formatted_categories = {
            category.id: category.type for category in categories
        }
        print(categories)
        return jsonify({'success': True,
                        'categories': formatted_categories,
                        'total_categories': len(formatted_categories)}), 200

    @app.route('/questions', methods=['GET'])
    def get_questions():
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * 10
        end = start + 10

        question = Question.query.order_by(Question.id).all()

        if len(question) == 0:
            abort(404)

        formatted_questions = [quest.format() for quest in question]
        # question_categories = Question.category
        categories = Category.query.all()
        formatted_categories = {
              category.id: category.type for category in categories
            }
        return jsonify({'success': True,
                        'questions': formatted_questions[start:end],
                        'total_questions': len(formatted_questions),
                        'categories': formatted_categories,
                        'current_category': "Sport"
                        }), 200

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(Question.id == question_id).all()
            print(question)
            if len(question) == 0:
                abort(422)

            question[0].delete()

        except Exception as e:
            print(e)
            abort(422)

        return jsonify({'success': True,
                        'deleted_question': question_id
                        }), 200

    @app.route('/questions', methods=['POST'])
    def add_question():
        # logic inspired from github/brunogarcia
        try:
            body = request.get_json()
            question = body.get('question', None)
            answer = body.get('answer', None)
            difficulty = body.get('difficulty', None)
            category = body.get('category', None)

            question = Question(
                question=question,
                answer=answer,
                difficulty=difficulty,
                category=category
            )
            question.insert()
        except Exception as e:
            print(e)
            abort(422)

        return jsonify({'success': True,
                        'created_question': question.id
                        }), 200

    @app.route('/questions/search', methods=['POST'])
    def search_question():
        try:
            body = request.get_json()
            term = body.get('searchTerm', None)
            print(term)

            question = Question.query.filter(Question.question.ilike('%{}%'.format(term)))
            print(question)
            questions_formatted = [
                quest.format() for quest in question
            ]
            print(questions_formatted)

            if len(questions_formatted) != 0:
                return jsonify({'success': True,
                                'questions': questions_formatted,
                                'total_questions': len(questions_formatted),
                                'current_category': None
                                }), 200
            else:
                return jsonify({'success': True,
                                'questions': None,

                                }), 200

        except Exception as e:
            print(e)
            abort(422)

    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_by_category_id(category_id):
        try:

            question = Question.query.filter(Question.category == category_id).all()
            questions_formatted = [
                quest.format() for quest in question
            ]
            if len(questions_formatted) != 0:
                return jsonify({'success': True,
                                'categories':category_id,
                                'questions': questions_formatted,
                                'total_questions': len(questions_formatted),
                                'current_category':None
                                }), 200
            else:
                abort(422)

        except Exception as e:
            print(e)
            abort(422)

    @app.route('/quizzes', methods=['POST'])
    def lets_play():
        try:
            body = request.get_json()
            #inspired by github - stenwire/Trivia-API
            category = body.get('quiz_category',None)
            previous_question = body.get('previous_questions',None)
            category_id = category.get('id', None)

            if category_id == 0:
                question = Question.query.filter(Question.id.notin_(previous_question)).all()
            else:
                question = Question.query.filter(Question.id.notin_(previous_question),
                                                 Question.category == category_id).all()

            questions_formatted = [
                quest.format() for quest in question
            ]

            if len(questions_formatted) != 0:
                print(random.choice(questions_formatted))
                return jsonify({'success': True,
                                'category': category_id,
                                'question': random.choice(questions_formatted)
                                }), 200
            else:
                return jsonify({'success': True,
                                'category': category_id,
                                'question': None
                                }), 200

        except Exception as e:
            print(e)
            abort(422)



    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "Resource Not Found"
        }), 404

    @app.errorhandler(422)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "Internal server error"
        }), 422
    return app
