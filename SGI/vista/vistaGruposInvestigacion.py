from flask import Flask, render_template, request, jsonify, url_for, redirect, session,Blueprint
import markupsafe
import requests
import json
from pprint import pprint


# Crear un Blueprint
vistaGruposInvestigacion = Blueprint('idVistaGruposInvestigacion', __name__, template_folder='templates')

projectName = 'SGI'
API_URL = "http://190.217.58.246:5185/api/{projectName}/procedures/execute"

@vistaGruposInvestigacion.route('/vistaGruposInvestigacion', methods=['GET'])
def vista_grupos_investigacion():
    select_data = {
        "projectName": 'SGI',
        "procedure": "select_json_entity",
        "parameters": {
            "table_name": "inv_grupos g INNER JOIN inv_investigadores p ON p.id_investigador = g.id_lider INNER JOIN inv_facultad f ON f.id_facultad = g.id_facultad",
            "json_data": {
                "estado": "En Progreso"
            },
            "where_condition": "",
            "select_columns": "g.nombre_proyecto, g.codigo_grup_lac, g.categoria_colciencias, f.nombre_facultad, p.nombre_investigador, g.id_grupo",
            "order_by": "g.id_grupo",
            "limit_clause": ""
        }
    }

    response = requests.post(API_URL, json=select_data)

    # Manejo de errores en la respuesta
    if response.status_code != 200:
        return f"Error al consultar la API: {response.status_code}"

    # Parsear la respuesta a JSON
    data = response.json()
    
    # Verifica si 'result' existe y contiene datos
    if 'result' in data and data['result']:
        # Extraer el string JSON y cargarlo como objeto Python
        grupos_str = data['result'][0]['result']
        grupos = json.loads(grupos_str)
       
    else:
        grupos = []
    print(grupos)
    # Pasar los datos a la plantilla
    ths = ['grupos de investigacion', 'codigo gruplac', 'categoria colciencias', 'facultad', 'lider de grupo']
    tds = [grupos]
    
    
    return render_template('vistaGruposInvestigacion.html', tds=grupos, ths= ths)

@vistaGruposInvestigacion.route("/creategrupo", methods = ['POST'])
def create_grupo():
    # Captura los datos del formulario enviado
    print(request)
    form_data = {
        "nombre_grupo": request.form.get('nombre_grupo'),
        "codigo_grup_lac": request.form.get('codigo_grup_lac'),
        "categoria_colciencias": request.form.get('categoria_colciencias'),
        "area_conocimiento": request.form.get('area_conocimiento'),
        "id_facultad": request.form.get('id_facultad'),
        "fecha_creacion": request.form.get('fecha_creacion'),
        "fecha_finalizacion": request.form.get('fecha_finalizacion'),
        "id_lider": request.form.get('id_lider'),
        "plan_estrategico": request.form.get('plan_estrategico'),
        "categoria_meta": request.form.get('categoria_meta'),
        "estrategia_meta": request.form.get('estrategia_meta'),
        "vision": request.form.get('vision'),
        "objetivos": request.form.get('objetivos')
    }

    # Enviar los datos a la API
    response = requests.post(API_URL.format(projectName=projectName), json={
        "procedure": "insert_inv_grupos",  # Supongamos que tienes un procedimiento almacenado para insertar
        "parameters": [form_data]
    })

    # Verificar la respuesta de la API
    if response.status_code == 200:
        return jsonify({"message": "Datos guardados exitosamente"}), 200
    else:
        return jsonify({"message": "Error al guardar los datos"}), 500
# from pprint import pprint
# from flask import Blueprint, request, render_template, redirect, url_for
# from controlador.ControlEntidad import ControlEntidad

# Crear un Blueprint
# vistaGruposInvestigacion = Blueprint('idVistaGruposInvestigacion', __name__, template_folder='templates')

# @vistaGruposInvestigacion.route('/vistaGruposInvestigacion', methods=['GET', 'POST'])
# def vista_GruposInvestigacion():
#     mensaje = ""
#     objControlEntidad = ControlEntidad('grupo_investigacion')
#     arregloGrupos = objControlEntidad.select_data()
    
#     boton = request.form.get('bt', '')
#     id_grupo = request.form.get('txtIdGrupo', '')
#     nombre_grupo = request.form.get('txtNombreGrupo', '')
#     codigo_grup_lac = request.form.get('txtCodigoGrupoLAC', '')
#     categoria_colciencias = request.form.get('txtCategoriaColciencias', '')
#     area_conocimiento = request.form.get('txtAreaConocimiento', '')
#     id_facultad = request.form.get('txtIdFacultad', '')
#     fecha_creacion = request.form.get('txtFechaCreacion', '')
#     fecha_finalizacion = request.form.get('txtFechaFinalizacion', '')
#     id_lider = request.form.get('txtIdLider', '')
#     plan_estrategico = request.form.get('txtPlanEstrategico', '')
#     categoria_meta = request.form.get('txtCategoriaMeta', '')
#     estrategia_meta = request.form.get('txtEstrategiaMeta', '')
#     vision = request.form.get('txtVision', '')
#     objetivos = request.form.get('txtObjetivos', '')

#     datosGrupo = {
#         'id_grupo': id_grupo,
#         'nombre_grupo': nombre_grupo,
#         'codigo_grup_lac': codigo_grup_lac,
#         'categoria_colciencias': categoria_colciencias,
#         'area_conocimiento': area_conocimiento,
#         'id_facultad': id_facultad,
#         'fecha_creacion': fecha_creacion,
#         'fecha_finalizacion': fecha_finalizacion,
#         'id_lider': id_lider,
#         'plan_estrategico': plan_estrategico,
#         'categoria_meta': categoria_meta,
#         'estrategia_meta': estrategia_meta,
#         'vision': vision,
#         'objetivos': objetivos
#     }

#     if boton == 'Guardar':
#         objGrupo = Entidad(datosGrupo)
#         objControlEntidad.insert_data(objGrupo)
#         return redirect(url_for('idVistaGruposInvestigacion.vista_GruposInvestigacion'))
    
#     elif boton == 'Consultar':
#         objGrupo = objControlEntidad.buscarPorId('id_grupo', id_grupo)
#         if objGrupo:
#             datosGrupo = objGrupo.__dict__
#         else:
#             mensaje = "El Grupo de Investigación no se encontró."
    
#     elif boton == 'Modificar':
#         objGrupo = Entidad(datosGrupo)
#         objControlEntidad.update_data('id_grupo', id_grupo, objGrupo)
#         return redirect(url_for('idVistaGruposInvestigacion.vista_GruposInvestigacion'))
    
#     elif boton == 'Borrar':
#         objControlEntidad.delete_data('id_grupo', id_grupo)
#         return redirect(url_for('idVistaGruposInvestigacion.vista_GruposInvestigacion'))

#     # Renderizar la plantilla al final, pasando las variables necesarias
#     return render_template('vistaGruposInvestigacion.html', arregloGrupos=arregloGrupos, mensaje=mensaje, grupo=datosGrupo)
