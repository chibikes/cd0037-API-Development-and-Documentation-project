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

    CORS(app)

    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    @app.route('/categories', methods=['GET'])
    def get_categories():
        categories = Category.query.all()
        formatted_categories = [category.type for category in categories]
        return jsonify({
            "sucess": True,
            "categories": formatted_categories
        })

    @app.route('/questions', methods=['GET'])
    def get_questions():
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE
        questions = Question.query.all()
        categories = Category.query.all()

        formatted_questions = [question.format() for question in questions]
        formatted_categories = [category.type for category in categories]
        if len(formatted_questions[start:end]) == 0:
            abort(404)
        return jsonify({
            "success": True,
            "questions": formatted_questions[start:end],
            "total_questions": len(questions),
            "categories": formatted_categories
        })

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):

        question = Question.query.get(question_id)
        if question is None:
            abort(404)
        else:
            question.delete()
            return jsonify({
                'success': True,
                'id': question_id
            })

    @app.route('/questions', methods=['POST'])
    def create_question():
        try:
            body = request.get_json()
            new_question = body.get('question', None)
            new_answer = body.get('answer', None)
            new_category = body.get('category', None)
            new_difficulty = body.get('difficulty', None)

            question = Question(
                question=new_question,
                answer=new_answer,
                category=new_category,
                difficulty=new_difficulty)
            question.insert()

            return jsonify({
                'success': True,
            })
        except BaseException:
            abort(422)

    @app.route('/search/questions', methods=['POST'])
    def search_questions():
        try:
            search_term = request.get_json().get('searchTerm')

            query_string = 'SELECT * FROM questions WHERE question ILIKE \'%'
            sql = query_string + search_term + '%\''
            result = db.engine.execute(db.text(sql))
            questions = result.fetchall()

            formatted_questions = [{'id': question.id,
                                    'question': question.question,
                                    'answer': question.answer,
                                    'category': question.category,
                                    'difficulty': question.difficulty
                                    } for question in questions]

            return jsonify({
                'success': True,
                'questions': formatted_questions,
                'total_questions': len(formatted_questions)
            })
        except BaseException:
            print(sys.exc_info())
            abort(422)

    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_by_category(category_id):

        current_category = Category.query.get(category_id + 1)
        if current_category is None:
            abort(404)
        else:
            questions = Question.query.filter_by(category=category_id + 1)

            formatted_questions = [question.format() for question in questions]

            return jsonify({
                'questions': formatted_questions,
                'total_questions': len(formatted_questions),

            })

    @app.route('/quizzes', methods=['POST'])
    def get_question_for_quiz():
        try:
            body = request.get_json()
            prev_ques = body.get('previous_questions', None)

            current_category = body.get('quiz_category', None)

            try:
                current_category = int(current_category['id'])
            except BaseException:
                current_category = None

            if current_category is not None:
                questions = Question.query.filter_by(
                    category=current_category).all()
                total_length = len(questions)
            else:
                questions = Question.query.all()
                total_length = len(questions)
            prev_length = len(prev_ques)

            random_numbers = []
            if prev_ques is not None and prev_length < total_length:
                n = random.randint(0, total_length - 1)
                for question in questions:
                    random_numbers.append(n)
                    question = questions[n].format()
                    if question['id'] in prev_ques:
                        while n in random_numbers:
                            n = random.randint(0, total_length - 1)
                        question = questions[n].format()
                    else:
                        break
            elif prev_length >= total_length:
                question = None

            return jsonify({
                'question': question
            })

        except BaseException:
            print(sys.exc_info())

            if body is None:
                abort(422)
            elif total_length == 0:
                abort(404)
            else:
                abort(422)

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
    def bad_request(error):
        return jsonify({
            "Success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "Success": False,
            "error": 405,
            "message": "method not allowed"
        }), 405

    return app
