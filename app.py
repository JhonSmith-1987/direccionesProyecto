from flask import Flask, render_template, request, url_for
from flask_migrate import Migrate
from werkzeug.utils import redirect
from database import db
import models
from forms import DireccionForm

app = Flask(__name__)

# configuracion de la base de datos
USER_DB = 'postgres'
PASS_DB = 'admin'
URL_DB = 'localhost'
NAME_DB = 'mis_direcciones'

FULL_URL_DB = f'postgresql://{USER_DB}:{PASS_DB}@{URL_DB}/{NAME_DB}'

app.config['SQLALCHEMY_DATABASE_URI'] = FULL_URL_DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)
db.init_app(app)

# configurar flask_migrate
migrate = Migrate()
migrate.init_app(app, db)

# configuracion de flask-wtf
app.config['SECRET_KEY'] = 'terreno_amarillo'


@app.route('/')
def inicio():
    # listado de personas
    direcciones = models.Direccion.query.order_by()
    total_direcciones = models.Direccion.query.count()
    app.logger.debug(f'Listado de direcciones: {direcciones}')
    app.logger.debug(f'Direcciones en total: {total_direcciones}')
    return render_template('index.html', direcciones=direcciones, total_direcciones=total_direcciones)


@app.route('/ver/<int:id>')
def verDetalle(id):
    direccion = models.Direccion.query.get(id)
    app.logger.debug(f'ver direccion recuperada: {direccion}')
    return render_template('detalle.html', direccion=direccion)


@app.route('/agregar', methods=['GET', 'POST'])
def agregar():
    direccion = models.Direccion()
    direccionForm = DireccionForm(obj=direccion)
    if request.method == 'POST':
        if direccionForm.validate_on_submit():
            direccionForm.populate_obj(direccion)
            app.logger.debug(f'direccion a insertar: {direccion}')
            db.session.add(direccion)
            db.session.commit()
            return redirect(url_for('inicio'))
    return render_template('agregar.html', forma=direccionForm)


@app.route('/buscar', methods=['GET', 'POST'])
def buscar():
    nuevo = request.form['nuevo']
    app.logger.debug(f'el dato recibido es: {nuevo}')
    search = "%{}%".format(nuevo)
    direcciones = models.Direccion.query.filter(models.Direccion.nombre.like(search)).all()
    dato = type(direcciones)
    app.logger.debug(f'el dato es igual a: {dato}')
    if direcciones != []:    
        for direccion in direcciones:
            app.logger.debug(f'Se econtro esta coincidencia {direccion}')
        app.logger.debug(f'los datos filtrados por direccion son: {direcciones}')
        return render_template('nueva_direccion.html', direcciones=direcciones)
    else:
        error = 'No se encontraron considencias'
        app.logger.debug(f'el error es igual a: {error}')  
        return render_template('error.html', error=error)  


@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    direccion = models.Direccion.query.get(id)
    direccionForm = DireccionForm(obj=direccion)
    if request.method == 'POST':
        if direccionForm.validate_on_submit():
            direccionForm.populate_obj(direccion)
            app.logger.debug(f'direccion a actualizar: {direccion}')
            db.session.commit()
            return redirect(url_for('inicio'))
    return render_template('editar.html', forma=direccionForm)


@app.route('/eliminar/<int:id>')
def eliminar(id):
    direccion = models.Direccion.query.get(id)
    app.logger.debug(f'Direccion a eliminar: {direccion}')
    db.session.delete(direccion)
    db.session.commit()
    return redirect(url_for('inicio'))


if __name__ == '__main__':
    app.run(debug=True)
