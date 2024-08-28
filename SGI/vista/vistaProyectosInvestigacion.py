from pprint import pprint
from flask import Blueprint, request, render_template, redirect, url_for
from controlador.ControlEntidad import ControlEntidad

# Crear un Blueprint
vistaProyectosInvestigacion = Blueprint('idVistaProyectosInvestigacion', __name__, template_folder='templates')

@vistaProyectosInvestigacion.route('/vistaProyectosInvestigacion', methods=['GET', 'POST'])
def vista_ProyectosInvestigacion():
    mensaje = ""
    objControlEntidad = ControlEntidad('investigador_proyecto')
    arregloProyectos = objControlEntidad.select_data()

    boton = request.form.get('bt', '')
    id_investigador_proyecto = request.form.get('txtIdInvestigadorProyecto', '')
    id_investigador = request.form.get('txtIdInvestigador', '')
    id_proyecto = request.form.get('txtIdProyecto', '')
    tipo_participacion = request.form.get('txtTipoParticipacion', '')
    estado = request.form.get('txtEstado', '')
    horas_fase_1 = request.form.get('txtHorasFase1', '')
    horas_fase_2 = request.form.get('txtHorasFase2', '')
    horas_fase_3 = request.form.get('txtHorasFase3', '')
    horas_fase_4 = request.form.get('txtHorasFase4', '')
    horas_fase_5 = request.form.get('txtHorasFase5', '')
    horas_fase_6 = request.form.get('txtHorasFase6', '')

    datosProyecto = {
        'id_investigador_proyecto': id_investigador_proyecto,
        'id_investigador': id_investigador,
        'id_proyecto': id_proyecto,
        'tipo_participacion': tipo_participacion,
        'estado': estado,
        'horas_fase_1': horas_fase_1,
        'horas_fase_2': horas_fase_2,
        'horas_fase_3': horas_fase_3,
        'horas_fase_4': horas_fase_4,
        'horas_fase_5': horas_fase_5,
        'horas_fase_6': horas_fase_6
    }

    if boton == 'Guardar':
        objProyecto = Entidad(datosProyecto)
        objControlEntidad.guardar(objProyecto)
        return redirect(url_for('idVistaProyectosInvestigacion.vista_ProyectosInvestigacion'))
    
    elif boton == 'Consultar':
        objProyecto = objControlEntidad.buscarPorId('id_investigador_proyecto', id_investigador_proyecto)
        if objProyecto:
            datosProyecto = objProyecto.__dict__
        else:
            mensaje = "El Proyecto de Investigación no se encontró."
    
    elif boton == 'Modificar':
        objProyecto = Entidad(datosProyecto)
        objControlEntidad.modificar('id_investigador_proyecto', id_investigador_proyecto, objProyecto)
        return redirect(url_for('idVistaProyectosInvestigacion.vista_ProyectosInvestigacion'))
    
    elif boton == 'Borrar':
        objControlEntidad.borrar('id_investigador_proyecto', id_investigador_proyecto)
        return redirect(url_for('idVistaProyectosInvestigacion.vista_ProyectosInvestigacion'))

    # Renderizar la plantilla al final, pasando las variables necesarias
    return render_template('vistaProyectosInvestigacion.html', arregloProyectos=arregloProyectos, mensaje=mensaje, proyecto=datosProyecto)
