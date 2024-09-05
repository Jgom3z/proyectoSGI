from flask import Flask, render_template, request, jsonify, Blueprint
from datetime import datetime
import requests
import json

# Crear un Blueprint
vistaGruposInvestigacion = Blueprint('idVistaGruposInvestigacion', __name__, template_folder='templates')

projectName = 'SGI'
API_URL = "http://190.217.58.246:5185/api/{projectName}/procedures/execute"

@vistaGruposInvestigacion.route('/vistaGruposInvestigacion', methods=['GET'])
def vista_grupos_investigacion():
    # Obtener datos de grupos
    select_data_grupos = {
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

    response_grupos = requests.post(API_URL, json=select_data_grupos)
    if response_grupos.status_code != 200:
        return f"Error al consultar la API: {response_grupos.status_code}"
    
    data_grupos = response_grupos.json()
    if 'result' in data_grupos and data_grupos['result']:
        grupos_str = data_grupos['result'][0]['result']
        grupos = json.loads(grupos_str)
    else:
        grupos = []

    # Obtener datos de facultades
    select_data_facultades = {
        "projectName": 'SGI',
        "procedure": "select_json_entity",
        "parameters": {
            "table_name": "inv_facultad",
            "json_data": {},
            "where_condition": "",
            "select_columns": "id_facultad, nombre_facultad",
            "order_by": "id_facultad",
            "limit_clause": ""
        }
    }

    response_facultades = requests.post(API_URL, json=select_data_facultades)
    if response_facultades.status_code != 200:
        return f"Error al consultar la API: {response_facultades.status_code}"

    data_facultades = response_facultades.json()
    if 'result' in data_facultades and data_facultades['result']:
        facultades_str = data_facultades['result'][0]['result']
        facultades = json.loads(facultades_str)
    else:
        facultades = []

    #obtener datos de investigador lider
    
    select_data_investigadores = {
        "projectName": 'SGI',
        "procedure": "select_json_entity",
        "parameters": {
            "table_name": "inv_investigadores",
            "json_data": {},
            "where_condition": "",
            "select_columns": "id_investigador, nombre_investigador",
            "order_by": "id_investigador",
            "limit_clause": ""
        }
    }

    response_investigadores = requests.post(API_URL, json=select_data_investigadores)
    if response_investigadores.status_code != 200:
        return f"Error al consultar la API: {response_investigadores.status_code}"

    select_data_investigadores = response_investigadores.json()
    if 'result' in select_data_investigadores and select_data_investigadores['result']:
        investigadores_str = select_data_investigadores['result'][0]['result']
        investigadores = json.loads(investigadores_str)
    else:
        investigadores = []

 



    # Pasar los datos a la plantilla
    ths = ['grupos de investigacion', 'codigo grup lac', 'categoria colciencias', 'facultad', 'lider del grupo']
    return render_template('vistaGruposInvestigacion.html', grupos=grupos, facultades=facultades, investigadores = investigadores, ths=ths)

#PARA EL MODAL
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

    # Validar si 'fecha_finalizacion' está vacía o no se proporcionó
    if not form_data["fecha_finalizacion"]:
        form_data["fecha_finalizacion"] = None

     # Debug: Imprimir el formulario de datos
    print("Form Data: ", form_data)  

    # Enviar los datos a la API
    response = requests.post(API_URL.format(projectName=projectName), json={
        "procedure": "insert_json_entity",  # Supongamos que tienes un procedimiento almacenado para insertar
        "parameters":{
            "table_name":"inv_grupos",
            "json_data": form_data
                
        }
    } 
    )

       # Debug: Imprimir el estado de la respuesta y su contenido
    print("Response Status Code: ", response.status_code)
    print("Response Content: ", response.content)

    # Verificar la respuesta de la API
    if response.status_code == 200:
        output_params = response.json().get("outputParams", {})
        mensaje = output_params.get("mensaje", "Operación exitosa")
        return jsonify({"message": mensaje}), 200
    else:
        # Mostrar el mensaje de error detallado
        error_message = response.json().get("message", "Error desconocido al guardar los datos")
        return jsonify({"message": f"Error al guardar los datos: {error_message}"}), 500
    
@vistaGruposInvestigacion.route("/deletegrupo", methods = ['POST'])
def delete_grupo():
    # Captura los datos del formulario enviado
    print(request)
    form_data = {"id_grupo": request.json.get('id_grupo')}

     # Debug: Imprimir el formulario de datos
    print("Form Data: ", form_data)  

    # Enviar los datos a la API
    response = requests.post(API_URL.format(projectName=projectName), json={
        "procedure": "delete_json_entity", 
        "parameters":{
            "table_name":"inv_grupos",
            "where_condition": f"id_grupo = {form_data['id_grupo']}"
                
        }
    } 
    )

    # Debug: Imprimir el estado de la respuesta y su contenido
    print("Response Status Code: ", response.status_code)
    print("Response Content: ", response.content)

    # Verificar la respuesta de la API
    if response.status_code == 200:
        output_params = response.json().get("outputParams", {})
        mensaje = output_params.get("mensaje", "Operación exitosa")
        return jsonify({"message": mensaje}), 200
    else:
        # Mostrar el mensaje de error detallado
        error_message = response.json().get("message", "Error desconocido al eliminar el grupo")
        return jsonify({"message": f"Error al eliminar el grupo: {error_message}"}), 500
    
@vistaGruposInvestigacion.route("/updategrupo", methods = ['POST'])
def update_grupo():
    # Captura los datos del formulario enviado
    print(request)
    # Captura el ID del grupo y los demás datos del formulario enviado
    id_grupo = request.form.get('id_grupo')
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

     # Verifica y limpia las fechas
    
    if form_data["fecha_creacion"]:
        form_data["fecha_creacion"] = datetime.strptime(form_data["fecha_creacion"], "%Y-%m-%d").date().strftime("%Y-%m-%d")
    if form_data["fecha_finalizacion"]:
        form_data["fecha_finalizacion"] = datetime.strptime(form_data["fecha_finalizacion"], "%Y-%m-%d").date().strftime("%Y-%m-%d")
    else:
        form_data["fecha_finalizacion"] = None

     # Debug: Imprimir el formulario de datos
    print("Form Data: ", form_data)
    print("ID Grupo: ", id_grupo)  

    # Enviar los datos a la API
    response = requests.post(API_URL.format(projectName=projectName), json={
        "procedure": "update_json_entity",  # Supongamos que tienes un procedimiento almacenado para insertar
        "parameters":{
            "table_name":"inv_grupos",
            "json_data": form_data,
            "where_condition": f"id_grupo = {id_grupo}"
                
        }
    } 
    )

       # Debug: Imprimir el estado de la respuesta y su contenido
    print("Response Status Code: ", response.status_code)
    print("Response Content: ", response.content)

    # Verificar la respuesta de la API
    if response.status_code == 200:
        output_params = response.json().get("outputParams", {})
        mensaje = output_params.get("mensaje", "Operación exitosa")
        return jsonify({"message": mensaje}), 200
    else:
        # Mostrar el mensaje de error detallado
        error_message = response.json().get("message", "Error desconocido al actualizar el grupo")
        return jsonify({"message": f"Error al actualizar el grupo: {error_message}"}), 500
