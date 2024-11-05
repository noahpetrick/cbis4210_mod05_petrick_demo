from flask import Blueprint, render_template, request, url_for, redirect, flash
from app.db_connect import get_db

grades = Blueprint('grades', __name__)

@grades.route('/grade', methods=['GET', 'POST'])
def grade():
    db = get_db()
    cursor = db.cursor()

    # Handle POST request to add a new grade
    if request.method == 'POST':
        number_grade = int(request.form['number_grade'])
        student_name = request.form['student_name']

        # Determine letter grade
        if number_grade >= 90:
            letter_grade = "A"
        elif number_grade >= 80:
            letter_grade = "B"
        elif number_grade >= 70:
            letter_grade = "C"
        elif number_grade >= 60:
            letter_grade = "D"
        else:
            letter_grade = "you suck"

        # Insert the new grade into the database
        cursor.execute(
            'INSERT INTO grades (letter_grade, student_name, number_grade) VALUES (%s, %s, %s)',
            (letter_grade, student_name, number_grade)
        )
        db.commit()
        return redirect(url_for('grades.grade'))

    # Retrieve average grade per student
    cursor.execute('SELECT student_name, AVG(number_grade) AS avg_grade FROM grades GROUP BY student_name')
    student_averages = cursor.fetchall()

    # Calculate letter grades based on the average number grades
    averaged_grades = []
    for student in student_averages:
        avg_grade = student['avg_grade']
        if avg_grade >= 90:
            letter_grade = "A"
        elif avg_grade >= 80:
            letter_grade = "B"
        elif avg_grade >= 70:
            letter_grade = "C"
        elif avg_grade >= 60:
            letter_grade = "D"
        else:
            letter_grade = "you suck"

        # Append each student with their calculated letter grade
        averaged_grades.append((student['student_name'], letter_grade))

    return render_template('grades.html', all_grades=averaged_grades)

@grades.route('/update_grade/<int:grade_id>', methods=['GET', 'POST'])
def update_grade(grade_id):
    db = get_db()
    cursor = db.cursor()

    if request.method == 'POST':
        number_grade = request.form['number_grade']
        student_name = request.form['student_name']
        number_grade = int(number_grade)

        if number_grade >= 90:
            letter_grade = "A"
        elif number_grade >= 80:
            letter_grade = "B"
        elif number_grade >= 70:
            letter_grade = "C"
        elif number_grade >= 60:
            letter_grade = "D"
        else:
            letter_grade = "you suck"

        cursor.execute(
            'UPDATE grades SET letter_grade = %s, student_name = %s, number_grade = %s WHERE grade_id = %s',
            (letter_grade, student_name, number_grade, grade_id)
        )
        db.commit()
        return redirect(url_for('grades.grade'))

    cursor.execute('SELECT * FROM grades WHERE grade_id = %s', (grade_id,))
    current_grade = cursor.fetchone()
    return render_template('update_grade.html', current_grade=current_grade)

@grades.route('/delete_grade/<string:student_name>', methods=['POST'])
def delete_grade(student_name):
    db = get_db()
    cursor = db.cursor()

    # Delete all grades for the given student name
    cursor.execute('DELETE FROM grades WHERE student_name = %s', (student_name,))
    db.commit()
    return redirect(url_for('grades.grade'))

@grades.route('/view_grades/<string:student_name>', methods=['GET', 'POST'])
def view_grades(student_name):
    db = get_db()
    cursor = db.cursor()

    # Fetch individual grades for the selected student
    cursor.execute('SELECT grade_id, number_grade, letter_grade FROM grades WHERE student_name = %s', (student_name,))
    student_grades = cursor.fetchall()

    return render_template('view_grades.html', student_grades=student_grades, student_name=student_name)

@grades.route('/delete_individual_grade/<int:grade_id>', methods=['POST'])
def delete_individual_grade(grade_id):
    db = get_db()
    cursor = db.cursor()

    # Delete the specific grade by grade_id
    cursor.execute('DELETE FROM grades WHERE grade_id = %s', (grade_id,))
    db.commit()
    flash('Grade deleted successfully.', 'success')
    return redirect(url_for('grades.grade'))
