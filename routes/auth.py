from flask import Blueprint, request, jsonify
import sqlite3
import hashlib
from database import db_connection

# Create auth blueprint
auth_bp = Blueprint('auth', __name__)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")
        
        if not email or not password:
            return jsonify({"error": "Email and password are required"}), 400
        
        conn, cursor = db_connection()
        cursor.execute("SELECT * FROM Users WHERE email = ? OR password = ?", (email, password))
        user = dict(cursor.fetchone())
        conn.close()
        
        if user and user["password"] == hash_password(password):
            return jsonify({"message": "Login successful", "user": {"id": user["id"], "name": user["name"], "role": user["role"], "email": user["email"]}}), 200
        else:
            return jsonify({"error": "Invalid email or password"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500