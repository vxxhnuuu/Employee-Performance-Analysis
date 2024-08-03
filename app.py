from flask import Flask, render_template, request, redirect, url_for, flash , jsonify
import mysql.connector
import pandas as pd
from collections import Counter
from imblearn.over_sampling import RandomOverSampler
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import os

app = Flask(__name__)
app.secret_key = 'sk'

# Connect to MySQL
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Exynox7510#",
    database="login"
)
mycursor = mydb.cursor()

data = pd.read_csv(r'C:\Users\vishn\Desktop\Projects\Test\output.csv')


@app.route('/')
def login():
    return render_template('login.html')

@app.route('/authenticate', methods=['POST'])
def authenticate():
    userid = request.form['userid']
    password = request.form['password']
    
    # Check if userid and password match
    mycursor.execute("SELECT * FROM user WHERE userid = %s AND password = %s", (userid, password))
    user = mycursor.fetchone()
    
    if user:
        return redirect(url_for('index'))
    else:
        return "Login failed"
    
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/update')
def update():
    return render_template('update.html')


@app.route('/update_data', methods=['GET', 'POST'])
def update_data():
    if request.method == 'POST':
        name = request.form['name']
        age = int(request.form['age'])
        business_travel = int(request.form['business_travel'])
        daily_rate = int(request.form['daily_rate'])
        department = int(request.form['department'])
        distance_from_home = int(request.form['distance_from_home'])
        education = int(request.form['education'])
        education_field = int(request.form['education_field'])
        environment_satisfaction = int(request.form['environment_satisfaction'])
        gender = int(request.form['gender'])
        hourly_rate = int(request.form['hourly_rate'])
        job_involvement = int(request.form['job_involvement'])
        job_level = int(request.form['job_level'])
        job_role = int(request.form['job_role'])
        job_satisfaction = int(request.form['job_satisfaction'])
        marital_status = int(request.form['marital_status'])
        monthly_rate = int(request.form['monthly_rate'])
        num_companies_worked = int(request.form['num_companies_worked'])
        overtime = int(request.form['overtime'])
        percentage_salary_hike = int(request.form['percentage_salary_hike'])
        performance_rating = int(request.form['performance_rating'])
        relationship_satisfaction = int(request.form['relationship_satisfaction'])
        stock_option_level = int(request.form['stock_option_level'])
        total_working_years = int(request.form['total_working_years'])
        training_times_last_year = int(request.form['training_times_last_year'])
        worklife_balance = int(request.form['worklife_balance'])
        years_at_company = int(request.form['years_at_company'])
        years_in_currentrole = int(request.form['years_in_currentrole'])
        years_since_last_promotion = int(request.form['years_since_last_promotion'])
        years_with_current_manager = int(request.form['years_with_current_manager'])

        sql = "INSERT INTO employee_prediction (name, age, business_travel, daily_rate, department, distance_from_home, education, education_field, environment_satisfaction, gender, hourly_rate, job_involvement, job_level, job_role, job_satisfaction, marital_status, monthly_rate, num_companies_worked, overtime, percentage_salary_hike, performance_rating, relationship_satisfaction, stock_option_level, total_working_years, training_times_last_year, worklife_balance, years_at_company, years_in_currentrole, years_since_last_promotion, years_with_current_manager) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        val = (name, age, business_travel, daily_rate, department, distance_from_home, education, education_field, environment_satisfaction, gender, hourly_rate, job_involvement, job_level, job_role, job_satisfaction, marital_status, monthly_rate, num_companies_worked, overtime, percentage_salary_hike, performance_rating, relationship_satisfaction, stock_option_level, total_working_years, training_times_last_year, worklife_balance, years_at_company, years_in_currentrole, years_since_last_promotion, years_with_current_manager)
        mycursor.execute(sql, val)

        mydb.commit()

        return "Data entered successfully"

        return redirect(url_for('index'))

    return render_template('update.html')

@app.route('/view')
def view():
    mycursor.execute("SELECT name, id FROM employee_prediction")
    data = mycursor.fetchall()
    return render_template('view.html', data=data)

@app.route('/test', methods=['POST'])
def test_employee():
    name = request.form['name']
    
    # Fetch data for the employee from your SQL database
    mycursor.execute("SELECT * FROM employee_prediction WHERE name = %s", (name,))
    employee_data = mycursor.fetchone()

    if employee_data is None:
        return "Error: Employee not found"

    new_employee_data = {
        'Age': [employee_data[2]],
        'BusinessTravel': [employee_data[3]],
        'DailyRate': [employee_data[4]],
        'Department': [employee_data[5]],
        'DistanceFromHome': [employee_data[6]],
        'Education': [employee_data[7]],
        'EducationField': [employee_data[8]],
        'EnvironmentSatisfaction': [employee_data[9]],
        'Gender': [employee_data[10]],
        'HourlyRate': [employee_data[11]],
        'JobInvolvement': [employee_data[12]],
        'JobLevel': [employee_data[13]],
        'JobRole': [employee_data[14]],
        'JobSatisfaction': [employee_data[15]],
        'MaritalStatus': [employee_data[16]],
        'MonthlyRate': [employee_data[17]],
        'NumCompaniesWorked': [employee_data[18]],
        'OverTime': [employee_data[19]],
        'PercentSalaryHike': [employee_data[20]],
        'PerformanceRating': [employee_data[21]],
        'RelationshipSatisfaction': [employee_data[22]],
        'StockOptionLevel': [employee_data[23]],
        'TotalWorkingYears': [employee_data[24]],
        'TrainingTimesLastYear': [employee_data[25]],
        'WorkLifeBalance': [employee_data[26]],
        'YearsAtCompany': [employee_data[27]],
        'YearsInCurrentRole': [employee_data[28]],
        'YearsSinceLastPromotion': [employee_data[29]],
        'YearsWithCurrManager': [employee_data[30]],
        'Eligible_for_Promotion': [0]  # Placeholder value since this column is missing from new_df
    }

    new_df = pd.DataFrame(new_employee_data)

    # Check if 'Eligible_for_Promotion' exists in the DataFrame
    if 'Eligible_for_Promotion' in data.columns:
        X = data.drop(['Eligible_for_Promotion', 'Over18', 'EmployeeCount', 'StandardHours','EmployeeNumber','MonthlyIncome'], axis=1)
        y = data['Eligible_for_Promotion'].values

        ros = RandomOverSampler(random_state=42)
        X_resampled, y_resampled = ros.fit_resample(X, y)

        # Assuming X_resampled, y_resampled are already defined
        rf = RandomForestClassifier(random_state=42)
        rf.fit(X_resampled, y_resampled)

        # Ensure new_df has the same columns as X
        new_df = new_df[X.columns]

        prediction = rf.predict(new_df)

        if prediction == 0:
            result = "Not Eligible for Promotion"
        else:
            result = "Eligible for Promotion"

        return render_template('result.html', result=result)
    else:
        return "Error: 'Eligible_for_Promotion' column not found in data DataFrame"
    


if __name__ == '__main__':
    app.run(debug=True)