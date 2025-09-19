from flask import Flask, render_template, session, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, PasswordField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Chave forte'
bootstrap = Bootstrap(app)
moment = Moment(app)

class NameForm(FlaskForm):
    name = StringField('Informe o seu nome:', validators = [DataRequired()])
    last_name = StringField("Informe o seu sobrenome:", validators = [DataRequired()])
    institution = StringField("Informe a sua Instituição e Ensino:", [DataRequired()])
    course = SelectField("Informe a sua Disciplina:", choices=["DSWA5", "DWBA4", "Gestão de Projetos"])
    submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    username = StringField(validators = [DataRequired()])
    password = PasswordField(validators = [DataRequired()])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def main():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Você alterou o seu nome.')
        session['name'] = form.name.data
        session['last_name'] = form.last_name.data
        session['institution'] = form.institution.data
        session['course'] = form.course.data
        return redirect(url_for('index'))
    remote_addr = request.remote_addr
    host = request.host
    print("Sessão atual: ", dict(session))
    return render_template('index.html', form=form, name=session.get('name'), last_name=session.get('last_name'), institution=session.get('institution'), course=session.get('course'), remote_addr=remote_addr, host=host, current_time=datetime.utcnow())


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        session['username'] = form.username.data
        return redirect(url_for('login_response'))
    return render_template('login.html',
    form=form,
    current_time=datetime.utcnow()
    )


@app.route('/loginResponse')
def login_response():
    return render_template('login_response.html',
    username=session.get('username'),
    current_time=datetime.utcnow()
    )


if __name__ == "__main__":
    app.run(debug=True)