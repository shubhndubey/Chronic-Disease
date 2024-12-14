# import pickle
# from flask import Flask, request, render_template, redirect, url_for, flash, jsonify
# from flask_sqlalchemy import SQLAlchemy
# from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
# import numpy as np
# from sklearn.preprocessing import MinMaxScaler
# from langchain_ollama import OllamaLLM
# from langchain_core.prompts import ChatPromptTemplate
# import re
# from collections import defaultdict

# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'your_secret_key'  # replace with a strong secret key
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)
# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = 'login'  # redirects to login if not logged in

# # User model
# class User(UserMixin, db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(150), unique=True, nullable=False)
#     password = db.Column(db.String(150), nullable=False)

# # Load user function for Flask-Login
# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))

# @app.route('/')
# def home():
#     return render_template('base.html')

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         user = User.query.filter_by(username=username, password=password).first()
#         if user:
#             login_user(user)
#             return redirect(url_for('index'))  # Redirect to the index page after login
#         else:
#             flash('Invalid credentials, please try again.')
#     return render_template('login.html')

# @app.route('/signup', methods=['GET', 'POST'])
# def signup():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         existing_user = User.query.filter_by(username=username).first()
#         if existing_user is None:
#             user = User(username=username, password=password)
#             db.session.add(user)
#             db.session.commit()
#             login_user(user)
#             return redirect(url_for('index'))  # Redirect to the index page after signup
#         else:
#             flash('Username already exists, please choose another.')
#     return render_template('signup.html')

# @app.route('/index')
# @login_required
# def index():
#     return render_template('index.html')

# # Load the machine learning model using Pickle
# with open('ckdMLmodel.pkl', 'rb') as model_file:
#     model = pickle.load(model_file)


# @app.route("/prediction", methods=["GET", "POST"])
# def predict():
#     if request.method == "POST":
#         try:
#             # Collect form data
#             data = {
#                 'age':request.form.get('age'),
#                 'bp':request.form.get('bp'),
#                 'sg':request.form.get('sg'),
#                 'al':request.form.get('al'),
#                 'su':request.form.get('su'),
#                 'pc':request.form.get('pc'),
#                 'pcc':request.form.get('pcc'),
#                 'ba':request.form.get('ba'),
#                 'bgr':request.form.get('bgr'),
#                 'bu':request.form.get('bu'),
#                 'sc':request.form.get('sc'),
#                 'sod':request.form.get('sod'),
#                 'pot':request.form.get('pot'),
#                 'hemo':request.form.get('hemo'),
#                 'pcv':request.form.get('pcv'),
#                 'wc':request.form.get('wc'),
#                 'rc':request.form.get('rc'),
#                 'htn':request.form.get('htn'),
#                 'dm':request.form.get('dm'),
#                 'cad':request.form.get('cad'),
#                 'pe':request.form.get('pe'),
#                 'ane':request.form.get('ane'),
#             }
#             print("Data is: ", data)
            
#             features = np.array([[
#                 float(data['age']),
#                 float(data['bp']),
#                 float(data['sg']),
#                 float(data['al']),
#                 float(data['su']),
#                 float(data['pc']),
#                 1 if data['pcc'] == 'yes' else 0, 
#                 1 if data['ba'] == 'yes' else 0,                 
#                 float(data['bgr']),
#                 float(data['bu']),
#                 float(data['sc']),
#                 float(data['sod']),
#                 float(data['pot']),
#                 float(data['hemo']),
#                 float(data['pcv']),
#                 float(data['wc']),
#                 float(data['rc']),
#                 1 if data['htn'] == 'yes' else 0,  
#                 1 if data['dm'] == 'yes' else 0,   
#                 1 if data['cad'] == 'yes' else 0, 
#                 1 if data['pe'] == 'yes' else 0,     
#                 1 if data['ane'] == 'yes' else 0,   
#             ]])  

#             scaler = MinMaxScaler((-1, 1))
#             scaled_features = scaler.fit_transform(features)  

            
#             if scaled_features.shape[1] != 22:
#                 raise ValueError(f"Expected 22 features, but got {scaled_features.shape[1]}.")

#             # Make the prediction
#             prediction = model.predict(scaled_features)
#             print(prediction[0][0])
#             if prediction[0][0] > 0.5:
#                 result = "Have Chronic Kidney Disease"
#             else:
#                 result = "Do Not Have Chronic Kidney Disease"

            
#             return render_template("index.html", prediction=str(result))

#         except Exception as e:
#             print(f"Error during prediction: {e}")
#             return render_template("index.html", prediction="Error processing data.")
    
#     return render_template("index.html")

# @app.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     return redirect(url_for('login'))

# template = """
# You are a Health Guidance Bot specializing in providing advice and resources related to health, with a strong emphasis on chronic kidney disease (CKD). Assist users by answering health-related questions, offering insights about CKD , and suggesting lifestyle changes or resources to manage their health effectively.
# If the user asks something unrelated to health guidance or CKD, respond with:
# 'I'm sorry, I can only assist with health-related guidance, specifically chronic kidney disease.'"

# Here is the conversation history:
# {context}

# User 's Question: {question}

# Your Response:
# """
# # Initialize the LLM with the "llama3" model
# model = OllamaLLM(model="llama3.2")

# # Create a ChatPromptTemplate from the given template
# prompt = ChatPromptTemplate.from_template(template)

# # List of predefined greetings and responses
# greetings = {
#     "hello": "Hello! How can I assist you today?",
#     "hi": "Hi! How can I help with your career queries?",
#     "good morning": "Good morning! What CKD-related questions can I help with?",
#     "good afternoon": "Good afternoon! Let me know how I can assist.",
#     "good evening": "Good evening! Feel free to ask your questions.",
#     "good night": "Good night! Let me know if there's something I can help with before you rest."
# }

# @app.route('/chatbot', methods=['GET', 'POST'])
# def chatbot_index():
#     if request.method == 'POST':
#         user_input = request.json.get('user_input')  # Get user input from the frontend
#         context = request.json.get('context', '')  # Get conversation history

#         try:
#             # Prepare the full prompt using the template
#             formatted_prompt = prompt.format(context=context, question=user_input)

#             # Use the model to get a response
#             result = model.invoke(formatted_prompt)

#             # Update the context (conversation history)
#             context += f"\n:User  {user_input}\nAI: {result}"

#             # Return the response as JSON
#             return jsonify({
#                 'response': result,
#                 'context': context
#             })
#         except Exception as e:
#             # Handle errors gracefully and provide feedback to the user
#             return jsonify({
#                 'response': "I'm sorry, something went wrong. Please try again later.",
#                 'context': context
#             })

#     return render_template('chatbot.html')  # Render the frontend page

# @app.route('/contact')
# def contact():
#     return render_template('contact.html')

# @app.route('/about')
# def about():
#     return render_template('about.html')

# if __name__ == "__main__":
#     with app.app_context():
#         db.create_all()  # Ensure database is created
#     app.run(debug=True)




# import pickle
# from flask import Flask, request, render_template, redirect, url_for, flash, jsonify
# from flask_sqlalchemy import SQLAlchemy
# from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
# import numpy as np
# from sklearn.preprocessing import MinMaxScaler
# from langchain_ollama import OllamaLLM
# from langchain_core.prompts import ChatPromptTemplate
# import re
# from collections import defaultdict

# app = Flask(__name__)
# app.config['SECRET_KEY'] = 'your_secret_key'  # replace with a strong secret key
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)
# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = 'login'  # redirects to login if not logged in

# # User model
# class User(UserMixin, db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(150), unique=True, nullable=False)
#     password = db.Column(db.String(150), nullable=False)

# # Load user function for Flask-Login
# @login_manager.user_loader
# def load_user(user_id):
#     return db.session.get(User, int(user_id))  # Updated to use session.get()

# @app.route('/')
# def home():
#     return render_template('base.html')

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         user = User.query.filter_by(username=username, password=password).first()
#         if user:
#             login_user(user)
#             return redirect(url_for('index'))  # Redirect to the index page after login
#         else:
#             flash('Invalid credentials, please try again.')
#     return render_template('login.html')

# @app.route('/signup', methods=['GET', 'POST'])
# def signup():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         existing_user = User.query.filter_by(username=username).first()
#         if existing_user is None:
#             user = User(username=username, password=password)
#             db.session.add(user)
#             db.session.commit()
#             login_user(user)
#             return redirect(url_for('index'))  # Redirect to the index page after signup
#         else:
#             flash('Username already exists, please choose another.')
#     return render_template('signup.html')

# @app.route('/index')
# @login_required
# def index():
#     return render_template('index.html')

# # Load the machine learning model using Pickle
# with open('ckdMLmodel.pkl', 'rb') as model_file:
#     model = pickle.load(model_file)

# @app.route('/prediction', methods=['GET', 'POST'])
# def prediction():
#     if request.method == 'POST':
#         try:
#             # Collect form data
#             data = {
#                 'age': request.form.get('age'),
#                 'bp': request.form.get('bp'),
#                 'sg': request.form.get('sg'),
#                 'al': request.form.get('al'),
#                 'su': request.form.get('su'),
#                 'pc': request.form.get('pc'),
#                 'pcc': request.form.get('pcc'),
#                 'ba': request.form.get('ba'),
#                 'bgr': request.form.get('bgr'),
#                 'bu': request.form.get('bu'),
#                 'sc': request.form.get('sc'),
#                 'sod': request.form.get('sod'),
#                 'pot': request.form.get('pot'),
#                 'hemo': request.form.get('hemo'),
#                 'pcv': request.form.get('pcv'),
#                 'wc': request.form.get('wc'),
#                 'rc': request.form.get('rc'),
#                 'htn': request.form.get('htn'),
#                 'dm': request.form.get('dm'),
#                 'cad': request.form.get('cad'),
#                 'pe': request.form.get('pe'),
#                 'ane': request.form.get('ane'),
#             }
#             print("Data is: ", data)
            
#             features = np.array([[
#                 float(data['age']),
#                 float(data['bp']),
#                 float(data['sg']),
#                 float(data['al']),
#                 float(data['su']),
#                 float(data['pc']),
#                 1 if data['pcc'] == 'yes' else 0, 
#                 1 if data['ba'] == 'yes' else 0,                 
#                 float(data['bgr']),
#                 float(data['bu']),
#                 float(data['sc']),
#                 float(data['sod']),
#                 float(data['pot']),
#                 float(data['hemo']),
#                 float(data['pcv']),
#                 float(data['wc']),
#                 float(data['rc']),
#                 1 if data['htn'] == 'yes' else 0,  
#                 1 if data['dm'] == 'yes' else 0,   
#                 1 if data['cad'] == 'yes' else 0, 
#                 1 if data['pe'] == 'yes' else 0,     
#                 1 if data['ane'] == 'yes' else 0,   
#             ]])  

#             scaler = MinMaxScaler((-1, 1))
#             scaled_features = scaler.fit_transform(features)  

#             if scaled_features.shape[1] != 22:
#                 raise ValueError(f"Expected 22 features, but got {scaled_features.shape[1]}.")

#             # Make the prediction
#             prediction = model.predict(scaled_features)
#             print(prediction[0][0])
#             if prediction[0][0] > 0.5:
#                 result = "Have Chronic Kidney Disease"
#             else:
#                 result = "Do Not Have Chronic Kidney Disease"

#             return render_template("index.html", prediction=str(result))

#         except Exception as e:
#             print(f"Error during prediction: {e}")
#             return render_template("index.html", prediction="Error processing data.")
    
#     return render_template("index.html")

# @app.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     return redirect(url_for('login'))

# template = """
# You are a Health Guidance Bot specializing in providing advice and resources related to health, with a strong emphasis on chronic kidney disease (CKD). Assist users by answering health-related questions, offering insights about CKD, and suggesting lifestyle changes or resources to manage their health effectively.
# If the user asks something unrelated to health guidance or CKD, respond with:
# 'I'm sorry, I can only assist with health-related guidance, specifically chronic kidney disease.'"

# Here is the conversation history:
# {context}

# User 's Question: {question}

# Your Response:
# """

# # Initialize the LLM with the "llama3" model
# model = OllamaLLM(model="llama3.2")

# # Create a ChatPromptTemplate from the given template
# prompt = ChatPromptTemplate.from_template(template)

# # List of predefined greetings and responses
# greetings = {
#     "hello": "Hello! How can I assist you today?",
#     "hi": "Hi! How can I help with your health queries?",
#     "good morning": "Good morning! What CKD-related questions can I help with?",
#     "good afternoon": "Good afternoon! Let me know how I can assist.",
#     "good evening": "Good evening! Feel free to ask your questions.",
#     "good night": "Good night! Let me know if there's something I can help with before you rest."
# }

# @app.route('/chatbot', methods=['GET', 'POST'])
# def chatbot_index():
#     if request.method == 'POST':
#         user_input = request.json.get('user_input')  # Get user input from the frontend
#         context = request.json.get('context', '')  # Get conversation history

#         try:
#             # Prepare the full prompt using the template
#             formatted_prompt = prompt.format(context=context, question=user_input)

#             # Use the model to get a response
#             result = model.invoke(formatted_prompt)

#             # Update the context (conversation history)
#             context += f"\n:User   {user_input}\nAI: {result}"

#             # Return the response as JSON
#             return jsonify({
#                 'response': result,
#                 'context': context
#             })
#         except Exception as e:
#             # Handle errors gracefully and provide feedback to the user
#             return jsonify({
#                 'response': "I'm sorry, something went wrong. Please try again later.",
#                 'context': context
#             })

#     return render_template('chatbot.html')  # Render the frontend page

# @app.route('/contact')
# def contact():
#     return render_template('contact.html')

# @app.route('/about')
# def about():
#     return render_template('about.html')

# if __name__ == "__main__":
#     with app.app_context():
#         db.create_all()  # Ensure database is created
#     app.run(debug=True)


import pickle
from flask import Flask, request, render_template, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with a strong secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Redirects to login if not logged in

# User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

@app.route('/')
def home():
    return render_template('base.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials, please try again.')
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        existing_user = User.query.filter_by(username=username).first()
        if existing_user is None:
            user = User(username=username, password=password)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Username already exists, please choose another.')
    return render_template('signup.html')

@app.route('/index')
@login_required
def index():
    return render_template('index.html')

# Load the machine learning model using Pickle
with open('ckdMLmodel.pkl', 'rb') as model_file:
    model = pickle.load(model_file)

@app.route('/prediction', methods=['POST'])
def prediction():
    try:
        # Collect form data
        data = {key: request.form.get(key) for key in [
            'age', 'bp', 'sg', 'al', 'su', 'pc', 'pcc', 'ba', 'bgr', 
            'bu', 'sc', 'sod', 'pot', 'hemo', 'pcv', 'wc', 'rc', 
            'htn', 'dm', 'cad', 'pe', 'ane']}
        print("Form Data: ", data)  # Debugging

        # Convert data to features
        features = np.array([[float(data['age']),
                              float(data['bp']),
                              float(data['sg']),
                              float(data['al']),
                              float(data['su']),
                              float(data['pc']),
                              1 if data['pcc'] == 'yes' else 0,
                              1 if data['ba'] == 'yes' else 0,
                              float(data['bgr']),
                              float(data['bu']),
                              float(data['sc']),
                              float(data['sod']),
                              float(data['pot']),
                              float(data['hemo']),
                              float(data['pcv']),
                              float(data['wc']),
                              float(data['rc']),
                              1 if data['htn'] == 'yes' else 0,
                              1 if data['dm'] == 'yes' else 0,
                              1 if data['cad'] == 'yes' else 0,
                              1 if data['pe'] == 'yes' else 0,
                              1 if data['ane'] == 'yes' else 0]])

        print("Features: ", features)  # Debugging

        # Scale features
        scaler = MinMaxScaler((-1, 1))
        scaled_features = scaler.fit_transform(features)
        print("Scaled Features: ", scaled_features)  # Debugging

        # Ensure correct shape
        if scaled_features.shape[1] != 22:
            raise ValueError(f"Expected 22 features, but got {scaled_features.shape[1]}.")

        # Make the prediction
        prediction = model.predict(scaled_features)
        print("Raw Prediction: ", prediction)  # Debugging

        result = "Have Chronic Kidney Disease" if prediction[0][0] > 0.5 else "Do Not Have Chronic Kidney Disease"

        return render_template("index.html", prediction=result)

    except Exception as e:
        print(f"Error during prediction: {e}")  # Detailed error output
        return render_template("index.html", prediction="Error processing data.")

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/chatbot')
def chatbot():
    return render_template('chatbot.html')

template = """
You are a Health Guidance Bot specializing in providing advice and resources related to health, with a strong emphasis on chronic kidney disease (CKD). Assist users by answering health-related questions, offering insights about CKD, and suggesting lifestyle changes or resources to manage their health effectively.
If the user asks something unrelated to health guidance or CKD, respond with:
'I'm sorry, I can only assist with health-related guidance, specifically chronic kidney disease.'"

Here is the conversation history:
{context}

User 's Question: {question}

Your Response:
"""

# Initialize the LLM with the "llama3" model
model = OllamaLLM(model="llama3.2")

# Create a ChatPromptTemplate from the given template
prompt = ChatPromptTemplate.from_template(template)

# List of predefined greetings and responses
greetings = {
    "hello": "Hello! How can I assist you today?",
    "hi": "Hi! How can I help with your health queries?",
    "good morning": "Good morning! What CKD-related questions can I help with?",
    "good afternoon": "Good afternoon! Let me know how I can assist.",
    "good evening": "Good evening! Feel free to ask your questions.",
    "good night": "Good night! Let me know if there's something I can help with before you rest."
}

@app.route('/chatbot', methods=['GET', 'POST'])
def chatbot_index():
    if request.method == 'POST':
        user_input = request.json.get('user_input')  # Get user input from the frontend
        context = request.json.get('context', '')  # Get conversation history

        try:
            # Prepare the full prompt using the template
            formatted_prompt = prompt.format(context=context, question=user_input)

            # Use the model to get a response
            result = model.invoke(formatted_prompt)

            # Update the context (conversation history)
            context += f"\n:User   {user_input}\nAI: {result}"

            # Return the response as JSON
            return jsonify({
                'response': result,
                'context': context
            })
        except Exception as e:
            # Handle errors gracefully and provide feedback to the user
            return jsonify({
                'response': "I'm sorry, something went wrong. Please try again later.",
                'context': context
            })

    return render_template('chatbot.html')  # Render the frontend page

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Ensure database is created
    app.run(debug=True)
