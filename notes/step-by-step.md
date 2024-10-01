# Notes

-   [Install Requirements](#install-requirements)
-   [First app](#first-app)
-   [Static content, introduction](#static-content-introduction)
-   [CSS](#css)
-   [Databases](#databases)
-   [Adding methods to 'route' in app file](#adding-methods-to-route-in-app-file)
-   [CRUD](#crud)
-   [Improving one or two things](#improving-one-or-two-things)

## Install Requirements

-   Python (...)
-   `pip3 install virtualenv`
-   `virtualenv env`
-   activate environment `source env/bin/activate`
-   install flask and flask-sqlalchemy `pip3 install flask flask-sqlalchemy`

## First app

-   Files and folders (for now): .venv/, env/, app.py
-   We run app.py and we can see the web at http://127.0.0.1:5000/

```py
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, world!"

if __name__ == "__main__":
    app.run(debug=True)
```

## Static content, introduction

-   New files and folders: static/, templates/, templates/index.html, templates/base.html
-   We import render_template
-   Template inheritance: creating one master HTML file that contains the _skeleton_ of a page, then we inherit it in other pages, so we don't have to write the same HTML structure every time and just what is needed.
-   Jinja 2 syntax: `{% block head %} {% endblock %}`
    -   _Jinja is a fast, expressive, extensible templating engine. Special placeholders in the template allow writing code similar to Python syntax. Then the template is passed data to render the final document._ [Source](https://jinja.palletsprojects.com/en/3.0.x/)
    -   ⚠️ Jinja 3 is the newer version!
    -   `{% %}` is for _coding_ blocks, like _ifs_ or loops.
    -   `{{ }}` is for "printed strings"

templates/base.html

```py
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    {% block head %} {% endblock %}
</head>
<body>
    {% block body %} {% endblock %}
</body>
</html>
```

templates/index.html

```py
{% extends 'base.html' %}

{% block head %}
<title>Tasks</title>
{% endblock %}

{% block body %}
<h1>Template</h1>
{% endblock %}
```

## CSS

> [!CAUTION]
> In this point I found a problem (not related with the tutorial): I couln't not access my web after a long break from here. Solution: changing port from `5000` to `7000`.

-   New files: static/css/main.css,
-   Import module `url_for`
-   Changing the listening port.
-   In `base.html`, it won't work to put a route on `link` `href`, something like `static/css/main.css`. Instead, we have to use Jinja again. We need to use `{{ }}` and use a sort of _function_ given by Flask (`url_for`, previously imported) that will return a string. This function accepts two arguments, the name of the folder (_static_) and then the filename `css/main.css`. We'll do the same with JavaScript.
    app.py

```py
from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(port=7000, debug=True)
```

base.html

```html
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <link rel="stylesheet" href="{{ url_for('static',
        filename="css/main.css")}}"> {% block head %} {% endblock %}
    </head>
    <body>
        {% block body %} {% endblock %}
    </body>
</html>
```

main.css

```css
body {
    margin: 0;
    padding: 2rem;
    font-family: Georgia, 'Times New Roman', Times, serif;
    background-color: rgb(238, 255, 250);
}
```

## Databases

-   Import SQLAlchemy, `from flask_sqlalchemy import SQLAlchemy`
-   Add a config that tells where the DB is located, `app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'`
    -   `///` (3 slashes) is a relative path and `////` (4) is an absolute path.
    -   We're using SQLite just to keep things simple.
-   We initialize the DB with the settings from our app, `db = SQLAlchemy(app)`
-   We create a class that will represent how we organize data, `class Todo(db.Model)`...
    -   We're creating an ID
    -   Also the content of the task, which can't be null.
    -   The date when the task was created. With that goal, we also import `datetime`, `from datetime import datetime`.
    -   Function that will return a string every time we create a new element. It will return the task and its id.
-   We start a python3 shell and:

    -   `from app import db`. This will import the DB object
    -   Then, the tutorial suggests to type `db.create_all()` BUT this is outdated now, so this is a workaround:

        > Instead of Running the `db.create_all()` command in the terminal Initialize the Database in your code after your Database Models classes have been setup:
        >
        > `with app.app_context():`
        >
        > `    db.create_all()`
        >
        > Basically, put this in your Flask app under the Db.Model classes. Make sure to indent properly and run your flask app one time. It should create the database (also check your instance folder for the db file). Then comment it out. You can run other SQL commands under the with statement if you need info on what's in your database file.

    -   `exit()`

-   Finally, we prepare the index template to contain the tasks and the CRUD actions.

app.py

```py
from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":

    with app.app_context():
        db.create_all()

    app.run(port=7000, debug=True)

```

after the first run it will go:

```py
if __name__ == "__main__":
    #
    # with app.app_context():
    #    db.create_all()
    #
    app.run(debug=True)
```

(I need to change the port again and go back to the default one, i don't know why)

index.html

```html
{% extends 'base.html' %} {% block head %}
<title>Tasks</title>
{% endblock %} {% block body %}
<div class="content">
    <h1>Task Master</h1>
    <table>
        <tr>
            <th>Task</th>
            <th>Added</th>
            <th>Actions</th>
        </tr>
        <tr>
            <td></td>
            <td></td>
            <td>
                <a href="">Delete</a>
                <br />
                <a href="">Update</a>
            </td>
        </tr>
    </table>
</div>
{% endblock %}
```

main.css

```css
body {
    margin: 0;
    padding: 2rem;
    font-family: Georgia, 'Times New Roman', Times, serif;
    background-color: rgb(238, 255, 250);
}

table {
    width: 90%;
    text-align: center;
}

tr {
    margin: 2px;
}

form {
    margin: 10px 2px;
}

input[type='text'] {
    width: 70%;
}
```

## Adding methods to 'route' in app file

-   We're adding methods to the route to send data to the DB, `@app.route('/', methods=['POST', 'GET'])`
-   Adding inputs to the index.
-   Import request
-   If we access through POST:
    -   Create a variable equal to... form method of the request instance. and we pass it the id of the input we want to get the contents of. So `task_content` is equal to the contents of the input of the page.
    -   Now we should create a model for this. the content of this Todo will be the content of that input.
    -   Then we push it to the DB. And we'll do it inside a try-except.
    -   Then it should commit the task
    -   Finally redirects to the homepage. For this we import `redirect`.
    -   If that fails, send a message.
-   ELSE, look at all the database contents in the order they were created and return all of them. Instead of `all()` we could type `first()`, to show the most recent or other options.
    -   Then we pass it to the return
-   Then we go to the index.html and prepare the tables again to be dynamic. But the CRUD we'll be done afterwards.

app.py

```py
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)

if __name__ == "__main__":
    #
    # with app.app_context():
    #    db.create_all()
    #
    app.run(debug=True)

```

index.html

```html
{% extends 'base.html' %} {% block head %}
<title>Tasks</title>
{% endblock %} {% block body %}

<div class="content">
    <h1>Task Master</h1>
    <table>
        <tr>
            <th>Task</th>
            <th>Added</th>
            <th>Actions</th>
        </tr>
        {% for task in tasks %}
        <tr>
            <td>{{ task.content}}</td>
            <td>{{ task.date_created.date() }}</td>
            <td>
                <a href="">Delete</a>
                <br />
                <a href="">Update</a>
            </td>
        </tr>
        {% endfor%}
    </table>

    <form action="/" method="POST">
        <input type="text" name="content" id="content" />
        <input type="submit" value="Add task" />
    </form>
</div>
{% endblock %}
```

## CRUD

-   Delete
    -   We will delete tasks depending on its id, because it cannot be duplicated. so create a new route.
    -   We'll also need to set the url in the index.
-   Updating
    -   New route and new function
    -   Changing url in index
    -   Creation of new template for updating. this will be similar to index, but removing the table and editing a few things

update.html

```html
{% extends 'base.html' %} {% block head %}
<title>Tasks</title>
{% endblock %} {% block body %}

<div class="content">
    <h1>update task</h1>

    <form action="/update/{{task.id}}" method="POST">
        <input
            type="text"
            name="content"
            id="content"
            value="{{task.content}}"
        />
        <input type="submit" value="Update" />
    </form>
</div>
{% endblock %}
```

index.html

```html
{% extends 'base.html' %} {% block head %}
<title>Tasks</title>
{% endblock %} {% block body %}

<div class="content">
    <h1>Task Master</h1>
    <table>
        <tr>
            <th>Task</th>
            <th>Added</th>
            <th>Actions</th>
        </tr>
        {% for task in tasks %}
        <tr>
            <td>{{ task.content}}</td>
            <td>{{ task.date_created.date() }}</td>
            <td>
                <a href="/delete/{{task.id}}">Delete</a>
                <br />
                <a href="/update/{{task.id}}">Update</a>
            </td>
        </tr>
        {% endfor%}
    </table>

    <form action="/" method="POST">
        <input
            type="text"
            name="content"
            id="content"
            placeholder="Write your new task here"
        />
        <input type="submit" value="Add task" />
    </form>
</div>
{% endblock %}
```

app.py

```py
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)


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
    if request.method == 'POST':
        task.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was a problem updating the task'
    else:
        return render_template('update.html', task=task)


if __name__ == "__main__":
    #
    # with app.app_context():
    #    db.create_all()
    #
    app.run(port=4000, debug=True)

```

## Improving one or two things

-   Filter in case we don't have tasks

    ```jinja
    {% if tasks|length <1 %}
    <h4>There are no tasks. Create one below</h4>
    {% else %} {% endif %}
    ```
