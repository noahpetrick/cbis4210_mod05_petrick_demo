from flask import Blueprint, render_template, request, url_for, redirect, flash
from app.db_connect import get_db
from app.functions import calculate_letter_grade  # Import the function

grades = Blueprint('grades', __name__)

@grades.route('/grade', methods=['GET', 'POST'])
def grade():
    db = get_db()
    cursor = db.cursor()

    # Handle POST request to add a new grade
    if request.method == 'POST':
        number_grade = int(request.form['number_grade'])
        student_name = request.form['student_name']

        # Determine letter grade using the function
        letter_grade = calculate_letter_grade(number_grade)

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
    averaged_grades = [
        (student['student_name'], calculate_letter_grade(student['avg_grade']))
        for student in student_averages
    ]

    return render_template('grades.html', all_grades=averaged_grades)

@grades.route('/update_grade/<int:grade_id>', methods=['GET', 'POST'])
def update_grade(grade_id):
    db = get_db()
    cursor = db.cursor()

    if request.method == 'POST':
        number_grade = int(request.form['number_grade'])
        student_name = request.form['student_name']

        # Determine letter grade using the function
        letter_grade = calculate_letter_grade(number_grade)

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


@grades.route('/update_individual_grade/<int:grade_id>', methods=['GET', 'POST'])
def update_individual_grade(grade_id):
    db = get_db()
    cursor = db.cursor()

    # Fetch current grade information based on grade_id
    cursor.execute('SELECT * FROM grades WHERE grade_id = %s', (grade_id,))
    current_grade = cursor.fetchone()

    # Check if the grade record exists
    if not current_grade:
        flash('Grade record not found.', 'danger')
        return redirect(url_for('grades.view_grades'))

    if request.method == 'POST':
        # Retrieve the updated number grade from the form
        number_grade = int(request.form['number_grade'])

        # Calculate the updated letter grade
        letter_grade = calculate_letter_grade(number_grade)

        # Update the grade in the database
        cursor.execute(
            'UPDATE grades SET letter_grade = %s, number_grade = %s WHERE grade_id = %s',
            (letter_grade, number_grade, grade_id)
        )
        db.commit()
        flash('Grade updated successfully.', 'success')

        # Redirect to the student's grades page
        return redirect(url_for('grades.view_grades', student_name=current_grade['student_name']))

    # Render the form with the current grade information
    return render_template('update_individual_grade.html', current_grade=current_grade)
