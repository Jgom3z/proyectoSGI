from pprint import pprint
from flask import Blueprint, request, render_template, redirect, url_for
from controlador.ControlEntidad import ControlEntidad

# Crear un Blueprint
vistaProyectoFormacion = Blueprint('idVistaProyectoFormacion', __name__, template_folder='templates')

@vistaProyectoFormacion.route('/vistaProyectoFormacion', methods=['GET', 'POST'])
def vista_ProyectoFormacion():
    mensaje = ""
    objControlEntidad = ControlEntidad('proyecto_formacion')
    arregloProyectosFormacion = objControlEntidad.select_data()

    boton = request.form.get('bt', '')
    id_proyecto_formacion = request.form.get('txtIdProyectoFormacion', '')
    nombre_proy_form = request.form.get('txtNombreProyForm', '')
    fecha_inicio = request.form.get('txtFechaInicio', '')
    fecha_terminacion = request.form.get('txtFechaTerminacion', '')
    linea_investigacion = request.form.get('txtLineaInvestigacion', '')
    id_investigador = request.form.get('txtIdInvestigador', '')
    id_proyecto = request.form.get('txtIdProyecto', '')
    id_semillero = request.form.get('txtIdSemillero', '')
    objetivos = request.form.get('txtObjetivos', '')
    nivel = request.form.get('txtNivel', '')
    modalidad = request.form.get('txtModalidad', '')
    cod_proy_form = request.form.get('txtCodProyForm', '')
    id_codirector = request.form.get('txtIdCodirector', '')
    id_linea = request.form.get('txtIdLinea', '')

    datosProyectoFormacion = {
        'id_proyecto_formacion': id_proyecto_formacion,
        'nombre_proy_form': nombre_proy_form,
        'fecha_inicio': fecha_inicio,
        'fecha_terminacion': fecha_terminacion,
        'linea_investigacion': linea_investigacion,
        'id_investigador': id_investigador,
        'id_proyecto': id_proyecto,
        'id_semillero': id_semillero,
        'objetivos': objetivos,
        'nivel': nivel,
        'modalidad': modalidad,
        'cod_proy_form': cod_proy_form,
        'id_codirector': id_codirector,
        'id_linea': id_linea
    }

    if boton == 'Guardar':
        objProyectoFormacion = Entidad(datosProyectoFormacion)
        objControlEntidad.insert_data(objProyectoFormacion)
        return redirect(url_for('idVistaProyectoFormacion.vista_ProyectoFormacion'))
    
    elif boton == 'Consultar':
        objProyectoFormacion = objControlEntidad.buscarPorId('id_proyecto_formacion', id_proyecto_formacion)
        if objProyectoFormacion:
            datosProyectoFormacion = objProyectoFormacion.__dict__
        else:
            mensaje = "El Proyecto de Formación no se encontró."
    
    elif boton == 'Modificar':
        objProyectoFormacion = Entidad(datosProyectoFormacion)
        objControlEntidad.update_data('id_proyecto_formacion', id_proyecto_formacion, objProyectoFormacion)
        return redirect(url_for('idVistaProyectoFormacion.vista_ProyectoFormacion'))
    
    elif boton == 'Borrar':
        objControlEntidad.delete_data('id_proyecto_formacion', id_proyecto_formacion)
        return redirect(url_for('idVistaProyectoFormacion.vista_ProyectoFormacion'))

    # Renderizar la plantilla al final, pasando las variables necesarias
    return render_template('vistaProyectosFormacion.html', arregloProyectosFormacion=arregloProyectosFormacion, mensaje=mensaje, proyectoFormacion=datosProyectoFormacion)
