import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flaskr import create_app
from models import setup_db, Question
from settings import DB_TEST_NAME, DB_PASSWORD, DB_USER


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client

        self.database_path = "postgres://{}:{}@{}/{}".format(
            DB_USER, DB_PASSWORD, 'localhost:5432', DB_TEST_NAME)
        setup_db(self.app, self.database_path)

        self.new_question = {"question":
                             "When did Nigeria gain her independence",
                             "answer": 1960, "category": 4, "difficulty": 2
                             }
        self.search_term = {"searchTerm": "painting"}
        self.new_question_parameter = {"quiz_category": {
            "id": "5"}, "previous_questions": [2]}

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_questions(self):
        res = self.client().get('/questions')

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['categories'], True)
        self.assertTrue(len(data['questions']))

    def test_404_get_questions_beyond_page(self):
        res = self.client().get('/questions?page=1000')
        self.assertEqual(res.status_code, 404)

    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data['categories']))

    def test_405_get_categories(self):
        res = self.client().post('/categories')

        self.assertEqual(res.status_code, 405)

    def test_delete_question(self):
        question = Question.query.all()
        id = question[0].id
        query = '/questions/' + str(id)

        res = self.client().delete(query)
        data = json.loads(res.data)

        question = Question.query.filter_by(id=id)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'], True)
        self.assertTrue(question, None)

    def test_404_delete_question(self):
        res = self.client().delete('/questions/10000')

        self.assertEqual(res.status_code, 404)

    def test_create_questions(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_422_create_questions(self):
        res = self.client().post('/questions')

        self.assertEqual(res.status_code, 422)

    def test_search_questions(self):
        res = self.client().post('/search/questions', json=self.search_term)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_422_search_questions(self):
        res = self.client().post('/search/questions')

        self.assertEqual(res.status_code, 422)

    def test_get_questions_by_category(self):

        res = self.client().get('/categories/3/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

    def test_404_get_questions_by_category(self):
        res = self.client().get('/categories/1000/questions')

        self.assertEqual(res.status_code, 404)

    def test_get_question_for_quiz(self):
        res = self.client().post('/quizzes', json=self.new_question_parameter)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['question'])

    def test_422_get_question_for_quiz_without_parameters(self):
        res = self.client().post('/quizzes')

        self.assertEqual(res.status_code, 422)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
