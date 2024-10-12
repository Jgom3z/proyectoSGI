from flask import Flask, render_template, request, jsonify, url_for, redirect, session
import markupsafe
import requests
import json
from pprint import pprint
from dotenv import load_dotenv

load_dotenv()
#Iconos
from vista.inicio import vistaInicio
from vista.login import login
from vista.vistaEstudiantes import vistaEstudiantes
from vista.vistaGruposInvestigacion import vistaGruposInvestigacion
from vista.vistaInvestigaciones import vistaInvestigaciones
from vista.vistaInvestigadores import vistaInvestigadores
from vista.vistaLineasInvestigacion import vistaLineasInvestigacion
from vista.vistaProyectosFormacion import vistaProyectosFormacion
from vista.vistaProyectosInvestigacion import vistaProyectosInvestigacion
from vista.files import files_bp
from vista.vistaSemillerosInvestigacion import vistaSemillerosInvestigacion

app = Flask(__name__)
app.secret_key = 'supersecretkey'
# Registro de Blueprints
app.register_blueprint(vistaInicio)
app.register_blueprint(login)
app.register_blueprint(vistaEstudiantes, url_prefix= '/estudiantes')
app.register_blueprint(vistaGruposInvestigacion, url_prefix= '/grupos')
app.register_blueprint(vistaInvestigaciones)
app.register_blueprint(vistaInvestigadores, url_prefix= '/investigadores')
app.register_blueprint(vistaLineasInvestigacion)
app.register_blueprint(vistaProyectosFormacion, url_prefix='/ProyectosFormacion')
app.register_blueprint(vistaProyectosInvestigacion, url_prefix='/proyectos')
app.register_blueprint(files_bp, url_prefix='/files')
app.register_blueprint(vistaSemillerosInvestigacion, url_prefix='/semilleros')

# Configuración de la URL de la API
projectName = 'SGI'
API_URL = "http://190.217.58.246:5185/api/{projectName}/procedures/execute"

@app.route('/')
def index():
    return redirect(url_for('login.login_view'))

if __name__ == '__main__':
    app.run(debug=True)
