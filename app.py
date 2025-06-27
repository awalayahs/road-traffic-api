from flask import Flask, render_template, request, send_file, redirect, url_for, session, flash
import pandas as pd
import joblib
import os
from utils import generate_pdf

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Change this to a secure key in production

model = joblib.load('traffic_model.pkl')

columns = [
    'Age_band_of_driver', 'Sex_of_driver', 'Educational_level',
    'Vehicle_driver_relation', 'Driving_experience', 'Lanes_or_Medians',
    'Types_of_Junction', 'Road_surface_type', 'Light_conditions',
    'Weather_conditions', 'Type_of_collision', 'Vehicle_movement',
    'Pedestrian_movement', 'Cause_of_accident'
]

USER_CREDENTIALS = {
    'admin': 'password123'
}

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        uname = request.form['username']
        pwd = request.form['password']
        if USER_CREDENTIALS.get(uname) == pwd:
            session['user'] = uname
            return redirect(url_for('form'))
        else:
            return render_template('login.html', error='Invalid credentials')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    flash('You have been logged out successfully.')
    return redirect(url_for('login'))

@app.route('/form')
def form():
    if 'user' not in session:
        return redirect(url_for('login'))
    return render_template('form.html')

@app.route('/predict', methods=['POST'])
def predict():
    if 'user' not in session:
        return redirect(url_for('login'))

    user_input = [request.form[col] for col in columns]
    df = pd.DataFrame([user_input], columns=columns)

    for col in df.columns:
        df[col] = pd.factorize(df[col])[0]

    prediction = model.predict(df)[0]
    severity_map = {1: 'Low', 2: 'High'}
    result = severity_map.get(prediction, 'Unknown')

    pdf_path = generate_pdf(user_input, result)

    return render_template('dashboard.html', result=result, pdf_link=pdf_path)

@app.route('/download-pdf')
def download_pdf():
    if 'user' not in session:
        return redirect(url_for('login'))
    return send_file("report.pdf", as_attachment=True)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host='0.0.0.0', port=port)
