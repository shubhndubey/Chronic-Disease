# Chronic-Disease
Our project focuses on predicting chronic kidney disease (CKD) using data analysis or machine learning models. The chatbot component can interact with users to provide insights, early detection support, and educational information about CKD, enhancing accessibility and user engagement.
Chronic Kidney Disease Prediction

This project focuses on building a machine learning-based web application to predict chronic kidney disease (CKD). The application uses Neural Network  models to provide accurate predictions. This system is designed to assist users in assessing their risk for CKD and taking preventive or corrective health measures.

Features

Dataset: The dataset used was curated from Kaggle, containing relevant medical and clinical parameters for CKD prediction.

Machine Learning Model: Logistic Regression, SVM, and Random Forest models are employed for robust classification, minimizing errors and improving prediction accuracy.

User-Friendly Interface

Frontend: Built with HTML, CSS, and JavaScript to deliver an interactive and responsive user experience.

Backend: Developed using Flask for lightweight and scalable server-side logic.

SQLite Database: Efficiently stores user inputs and model outputs, seamlessly integrating with the web application.

Multi-Model Support: Allows users to select a preferred model, ensuring flexibility in prediction approaches.

Data Visualization: Key insights, such as feature importance and risk distribution, are presented through interactive graphs and charts.

How It Works

Users provide their medical details (e.g., age, blood pressure, creatinine levels) through an intuitive form on the web application.

The application processes the data and passes it to the selected trained Logistic Regression, SVM, or Random Forest model.

The model returns the CKD risk prediction, displayed in a user-friendly format.

Visual aids help users understand the factors influencing the prediction.

Technology Stack

Frontend: HTML, CSS, JavaScriptBackend: FlaskDatabase: SQLiteMachine Learning: Logistic Regression, Support Vector Machines (SVM), Random Forest

Requirements for the Project

Flask Framework Version: 2.x or higherReason: Leverages modern Flask features for enhanced routing and API integration.

Python Version: 3.10 or higherReason: Ensures compatibility with advanced libraries and features.

Libraries

NumPy: >=1.21.0For numerical operations in machine learning models.

pandas: >=1.3.0For data manipulation and preprocessing.

scikit-learn: >=1.0.0For implementing Logistic Regression, SVM, and Random Forest models.

joblib: >=1.2.0For saving and loading serialized models.

Deployment Requirements

Gunicorn: >=20.0.0

WhiteNoise: >=5.3.0 (for serving static files in production).

Steps or Commands to Run the Project

Download the project zip file and extract it.

Open the extracted folder in VSCode.

Open the terminal in VSCode.

Start the Flask development server by running:

python app.py

Open the provided URL in a browser to access the application.
