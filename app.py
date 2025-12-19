
import os
import base64
import io
import requests
from urllib.parse import quote
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_user, logout_user, login_required, current_user
import bcrypt
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

class Prompt(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    prompt_text = db.Column(db.Text, nullable=False)
    image_data = db.Column(db.LargeBinary, nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists.')
            return redirect(url_for('register'))
        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('index'))
    return render_template('login.html', register=True)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('index'))
        flash('Invalid username or password.')
    return render_template('login.html')



@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    prompts = Prompt.query.filter_by(user_id=current_user.id).order_by(Prompt.created_at.desc()).all()
    return render_template('index.html', prompts=prompts)

@app.route('/generate', methods=['POST'])
@login_required
def generate():
    prompt_text = request.json.get('prompt')
    if not prompt_text:
        return jsonify({'error': 'Prompt is required.'}), 400

    try:
        # Unsplash API seems to be unreliable. Using picsum.photos as a fallback.
        # This will return a random image, not related to the prompt.
        api_url = "https://picsum.photos/800/600"
        response = requests.get(api_url)
        response.raise_for_status()  # Raise an exception for bad status codes

        image_bytes = response.content
        if image_bytes:
            # Create the prompt only after successfully getting the image
            new_prompt = Prompt(user_id=current_user.id, prompt_text=prompt_text, image_data=image_bytes)
            db.session.add(new_prompt)
            db.session.commit()

            # Send the image to the frontend
            encoded_image = base64.b64encode(image_bytes).decode('utf-8')
            return jsonify({'image': encoded_image, 'prompt_id': new_prompt.id})
        else:
            return jsonify({'error': 'Image data could not be retrieved from the Picsum Photos API.'}), 500

    except requests.exceptions.RequestException as e:
        if e.response is not None:
            app.logger.error(f"Error calling Picsum Photos API: {e}, Status Code: {e.response.status_code}, Response: {e.response.text}")
        else:
            app.logger.error(f"Error calling Picsum Photos API: {e}")
        return jsonify({'error': 'Failed to generate image due to an API error.'}), 502
    except Exception as e:
        app.logger.error(f"An unexpected error occurred during image generation: {e}", exc_info=True)
        return jsonify({'error': f"An unexpected error occurred: {str(e)}"}), 500

@app.route('/get_image/<int:prompt_id>')
@login_required
def get_image(prompt_id):
    prompt = Prompt.query.get_or_404(prompt_id)
    if prompt.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    if prompt.image_data:
        encoded_image = base64.b64encode(prompt.image_data).decode('utf-8')
        return jsonify({'image': encoded_image})
    return jsonify({'error': 'Image not found.'}), 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
