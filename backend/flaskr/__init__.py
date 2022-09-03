import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


#This paginates the questions(accepts the page request and total selection and returns the current books for that page)
def paginate_questions(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions


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
    # CORS Headers
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
    @app.route('/categories')
    def retrieve_categories():
        category_selection = Category.query.all()        
        categories = [category.format() for category in category_selection]

        if len(categories) == 0:
            abort(404)

        categorydict = {}
        for category in categories:
            categorydict[category['id']] = category['type']
        
        return jsonify (
            {
                "success":True,
                "categories":categorydict
            }
        )
   



    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions."""
    @app.route('/questions')
    def retrieve_questions():
        question_selection = Question.query.all()
        current_questions = paginate_questions(request, question_selection)

        if len(current_questions) == 0:
            abort(404)
        
        category_selection = Category.query.all()
        categories = [category.format() for category in category_selection]

        categorydict = {}
        for category in categories:
            categorydict[category['id']] = category['type']

        print(categorydict)

        if len(current_questions) == 0:
            abort(404)

        return jsonify(
            {
                "success": True,
                "questions": current_questions,
                "totalQuestions":len(question_selection),
                "categories":categorydict,
                "currentCategory": 'Different categories'
            }
        )


    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:questionid>', methods = ["DELETE"])
    def delete_question(questionid):        
        question = Question.query.get(questionid)
        if question:                
            question.delete()
        else:
            abort(404)

        return jsonify(
            {
                "success":True
            }
        )
        






    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route('/questions', methods = ["POST"])
    def add_question():        
        try:
            body = request.get_json()
            question = body.get('question',None)
            answer = body.get('answer',None)
            difficulty = body.get('difficulty',None)
            category = body.get('category',None)
            searchterm = body.get('searchTerm',None)
            
            if searchterm:
                question_selection = Question.query.filter(Question.question.ilike("%{}%".format(searchterm))).all()
                print(question_selection)
                
                current_questions = paginate_questions(request, question_selection)
                return jsonify (
                    {
                        "success": True,
                        "questions":current_questions,
                        "totalQuestions":len(question_selection),
                        "currentCategory":"All categories"
                    }
                )
                

            else:
                new_question = Question(
                    question = question,
                    answer = answer,
                    difficulty = difficulty,
                    category = category
                )

                new_question.insert()

                return jsonify(
                    {
                        "success":True,
                    }
                )
        except:
            abort(422)

    
    """@TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start. """

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<categoryid>/questions')
    def retrieve_questioncategorically(categoryid):                        
        question_selection = Question.query.filter_by(category = categoryid).all()
        print(question_selection)
        current_questions = paginate_questions(request, question_selection)

        if len(current_questions) == 0:
            abort(404)

        currentCategory = Category.query.get(categoryid)
        currentCategory = currentCategory.format()['type']
        
        
        return jsonify(
            {
                "success":True,
                "questions":current_questions,
                'totalQuestions':len(question_selection),
                'currentCategory':currentCategory                
            }
        )





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
    @app.route('/quizzes', methods = ["POST"])
    def retrieve_quizquestions():
        try:
            previous_questions = request.get_json()['previous_questions']
            quiz_category = request.get_json()['quiz_category']

            print(previous_questions)            
            if quiz_category['type'] == 'click':                                                                   
                question_selection = Question.query.all()  
                question = []
                for quest in question_selection:
                    drew = quest.format()
                    question.append(drew)                                
                question = list(filter(lambda x: x['id'] not in previous_questions, question)) 
                question = random.choice(question)
                #question = Question.query.filter(Question.id != 10).first()
            else:
                categoryid = quiz_category['id']                
                question_selection = Question.query.filter_by(category = categoryid).all()
                question = []
                for quest in question_selection:
                    drew = quest.format()
                    question.append(drew)                                
                question = list(filter(lambda x: x['id'] not in previous_questions, question)) 
                if len(question) > 0:
                    question = random.choice(question)
                else:
                    question = None
                                
            return jsonify (
                {
                    'success':True,
                    'question':question
                }
            )
        except:
            abort(422)



    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def not_found(error):
        return jsonify(
            {
                "success":False,
                "error":404,
                "message": "Not found"                
            }
        ),404


    @app.errorhandler(400)
    def bad_request(error):
        return jsonify(
            {
                "success":False,
                "error":400,
                "message": "Bad Request"
            }
        ),400
    
    
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify(
            {
                "success":False,
                "error":422,
                "message": "Unprocessable"
            }
        ),422

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify(
            {
                "success":False,
                "error":405,
                "message": "Method Not Allowed"
            }
        ),405

    return app

