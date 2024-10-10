from flask import Flask, render_template, request, jsonify, Blueprint
from datetime import datetime
import requests
import json

# Crear un Blueprint
vistaLineasInvestigacion = Blueprint('idVistaLineasInvestigacion', __name__, template_folder='templates')

projectName = 'SGI'
API_URL = "http://190.217.58.246:5185/api/{projectName}/procedures/execute"

@vistaLineasInvestigacion.route('/vistaLineasInvestigacion', methods=['GET'])
def vista_lineas_investigacion():
    # Obtener datos de lineas
    select_data_lineas = {
        "projectName": 'SGI',
        "procedure": "select_json_entity",
        "parameters": {
            "table_name": "inv_linea_grupo l LEFT JOIN inv_grupos g ON g.id_grupo = l.id_grupo INNER JOIN inv_investigadores i ON i.id_investigador = l.id_lider LEFT JOIN inv_facultad f ON f.id_facultad = i.id_facultad",
            "json_data": {},
            "where_condition": "",
            "select_columns": "l.id_linea_grupo, l.nombre_linea, g.nombre_grupo, i.nombre_investigador, l.estado, f.nombre_facultad",
            "order_by": "l.id_linea_grupo",
            "limit_clause": ""
        }
    }

    # Realiza la solicitud a la API
    response_lineas = requests.post(API_URL, json=select_data_lineas)
    if response_lineas.status_code != 200:
        return f"Error al consultar la API: {response_lineas.status_code}"

    # Procesa la respuesta
    data_lineas = response_lineas.json()
    if 'result' in data_lineas and data_lineas['result']:
        lineas_str = data_lineas['result'][0]['result']
        lineas = json.loads(lineas_str)
    else:
        lineas = []

    # Obtener datos de grupos
    select_data_grupos = {
        "projectName": 'SGI',
        "procedure": "select_json_entity",
        "parameters": {
            "table_name": "inv_grupos",
            "json_data": {},
            "where_condition": "",
            "select_columns": "id_grupo, nombre_grupo",
            "order_by": "id_grupo",
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

    # Obtener datos de lider
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

    data_investigadores = response_investigadores.json()
    if 'result' in data_investigadores and data_investigadores['result']:
        investigadores_str = data_investigadores['result'][0]['result']
        investigadores = json.loads(investigadores_str)
    else:
        investigadores = []

    # Obtener datos de proyectos asociados a la linea
    select_data_proyectos = {
        "projectName": "SGI",
        "procedure": "select_json_entity",
        "parameters": {
            "table_name": "inv_proyecto", 
            "json_data": {},
            "where_condition": "",  
            "select_columns": "nombre_proyecto, fecha_inicio, fecha_fin",
            "order_by": "nombre_proyecto",
            "limit_clause": ""
        }
    }

    response_proyectos = requests.post(API_URL, json=select_data_proyectos)

    if response_proyectos.status_code != 200:
        return f"Error al consultar la API: {response_proyectos.status_code}"

    data_proyectos = response_proyectos.json()

    # Verifica si 'result' existe y no está vacío
    if 'result' in data_proyectos and data_proyectos['result']:
        proyectos_str = data_proyectos['result'][0].get('result')  # Utiliza .get() para evitar el NoneType error
        
        # Verifica si 'proyectos_str' no es None
        if proyectos_str:
            try:
                proyectos = json.loads(proyectos_str)  # Carga solo si no es None
            except json.JSONDecodeError as e:
                print(f"Error al decodificar JSON: {e}")
                proyectos = []
        else:
            print("El campo 'result' es None o vacío.")
            proyectos = []
    else:
        print("No se encontraron resultados en la respuesta de la API.")
        proyectos = []

    # Datos de consulta para investigadores asociados
    select_data_investigadores_asociados = {
        "procedure": "select_json_entity",
        "parameters": {
            "table_name": "inv_investigadores",
            "json_data": {},
            "where_condition": "JOIN inv_investigador_proyecto ON inv_investigadores.id_investigador = inv_investigador_proyecto.id_investigador",
            "select_columns": "inv_investigadores.nombre_investigador, inv_investigador_proyecto.estado",
            "order_by": "inv_investigadores.id_investigador",
            "limit_clause": ""
        }
    }

    response_investigadores_asociados = requests.post(API_URL, json=select_data_investigadores_asociados)

    # Verificar si la respuesta es exitosa
    if response_investigadores_asociados.status_code != 200:
        return f"Error al consultar la API: {response_investigadores_asociados.status_code}"

    # Convertir la respuesta a JSON
    data_investigadores_asociados = response_investigadores_asociados.json()

    # Verificar si 'result' está en la respuesta y contiene datos válidos
    if 'result' in data_investigadores_asociados and data_investigadores_asociados['result']:
        investigadores_asociados_str = data_investigadores_asociados['result'][0].get('result')
        
        # Validar si investigadores_asociados_str no es None y es una cadena válida
        if investigadores_asociados_str:
            try:
                investigadores_asociados = json.loads(investigadores_asociados_str)
            except json.JSONDecodeError as e:
                return f"Error al decodificar JSON: {e}"
        else:
            investigadores_asociados = []  # Maneja el caso cuando investigadores_asociados_str es None o vacío
    else:
        investigadores_asociados = []  # Maneja el caso cuando 'result' no está presente o está vacío

    # Obtener datos de semilleros
    select_data_semilleros = {
        "procedure": "select_json_entity",
        "parameters": {
            "table_name": "inv_semilleros s JOIN inv_investigadores i ON s.id_lider = i.id_investigador",
            "json_data": {},
            "where_condition": "",
            "select_columns": "s.nombre_semillero, s.fecha_inicio, s.fecha_fin, i.nombre_investigador AS nombre_lider",
            "order_by": "s.id_semillero",
            "limit_clause": ""
        }
    }

    response_semilleros = requests.post(API_URL, json=select_data_semilleros)

    if response_semilleros.status_code != 200:
        return f"Error al consultar la API: {response_semilleros.status_code}"

    data_semilleros = response_semilleros.json()

    if 'result' in data_semilleros and data_semilleros['result']:
        semilleros_str = data_semilleros['result'][0]['result']
        if semilleros_str:  # Verifica si semilleros_str no es None ni vacío
            try:
                semilleros = json.loads(semilleros_str)
            except json.JSONDecodeError as e:
                return f"Error al decodificar JSON: {e}"
        else:
            semilleros = []  # Maneja el caso cuando semilleros_str es None o vacío
    else:
        semilleros = []  # Maneja el caso cuando 'result' no está presente o está vacío

    # Pasar los datos a la plantilla
    ths = ['Linea de investigación', 'Grupo de investigación', 'Jefe de linea', 'Estado', 'facultad']
    return render_template('vistaLineasInvestigacion.html', lineas=lineas, grupos=grupos, investigadores=investigadores, semilleros=semilleros, investigadores_asociados=investigadores_asociados, proyectos=proyectos, ths=ths)


# PARA EL MODAL
@vistaLineasInvestigacion.route("/createlinea", methods=['POST'])
def create_linea():
    # Captura los datos del formulario enviado
    print(request)
    form_data = {
        "nombre_linea": request.form.get('nombre_linea'),
        "id_grupo": request.form.get('id_grupo'),
        "descripcion": request.form.get('descripcion'),
        "id_lider": request.form.get('id_lider'),
        "temas_de_trabajo": request.form.get('temas_de_trabajo'),
        "objetivos": request.form.get('objetivos'),
        "vision": request.form.get('vision'),
        "estado": request.form.get('estado'),
        "mision": request.form.get('mision')
    } 

    # Debug: Imprimir el formulario de datos
    print("Form Data: ", form_data)  

    # Enviar los datos a la API
    response = requests.post(API_URL.format(projectName=projectName), json={
        "procedure": "insert_json_entity",  # Supongamos que tienes un procedimiento almacenado para insertar
        "parameters": {
            "table_name": "inv_linea_grupo",
            "json_data": form_data
        }
    })

    # Debug: Imprimir el estado de la respuesta y su contenido
    print("Response Status Code: ", response.status_code)
    print("Response Content: ", response.content)

    # Verificar la respuesta de la API
    if response.status_code == 200:
        output_params = response.json().get("outputParams", {})
        mensaje = output_params.get("mensaje", "Operación exitosa")
        return jsonify({"message": mensaje}), 200  # Respuesta exitosa
    else:
        # Mostrar el mensaje de error detallado
        error_message = response.json().get("message", "Error desconocido al guardar los datos")
        return jsonify({"message": f"Error al guardar los datos: {error_message}"}), 500  # Respuesta de error

@vistaLineasInvestigacion.route("/deletelinea", methods=['POST'])
def linea_grupo():
    # Captura los datos del formulario enviado
    print(request)
    form_data = {"id_linea_grupo": request.json.get('id_linea_grupo')}

    # Debug: Imprimir el formulario de datos
    print("Form Data: ", form_data)  

    # Enviar los datos a la API
    response = requests.post(API_URL.format(projectName=projectName), json={
        "procedure": "delete_json_entity", 
        "parameters": {
            "table_name": "inv_linea_grupo",
            "where_condition": f"id_linea_grupo = {form_data['id_linea_grupo']}"
        }
    })

    # Debug: Imprimir el estado de la respuesta y su contenido
    print("Response Status Code: ", response.status_code)
    print("Response Content: ", response.content)

    # Verificar la respuesta de la API
    if response.status_code == 200:
        output_params = response.json().get("outputParams", {})
        mensaje = output_params.get("mensaje", "Operación exitosa")
        return jsonify({"message": mensaje}), 200  # Respuesta exitosa
    else:
        # Mostrar el mensaje de error detallado
        error_message = response.json().get("message", "Error desconocido al eliminar la linea")
        return jsonify({"message": f"Error al eliminar la linea: {error_message}"}), 500  # Respuesta de error

@vistaLineasInvestigacion.route("/updatelinea", methods=['POST'])
def update_linea():
    # Captura los datos del formulario enviado
    print(request)
    # Captura el ID de la linea y los demás datos del formulario enviado
    id_linea_grupo = request.form.get('id_linea_grupo')
    form_data = {
        "nombre_linea": request.form.get('nombre_linea'),
        "id_grupo": request.form.get('id_grupo'),
        "descripcion": request.form.get('descripcion'),
        "id_lider": request.form.get('id_lider'),
        "temas_de_trabajo": request.form.get('temas_de_trabajo'),
        "objetivos": request.form.get('objetivos'),
        "vision": request.form.get('vision'),
        "estado": request.form.get('estado'),
        "mision": request.form.get('mision')
    }

    # Debug: Imprimir el formulario de datos
    print("Form Data: ", form_data)
    print("ID linea: ", id_linea_grupo)  

    # Enviar los datos a la API
    response = requests.post(API_URL.format(projectName=projectName), json={
        "procedure": "update_json_entity",  # Supongamos que tienes un procedimiento almacenado para actualizar
        "parameters": {
            "table_name": "inv_linea_grupo",
            "json_data": form_data,
            "where_condition": f"id_linea_grupo = {id_linea_grupo}"
        }
    })

    print("Response Status Code: ", response.status_code)
    print("Response Content: ", response.content)

    if response.status_code == 200:
        output_params = response.json().get("outputParams", {})
        mensaje = output_params.get("mensaje", "Operación exitosa")
        return jsonify({"message": mensaje}), 200  # Respuesta exitosa
    else:
        error_message = response.json().get("message", "Error desconocido al actualizar el grupo")
        return jsonify({"message": f"Error al actualizar el grupo: {error_message}"}), 500  # Respuesta de error