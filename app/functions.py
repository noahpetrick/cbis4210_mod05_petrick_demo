def loan_amortization(loan_amount, interest_rate, loan_term_years):
    loan_term_months = loan_term_years * 12  # Convert loan term to months
    monthly_interest_rate = interest_rate / 12 / 100  # Calculate monthly interest rate

    # Calculate the monthly payment
    if monthly_interest_rate > 0:
        monthly_payment = loan_amount * (monthly_interest_rate / (1 - (1 + monthly_interest_rate) ** -loan_term_months))
    else:
        monthly_payment = loan_amount / loan_term_months  # Handle no interest case

    # Create a list to store the loan amortization details
    loan_amortization_list = []

    # Loop to calculate the loan amortization details for each month
    for i in range(1, loan_term_months + 1):
        interest_paid = loan_amount * monthly_interest_rate  # Calculate interest paid for the current month
        principal_paid = monthly_payment - interest_paid  # Calculate principal paid
        remaining_balance = loan_amount - principal_paid  # Calculate remaining balance after payment

        # Append the details for the current month
        loan_amortization_list.append({
            'month': i,
            'starting_balance': loan_amount,
            'interest_paid': interest_paid,
            'principal_paid': principal_paid,
            'monthly_payment': monthly_payment,
            'remaining_balance': remaining_balance
        })

        # Update the loan amount for the next month
        loan_amount = remaining_balance

    return loan_amortization_list

def calculate_letter_grade(number_grade):
    """Calculate the letter grade based on the number grade."""
    if number_grade >= 90:
        return "A"
    elif number_grade >= 80:
        return "B"
    elif number_grade >= 70:
        return "C"
    elif number_grade >= 60:
        return "D"
    else:
        return "you suck"

