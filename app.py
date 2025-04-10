from flask import Flask, render_template, request, redirect, url_for, jsonify
import mysql.connector

app = Flask(__name__)

# Database Configuration
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="tiger",
    database="student_db"
)
cursor = db.cursor()

# Login Page
@app.route('/', methods=['GET', 'POST'])
def login():
    print("Login route accessed")  # Debug print
    if request.method == 'POST':
        print("POST request received")  # Debug print
        username = request.form.get('username')
        password = request.form.get('password')
        print(f"Username: {username}, Password: {password}")  # Debug print
        
        try:
            print("Attempting database connection")  # Debug print
            if not db.is_connected():
                print("Reconnecting to database")  # Debug print
                db.reconnect()
                
            print("Executing query")  # Debug print
            cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
            user = cursor.fetchone()
            print(f"Query result: {user}")  # Debug print
            
            if user:
                print("Login successful")  # Debug print
                return redirect(url_for('dashboard.html'))
            else:
                print("Invalid credentials")  # Debug print
                return render_template('login.html', error="Invalid username or password")
        except mysql.connector.Error as err:
            print(f"Database error: {err}")  # Debug print
            return render_template('login.html', error=f"Database error: {err}")
        except Exception as e:
            print(f"General error: {str(e)}")  # Debug print
            return render_template('login.html', error=f"An error occurred: {str(e)}")
    
    return render_template('login.html')

@app.route('/test_db')
def test_db():
    try:
        # Test users table
        cursor.execute("SELECT * FROM users LIMIT 1")
        users = cursor.fetchall()
        
        # Test students table
        cursor.execute("SELECT * FROM students LIMIT 1")
        students = cursor.fetchall()
        
        return jsonify({
            "users_table": bool(users),
            "students_table": bool(students),
            "db_connection": db.is_connected()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Dashboard Route
@app.route('/dashboard')
def dashboard():
    try:
        cursor.execute("SELECT * FROM students")
        students = cursor.fetchall()
        return render_template('dashboard.html', students=students)
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

# Check Registration Number Route
@app.route('/check_reg_number')
def check_reg_number():
    reg_number = request.args.get('reg_number')
    cursor.execute("SELECT * FROM students WHERE reg_number = %s", (reg_number,))
    student = cursor.fetchone()
    return jsonify({"exists": student is not None})

# Add Student Route
@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        reg_number = request.form['reg_number']
        name = request.form['name']
        phone_number = request.form['phone_number']
        course_name = request.form['course_name']
        mentor = request.form['mentor']

        cursor.execute(
            "INSERT INTO students (reg_number, name, phone_number, course_name, mentor) VALUES (%s, %s, %s, %s, %s)",
            (reg_number, name, phone_number, course_name, mentor)
        )
        db.commit()
        return redirect(url_for('dashboard'))
    return render_template('add_student.html')


# Edit Student Route
@app.route('/edit_student/<int:student_id>', methods=['GET', 'POST'])
def edit_student(student_id):
    if request.method == 'POST':
        # Get updated data from the form
        reg_number = request.form['reg_number']
        name = request.form['name']
        phone_number = request.form['phone_number']
        course_name = request.form['course_name']
        mentor = request.form['mentor']

        # Update the student in the database
        cursor.execute(
            "UPDATE students SET reg_number=%s, name=%s, phone_number=%s, course_name=%s, mentor=%s WHERE id=%s",
            (reg_number, name, phone_number, course_name, mentor, student_id)
        )
        db.commit()
        return redirect(url_for('dashboard'))

    # Fetch the selected student's data
    cursor.execute("SELECT * FROM students WHERE id = %s", (student_id,))
    student = cursor.fetchone()
    return render_template('edit_student.html', student=student)

# Delete Student Route
@app.route('/delete_student/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    try:
        print(f"Attempting to delete student with ID: {student_id}")  # Debug print
        cursor.execute("DELETE FROM students WHERE id = %s", (student_id,))
        db.commit()
        print("Student deleted successfully")  # Debug print
        return jsonify({"success": True, "message": "Student deleted successfully"})
    except Exception as e:
        db.rollback()
        print(f"Error deleting student: {e}")  # Debug print
        return jsonify({"success": False, "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)