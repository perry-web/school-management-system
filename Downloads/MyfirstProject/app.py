from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Sample data (replace with your actual data)
student_list = [
    {"name": "Jennifer", "age": 20, "grades": [90, 85, 75, 100]},
    {"name": "Mac", "age": 20, "grades": [91, 65, 85, 99]},
    {"name": "Miriam", "age": 20, "grades": [95, 80, 99, 100]},
    {"name": "Anderson", "age": 20, "grades": [91.35, 87, 50, 90]},
    {"name": "Glory", "age": 20, "grades": [90.25, 50, 98, 63]},
    {"name": "Berenice", "age": 20, "grades": [92.5, 80, 100, 87]},
]
student_dict = {
    "Jennifer": {"age": 20, "grades": [90, 85, 75, 100]},
    "Mac": {"age": 21, "grades": [91, 65, 85, 99]},
    "Miriam": {"age": 22, "grades": [95, 80, 99, 100]},
    # Add other students similarly
}


def calculate_average(grades):
    return round(sum(grades) / len(grades), 2)


# Route to serve the HTML page
@app.route("/")
def index():
    return render_template("index.html")


# Route to get student data
@app.route("/students", methods=["GET"])
def get_students():
    student_data = [
        {
            "name": student["name"],
            "age": student["age"],
            "grades": ",".join(map(str, student["grades"])),
            "average_grade": calculate_average(student["grades"]),
        }
        for student in student_list
    ]
    return jsonify({"students": student_data})


# Route to add a new student
@app.route("/add_student", methods=["POST"])
def add_student():
    data = request.json
    name = data.get("name")
    age = data.get("age")
    grades = data.get("grades")

    if not all([name, age, grades]):
        return jsonify({"error": "Missing required fields"}), 400

    if name in student_dict:
        return jsonify({"error": "Student already exists"}), 400

    # Add the new student to the list and dictionary
    student_list.append({"name": name, "age": age, "grades": grades})
    student_dict[name] = {"age": age, "grades": grades}

    return jsonify({"message": f"NEW STUDENT {name} WAS ADDED SUCCESSFULLY"})


# Route to update a student
@app.route("/update_student", methods=["PUT"])
def update_student():
    data = request.json
    name = data.get("name")
    age = data.get("age")
    grades = data.get("grades")

    if not all([name, age, grades]):
        return jsonify({"error": "Missing required fields"}), 400

    if name not in student_dict:
        return jsonify({"error": "Student not found"}), 404

    # Update the student in the list and dictionary
    for student in student_list:
        if student["name"] == name:
            student["age"] = age
            student["grades"] = grades
    student_dict[name] = {"age": age, "grades": grades}

    return jsonify({"message": f"STUDENT {name} WAS UPDATED SUCCESSFULLY"})


# Route to delete a student
@app.route("/delete_student", methods=["DELETE"])
def delete_student():
    data = request.json
    name = data.get("name")

    if not name:
        return jsonify({"error": "Missing required fields"}), 400

    if name not in student_dict:
        return jsonify({"error": "Student not found"}), 404

    # Remove the student from the list and dictionary
    student_list = [student for student in student_list if student["name"] != name]
    del student_dict[name]

    return jsonify({"message": f"STUDENT {name} WAS DELETED SUCCESSFULLY"})


if __name__ == "__main__":
    app.run(debug=True)
