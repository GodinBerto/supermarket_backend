from functools import wraps
from flask import redirect, session, url_for, jsonify
from database import db_connection

def get_user_by_id(user_id):
    """Fetch user details by ID from the database."""
    conn, cursor = db_connection()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

def role_required(role=None):
    """Decorator to restrict access based on user roles."""
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            # Check if the user is logged in
            if 'user_id' not in session:
                return jsonify({"message": "User not found"}), 403  # Unauthorized

            # Get user details from the database
            user_id = session['user_id']
            user = get_user_by_id(user_id)

            if not user:
                return jsonify({"message": "User does not exist"}), 404  # Not Found
            
            # Assuming 'role' is the second column (adjust index accordingly)
            role_index = 1  # Change this if the role is in another position
            user_role = user[role_index]

            # Check if the user has the required role
            if role and user_role != role:
                return jsonify({"message": "Unauthorized"}), 401  # Forbidden

            return fn(*args, **kwargs)
        return decorated_view
    return wrapper
