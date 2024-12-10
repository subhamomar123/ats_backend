
# ATS System

## Project Setup

### Requirements
1. Python 3.x
2. Django
3. SQLite (default database)

### Setup Instructions
1. Clone the repository:
   ```
   git clone <repository-url>
   cd ats_backend
   ```
2. Create and activate a virtual environment:
   - For Windows:
     ```
     python -m venv venv
     .env\Scripts\activate
     ```
   - For Linux/macOS:
     ```
     python3 -m venv venv
     source venv/bin/activate
     ```
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Apply migrations:
   ```
   python manage.py migrate
   ```

### Running the Project
1. Start the development server:
   ```
   python manage.py runserver
   ```
2. Open the browser and visit `http://127.0.0.1:8000/` to see the app in action.

### Running Tests
1. To run the tests for the application, use the following command:
   ```
   python manage.py test candidates.tests
   ```

## Project Structure

```
ats_backend/
│   manage.py
│   __init__.py
│
├───ats_system
│   │   asgi.py
│   │   settings.py
│   │   urls.py
│   │   wsgi.py
│   │   __init__.py
│
└───candidates
    │   admin.py
    │   apps.py
    │   models.py
    │   serializers.py
    │   tests.py
    │   urls.py
    │   views.py
    │   __init__.py
    │
    ├───migrations
    │   │   0001_initial.py
    │   │   __init__.py
    │
    ├───tests
    │   │   test_models.py
    │   │   test_views.py
    │   │   __init__.py
    │
    └───__pycache__
        (No pycache files will be listed here)
```

## API Endpoints

### Search Candidates
- **URL:** `/candidates/search/`
- **Method:** `GET`
- **Parameters:** `q=<search_query>`
- **Response:** Returns a list of candidates whose name partially matches the search query.
  - Example query: `?q=Ajay Yadav`
  - Example response: 
  ```json
  [
    {
      "id": 1,
      "name": "Ajay Kumar Yadav",
      "email": "ajay@example.com"
    }
  ]
  ```

### Candidate Creation
- **URL:** `/candidates/create/`
- **Method:** `POST`
- **Body:** 
  ```json
  {
    "name": "New Candidate",
    "email": "newcandidate@example.com",
    "phone": "1234567890"
  }
  ```
- **Response:** Returns the created candidate object.

## Models

### Candidate
Represents a candidate's information.

- **Fields:**
  - `name`: The full name of the candidate.
  - `email`: The email address of the candidate.
  - `phone`: The phone number of the candidate.

## Notes
- SQLite is used as the default database.
- The project includes basic views for searching and creating candidates.

