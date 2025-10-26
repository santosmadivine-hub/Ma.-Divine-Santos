from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample in-memory data (acts like a mini database)
students = [
    {"id": 1, "name": "Ma. Divine Santos", "grade": 12, "section": "Zechariah"},
    {"id": 2, "name": "John Cruz", "grade": 11, "section": "Gabriel"}
]

# Home route
@app.route('/')
def home():
    return "🎓 Welcome to my Enhanced Flask API!"

# GET all students
@app.route('/students', methods=['GET'])
def get_students():
    return jsonify({
        "message": "List of all students",
        "data": students
    })

# GET one student by ID
@app.route('/students/<int:student_id>', methods=['GET'])
def get_student(student_id):
    student = next((s for s in students if s["id"] == student_id), None)
    if student:
        return jsonify({"student": student})
    return jsonify({"error": "Student not found"}), 404

# POST - add a new student
@app.route('/students', methods=['POST'])
def add_student():
    data = request.get_json()
    
    # Validate input
    if not data or 'name' not in data or 'grade' not in data or 'section' not in data:
        return jsonify({"error": "Please include name, grade, and section"}), 400

    new_id = max([s["id"] for s in students]) + 1 if students else 1
    new_student = {
        "id": new_id,
        "name": data["name"],
        "grade": data["grade"],
        "section": data["section"]
    }
    students.append(new_student)
    return jsonify({
        "message": "✅ New student added successfully!",
        "student": new_student
    }), 201

# PUT - update a student by ID
@app.route('/students/<int:student_id>', methods=['PUT'])
def update_student(student_id):
    data = request.get_json()
    student = next((s for s in students if s["id"] == student_id), None)

    if not student:
        return jsonify({"error": "Student not found"}), 404

    student.update({
        "name": data.get("name", student["name"]),
        "grade": data.get("grade", student["grade"]),
        "section": data.get("section", student["section"])
    })
    return jsonify({
        "message": "📝 Student updated successfully!",
        "student": student
    })

# DELETE - remove a student by ID
@app.route('/students/<int:student_id>', methods=['DELETE'])
def delete_student(student_id):
    global students
    student = next((s for s in students if s["id"] == student_id), None)

    if not student:
        return jsonify({"error": "Student not found"}), 404

    students = [s for s in students if s["id"] != student_id]
    return jsonify({"message": "🗑️ Student deleted successfully!"})

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
    
