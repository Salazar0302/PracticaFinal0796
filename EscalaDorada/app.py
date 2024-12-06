import re
from flask import Flask, render_template, request, redirect, flash, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config.from_object('config.Config')

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Modelos
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

class Participant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Función para validar la contraseña
def validar_contraseña(password):
    # Expresión regular para validar contraseña (al menos 8 caracteres, 1 mayúscula, 1 carácter especial)
    if len(password) < 8:
        return False, "La contraseña debe tener al menos 8 caracteres."
    if not re.search(r'[A-Z]', password):  # Al menos una mayúscula
        return False, "La contraseña debe contener al menos una letra mayúscula."
    if not re.search(r'[!@#$%^&*]', password):  # Al menos un carácter especial
        return False, "La contraseña debe contener al menos un carácter especial (como !@#$%^&*)."
    return True, "Contraseña válida."

# Rutas
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        flash('Credenciales incorrectas.')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Validación de la contraseña
        es_valida, mensaje = validar_contraseña(password)
        if not es_valida:
            flash(mensaje)  # Usamos flash para mostrar el mensaje de error
            return render_template('register.html')

        # Si la contraseña es válida, encriptamos y almacenamos el usuario
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, email=email, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    participants = Participant.query.all()
    return render_template('ruleta.html', participants=participants)

@app.route('/add', methods=['POST'])
@login_required
def add_participant():
    name = request.form['name']
    if len(Participant.query.all()) >= 60:
        flash('No se pueden agregar más de 60 nombres.')
    else:
        participant = Participant(name=name)
        db.session.add(participant)
        db.session.commit()
    return redirect('/')

@app.route('/reset')
@login_required
def reset():
    db.session.query(Participant).delete()
    db.session.commit()
    return redirect('/')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
app.run(host="0.0.0.0", port=5000, debug=True)