from flask import Flask, render_template, redirect, url_for, flash
from flask_mysqldb import MySQL
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, validators
from wtforms.validators import DataRequired, Length, EqualTo
 
app = Flask(__name__)
app.config['SECRET_KEY'] = 'ddAs242AmVCEH7gebRFEG'


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'client'

mysql = MySQL(app)

class RegisterForm(FlaskForm):
    username = StringField('Nombre de usuario', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Correo electrónico', validators=[DataRequired(), Length(max=50)])
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(min=8, max=50)])
    confirm_password = PasswordField('Confirmar contraseña', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Registrarse')

class LoginForm(FlaskForm):
    email = StringField('Correo electrónico', validators=[DataRequired(), Length(max=50)])
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(min=8, max=50)])
    submit = SubmitField('Iniciar sesión')
                                    

@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        confirm = form.confirm_password.data
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM users WHERE email = %s', [email])
        user = cur.fetchone()
        if user:
            flash('El correo electrónico ya está registrado', 'danger')
            return redirect(url_for('register'))
        elif password != confirm:
            flash('Lo Sentimos pero las contraseñas no coinciden')
            return redirect(url_for('register'))
        else:
            cur.execute('INSERT INTO users(name, email, pas) VALUES(%s, %s, %s)', (username, email, password))
            mysql.connection.commit()
            cur.close()
            flash('Registro exitoso','success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    formu = LoginForm()
    if formu.validate_on_submit():
        email = formu.email.data
        password = formu.password.data
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM users WHERE email = %s AND pas = %s', [email, password])
        user = cur.fetchone()
        if user:
            flash('Inicio de sesión exitoso', 'seguro')
            return redirect(url_for('gracias'))
        else:
            flash('Correo o contraseña invalidos', 'peligro')
            return redirect(url_for('login'))
    return render_template("login.html", formu = formu)

@app.route('/gracias')
def gracias():
    return render_template('gracias.html')

if __name__ == '__main__':
    app.run(debug=True)