from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

app = Flask(__name__)

# Настройки базы данных SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Инициализация SQLAlchemy и Flask-Bcrypt
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Модель пользователя
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    FIO = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)

    @staticmethod
    def hash_password(password):
        """Хеширование пароля"""
        return bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        """Проверка пароля"""
        return bcrypt.check_password_hash(self.password_hash, password)

# Создание таблицы
with app.app_context():
    db.create_all()

# API для получения списка пользователей
@app.route('/api/users', methods=['GET'])
def get_users():
    users = User.query.all()
    users_data = [{"id": u.id, "username": u.username, "FIO": u.FIO, "phone": u.phone} for u in users]
    return jsonify(users_data)

# API для регистрации пользователя
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    FIO = data.get('FIO')
    phone = data.get('phone')

    if not username or not password or not FIO or not phone:
        return jsonify({'error': 'Заполните все поля'}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Пользователь уже существует'}), 400

    if User.query.filter_by(phone=phone).first():
        return jsonify({'error': 'Этот номер уже используется'}), 400

    hashed_password = User.hash_password(password)
    new_user = User(username=username, password_hash=hashed_password, FIO=FIO, phone=phone)
    
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'Пользователь зарегистрирован'}), 201

# API для входа
@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        return jsonify({'message': 'Вход выполнен'}), 200
    return jsonify({'error': 'Неверные учетные данные'}), 401

if __name__ == '__main__':
    app.run(debug=True)
