# Foodkoala

This is a simplified implementation of a food delivery app. Currently, the backend is under development.

## Backend

The web server is written in Python using FastAPI, with SQLModel (which fuses Pydantic with SQLAlchemy) as a data validation and ORM layer.


## Frontend

[Not created yet]


## How to run

1. Create and activate a Python virtual environment:

   ```
   python -m venv .venv
   source .venv/bin/activate
   ```

2. Install the dependencies:

   ```
   pip install -r requirements.txt
   ```

3. Run the development server:

   ```
   fastapi dev app/main.py
   ```
The server will be running at http://127.0.0.1:8000 and the Swagger (OpenAPI) API documentation will be available at http://127.0.0.1:8000/docs.
  
