# TRIVIA APP

## Setting Up
To use this project python3, pip and node should be installed.
> View the [Backend README](./backend/README.md) for remaining information on setting up and starting the server

## API REFERENCE

### Getting Started
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/` (running flask run where directed in the backend readme should set this up )
- Authentication: This version of the application does not require authentication or API keys. 


### Error Handling
Errors are returned as JSON objects.

The API will return four error types when requests fail and in the following format:
- 400: Bad Request:
```
{
    "success": False, 
    "error": 400,
    "message": "Bad Request"
}
```
- 404: Not Found:
```
{
    "success": False, 
    "error": 404,
    "message": "Not Found"
}
```
- 422: Unprocessable :
```
{
    "success": False, 
    "error": 400,
    "message": "Unprocessable"
}
```
- 405: Method Not Allowed:
```
{
    "success": False, 
    "error": 400,
    "message": "Method Not Allowed"
}
```



### Endpoints

#### GET /categories
 - General:
    - Returns an object containing all available categories
 - Sample: `curl http://127.0.0.1:5000/categories`
 ```
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "success": true
}
```

#### GET /questions
 - General:
    - Returns a list of question objects, total number of questions, a dictionary of all categories, current category and success value.
    - List of question objects returned is paginated in groups of 10, choose a page starting from 1 by including a 'page' argument in your request.
- sample : `curl http://127.0.0.1:5000/questions?page=2`
```
{
  "categories": {
    "1": "Science", 
    "2": "Art", 
    "3": "Geography", 
    "4": "History", 
    "5": "Entertainment", 
    "6": "Sports"
  }, 
  "currentCategory": "Different categories", 
  "questions": [
    {
      "answer": "Agra", 
      "category": "3", 
      "difficulty": 2, 
      "id": 15, 
      "question": "The Taj Mahal is located in which Indian city?"
    }, 
    {
      "answer": "Escher", 
      "category": "2", 
      "difficulty": 1, 
      "id": 16, 
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    }, 
    {
      "answer": "Mona Lisa", 
      "category": "2", 
      "difficulty": 3, 
      "id": 17, 
      "question": "La Giaconda is better known as what?"
    }, 
    {
      "answer": "One", 
      "category": "2", 
      "difficulty": 4, 
      "id": 18, 
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    }, 
    {
      "answer": "Jackson Pollock", 
      "category": "2", 
      "difficulty": 2, 
      "id": 19, 
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    }, 
    {
      "answer": "The Liver", 
      "category": "1", 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }, 
    {
      "answer": "Alexander Fleming", 
      "category": "1", 
      "difficulty": 3, 
      "id": 21, 
      "question": "Who discovered penicillin?"
    }, 
    {
      "answer": "Blood", 
      "category": "1", 
      "difficulty": 4, 
      "id": 22, 
      "question": "Hematology is a branch of medicine involving the study of what?"
    }, 
    {
      "answer": "Scarab", 
      "category": "4", 
      "difficulty": 4, 
      "id": 23, 
      "question": "Which dung beetle was worshipped by the ancient Egyptians?"
    }
  ], 
  "success": true, 
  "totalQuestions": 19
}
```

#### GET /categories/{id}/questions
 - General:
    - Returns a list containing questions objects in the category whose id was specified, the current category which is the category whose id was specified, the total number of questions in the current category and a success value 
    - List of question objects returned is also paginated in groups of 10
- sample : `curl localhost:5000/categories/1/questions`
```
{
  "currentCategory": "Science", 
  "questions": [
    {
      "answer": "The Liver", 
      "category": "1", 
      "difficulty": 4, 
      "id": 20, 
      "question": "What is the heaviest organ in the human body?"
    }, 
    {
      "answer": "Alexander Fleming", 
      "category": "1", 
      "difficulty": 3, 
      "id": 21, 
      "question": "Who discovered penicillin?"
    }, 
    {
      "answer": "Blood", 
      "category": "1", 
      "difficulty": 4, 
      "id": 22, 
      "question": "Hematology is a branch of medicine involving the study of what?"
    }
  ], 
  "success": true, 
  "totalQuestions": 3
}
```

#### POST /quizzes
- General:
    - Returns a new question always whose id isn't in a previous_questions array provided in request body for the quiz, the question is also from a category specified in the request body. Also returns a success value.
- sample : `curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions":[1,4], "quiz_category":{"id":"1", "type":"Science"}}'`
```
{
  "question": {
    "answer": "The Liver", 
    "category": "1", 
    "difficulty": 4, 
    "id": 20, 
    "question": "What is the heaviest organ in the human body?"
  }, 
  "success": true
}
```

#### POST /questions
- General:
    - This creates a new question using the question,answer,category and difficulty submitted in the request body.
    - It however searches for questions instead using the searchterm provided in request body if one is provided.
    - If a new question is created, a success value is returned.
    - If it searches for questions instead it returns a list containing questions in the search result, the total number of questions in the search result, the current category and a success value.
- sample for creating new questions : `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question":"Which club is the best in the world", "answer":"manchester united", "category":"6", "difficulty":"1"}'`
```
{
  "success": true
}
```

- sample for searching questions : `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"searchTerm":"who"}'`
```
{
  "currentCategory": "All categories", 
  "questions": [
    {
      "answer": "George Washington Carver", 
      "category": "4", 
      "difficulty": 2, 
      "id": 12, 
      "question": "Who invented Peanut Butter?"
    }, 
    {
      "answer": "Alexander Fleming", 
      "category": "1", 
      "difficulty": 3, 
      "id": 21, 
      "question": "Who discovered penicillin?"
    }
  ], 
  "success": true, 
  "totalQuestions": 2
}
```

#### DELETE /questions/{id}
- General:
    - Deletes the question with the specified id if it exists, returns a success value.
- Sample : `curl localhost:5000/questions/6 -X DELETE`
```
{
  "success": true
}
```
