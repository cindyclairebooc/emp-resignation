from flask import Flask, render_template, request
import joblib
import pandas as pd
import numpy as np
from datetime import datetime

app = Flask(__name__)

model = joblib.load('voting_clf_model.pkl')
emp_feature_columns = joblib.load('emp_feature_columns.pkl')

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/results', methods=['POST'])
def results():
    form = request.form
    try:
        data = {
            'Age': int(form['age']),
            'Performance_Score': float(form['performance_score']),
            'Monthly_Salary': float(form['monthly_salary']),
            'Projects_Handled': int(form['projects_handled']),
            'Sick_Days': int(form['sick_days']),
            'Remote_Work_Frequency': int(form['remote_work']),
            'Team_Size': int(form['team_size']),
            'Training_Hours': float(form['training_hours']),
            'Promotions': int(form['promotions']),
            'Employee_Satisfaction_Score': float(form['satisfaction']),
            'Tenure': int(form['years_at_company']),
            'Overtime_Ratio': float(form['overtime_ratio']),
            'Gender': form['gender'],
            'Department': form['department'],
            'Job_Title': form['job_title'],
            'Education_Level': form['education']
        }

        df = pd.DataFrame([data])
        df['Salary_Per_Project'] = df['Monthly_Salary'] / df['Projects_Handled'].replace(0, np.nan)

        if df['Salary_Per_Project'].isna().any():
            return render_template("results.html", result="Error: Projects Handled must be greater than 0.")

        df = pd.get_dummies(df, columns=['Gender', 'Department', 'Job_Title', 'Education_Level'], drop_first=True)
        df = df.reindex(columns=emp_feature_columns, fill_value=0)

        prediction = model.predict(df)[0]
        probability = model.predict_proba(df)[0][1]

        result = f"Prediction: {'Resigned' if prediction else 'Stayed'} (Probability: {probability:.2f})"
    except Exception as e:
        result = f"Error: {str(e)}"

        print(request.form)

    return render_template("results.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
