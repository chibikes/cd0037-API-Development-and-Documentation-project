# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createdb trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```
### Set up environmental variables
Create a `.env` file which will be used to load up your database username, password and name

Inside the `.env` file put

```
DB_NAME=<your database name>
DB_USER=<your database username>
DB_PASSWORD=<your database password>
DB_TEST_NAME=<your database used for testing>

```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## To Do Tasks

These are the files you'd want to edit in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle `GET` requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle `GET` requests for all available categories.
4. Create an endpoint to `DELETE` a question using a question `ID`.
5. Create an endpoint to `POST` a new question, which will require the question and answer text, category, and difficulty score.
6. Create a `POST` endpoint to get questions based on category.
7. Create a `POST` endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a `POST` endpoint to get questions to play the quiz. This endpoint should take a category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422, and 500.

## Documenting your Endpoints

You will need to provide detailed documentation of your API endpoints including the URL, request parameters, and the response body. Use the example below as a reference.

### Documentation Example

`GET '/api/v1.0/categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, `categories`, that contains an object of `id: category_string` key: value pairs.

```json
{
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"
}
```
**API DOCUMENTATION**

Getting Started
Base URL: The main url is located at http://127.0.0.1:5000/. Note that this is for development purposes only
Authentication: There are no authentication keys for this api

Error Handling

Errors are returned in the following format:

```json
{
    "success": false,
    "error": 400,
    "message": "bad request"
}
```

The API will return the following error types when requests fail:

- 400: Bad Request
- 404: Resource Not Found
- 405: Method not allowed
- 422: Indicates a non processable request

`GET '/api/v1/questions'`

General:
Returns success value, a list of question objects, total number of questions, and a list of categories
Results are organized in pages, and a page consist of 10 question objects. Include a request argument to
select page number. If no request argument for page number is included it defaults to 1.

Sample Request: curl http://127.0.0.1:5000/questions

Sample Response:

```json 
{
    "questions": [
        {
            "answer":"Maya Angelou",
            "category":4,
            "difficulty":2,
            "id":5,
            "question":"Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        },
        {
            "answer":"Muhammad Ali",
            "category":4,
            "difficulty":1,
            "id":9,
            "question":"What boxer's original name is Cassius Clay?"
        },
        {
            "answer":"Apollo 13",
            "category":5,
            "difficulty":4,
            "id":2,
            "question":"What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        },
        {
            "answer":"Tom Cruise",
            "category":5,
            "difficulty":4,
            "id":4,
            "question":"What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
        },
        {
            "answer":"Edward Scissorhands",
            "category":5,
            "difficulty":3,
            "id":6,
            "question":"What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
        },
        {
            "answer":"Brazil",
            "category":6,
            "difficulty":3,
            "id":10,
            "question":"Which is the only team to play in every soccer World Cup tournament?"
        },
        {
            "answer":"Uruguay",
            "category":6,
            "difficulty":4,
            "id":11,
            "question":"Which country won the first ever soccer World Cup in 1930?"
        },
        {
            "answer":"George Washington Carver",
            "category":4,
            "difficulty":2,
            "id":12,
            "question":"Who invented Peanut Butter?"
        },
        {
            "answer":"Lake Victoria",
            "category":3,
            "difficulty":2,
            "id":13,
            "question":"What is the largest lake in Africa?"
        },
        {
            "answer":"The Palace of Versailles",
            "category":3,
            "difficulty":3,
            "id":14,
            "question":"In which royal palace would you find the Hall of Mirrors?"
        }
    ],
    "categories": [
        "Science",
        "Art",
        "Geography",
        "History",
        "Entertainment",
        "Sports"
    ],
    "success": true,
    "total_questions": 24
}

```
`POST '/api/v1/questions'`

General:
Creates a new question using the provided question ,answer, category, and difficulty. Returns a success value of true if created successfully.

Sample Request:
curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question":"When did Nigeria gain her independence", "answer":"1960", "category": "History", "difficulty":"5"}'

Sample Response:

```json

{
    "success": true
}

```

`DELETE '/api/v1/questions/${question_id}'`

General:
Deletes a question with a given id of question_id. Returns a success value of true if the question was successfully deleted.

Sample Request: curl -X DELETE http://127.0.0.1:5000/questions/1

Sample Response:

```json
{
    "success": true
}

```

`GET '/api/v1/categories'`

General:
Returns a list of categories and a success value of true if no errors encountered

Sample Request: curl http://127.0.0.1:5000/categories

Sample Response:

```json
{
    "categories": [
        "Science",
        "Art",
        "Geography",
        "History",
        "Entertainment",
        "Sports"
    ],
    "success": true,
}

```
`GET '/api/v1/categories/${category_id}/questions'`

General:
Returns a list of questions in a category by using the provided category_id, and returns the total number of questions in that category

Sample Request: curl http://127.0.0.1:5000/categories/5/questions

Sample Response:

```json
{
   "questions": [
    
        {
            "answer":"Tom Cruise",
            "category":5,
            "difficulty":4,
            "id":4,
            "question":"What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
        },
        {
            "answer":"Apollo 13",
            "category":5,
            "difficulty":4,
            "id":2,
            "question":"What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
        }
        
  ],
   "total_questions": 2 
}

```

`POST '/api/v1/search/questions'`

General:
Returns a list of questions based on the provided search term and the total number of questions containing that search term.

Sample Request:
curl http://127.0.0.1:5000/search/questions -X POST -H "Content-Type: application/json" -d '{"searchTerm": "actor"}'

Sample Response:

```json
{
    "questions" [
        {
            "answer":"Tom Cruise",
            "category":5,
            "difficulty":4,
            "id":4,
            "question":"What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
        },
    ],
    "total_questions": 1
}

```
`POST '/api/v1/quizzes'`

General:
Returns a random question based on provided category and a list of ids of previous questions. The question returned is not contained in the list of previous questions provided unless the previous questions' length equals the maximum number of questions available in that category.

Sample Request: 

curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{ "previous_questions": [4,3,8], "category": 4 }'

Sample Response:

```json
{
    "question": {
            "answer":"Muhammad Ali",
            "category":4,
            "difficulty":1,
            "id":9,
            "question":"What boxer's original name is Cassius Clay?"
        },
}

```


## Testing

Write at least one test for the success and at least one error behavior of each endpoint using the unittest library.

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
