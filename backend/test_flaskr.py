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
        self.database_path = 'postgresql://postgres:abc@localhost:5432/trivia_test'
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


    def test_retrieve_categories(self):
        response = self.client().get("/categories")
        data = json.loads(response.data)

        self.assertEqual(response.status_code,200)
        self.assertTrue(data["categories"])
        self.assertIsInstance(data["categories"], dict)    


    def test_retrieve_questions(self):
        response = self.client().get("/questions")
        data = json.loads(response.data)

        self.assertEqual(response.status_code,200)
        self.assertEqual(data["success"],True)
        self.assertTrue(data["questions"])
        self.assertTrue(data["totalQuestions"])
        self.assertTrue(data["categories"])
        self.assertTrue(data["currentCategory"])


    def test_retrieve_questions_failure_requesting_over_total_pages(self):
        response = self.client().get("/questions?page=50")
        data = json.loads(response.data)

        self.assertEqual(data["success"],False)
        self.assertEqual(data["message"],"Not found")
        self.assertEqual(response.status_code,404)

    def test_retrieve_questions_categorically(self):
        response = self.client().get("/categories/2/questions")
        data = json.loads(response.data)

        self.assertEqual(response.status_code,200)
        self.assertEqual(data["success"],True)
        self.assertTrue(data["questions"])
        self.assertTrue(data["totalQuestions"])        
        self.assertTrue(data["currentCategory"])

    def test_retrieve_questions_categorically_failure_requesting_unexisting_categories(self):
        response = self.client().get("categories/10/questions")
        data = json.loads(response.data)

        self.assertEqual(data["success"],False)
        self.assertEqual(data["message"],"Not found")
        self.assertEqual(response.status_code,404)


    def test_retrieve_quiz_questions(self):
        response = self.client().post("/quizzes", json = {"previous_questions":[5,4,3],"quiz_category":{"type":"science", "id":"1"}})
        data = json.loads(response.data)

        self.assertEqual(response.status_code,200)
        self.assertEqual(data["success"],True)
        self.assertTrue(data["question"])

    def test_retrieve_quiz_questions_failure_no_data_provided(self):
        response = self.client().post("/quizzes")
        data = json.loads(response.data)
        
        self.assertEqual(data["success"],False)
        self.assertEqual(data["message"],"Unprocessable")
        self.assertEqual(response.status_code,422)


    #This was commented out after initial test as the question with the id was deleted in the initial test
    '''def test_delete_questions(self):
        response = self.client().delete("/questions/10")
        data = json.loads(response.data)

        self.assertEqual(response.status_code,200)
        self.assertEqual(data["success"],True)'''

    def test_delete_questions_failure_invalid_questionid(self):
        response = self.client().delete("/questions/45")
        data = json.loads(response.data)

        self.assertEqual(data["success"],False)
        self.assertEqual(data["message"],"Not found")
        self.assertEqual(response.status_code,404)



    def test_add_new_question(self):
        response = self.client().post("/questions", json = {
        "question":"Which club is the best in the world",
        "answer":"manchester united",
        "difficulty":"1",
        "category":"6"
        })
        data = json.loads(response.data)

        self.assertEqual(response.status_code,200)
        self.assertEqual(data["success"],True)

    def test_search_questions(self):
        response = self.client().post("/questions", json = { "searchTerm":"who"})
        data = json.loads(response.data)

        self.assertEqual(response.status_code,200)
        self.assertEqual(data["success"],True)
        self.assertTrue(data["questions"])
        self.assertTrue(data["totalQuestions"])        
        self.assertTrue(data["currentCategory"])

    def test_search_questions_without_result(self):
        response = self.client().post("/questions", json = { "searchTerm":"abcdefghighijjsak"})
        data = json.loads(response.data)

        self.assertEqual(response.status_code,200)
        self.assertEqual(data["success"],True)
        self.assertEqual(len(data["questions"]),0)
        self.assertEqual(data["totalQuestions"],0)                

    def test_add_new_question_and_search_question_failure_no_data_provided(self):
        response = self.client().post("/questions")
        data = json.loads(response.data)
        
        self.assertEqual(data["success"],False)
        self.assertEqual(data["message"],"Unprocessable")
        self.assertEqual(response.status_code,422)





# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()