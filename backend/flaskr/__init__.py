import os
import sys
from unicodedata import category
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app)
    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response
    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories', methods=['GET'])
    def get_categories():
        categories = Category.query.all()
        formatted_categories = [category.type for category in categories]
        return jsonify({
            "sucess": True,
            "categories" : formatted_categories
        })

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/questions', methods=['GET'])
    def get_questions():
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE
        questions = Question.query.all()
        categories = Category.query.all()

        if len(questions) == 0:
            abort(404)

        formatted_questions = [question.format() for question in questions]
        formatted_categories = [category.type for category in categories]
        return jsonify({
            "success": True,
            "questions" : formatted_questions[start:end],
            "total_questions" : len(questions),
            "categories" : formatted_categories
        })
    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.get(question_id)
            question.delete()
            return jsonify({
                'success': True,
            })
        except:
            abort(404)
    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route('/questions', methods=['POST'])
    def create_question():
        try:
            body = request.get_json()
            new_question = body.get('question', None)
            new_answer = body.get('answer', None)
            new_category = body.get('category', None)
            new_difficulty = body.get('difficulty', None)

            question = Question(question=new_question, answer=new_answer, category=new_category + 1, difficulty=new_difficulty)
            question.insert()

            return jsonify({
                'success': True,
            })
        except:
            abort(422)
    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route('/search', methods=['POST'])
    def search_questions():
        try:
            search_term = request.get_json().get('searchTerm')
            
            sql = 'SELECT * FROM questions WHERE question LIKE \'%' + search_term + '%\''
            result = db.engine.execute(db.text(sql))
            questions = result.fetchall()

            if(questions is None):
                abort(404)

            formatted_questions = [{'id': question.id,
            'question': question.question,
            'answer': question.answer,
            'category': question.category,
            'difficulty': question.difficulty
            } for question in questions]

            print('success')
            return jsonify({
                'success': True,
                'questions' : formatted_questions,
                'total_questions' : len(formatted_questions)
            })
        except:
            print(sys.exc_info())
            abort(422)
    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_by_category(category_id):
        questions = Question.query.filter_by(category=category_id+1)
        formatted_questions = [question.format() for question in questions]
        current_category = Category.query.get(category_id+1)
        return jsonify({
            'questions' : formatted_questions,
            'total_questions' : len(formatted_questions),
            # 'current_category' : current_category.format()
            
        })
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
    @app.route('/quizzes', methods=['POST'])
    def get_questions_to_play():
        body = request.get_json()
        prev_ques = body.get('previous_questions', None)
        category = body.get('quiz_category', None)
        questions = Question.query.all()
        question = questions[0]
        while any(question in prev_ques.question):
            n = random.randint(0, len(questions))
            question = questions[n]

        return jsonify({
            'question' : question
        })
    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "Success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "Success": False,
            "error": 422,
            "message": "cannot process"
        }), 422

    @app.errorhandler(400)
    def unprocessable(error):
        return jsonify({
            "Success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(405)
    def unprocessable(error):
        return jsonify({
            "Success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405

    return app

