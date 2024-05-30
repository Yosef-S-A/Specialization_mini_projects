from flask import Flask
from config import Config
from models import db

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

from flask_migrate import Migrate
migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, request, jsonify
from config import Config
from models import db, User

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

from flask_migrate import Migrate
migrate = Migrate(app, db)

@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/users', methods=['POST'])
def create_user():
    username = request.json.get('username')
    email = request.json.get('email')
    if not username or not email:
        return jsonify({'error': 'Missing username or email'}), 400
    
    user = User(username=username, email=email)
    db.session.add(user)
    db.session.commit()
    return jsonify({'id': user.id, 'username': user.username, 'email': user.email}), 201

@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{'id': user.id, 'username': user.username, 'email': user.email} for user in users])

if __name__ == '__main__':
    app.run(debug=True)
