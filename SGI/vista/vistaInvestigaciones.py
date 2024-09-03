from flask import Blueprint, request, render_template, redirect, url_for


# Crear un Blueprint
vistaInvestigaciones = Blueprint('idVistaInvestigaciones', __name__, template_folder='templates')

@vistaInvestigaciones.route('/vistaInvestigaciones', methods=['GET', 'POST'])
def vista_Investigaciones():
    

    # Renderizar la plantilla al final, pasando las variables necesarias
    return render_template('vistaInvestigaciones.html')
