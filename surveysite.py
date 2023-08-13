#WELCOME TO TASK 2 OF WEB DEVELOPMENT!

from flask import Flask, render_template, request, redirect, url_for
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

app = Flask(__name__)

RECAPTCHA_SECRET_KEY = "6LdU86EnAAAAAJg9a9hxzJ_v1xI5AlgdeoTsiOUq"

# Store survey data temporarily in memory
survey_data = {}


@app.route('/')
def index():
    if request.method == 'POST':
        # Store data from page 1
        survey_data['page1_data'] = request.form
        return redirect(url_for('page2'))
    return render_template('page1.html')


@app.route('/page2', methods=['GET', 'POST'])
def page2():
    if request.method == 'POST':
        # Store data from page 1
        survey_data['page1_data'] = request.form
        return redirect(url_for('page2'))
    return render_template('page2.html')


@app.route('/page3', methods=['GET', 'POST'])
def page3():
    if request.method == 'POST':
        # Verify reCAPTCHA response
        recaptcha_response = request.form.get('g-recaptcha-response')
        if verify_recaptcha(recaptcha_response):
            # Store data from page 3
            survey_data['page3_data'] = request.form

            # Save survey data as PDF
            save_survey_as_pdf(survey_data)
            return redirect(url_for('page3'))
        
    return render_template('page3.html')



@app.route('/page4', methods=['GET', 'POST'])
def page4():
       
    return render_template('page4.html')

def verify_recaptcha(response):
    import requests
    recaptcha_verify_url = "https://www.google.com/recaptcha/api/siteverify"
    payload = {
        'secret': RECAPTCHA_SECRET_KEY,
        'response': response
    }
    response = requests.post(recaptcha_verify_url, data=payload)
    result = response.json()
    return result.get('success', False)


def save_survey_as_pdf(data):
    doc = SimpleDocTemplate("survey_data.pdf", pagesize=letter)
    elements = []

    # Create a table with survey data
    table_data = []
    for key, value in data.items():
        table_data.append([key, value])

    table = Table(table_data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    elements.append(table)
    doc.build(elements)


if __name__ == '__main__':
    app.run(debug=True)
