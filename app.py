
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = "student-dashboard-secret"

# Temporary storage (No Database)
students = [
    {
        "id": 1,
        "name": "Anu",
        "department": "Biotechnology",
        "marks": 85
    },
    {
        "id": 2,
        "name": "Meera",
        "department": "Computer Science",
        "marks": 72
    },
    {
        "id": 3,
        "name": "Rahul",
        "department": "Mechanical",
        "marks": 35
    }
]


# Dashboard
@app.route('/')
def dashboard():

    total = len(students)

    average = (
        sum(s["marks"] for s in students) / total
        if total else 0
    )

    passed = sum(s["marks"] >= 40 for s in students)
    failed = total - passed

    return render_template(
        "dashboard.html",
        students=students,
        total=total,
        average=round(average, 2),
        passed=passed,
        failed=failed
    )


# Add Student
@app.route('/add', methods=['GET', 'POST'])
def add_student():

    if request.method == 'POST':

        name = request.form['name'].strip()
        department = request.form['department'].strip()

        try:
            marks = float(request.form['marks'])
        except ValueError:
            flash("Enter valid marks!")
            return redirect(url_for('add_student'))

        if not name or not department or not 0 <= marks <= 100:
            flash("Please enter valid student details!")
            return redirect(url_for('add_student'))

        new_student = {
            "id": max((s["id"] for s in students), default=0) + 1,
            "name": name,
            "department": department,
            "marks": marks
        }

        students.append(new_student)

        flash("Student added successfully!")

        return redirect(url_for('dashboard'))

    return render_template('add_student.html')


# Search Student
@app.route('/search')
def search():

    keyword = request.args.get('q', '').lower()

    filtered = [
        s for s in students
        if keyword in s["name"].lower()
    ]

    return render_template(
        "dashboard.html",
        students=filtered,
        total=len(filtered),
        average=round(
            sum(s["marks"] for s in filtered) / len(filtered), 2
        ) if filtered else 0,
        passed=sum(s["marks"] >= 40 for s in filtered),
        failed=sum(s["marks"] < 40 for s in filtered)
    )


# Edit Student
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):

    student = next((s for s in students if s["id"] == id), None)

    if student is None:
        return "Student not found", 404

    if request.method == 'POST':

        name = request.form['name'].strip()
        department = request.form['department'].strip()

        try:
            marks = float(request.form['marks'])
        except ValueError:
            flash("Enter valid marks!")
            return redirect(url_for('edit_student', id=id))

        if not name or not department or not 0 <= marks <= 100:
            flash("Please enter valid details!")
            return redirect(url_for('edit_student', id=id))

        student["name"] = name
        student["department"] = department
        student["marks"] = marks

        flash("Student updated successfully!")

        return redirect(url_for('dashboard'))

    return render_template(
        "add_student.html",
        student=student
    )


# Delete Student
@app.route('/delete/<int:id>', methods=['POST'])
def delete_student(id):

    global students

    students = [s for s in students if s["id"] != id]

    flash("Student deleted successfully!")

    return redirect(url_for('dashboard'))


if __name__ == '__main__':
    app.run(debug=True)
