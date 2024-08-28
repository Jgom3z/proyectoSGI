from pprint import pprint
from flask import Blueprint, request, render_template, redirect, url_for
from controlador.ControlEntidad import ControlEntidad

# Crear un Blueprint
vistaLineasInvestigacion = Blueprint('idVistaLineasInvestigacion', __name__, template_folder='templates')

@vistaLineasInvestigacion.route('/vistaLineasInvestigacion', methods=['GET', 'POST'])
def vista_LineasInvestigacion():
    mensaje = ""
    objControlEntidad = ControlEntidad('linea_investigador')
    arregloLineasInvestigacion = objControlEntidad.select_data()
    
    boton = request.form.get('bt', '')
    id_linea_investigador = request.form.get('txtIdLineaInvestigador', '')
    id_investigador = request.form.get('txtIdInvestigador', '')
    id_linea = request.form.get('txtIdLinea', '')
    estado = request.form.get('txtEstado', '')

    datosLineaInvestigacion = {
        'id_linea_investigador': id_linea_investigador,
        'id_investigador': id_investigador,
        'id_linea': id_linea,
        'estado': estado
    }

    if boton == 'Guardar':
        objLineaInvestigacion = Entidad(datosLineaInvestigacion)
        objControlEntidad.insert_data(objLineaInvestigacion)
        return redirect(url_for('idVistaLineasInvestigacion.vista_LineasInvestigacion'))
    
    elif boton == 'Consultar':
        objLineaInvestigacion = objControlEntidad.buscarPorId('id_linea_investigador', id_linea_investigador)
        if objLineaInvestigacion:
            datosLineaInvestigacion = objLineaInvestigacion.__dict__
        else:
            mensaje = "La Línea de Investigación no se encontró."
    
    elif boton == 'Modificar':
        objLineaInvestigacion = Entidad(datosLineaInvestigacion)
        objControlEntidad.update_data('id_linea_investigador', id_linea_investigador, objLineaInvestigacion)
        return redirect(url_for('idVistaLineasInvestigacion.vista_LineasInvestigacion'))
    
    elif boton == 'Borrar':
        objControlEntidad.delete_data('id_linea_investigador', id_linea_investigador)
        return redirect(url_for('idVistaLineasInvestigacion.vista_LineasInvestigacion'))

    # Renderizar la plantilla al final, pasando las variables necesarias
    return render_template('vistaLineasInvestigacion.html', arregloLineasInvestigacion=arregloLineasInvestigacion, mensaje=mensaje, lineaInvestigacion=datosLineaInvestigacion)
