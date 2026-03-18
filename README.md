# Task Manager API

A RESTful API built with FastAPI, SQLAlchemy, SQLite, and Pydantic. Features JWT-based authentication.

## Setup Instructions

1.  **Navigate to the project directory:**
    ```bash
    cd task_manager
    ```

2.  **Create a virtual environment:**
    ```bash
    python -m venv venv
    ```

3.  **Activate the virtual environment:**
    -   **Windows:**
        ```powershell
        .\venv\Scripts\activate
        ```
    -   **macOS/Linux:**
        ```bash
        source venv/bin/activate
        ```

4.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Run the application:**
    ```bash
    uvicorn app.main:app --reload
    ```

6.  **Access the API documentation:**
    Open your browser and navigate to `http://127.0.0.1:8000/docs` to use the interactive Swagger UI.

## Features

-   **User Authentication:** Register and login with JWT.
-   **Task Management:** CRUD operations for tasks.
-   **Security:** JWT tokens are required for all task-related endpoints.
-   **Database:** SQLite with SQLAlchemy ORM.
-   **Validation:** Pydantic models for request and response validation.

## API Endpoints

### Authentication
- `POST /register`: Register a new user.
- `POST /token`: Login and get a JWT token.

### Tasks
- `GET /tasks/`: Get all tasks for the logged-in user.
- `POST /tasks/`: Create a new task.
- `GET /tasks/{task_id}`: Get a specific task.
- `PUT /tasks/{task_id}`: Update a task.
- `DELETE /tasks/{task_id}`: Delete a task.
