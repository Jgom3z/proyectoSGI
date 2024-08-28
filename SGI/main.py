#main
from pprint import pprint
from flask import Flask, render_template, request, url_for, redirect, session
import markupsafe


from vista.inicio import vistaInicio
from vista.login import login
from vista.vistaEstudiante import vistaEstudiante
from vista.vistaGruposInvestigacion import vistaGruposInvestigacion
from vista.vistaInvestigaciones import vistaInvestigaciones
from vista.vistaInvestigadores import vistaInvestigadores
from vista.vistaLineasInvestigacion import vistaLineasInvestigacion
from vista.vistaProyectoFormacion import vistaProyectoFormacion
from vista.vistaProyectosInvestigacion import vistaProyectosInvestigacion
from vista.vistaSemillerosInvestigacion import vistaSemillerosInvestigacion

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_aqui'  # Asegúrate de tener una clave secreta para sesiones

# Registro de Blueprints
app.register_blueprint(vistaInicio)
app.register_blueprint(login)
app.register_blueprint(vistaEstudiante)
app.register_blueprint(vistaGruposInvestigacion)
app.register_blueprint(vistaInvestigaciones)
app.register_blueprint(vistaInvestigadores)
app.register_blueprint(vistaLineasInvestigacion)
app.register_blueprint(vistaProyectoFormacion)
app.register_blueprint(vistaProyectosInvestigacion)
app.register_blueprint(vistaSemillerosInvestigacion)

@app.route('/')
def index():
    return redirect(url_for('login.login_view'))

if __name__ == '__main__':
    app.run(debug=True)



"""
@app.route('/login', methods=['GET', 'POST'])
def login_view():
    if request.method == 'POST':
        email = markupsafe.escape(request.form['txtEmail'])
        contrasena = markupsafe.escape(request.form['txtContrasena'])
        print(email)
        print(contrasena)
        if request.form['btnLogin'] == 'Login':
            datosEntidad = {'email': email, 'contrasena': contrasena}
            print(datosEntidad.items)
            print(datosEntidad)

            objEntidad = Entidad(datosEntidad)
            objControlEntidad = ControlEntidad('usuario')
            validar = objControlEntidad.validarIngreso('email', email, 'contrasena', contrasena)
            if validar:
                session['email'] = email  # Guarda el email en la sesión
                return redirect(url_for('inicio'))  # Redirige a la vista de inicio
            else:
                return render_template('login.html', error="Credenciales inválidas")
    return render_template('login.html')

@app.route('/inicio')
def inicio():
    email = session.get('email')
    if email:
        return render_template('inicio.html', ema=email)
    else:
        return redirect(url_for('login_view'))

@app.route('/cerrarSesion')
def cerrar_sesion():
    session.clear()  # Limpia la sesión
    return redirect(url_for('login_view'))
"""

    
"""
# main.py
from flask import Flask
from your_blueprint_factory_module import create_crud_blueprint  # Importa la funciรณn fรกbrica de blueprints

app = Flask(__name__)

# Diccionario o lista de tus entidades
# Puedes hacer esto de manera mรกs dinรกmica, por ejemplo, leyendo de tu base de datos o mรณdulos, etc.
entities = {
    'rol': ['id', 'nombre', 'permisos'],
    'usuario': ['id', 'nombre', 'email', 'contrasena']
}

# Funciรณn para registrar blueprints de manera genรฉrica
def register_entity_blueprints(app, entities):
    for entity_name, entity_columns in entities.items():
        blueprint = create_crud_blueprint(entity_name, entity_columns)
        app.register_blueprint(blueprint, url_prefix=f'/{entity_name}')

# Llamar a la funciรณn para registrar los blueprints
register_entity_blueprints(app, entities)

@app.route('/')
def inicio():
    # Redirige al inicio o a la pรกgina que desees por defecto
    return "Bienvenido a la aplicaciรณn! Utiliza las entidades definidas para interactuar."

if __name__ == '__main__':
    app.run(debug=True)

"""