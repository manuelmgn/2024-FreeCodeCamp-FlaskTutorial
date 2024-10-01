# Explicacións en detalle

## `app.py`

### Importacións

```py
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
```

Importa clases e funcións de Flask

-   `Flask`: Clase principal para crear as webs
-   `render_template`: Función para randerizar arquivos HTML
-   `url_for`: Xera URLs para as funcións de vista.
-   `request`: Permite acceder aos datos da solicitude HTTP.
-   `redirect`: Redirixe a outras URL.
-   `SQLAlchemy`: utilízase para interactuar coas bases de datos SQL.
-   `datetime`: traballa con datas e horas

### Configuración da app

```py
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)
```

-   `app = Flask(__name__)`: Crea unha instancia da aplicación Flask e a garda na variábel `app`. `__name__` pásase para que Flask saiba onde procurar recursos como plantillas e arquivos estáticos.
-   `app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'`: Configura a URI da BD SQLite. Creará un arquivo `test.db` no directorio actual ???
-   `db = SQLAlchemy(app)`: Crea unha instalacia de SQLAlchemy e a vincula á aplicación Flask.

### Modelo de Datos

```py
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id
```

-   `class Todo(db.Model):`
