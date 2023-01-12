from . import api
from .auth import basic_auth, token_auth
from flask import jsonify, request
from app.models import User


@api.route('/token')
@basic_auth.login_required
def get_token():
    user = basic_auth.current_user()
    token = user.get_token()
    return jsonify({'token': token, 'token_expiration': user.token_expiration})



# Get a user by user_id
@api.route('/users/<user_id>')
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())


# Create a new user
@api.route('/users', methods=["POST"])
def create_user():
    # Check to make sure there is a JSON body on the request
    if not request.is_json:
        return jsonify({"error": "Your request content-type must be application/json"}), 400
    # Get data from request
    data = request.json
    # Make sure data has all of the required fields
    for field in ['email', 'username', 'password']:
        if field not in data:
            return jsonify({"error": f"'{field}' must be in request body"}), 400
    # Getting the data from the dictionary
    email = data.get('email')
    username = data.get('username')
    password = data.get('password')
    # Before we add the user to the database, check to see if there is already a user with username or email
    existing_user = User.query.filter((User.email == email) | (User.username == username)).first()
    if existing_user:
        return jsonify({"error": "User with username and/or email already exists"}), 400
    # Create new user with request data
    new_user = User(email=email, username=username, password=password)
    return jsonify(new_user.to_dict()), 201