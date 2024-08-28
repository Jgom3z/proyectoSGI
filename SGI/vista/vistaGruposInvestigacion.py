from pprint import pprint
from flask import Blueprint, request, render_template, redirect, url_for
from controlador.ControlEntidad import ControlEntidad

# Crear un Blueprint
vistaGruposInvestigacion = Blueprint('idVistaGruposInvestigacion', __name__, template_folder='templates')

@vistaGruposInvestigacion.route('/vistaGruposInvestigacion', methods=['GET', 'POST'])
def vista_GruposInvestigacion():
    mensaje = ""
    objControlEntidad = ControlEntidad('grupo_investigacion')
    arregloGrupos = objControlEntidad.select_data()
    
    boton = request.form.get('bt', '')
    id_grupo = request.form.get('txtIdGrupo', '')
    nombre_grupo = request.form.get('txtNombreGrupo', '')
    codigo_grup_lac = request.form.get('txtCodigoGrupoLAC', '')
    categoria_colciencias = request.form.get('txtCategoriaColciencias', '')
    area_conocimiento = request.form.get('txtAreaConocimiento', '')
    id_facultad = request.form.get('txtIdFacultad', '')
    fecha_creacion = request.form.get('txtFechaCreacion', '')
    fecha_finalizacion = request.form.get('txtFechaFinalizacion', '')
    id_lider = request.form.get('txtIdLider', '')
    plan_estrategico = request.form.get('txtPlanEstrategico', '')
    categoria_meta = request.form.get('txtCategoriaMeta', '')
    estrategia_meta = request.form.get('txtEstrategiaMeta', '')
    vision = request.form.get('txtVision', '')
    objetivos = request.form.get('txtObjetivos', '')

    datosGrupo = {
        'id_grupo': id_grupo,
        'nombre_grupo': nombre_grupo,
        'codigo_grup_lac': codigo_grup_lac,
        'categoria_colciencias': categoria_colciencias,
        'area_conocimiento': area_conocimiento,
        'id_facultad': id_facultad,
        'fecha_creacion': fecha_creacion,
        'fecha_finalizacion': fecha_finalizacion,
        'id_lider': id_lider,
        'plan_estrategico': plan_estrategico,
        'categoria_meta': categoria_meta,
        'estrategia_meta': estrategia_meta,
        'vision': vision,
        'objetivos': objetivos
    }

    if boton == 'Guardar':
        objGrupo = Entidad(datosGrupo)
        objControlEntidad.insert_data(objGrupo)
        return redirect(url_for('idVistaGruposInvestigacion.vista_GruposInvestigacion'))
    
    elif boton == 'Consultar':
        objGrupo = objControlEntidad.buscarPorId('id_grupo', id_grupo)
        if objGrupo:
            datosGrupo = objGrupo.__dict__
        else:
            mensaje = "El Grupo de Investigación no se encontró."
    
    elif boton == 'Modificar':
        objGrupo = Entidad(datosGrupo)
        objControlEntidad.update_data('id_grupo', id_grupo, objGrupo)
        return redirect(url_for('idVistaGruposInvestigacion.vista_GruposInvestigacion'))
    
    elif boton == 'Borrar':
        objControlEntidad.delete_data('id_grupo', id_grupo)
        return redirect(url_for('idVistaGruposInvestigacion.vista_GruposInvestigacion'))

    # Renderizar la plantilla al final, pasando las variables necesarias
    return render_template('vistaGruposInvestigacion.html', arregloGrupos=arregloGrupos, mensaje=mensaje, grupo=datosGrupo)
