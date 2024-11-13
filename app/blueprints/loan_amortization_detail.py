from flask import Blueprint, render_template, request, url_for, redirect, flash
from app.db_connect import get_db
from app.functions import loan_amortization

loan_amortization_detail = Blueprint('loan_amortization_detail', __name__)

@loan_amortization_detail.route('/loan_detail/<int:loan_info_id>')
def loan_detail(loan_info_id):
    db = get_db()
    cursor = db.cursor()

    # Fetch the loan details using the loan_info_id
    cursor.execute('SELECT loan_amount, interest_rate, term_years FROM loan_info WHERE loan_info_id = %s', (loan_info_id,))
    loan_data = cursor.fetchone()

    # print(loan_data)

    # Convert the fetched data to the appropriate types
    loan_amount = float(loan_data['loan_amount'])  # Convert loan_amount from Decimal to float
    interest_rate = float(loan_data['interest_rate'])  # Convert interest_rate from Decimal to float
    loan_term_years = int(loan_data['term_years'])  # Convert loan_term_years to int


    # Get the amortization details
    amortization_schedule = loan_amortization(loan_amount, interest_rate, loan_term_years)

    # Render the loan detail template and pass the amortization schedule
    return render_template('loan_detail.html', loan_schedule=amortization_schedule, loan_id=loan_info_id)