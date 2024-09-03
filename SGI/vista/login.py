#login
from flask import Blueprint, render_template, request, redirect,url_for, flash, session
import markupsafe
import requests




# Define el Blueprint para login
login = Blueprint('login', __name__, template_folder='templates')

@login.route('/login', methods=['GET', 'POST'])
def login_view():
    
    if request.method == 'POST':
        email = markupsafe.escape(request.form['txtEmail'])
        contrasena = markupsafe.escape(request.form['txtContrasena'])

        api_url = "http://190.217.58.246:5185/api/SGI/procedures/execute"
        payload = {
            "procedure": "select_json_entity",
            "parameters": {
                "table_name": "usuario",
                "select_columns": "email, contrasena",
                "where_condition": f"email = '{email}'"
            }
        }
        """
        {
            "email": 'isabela@usbmed.com",
            "contrasena": "password123"
        }
        """
        response = requests.post(api_url, json=payload)
        if response.status_code == 200:
            users = response.json()
            user = users['outputParams']['result'][0] if users['outputParams']['result'] else None
            print(users)
            print(user)

            if user:
                if contrasena == user['contrasena']:
                    session['user_email'] = user['email']
                    return redirect(url_for('idVistaInicio.vista_Inicio'))  # Asume que tienes una ruta 'home'
                else:
                    flash('Correo electrónico o contraseña inválidos', 'error')
            else:
                flash('Correo electrónico o contraseña inválidos', 'error')
        else:
            flash('Error al conectar con el servicio de autenticación.', 'error')
    
            
    return render_template('inicio.html')





# Establecer la ruta base si es necesario, por defecto es '/'
#breakpoint();
"""
@app.route('/', methods = ['GET', 'POST'])
@app.route('/login', methods = ['GET', 'POST']) 
def login():
    email=""
    contrasena=""
    bot=""
    if request.method == 'GET':
        pass
    if request.method == 'POST':
        email=markupsafe.escape(request.form['txtEmail'])
        contrasena=markupsafe.escape(request.form['txtContrasena'])
        bot=markupsafe.escape(request.form['btnLogin'])
        datosEntidad = {'email': email, 'contrasena': contrasena}
        if bot=='Login':
            validar=False
            objEntidad= Entidad(datosEntidad)
            objControlEntidad=ControlEntidad('usuario')
            validar=objControlEntidad.validarIngreso('email',email,'contrasena',contrasena)
            if validar:
                return render_template('/inicio.html',ema=email)
            else:
                return render_template('/login.html')
        else:
            return render_template('/login.html')
    else:
        return render_template('/login.html')




@app.route('/cerrarSesion')
def cerrarSesion():
    #session.clear()
    return redirect('login.html')

if __name__ == '__main__':
    # Corre la aplicaciรณn en el modo debug, lo que permitirรก 
    # la recarga automรกtica del servidor cuando se detecten cambios en los archivos.
    app.run(debug=True)
    

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
