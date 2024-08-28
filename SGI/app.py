from flask import Flask, render_template, request, jsonify, url_for, redirect, session
import markupsafe
import requests
import json
from pprint import pprint

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

# Configuración de la URL de la API
projectName = 'SGI'
API_URL = "http://190.217.58.246:5185/api/{projectName}/procedures/execute"

@app.route('/')
def index():
    return redirect(url_for('login.login_view'))

if __name__ == '__main__':
    app.run(debug=True)
