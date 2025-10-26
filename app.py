from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)

# Sample in-memory data (acts like a mini database)
students = [
    {"id": 1, "name": "Divine Santos", "grade": 12, "section": "Zechariah"},
    {"id": 2, "name": "John Cruz", "grade": 11, "section": "Gabriel"}
]

# Home route - HTML + Live student table
@app.route('/')
def home():
    html_page = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>🎓 Student Management API</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #4f8ef7, #6ec9ff);
                color: white;
                text-align: center;
                margin: 0;
                padding: 40px;
            }
            h1 {
                font-size: 2.5em;
                margin-bottom: 10px;
            }
            p {
                font-size: 1.2em;
            }
            table {
                margin: 30px auto;
                border-collapse: collapse;
                width: 80%;
                background: white;
                color: #333;
                border-radius: 10px;
                overflow: hidden;
                box-shadow: 0 0 10px rgba(0,0,0,0.2);
            }
            th, td {
                padding: 12px;
                border-bottom: 1px solid #ddd;
            }
            th {
                background-color: #0077ff;
                color: white;
            }
            tr:hover {
                background-color: #f2f2f2;
            }
            button {
                background: #0077ff;
                color: white;
                border: none;
                padding: 8px 14px;
                border-radius: 6px;
                cursor: pointer;
                margin: 10px;
            }
            button:hover {
                background: #005ccc;
            }
        </style>
    </head>
    <body>
        <h1>🎓 Student Management API</h1>
        <p>Below is a live table showing all students from the API:</p>

        <table id="studentTable">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Grade</th>
                    <th>Section</th>
                </tr>
            </thead>
            <tbody></tbody>
        </table>

        <button onclick="loadStudents()">🔄 Refresh List</button>

        <script>
            async function loadStudents() {
                const response = await fetch('/students');
                const data = await response.json();
                const tbody = document.querySelector('#studentTable tbody');
                tbody.innerHTML = ''; // Clear old rows

                data.data.forEach(student => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${student.id}</td>
                        <td>${student.name}</td>
                        <td>${student.grade}</td>
                        <td>${student.section}</td>
                    `;
                    tbody.appendChild(row);
                });
            }

            // Load data on page load
            window.onload = loadStudents;
        </script>
    </body>
    </html>
    """
    return render_template_string(html_page)

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
    
