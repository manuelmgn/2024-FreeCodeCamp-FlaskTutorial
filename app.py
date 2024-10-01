from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import InputRequired, Length

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SECRET_KEY'] = '73decbbc27df3d143a43dfc50e1e9f9c9af943218475279d50ac088eaa121b3d0fa33887a93ccbbc2613d7da85d6be0d9d660d963c372af429c6408dd1fcf23e'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

class TodoForm(FlaskForm):
    new_content = StringField('Nova tarefa', validators=[InputRequired('A tarefa non pode estar en branco'), Length(min=1)])
    submit = SubmitField('Enviar')



@app.route('/', methods=['POST', 'GET'])
def index():
    form = TodoForm()
    if request.method == 'POST':
        task_content = form.new_content.data
        new_task = Todo(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks, form=form)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    form = TodoForm()
    form.new_content.data = task.content
    if request.method == 'POST':
        task.content = form.new_content.data
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was a problem updating the task'
    else:
        return render_template('update.html', task=task, form=form)


if __name__ == "__main__":
    #
    # with app.app_context():
    #    db.create_all()
    #
    app.run(port=9000, debug=True)
