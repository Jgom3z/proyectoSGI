from pprint import pprint
from flask import Blueprint, request, render_template, redirect, url_for
from controlador.ControlEntidad import ControlEntidad

# Crear un Blueprint
vistaSemillerosInvestigacion = Blueprint('idVistaSemillerosInvestigacion', __name__, template_folder='templates')

@vistaSemillerosInvestigacion.route('/vistaSemillerosInvestigacion', methods=['GET', 'POST'])
def vista_SemillerosInvestigacion():
    mensaje = ""
    objControlEntidad = ControlEntidad('semillero_investigacion')
    arregloSemilleros = objControlEntidad.select_data()

    boton = request.form.get('bt', '')
    id_semillero = request.form.get('txtIdSemillero', '')
    nombre_semillero = request.form.get('txtNombreSemillero', '')
    objetivos = request.form.get('txtObjetivos', '')
    id_linea_grupo = request.form.get('txtIdLineaGrupo', '')
    fecha_inicio = request.form.get('txtFechaInicio', '')
    fecha_final = request.form.get('txtFechaFinal', '')
    id_lider = request.form.get('txtIdLider', '')
    areas_de_trabajo = request.form.get('txtAreasDeTrabajo', '')
    descripcion_semillero = request.form.get('txtDescripcionSemillero', '')

    datosSemillero = {
        'id_semillero': id_semillero,
        'nombre_semillero': nombre_semillero,
        'objetivos': objetivos,
        'id_linea_grupo': id_linea_grupo,
        'fecha_inicio': fecha_inicio,
        'fecha_final': fecha_final,
        'id_lider': id_lider,
        'areas_de_trabajo': areas_de_trabajo,
        'descripcion_semillero': descripcion_semillero
    }

    if boton == 'Guardar':
        objSemillero = Entidad(datosSemillero)
        objControlEntidad.insert_data(objSemillero)
        return redirect(url_for('idVistaSemillerosInvestigacion.vista_SemillerosInvestigacion'))
    
    elif boton == 'Consultar':
        objSemillero = objControlEntidad.buscarPorId('id_semillero', id_semillero)
        if objSemillero:
            datosSemillero = objSemillero.__dict__
        else:
            mensaje = "El Semillero de Investigación no se encontró."
    
    elif boton == 'Modificar':
        objSemillero = Entidad(datosSemillero)
        objControlEntidad.update_data('id_semillero', id_semillero, objSemillero)
        return redirect(url_for('idVistaSemillerosInvestigacion.vista_SemillerosInvestigacion'))
    
    elif boton == 'Borrar':
        objControlEntidad.delete_data('id_semillero', id_semillero)
        return redirect(url_for('idVistaSemillerosInvestigacion.vista_SemillerosInvestigacion'))

    # Renderizar la plantilla al final, pasando las variables necesarias
    return render_template('vistaSemillerosInvestigacion.html', arregloSemilleros=arregloSemilleros, mensaje=mensaje, semillero=datosSemillero)
