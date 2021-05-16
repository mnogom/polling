# Polling API

---


---
### Installation
Package was created with poetry.

```commandline
  -- install poetry
% pip3 install --upgrade poetry

  -- clone repo
% git clone https://github.com/mnogom/polling.git
% cd polling

  -- create and setup virtual env
% python3 -m venv .venv
% poetry env use .venv/bin/python
% make install

  -- migrations and migrate
% make migrations
% make migrate

  -- run with manage.py
% make run

  -- setup gunicorn
% source .venv/bin/activate
% export DJANGO_SETTINGS_MODULE=polling_app.settings
% deactivate
  -- run with gunicorn
% make gunicorn-run

  -- run manage.py shell
% make django-shell
```

---
### Usage
#### Admin panel
* Path: /admin
* Description: From admin panel you can create quizzes. 
  Quiz is set of questions. Questions has types: 
  1 - Single choice question, 
  2 - multiple choices questions, 
  3 - Text answer
* TODO: make quiz adding interface easier

#### Quiz references
_look for examples below_
* Path: /api/quizzes/\<str:group>
* Allowed method: GET
* Description: group is keyword "all" or "active"

#### User references
_look for examples below_
1. Create new user
    * Path: /api/user/new
    * Allowed method: POST [type: application/json]
    * Description: create new user
2. Get History of user quizzes
    * Path /api/user/\<int:user_id>/quizzes
    * Allowed method: GET
    * Description: Get users's history of completed quizzes
3. Get Detailed history for user
    * Path: /api/user/\<int:user_id>/quiz/\<int:quiz_id>
    * Allowed method: GET
    * Description: Get user's detailed completed quiz
4. Save user answers for quiz
    * Path: /api/user/\<int:user_id>/save_answers
    * Allowed method: POST
    * Description: Save user's answers for quiz 

---
### Examples
* Example: /api/quizzes/all:
```json
HTTP 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "quizzes": [
        {
            "id": 3,
            "name": "Some old quiz",
            "date_start": "2021-05-02",
            "date_end": "2021-05-13",
            "description": "Nevermind"
        },
        {
            "id": 1,
            "name": "What is your best color?",
            "date_start": "2021-05-13",
            "date_end": "2021-05-24",
            "description": "May be red?"
        },
        {
            "id": 2,
            "name": "Who is Mr. Chechill?",
            "date_start": "2021-05-14",
            "date_end": "2021-05-24",
            "description": "Do you know?"
        },
        {
            "id": 4,
            "name": "Brand new quiz",
            "date_start": "2021-05-31",
            "date_end": "2021-06-30",
            "description": "It will blow your mind"
        }
    ]
}
```
* Example: /api/quizzes/active
```json
HTTP 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "quizzes": [
        {
            "id": 1,
            "name": "What is your best color?",
            "date_start": "2021-05-13",
            "date_end": "2021-05-24",
            "description": "May be red?"
        },
        {
            "id": 2,
            "name": "Who is Mr. Chechill?",
            "date_start": "2021-05-14",
            "date_end": "2021-05-24",
            "description": "Do you know?"
        }
    ]
}
```
* Example: /api/user/new
```json
Post data example

{
  "username": "Sherlock Holmes"
}
```
```json
HTTP 200 OK
Allow: POST, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "detail": "user saved",
    "user_id": 7
}
```
Errors:
```json
HTTP 400 Bad Request
Allow: POST, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "detail": "data must contains \"username\",but it contains ['1']"
}
```
* Example: /api/user/3/quizzes
```json
HTTP 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "quizzes": [
        {
            "id": "1",
            "quiz_text": "What is your best color?"
        },
        {
            "id": "2",
            "quiz_text": "Who is Mr. Chechill?"
        }
    ]
}
```
* Example: /api/user/3/quiz/1
```json
HTTP 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "quiz": {
        "id": 1,
        "name": "What is your best color?",
        "question": [
            {
                "id": 1,
                "text": "Is it red?",
                "choices": [
                    {
                        "id": 1,
                        "text": "red",
                        "answer": "0"
                    },
                    {
                        "id": 2,
                        "text": "green",
                        "answer": "1"
                    }
                ]
            },
            {
                "id": 2,
                "text": "Is it green?",
                "choices": [
                    {
                        "id": 3,
                        "text": "red",
                        "answer": "1"
                    },
                    {
                        "id": 4,
                        "text": "green",
                        "answer": "0"
                    }
                ]
            }
        ]
    }
}
```
Errors:
```json
HTTP 404 Not Found
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "detail": "User 4 didn't complete quiz 1"
}
```
* Example: /api/user/4/save_answers
```json
Post data example

{
  "quiz_id": 2,
  "answers": [
    {
      "choice_id": 5,
      "value": "0"
    },
    {
      "choice_id": 6,
      "value": "1"
    },
    {
      "choice_id": 7,
      "value": "Person"}
  ]
}
```
```json
HTTP 200 OK
Allow: POST, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "detail": "Quiz saved"
}
```
Errors:
```json
HTTP 400 Bad Request
Allow: POST, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "detail": "Keys in data not full"
}
```
```json
HTTP 400 Bad Request
Allow: POST, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "detail": "data[\"answers\"] must be \"list\"but it type is <class 'int'>"
}
```
```json
HTTP 400 Bad Request
Allow: POST, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "detail": "Question ID 3 has only one answer"
}
```
```json
HTTP 400 Bad Request
Allow: POST, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "detail": "User ID not found"
}
```
```json
HTTP 400 Bad Request
Allow: POST, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "detail": "Quiz ID not found"
}
```
```json
HTTP 400 Bad Request
Allow: POST, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "detail": "Data choices IDs doesn't similar with Question choices IDs"
}
```
```json
HTTP 400 Bad Request
Allow: POST, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "detail": "User 4 already pass Quiz 2"
}
```