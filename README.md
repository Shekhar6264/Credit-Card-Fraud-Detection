# Credit Card Fraud Detection (Flask + ML + MongoDB)

A machine learning–powered web application for detecting fraudulent credit card transactions.  
Built using **Flask**, **MongoDB**, and **Scikit-Learn** models such as Isolation Forest, SVC, and Logistic Regression.

---

## 🚀 Installation & Setup

### **1. Clone the repository**
```bash
git clone https://github.com/Shekhar6264/Credit-Card-Fraud-Detection.git
cd Credit-Card-Fraud-Detection
2. Set up Python environment
bash
Copy code
python -m venv env
Activate environment
Windows

bash
Copy code
env\Scripts\activate
Mac/Linux

bash
Copy code
source env/bin/activate
3. Install dependencies
bash
Copy code
pip install -r requirements.txt
4. Download the Dataset
The dataset is not included in this repository due to size constraints.

Download from Google Drive:
https://drive.google.com/file/d/1GNxFy8jlTZQLny81XoaYOqfQDQWNFQgh/view?usp=sharing

Place it inside:

kotlin
Copy code
data/
    creditcard.csv
5. Set up MongoDB
Install MongoDB locally or use MongoDB Atlas.

Configure MongoDB connection URI in app.py (or a separate config file):

python
Copy code
MONGO_URI = "mongodb://localhost:27017/fraud_db"
6. Run the application
bash
Copy code
python app.py
or

bash
Copy code
flask run
Your app will be available at:

arduino
Copy code
http://localhost:5000
📁 Project Structure
powershell
Copy code
Credit-Card-Fraud-Detection/
│
├── app.py                # Flask app + ML prediction logic
├── requirements.txt
│
├── templates/            # Frontend HTML templates
├── static/               # CSS and assets
│
├── data/                 # Dataset folder (user must add)
└── models/               # Saved ML models (optional)
🤖 Machine Learning Models
This project uses the following scikit-learn models:

Isolation Forest

Support Vector Classifier (SVC)

Logistic Regression

Libraries Used
nginx
Copy code
pandas
numpy
scikit-learn
Flask
pymongo
bcrypt
werkzeug
🤝 Contributing
Contributions are welcome!
Please fork the repository, make changes, and submit a pull request for any improvements or fixes.
