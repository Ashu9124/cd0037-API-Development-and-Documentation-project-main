import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://postgres@{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_question(self):
        res = self.client().get('/questions?page=1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        # testing since front end errored out
        self.assertIsInstance(data['questions'], list)
        self.assertEqual(len(data['questions']), 10)
    def test_delete_button(self):
        questions_before_del = Question.query.all()
        res = self.client().delete('/questions/2')
        print(res)
        data = json.loads(res.data)
        questions_after_del = Question.query.all()
        # testing db persistence
        self.assertEqual((len(questions_before_del)-len(questions_after_del)), 1)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data['deleted_question'], 2)

    def test_delete_failure(self):
        res = self.client().delete('/questions/1')
        # print(res)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)

    def test_add_feature(self):

        new_question = {
            'id':'24',
            'question': "Who was the man of the series of 2011 ICC cricket world cup ?",
            'answer': "Yuvraj Singh",
            'category': "6",
            'difficulty': "3"}
        res = self.client().post('/questions', json=new_question)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_search(self):
        search_term = {'searchTerm' : "what"}
        res=self.client().post('/questions/search', json=search_term)
        data=json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_search_failure(self):
        search_term = {'searchTerm': "ash"}
        res = self.client().post('/questions/search', json=search_term)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)

    def test_question_by_category(self):
        res = self.client().get('/categories/6/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_question_by_category_failure(self):
        res = self.client().get('/categories/422/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)

    def test_trivia(self):
        trivia_request = {'category': {'id': '3'},
                          'previous_questions':[15,14]
                          }
        res = self.client().post('/quizzes', json=trivia_request)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_trivia_failure(self):
        trivia_request = {
                          'previous_questions':[]
                          }
        res = self.client().post('/quizzes', json=trivia_request)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)


    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """


# Make the tests conveniently executable
if __name__ == "__main__":

    unittest.main()