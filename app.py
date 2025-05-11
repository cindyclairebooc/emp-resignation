from flask import Flask, render_template, request
import joblib
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import numpy as np
from datetime import datetime

app = Flask(__name__)

model = joblib.load('voting_clf_model.pkl')

cols_to_one_hot = {
    'Gender': LabelEncoder(),
    'Department': LabelEncoder(),
    'Job_Title': LabelEncoder(),
    'Education_Level': LabelEncoder(),
}

categorical_cols = ['Gender', 'Department', 'Job_Title', 'Education_Level']
numerical_cols = ['Age', 'Performance_Score', 'Monthly_Salary', 'Projects_Handled', 'Sick_Days', 'Remote_Work_Frequency', 'Team_Size', 'Training_Hours', 'Promotions', 'Employee_Satisfaction_Score', 'Tenure', 'Salary_Per_Project', 'Total_Work_Hours', 'Overtime_Ratio']

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/predict', methods=['POST'])
def predict():
    # Extract form inputs
    form = request.form
    try:
        # Construct DataFrame from input (make sure names match the input field names in index.html)
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
            'Work_Hours_Per_Week': float(form['work_hours']),
            'Overtime_Hours': float(form['overtime_hours']),
            'Hire_Date': pd.to_datetime(form['hire_date']),
            'Gender': form['gender'],
            'Department': form['department'],
            'Job_Title': form['job_title'],
            'Education_Level': form['education'],
        }

        df = pd.DataFrame([data])

        # Feature Engineering
        current_date = datetime.now()
        df['Tenure'] = (current_date - df['Hire_Date']).dt.days // 365
        df['Salary_Per_Project'] = df['Monthly_Salary'] / df['Projects_Handled'].replace(0, np.nan)
        df['Total_Work_Hours'] = (df['Work_Hours_Per_Week'] * 52) + df['Overtime_Hours']
        df['Overtime_Ratio'] = df['Overtime_Hours'] / df['Total_Work_Hours'].replace(0, np.nan)

        # Encode categorical variables using the same LabelEncoders
        for col, encoder in cols_to_one_hot.items():
            df[col] = encoder.fit_transform(df[col])  # WARNING: use `.transform()` in production (fit only once on training set)

        # Final feature list
        features = categorical_cols + numerical_cols
        prediction = model.predict(df[features])[0]
        probability = model.predict_proba(df[features])[0][1]

        result = f"Prediction: {'Resigned' if prediction else 'Stayed'} (Probability: {probability:.2f})"
    except Exception as e:
        result = f"Error: {str(e)}"

    return render_template("results.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)