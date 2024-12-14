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
        # Collect and validate form data
        data = {key: request.form.get(key, '').strip() for key in [
            'age', 'bp', 'sg', 'al', 'su', 'pc', 'pcc', 'ba', 'bgr', 
            'bu', 'sc', 'sod', 'pot', 'hemo', 'pcv', 'wc', 'rc', 
            'htn', 'dm', 'cad', 'pe', 'ane']}

        print("Form Data (Raw):", data)  # Debugging

        # Convert data to numeric values
        try:
            features = np.array([[
                float(data.get('age', 0) or 0),        # Default to 0 if empty
                float(data.get('bp', 0) or 0),
                float(data.get('sg', 0) or 0),
                float(data.get('al', 0) or 0),
                float(data.get('su', 0) or 0),
                float(data.get('pc', 0) or 0),
                1 if data.get('pcc', '').lower() == 'yes' else 0,
                1 if data.get('ba', '').lower() == 'yes' else 0,
                float(data.get('bgr', 0) or 0),
                float(data.get('bu', 0) or 0),
                float(data.get('sc', 0) or 0),
                float(data.get('sod', 0) or 0),
                float(data.get('pot', 0) or 0),
                float(data.get('hemo', 0) or 0),
                float(data.get('pcv', 0) or 0),
                float(data.get('wc', 0) or 0),
                float(data.get('rc', 0) or 0),
                1 if data.get('htn', '').lower() == 'yes' else 0,
                1 if data.get('dm', '').lower() == 'yes' else 0,
                1 if data.get('cad', '').lower() == 'yes' else 0,
                1 if data.get('pe', '').lower() == 'yes' else 0,
                1 if data.get('ane', '').lower() == 'yes' else 0
            ]])
        except ValueError as e:
            raise ValueError(f"Invalid input: {e}")

        print("Features (Converted):", features)  # Debugging

        # Scale features
        scaler = MinMaxScaler((-1, 1))
        scaled_features = scaler.fit_transform(features)
        print("Scaled Features:", scaled_features)  # Debugging

        # Ensure correct shape
        if scaled_features.shape[1] != 22:
            raise ValueError(f"Expected 22 features, but got {scaled_features.shape[1]}.")

        # Make the prediction
        prediction = model.predict(scaled_features)
        print("Raw Prediction:", prediction)  # Debugging

        result = "Have Chronic Kidney Disease" if prediction[0][0] > 0.5 else "Do Not Have Chronic Kidney Disease"

        return render_template("index.html", prediction=result)

    except Exception as e:
        print(f"Error during prediction: {e}")  # Debugging
        return render_template("index.html", prediction="Error processing data. Please check your inputs.")

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
You are a Health Guidance Bot specializing in providing advice and resources related to health. Assist users by answering health-related questions, offering general health insights, and suggesting lifestyle changes or resources to manage their health effectively.
If the user asks something unrelated to health guidance, respond with:
"I'm sorry, I can only assist with health-related guidance."

Here is the conversation history:
{context}

User 's Question: {question}

Your Response:
"""

# Initialize the LLM with the "llama3" model
llm_model = OllamaLLM(model="llama3.2")

# Create a ChatPromptTemplate from the given template
prompt = ChatPromptTemplate.from_template(template)

# List of predefined greetings and responses
greetings = {
    "hello": "Hello! How can I assist you today?",
    "hi": "Hi! How can I help with your health queries?",
    "good morning": "Good morning! What Health-related questions can I help with?",
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
            result = llm_model.invoke(formatted_prompt)

            # Update the context (conversation history)
            context += f"\nUser: {user_input}\nAI: {result}"

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
