# Explicacións en detalle

-   [`app.py`](#apppy)
    -   [Importacións](#importacións)
    -   [Configuración da app](#configuración-da-app)
    -   [Modelo de Datos](#modelo-de-datos)
    -   [Rutas da aplicación](#rutas-da-aplicación)
        -   [Ruta principal](#ruta-principal)
        -   [Ruta para eliminar tarefas](#ruta-para-eliminar-tarefas)
        -   [Ruta para actualizar tarefas](#ruta-para-actualizar-tarefas)
    -   [Determinar onde se executa](#determinar-onde-se-executa)

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

-   `class Todo(db.Model):` Define un modelo chamado `Todo`, que representa **unha tarefa** na base de datos. Herda de `db.Model`, o que significa que é un modelo de SQLAlchemy. Para resumir, diríamos que `Todo` se convirte nunha representación dunha táboa na base de datos, representando unha tarefa na lista.
    -   `id = db.Column(db.Integer, primary_key=True)`: Define unha columna `id`, que é un enteiro (`db.Integer`) e é a chave primaria da táboa.
    -   `content = db.Column(db.String(200), nullable=False)`: Define unha columna `content` que é unha cadea de texto (`db.String()`) de até 200 caracteres e que non pode ser nula.
    -   `    date_created = db.Column(db.DateTime, default=datetime.utcnow)`: Define unha columna `date_created` que almacena a data e a hora de creación da tarefa, cun valor predeterminado de data e hora actuais.
    -   `def __repr__(self):`: Define un **método especial en Python** que se utiliza para definir como se representa un obxecto da clase cando se imprima ou se convirte a unha cadea. É útil para a depuración e o logging.
        -   `return '<Task %r>' % self.id`: Estamos devolvendo unha cadea que inclúa o ID da tarefa. O uso de `%r`asegura que se utilice a representación "oficial" do ID. Por exemplo, se o ID da tarefa é 1, a representación será `<Task 1>`. Isto facilitaa identificación de instancias de `Todo` cando se imprimen na consola ou se rexistran.

### Rutas da aplicación

#### Ruta principal

```py
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
```

-   `@app.route('/', methods=['POST', 'GET'])`: Define a ruta para a URL raíz (`/`), aceptando métodos `POST` e `GET`.
    -   `def index():`: Define a función de vista `index`, que manexa as solicitudes á ruta raíz.
        -   `if request.method == 'POST':`: Comproba se a solicitude é un `POST`, o que indica que se está enviando un novo contido de tarefa.
            -   `task_content = request.form['content']`: Obtén o contido da tarefa do formulario enviado.
            -   `new_task = Todo(content=task_content)`: Crea unha nova istancia de `Todo`, facendo que o campo `content` sexa o da variábel recén creada `task_content`.
            -   `try`: Bloque `try` para manexar posíbeis erros.
                -   `db.session.add(new_task)`: Agrega unha nova tarefa á sesión actual da base de datos. En SQLAlchemy, unha "sesión" é un espazo de traballo onde se poden realizar operacións de base de datos. Aquí estamos preparando a tarefa para ser gardada.
                -   _The Session establishes all conversations with the database. The session is a regular Python class which can be directly instantiated_.
                -   `db.session.commit()`: Confirma todos os cambios realizados na sesión actual, é dicir, que a nova tarefa é gardada na base de datos. Se non se chamase o `commit()` os cambios perderíanse.
                -   `return redirect('/')`: Redirixe ao usuario de volta á rúta raíz
            -   `except`: Captura calquera exceptión que aconteza durante o proceso de agregar a tarefa.
                -   `return 'There was an issue adding your task'`: Se acontece un erro, devolve unha mensaxe de erro.
        -   `else`: Se a solicitude non é un `POST`, entón é que é un `GET`, polo tanto vanse devolver as tarefas existentes.
            -   `tasks = Todo.query.order_by(Todo.date_created).all()`: Realiza unha consulta á base de datos para obter todas as tarefas (`Todo`) e as ordena pola data de creación (`date_created`). Vai devolver todas polo `all`,
            -   `return render_template('index.html', tasks=tasks)`: Randeriza a plantilla `index.html`, pasando a lista de tarefas (`tasks`) para que se mostre na páxina. `index.html` necesita que se lle pase `tasks` para funcionar.

#### Ruta para eliminar tarefas

```py
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'
```

-   `@app.route('/delete/<int:id>')`: define unha ruta para eliminar tarefas. `<int:id>` é un parámetro da URL que representa o ID da tarefa que se vai eliminar. Isto é o link de _Delete_ en `index.html`.
-   `def delete(id)`: Define a función de vista `delete`, que manexa a eliminación da tarefa co ID dado.
    -   `task_to_delete = Todo.query.get_or_404(id)`: crea unha variábel `task_to_delete` onde almanace a tarefa que se vai procurar. Esta encóntrase a través do método `get_or_404` de `query`, que pertence ao obxecto `Todo`. O que fai este método é que se non encontra a tarefa por esa id que se lle pasa por parámetros, devolve un erro `404`.
        -   `try:`: (...)
            -   `db.session.delete(task_to_delete)`: Elimina a tarefa actual da sesión da DB.
            -   `db.session.commit()`: Confirma os cambios.
            -   `return redirect('/')`: Redirixe.
        -   `except:`: (...)
            -   `return 'There was a problem deleting that task'`: Devolve unha mensaxe indicando que houbo un erro.

#### Ruta para actualizar tarefas

```py
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
```

Semellante ao feito antes.

### Determinar onde se executa

```py
if __name__ == "__main__":
    #
    # with app.app_context():
    #    db.create_all()
    #
    app.run(port=4000, debug=True)
```

-   `if __name__ == "__main__":`: É unha construción comíun en Python, que se utiliza para determinar se o arquivo se está executando como un programa principal ou se se está importando como un módulo noutro arquivo.
-   Se o arquivo que se executa directamente (por exemplo con `python app.py` na terminal), `__name__` estabelécese en `__main__` e o bloque de código dentro do `if` execútase.
-   Se o arquivo impoórtase noutro módulo, `__name__` tomará o nome do módulo, e o bloque de código do `if` non se executa.
