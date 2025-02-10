from flask import Blueprint, request, jsonify
import sqlite3
import hashlib
from database import db_connection


# Create staff blueprint
staff_bp = Blueprint('staff', __name__)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def get_user_by_email(email):
    conn_users, cursor = db_connection()
    cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
    user = cursor.fetchone()
    conn_users.close()
    return user

# Add new staff
@staff_bp.route('/', methods=['POST'])
def add_staff():
    try:
        data = request.get_json()
        name = data.get("name")
        email = data.get("email")
        password = data.get("password")
        phone = data.get("phone")
        role = data.get("role", "Staff")

        staff = get_user_by_email(email)

        if not all([name, email, password, phone]):
            return jsonify({"error": "All fields are required"}), 400
        
        if staff: 
            return jsonify({"error": "Staff already exists"}), 400
        
        hashed_password = hash_password(password)
        conn, cursor = db_connection()
    
        cursor.execute("INSERT INTO Users (name, email, password, phone, role) VALUES (?, ?, ?, ?, ?)", 
                       (name, email, hashed_password, phone, role))
        conn.commit()
        conn.close()
        return jsonify({"message": "Staff added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
        

# Get all staff
@staff_bp.route('/', methods=['GET'])
def get_all_staff():
    try:
        conn, cursor = db_connection()
        cursor.execute("SELECT * FROM users")
        staff_rows = cursor.fetchall()
        conn.close()

        staff = [dict(row) for row in staff_rows]
        return jsonify(staff)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Get staff by ID
@staff_bp.route('/<int:staff_id>', methods=['GET'])
def get_staff(staff_id):
    try:
        conn = db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, email, phone FROM Users WHERE id = ? AND role = 'Staff'", (staff_id,))
        staff = cursor.fetchone()
        conn.close()
        if staff:
            return jsonify(dict(staff))
        return jsonify({"error": "Staff not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)})

# Update staff
@staff_bp.route('/<int:staff_id>', methods=['PUT'])
def update_staff(staff_id):
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    phone = data.get("phone")
    
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE Users SET name = ?, email = ?, phone = ? WHERE id = ? AND role = 'Staff'", 
                   (name, email, phone, staff_id))
    if cursor.rowcount == 0:
        return jsonify({"error": "Staff not found or no changes made"}), 404
    conn.commit()
    conn.close()
    return jsonify({"message": "Staff updated successfully"})

# Delete staff
@staff_bp.route('/<int:staff_id>', methods=['DELETE'])
def delete_staff(staff_id):
    conn = db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Users WHERE id = ? AND role = 'Staff'", (staff_id,))
    if cursor.rowcount == 0:
        return jsonify({"error": "Staff not found"}), 404
    conn.commit()
    conn.close()
    return jsonify({"message": "Staff deleted successfully"})
