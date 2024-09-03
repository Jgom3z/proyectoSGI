
from pprint import pprint
from flask import Blueprint, request, render_template, redirect, url_for


# Crear un Blueprint
vistaInicio = Blueprint('idVistaInicio', __name__, template_folder='templates')

@vistaInicio.route('/vistaInicio', methods=['GET', 'POST'])
def vista_Inicio():
 return render_template('inicio.html')   
 
