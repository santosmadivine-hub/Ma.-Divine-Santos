from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)

# Sample in-memory data (like a temporary database)
students = [
    {"id": 1, "name": "Divine Santos", "grade": 12, "section": "Zechariah"},
    {"id": 2, "name": "John Cruz", "grade": 11, "section": "Gabriel"}
]

# Dashboard Home Page
@app.route('/')
def home():
    html_page = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>🎓 Student Dashboard</title>
        <style>
            body {
                font-family: 'Segoe UI', sans-serif;
                background: linear-gradient(135deg, #4f8ef7, #6ec9ff);
                color: white;
                text-align: center;
                margin: 0;
                padding: 30px;
            }
            h1 {
                font-size: 2.5em;
                margin-bottom: 10px;
            }
            p {
                font-size: 1.2em;
                margin-bottom: 30px;
            }
            .container {
                background: white;
                color: #333;
                border-radius: 12px;
                padding: 20px;
                width: 90%;
                max-width: 900px;
                margin: auto;
                box-shadow: 0 0 15px rgba(0,0,0,0.2);
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin-bottom: 20px;
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
            input, select {
                padding: 8px;
                border-radius: 6px;
                border: 1px solid #ccc;
                width: 100%;
                margin-bottom: 10px;
            }
            button {
                background: #0077ff;
                color: white;
                border: none;
                padding: 10px 15px;
                border-radius: 6px;
                cursor: pointer;
                margin: 5px;
            }
            button:hover {
                background: #005ccc;
            }
            .form-container {
                text-align: left;
                margin-bottom: 30px;
            }
        </style>
    </head>
    <body>
        <h1>🎓 Student Management Dashboard</h1>
        <p>Manage and register students easily using this Flask-powered dashboard.</p>

        <div class="container">
            <div class="form-container">
                <h3>➕ Register New Student</h3>
                <form id="studentForm">
                    <label>Name:</label>
                    <input type="text" id="name" required>
                    <label>Grade:</label>
                    <input type="number" id="grade" min="1" max="12" required>
                    <label>Section:</label>
                    <input type="text" id="section" required>
                    <button type="submit">Add Student</button>
                </form>
            </div>

            <h3>📋 Student List</h3>
            <table id="studentTable">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Name</th>
                        <th>Grade</th>
                        <th>Section</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody></tbody>
            </table>
            <button onclick="loadStudents()">🔄 Refresh List</button>
        </div>

        <script>
            async function loadStudents() {
                const response = await fetch('/students');
                const data = await response.json();
                const tbody = document.querySelector('#studentTable tbody');
                tbody.innerHTML = '';
                data.data.forEach(student => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${student.id}</td>
                        <td>${student.name}</td>
                        <td>${student.grade}</td>
                        <td>${student.section}</td>
                        <td>
                            <button onclick="deleteStudent(${student.id})">🗑️ Delete</button>
                        </td>
                    `;
                    tbody.appendChild(row);
                });
            }

            document.getElementById('studentForm').addEventListener('submit', async (e) => {
                e.preventDefault();
                const name = document.getElementById('name').value;
                const grade = document.getElementById('grade').value;
                const section = document.getElementById('section').value;

                const response = await fetch('/students', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({name, grade, section})
                });

                const result = await response.json();
                alert(result.message || "Student added!");
                e.target.reset();
                loadStudents();
            });

            async function deleteStudent(id) {
                if (!confirm("Are you sure you want to delete this student?")) return;
                const response = await fetch(`/students/${id}`, { method: 'DELETE' });
                const result = await response.json();
                alert(result.message);
                loadStudents();
            }

            window.onload = loadStudents;
        </script>
    </body>
    </html>
    """
    return render_template_string(html_page)

# API: Get all students
@app.route('/students', methods=['GET'])
def get_students():
    return jsonify({
        "message": "List of all students",
        "data": students
    })

# API: Add new student
@app.route('/students', methods=['POST'])
def add_student():
    data = request.get_json()
    if not data or 'name' not in data or 'grade' not in data or 'section' not in data:
        return jsonify({"error": "Missing required fields"}), 400

    new_id = max([s["id"] for s in students]) + 1 if students else 1
    new_student = {
        "id": new_id,
        "name": data["name"],
        "grade": data["grade"],
        "section": data["section"]
    }
    students.append(new_student)
    return jsonify({"message": "✅ Student added successfully!", "student": new_student}), 201

# API: Delete student
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
    
