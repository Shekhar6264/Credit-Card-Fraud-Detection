import pandas as pd
import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, session, flash
from pymongo import MongoClient
import bcrypt
from sklearn.ensemble import IsolationForest
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from werkzeug.utils import secure_filename

app = Flask(__name__)

# for security purpose
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
        
# Define the directory where uploaded files will be stored
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
# Database
client = MongoClient(MONGO_URI)
db = client['user_database']
collection = db['users']

def format_classification_report(report_str):
    """Convert classification report to properly formatted HTML with monospace font"""
    # Replace multiple spaces with HTML non-breaking spaces and add proper line breaks
    formatted_report = report_str.replace(' ', '&nbsp;').replace('\n', '<br>')
    return formatted_report

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        if collection.find_one({'username': username}):
            session['error'] = "Username already exists!"
            return redirect(url_for('login_page'))
        elif collection.find_one({'email': email}):
            session['error'] = "Email already exists!"
            return redirect(url_for('login_page'))

        user_data = {
            'username': username,
            'password': hashed_password,
            'email': email
        }
        collection.insert_one(user_data)

        return redirect(url_for('login_page'))

    return render_template("login.html")

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    # Handle GET request - show login page
    if request.method == 'GET':
        return render_template("login.html")
    
    # Handle POST request - process login
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Allow dummy login without checking DB
        if username == 'dummy' and password == 'dummy':
            session['username'] = 'Demo User'
            return redirect(url_for('dashboard'))

        user = collection.find_one({'username': username})

        if user and 'password' in user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
            session['username'] = user['username']
            return redirect(url_for('dashboard'))
        else:
            session['error'] = "Invalid username or password"
            return redirect(url_for('login_page'))

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        username = session['username']
        return render_template("dashboard.html", username=username)
    else:
        return redirect(url_for('login_page'))
    
@app.route('/home')
def home():
    if 'username' in session:
        username = session['username']
        return render_template("home.html", username=username)
    else:
        return redirect(url_for('login_page'))
    
@app.route('/admin')
def admin_page():
    if 'username' in session:
        username = session['username']
        return render_template("admin.html", username=username)
    else:
        return redirect(url_for('login_page'))
    

@app.route('/profile')
def profile_page():
    if 'username' in session:
        username = session['username']
        # Fetch user data from the database
        user_data = collection.find_one({'username': username})
        if user_data:
            # Pass user data to the template
            return render_template("profile.html", username=username, user_data=user_data)
        else:
            return "User not found in database"
    else:
        return redirect(url_for('login_page'))


@app.route('/profile/update', methods=['POST'])
def update_profile():
    if 'username' in session:
        username = session['username']
        # Fetch user data from the form
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        organization_name = request.form['organization_name']
        location = request.form['location']
        phone_number = request.form['phone_number']
        birthday = request.form['birthday']
        
        # Update user data in the database
        collection.update_one({'username': username}, {'$set': {
            'first_name': first_name,
            'last_name': last_name,
            'organization_name': organization_name,
            'location': location,
            'phone_number': phone_number,
            'birthday': birthday
        }})
        
        # Redirect to profile page
        return redirect(url_for('profile_page'))
    else:
        return redirect(url_for('login_page'))


@app.route('/predict', methods=['POST'])
def predict():
    if 'username' not in session:
        return redirect(url_for('login_page'))
        
    if 'file' not in request.files:
        flash('No file part', 'error')
        return redirect(url_for('admin_page'))

    file = request.files['file']

    if file.filename == '':
        flash('No selected file', 'error')
        return redirect(url_for('admin_page'))

    try:
        # Assuming the file is a CSV file, you can read it into a DataFrame
        data = pd.read_csv(file)

        # Check if 'Class' column exists
        if 'Class' not in data.columns:
            flash('CSV file must contain "Class" column', 'error')
            return redirect(url_for('admin_page'))

        # Statistical analysis - convert to HTML with proper formatting
        statistical_analysis_html = data.describe().to_html(
            classes='table table-striped table-bordered',
            float_format='%.4f',
            index=True
        )

        # Number of fraudulent and non-fraudulent data points
        fraudulent_count = (data['Class'] == 1).sum()
        non_fraudulent_count = (data['Class'] == 0).sum()

        # Calculate additional statistics
        total_transactions = len(data)
        fraud_percentage = (fraudulent_count / total_transactions) * 100

        # Split the dataset into features and target variable
        X = data.drop(columns=["Class"])
        y = data["Class"]

        # Train Isolation Forest Model
        iso_forest = IsolationForest(random_state=42)
        iso_forest.fit(X)
        iso_forest_predictions = iso_forest.predict(X)
        iso_forest_accuracy = accuracy_score(y, [-1 if pred == -1 else 0 for pred in iso_forest_predictions])
        iso_forest_error = 1 - iso_forest_accuracy
        iso_forest_classification_report = format_classification_report(
            classification_report(y, [-1 if pred == -1 else 0 for pred in iso_forest_predictions])
        )

        # Train SVM Model
        svm_model = SVC(random_state=42)
        svm_model.fit(X, y)
        svm_predictions = svm_model.predict(X)
        svm_accuracy = accuracy_score(y, svm_predictions)
        svm_error = 1 - svm_accuracy
        svm_classification_report = format_classification_report(
            classification_report(y, svm_predictions)
        )

        # Train Logistic Regression Model
        logistic_model = LogisticRegression(random_state=42)
        logistic_model.fit(X, y)
        logistic_predictions = logistic_model.predict(X)
        logistic_accuracy = accuracy_score(y, logistic_predictions)
        logistic_error = 1 - logistic_accuracy
        logistic_classification_report = format_classification_report(
            classification_report(y, logistic_predictions)
        )

        return render_template('admin.html', username=session['username'], 
                               statistical_analysis=statistical_analysis_html,
                               fraudulent_count=fraudulent_count, 
                               non_fraudulent_count=non_fraudulent_count,
                               total_transactions=total_transactions,
                               fraud_percentage=round(fraud_percentage, 4),
                               iso_forest_accuracy=round(iso_forest_accuracy, 4), 
                               iso_forest_error=round(iso_forest_error, 4),
                               iso_forest_classification_report=iso_forest_classification_report,
                               svm_accuracy=round(svm_accuracy, 4), 
                               svm_error=round(svm_error, 4),
                               svm_classification_report=svm_classification_report,
                               logistic_accuracy=round(logistic_accuracy, 4), 
                               logistic_error=round(logistic_error, 4),
                               logistic_classification_report=logistic_classification_report)
    
    except Exception as e:
        flash(f'Error processing file: {str(e)}', 'error')
        return redirect(url_for('admin_page'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('error', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)