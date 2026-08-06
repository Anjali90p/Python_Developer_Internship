from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory storage for users
users = {
    1: {"name": "Alice Smith", "email": "alice@example.com"},
    2: {"name": "Bob Jones", "email": "bob@example.com"}
}
current_id = 2

@app.route('/users', methods=['GET'])
def get_users():
    """Get all users"""
    return jsonify({"users": users}), 200

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get a specific user by ID"""
    user = users.get(user_id)
    if user:
        return jsonify({"user": user}), 200
    return jsonify({"error": "User not found"}), 404

@app.route('/users', methods=['POST'])
def create_user():
    """Create a new user"""
    global current_id
    data = request.get_json()
    
    if not data or not 'name' in data or not 'email' in data:
        return jsonify({"error": "Please provide both name and email"}), 400
        
    current_id += 1
    new_user = {
        "name": data['name'],
        "email": data['email']
    }
    users[current_id] = new_user
    
    return jsonify({"message": "User created successfully", "user": new_user, "id": current_id}), 201

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """Update an existing user"""
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404
        
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
        
    if 'name' in data:
        users[user_id]['name'] = data['name']
    if 'email' in data:
        users[user_id]['email'] = data['email']
        
    return jsonify({"message": "User updated successfully", "user": users[user_id]}), 200

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete a user"""
    if user_id in users:
        del users[user_id]
        return jsonify({"message": "User deleted successfully"}), 200
    return jsonify({"error": "User not found"}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
