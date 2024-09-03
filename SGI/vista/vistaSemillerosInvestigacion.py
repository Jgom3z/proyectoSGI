from pprint import pprint
from flask import Blueprint, request, render_template, redirect, url_for


# Crear un Blueprint
vistaSemillerosInvestigacion = Blueprint('idVistaSemillerosInvestigacion', __name__, template_folder='templates')

@vistaSemillerosInvestigacion.route('/vistaSemillerosInvestigacion', methods=['GET', 'POST'])
def vista_SemillerosInvestigacion():
   

    # Renderizar la plantilla al final, pasando las variables necesarias
    return render_template('vistaSemillerosInvestigacion.html')
