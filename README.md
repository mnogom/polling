# Polling API

---
[![linter-check](https://github.com/mnogom/polling/actions/workflows/linter-check.yml/badge.svg)](https://github.com/mnogom/polling/actions/workflows/linter-check.yml)
[![Maintainability](https://api.codeclimate.com/v1/badges/363d7ad403484bcda165/maintainability)](https://codeclimate.com/github/mnogom/polling/maintainability)

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
% mv .example_env .env

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

#### Quiz references
_look for examples below_
1. Get all quizzes
    * GET /api/quizzes
    * Description: Get list of quizzes. Allow query params: _?group=all_ to get all quizzes 
      or _?group=active_ to get active quizzes. Default: group is "active" 

2. Get detailed quiz by id
    * GET /api/quizzes/\<int:quiz_id>
    * Description: Get detailed quiz by id

#### User references
_look for examples below_
1. Create new user
    * Post [type: application/json] /api/users
    * Description: create new user

2. Get history of user quizzes
    * GET /api/users/\<int:user_id>/quizzes
    * Description: Get users's history of completed quizzes

3. Get detailed history of quiz for user
    * GET /api/users/\<int:user_id>/quizzes/\<int:quiz_id>
    * Description: Get user's detailed completed quiz

4. Save user answers for quiz
    * POST [type: application/json] /api/users/\<int:user_id>/quizzes/\<int:quiz_id>
    * Description: Save user's answers for quiz

---
### TODO
1. Make quiz adding interface easier
2. Add tests
3. Client part

---
### Examples
* GET /api/quizzes and /api/quizzes?group=active:
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
* GET /api/quizzes?group=all
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
* GET /api/quizzes/1
```json
HTTP 200 OK
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "id": 1,
    "name": "What is your best color?",
    "date_start": "2021-05-13",
    "date_end": "2021-05-24",
    "description": "May be red?",
    "questions": [
        {
            "id": 1,
            "text": "Is it red?",
            "type": 1,
            "choices": [
                {
                    "id": 1,
                    "text": "red"
                },
                {
                    "id": 2,
                    "text": "green"
                }
            ]
        },
        {
            "id": 2,
            "text": "Is it green?",
            "type": 2,
            "choices": [
                {
                    "id": 3,
                    "text": "red"
                },
                {
                    "id": 4,
                    "text": "green"
                }
            ]
        }
    ]
}
```
```json
HTTP 404 Not Found
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "detail": "Quiz 23 doesn't exists"
}
```
* POST /api/users
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
```json
HTTP 400 Bad Request
Allow: POST, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "detail": "data must contains \"username\",but it contains ['wrong_key']"
}
```
* GET /api/users/3/quizzes
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
```json
HTTP 400 Bad Request
Allow: GET, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "detail": "User 13 doesn't exists"
}
```
* GET /api/users/3/quizzes/2
```json
HTTP 200 OK
Allow: GET, POST, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "quiz": {
        "id": 2,
        "name": "Who is Mr. Chechill?",
        "question": [
            {
                "id": 3,
                "text": "Do you know?",
                "choices": [
                    {
                        "id": 5,
                        "text": "yes",
                        "answer": "0"
                    },
                    {
                        "id": 6,
                        "text": "no",
                        "answer": "1"
                    }
                ]
            },
            {
                "id": 4,
                "text": "So?",
                "choices": [
                    {
                        "id": 7,
                        "text": "placeholder",
                        "answer": "Person"
                    }
                ]
            }
        ]
    }
}
```
```json
HTTP 400 Bad Request
Allow: GET, POST, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "detail": "User 3 didn't complete quiz 10"
}
```
```json
HTTP 400 Bad Request
Allow: GET, POST, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "detail": "User 100 doesn't exists"
}
```
```json
HTTP 400 Bad Request
Allow: GET, POST, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "detail": "Quiz 10 doesn't exists"
}
```
* POST /api/users/7/quizzes/2
```json
Post data example

{
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
      "value": "British statesman and politician"}
  ]
}
```
```json
HTTP 200 OK
Allow: GET, POST, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "detail": "Quiz saved"
}
```
```json
HTTP 400 Bad Request
Allow: GET, POST, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "detail": "User 7 already pass Quiz 2"
}
```
```json
HTTP 400 Bad Request
Allow: GET, POST, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "detail": "Keys in data not full"
}
```
```json
HTTP 400 Bad Request
Allow: GET, POST, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "detail": "Data choices IDs doesn't similar with Question choices IDs"
}
```
```json
HTTP 400 Bad Request
Allow: GET, POST, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "detail": "data[\"answers\"] must be \"list\"but it type is <class 'int'>"
}
```
```json
HTTP 400 Bad Request
Allow: GET, POST, HEAD, OPTIONS
Content-Type: application/json
Vary: Accept

{
    "detail": "Question ID 3 has only one answer"
}
```