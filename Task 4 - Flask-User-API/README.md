# Flask User REST API

A simple RESTful API built with Python and Flask for managing user data.

## Features
- **GET /users**: Retrieve all users
- **GET /users/\<id\>**: Retrieve a specific user
- **POST /users**: Create a new user (requires JSON body with `name` and `email`)
- **PUT /users/\<id\>**: Update an existing user
- **DELETE /users/\<id\>**: Delete a user

## How to Run

1. Ensure Python is installed.
2. Install Flask:
   ```bash
   pip install Flask
   ```
3. Run the application:
   ```bash
   python app.py
   ```
4. The server will start on `http://127.0.0.1:5000`.

## How to Test
You can use **Postman**, **cURL**, or any API testing tool.

**Example cURL Commands:**
- Get all users: `curl -X GET http://127.0.0.1:5000/users`
- Create a user: `curl -X POST http://127.0.0.1:5000/users -H "Content-Type: application/json" -d '{"name": "Charlie", "email": "charlie@example.com"}'`
- Update a user: `curl -X PUT http://127.0.0.1:5000/users/1 -H "Content-Type: application/json" -d '{"name": "Alice Updated"}'`
- Delete a user: `curl -X DELETE http://127.0.0.1:5000/users/2`
