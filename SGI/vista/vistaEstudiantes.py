from flask import Flask, render_template, request, jsonify, Blueprint
from datetime import datetime
import requests
import json

# Crear un Blueprint
vistaEstudiantes = Blueprint('idVistaEstudiantes', __name__, template_folder='templates')

projectName = 'SGI'
API_URL = "http://190.217.58.246:5185/api/{projectName}/procedures/execute"

@vistaEstudiantes.route('/vistaEstudiantes', methods=['GET'])
def vista_estudiantes():
    # Obtener datos de estudiantes
    select_data_estudiantes = {
        "projectName": "SGI",
        "procedure": "select_json_entity",
        "parameters": {
            "table_name": "inv_estudiantes LEFT JOIN inv_facultad ON inv_estudiantes.id_facultad::VARCHAR = inv_facultad.id_facultad::VARCHAR",
            "json_data": {
                "estado": "En Progreso"
            },
            "where_condition": "",
            "select_columns": "inv_estudiantes.identificacion, inv_estudiantes.nombre_estudiante, inv_estudiantes.codigo, inv_estudiantes.correo, inv_facultad.nombre_facultad",
            "order_by": "inv_estudiantes.identificacion",
            "limit_clause": ""
        }
    }


    response_estudiantes = requests.post(API_URL, json=select_data_estudiantes)

    # Verificar que la solicitud fue exitosa
    if response_estudiantes.status_code != 200:
        return f"Error al consultar la API: {response_estudiantes.status_code}"

    # Intentar obtener la respuesta en formato JSON
    try:
        data_estudiantes = response_estudiantes.json()
    except json.JSONDecodeError:
        return "Error al decodificar la respuesta de la API como JSON"

    # Verificar si la respuesta contiene el campo 'result'
    if 'result' in data_estudiantes and data_estudiantes['result']:
        estudiantes_str = data_estudiantes['result'][0].get('result')

        # Verificar que estudiantes_str no sea None
        if estudiantes_str:
            try:
                estudiantes = json.loads(estudiantes_str)
            except json.JSONDecodeError:
                return "Error al decodificar 'estudiantes_str' como JSON"
        else:
            estudiantes = []  # No hay datos en 'result'
    else:
        estudiantes = []  # No hay resultados en la API


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



    # Pasar los datos a la plantilla
    ths = ['grupos de investigacion', 'codigo grup lac', 'categoria colciencias', 'facultad', 'lider del grupo']
    return render_template('vistaEstudiantes.html', estudiantes=estudiantes, facultades=facultades, ths=ths)
#PARA EL MODAL
@vistaEstudiantes.route("/createestudiante", methods = ['POST'])
def create_estudiante():
    # Captura los datos del formulario enviado
    print(request)
    form_data = {
    "codigo": request.form.get('codigo'),
    "id_facultad": request.form.get('id_facultad'),
    "correo": request.form.get('correo'),
    "identificacion": request.form.get('identificacion'),
    "nombre_estudiante": request.form.get('nombre_estudiante')
}


    
     # Debug: Imprimir el formulario de datos
    print("Form Data: ", form_data)  

    # Enviar los datos a la API
    response = requests.post(API_URL.format(projectName=projectName), json={
        "procedure": "insert_json_entity",  # Supongamos que tienes un procedimiento almacenado para insertar
        "parameters":{
            "table_name":"inv_estudiantes",
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
    
@vistaEstudiantes.route("/deleteestudiante", methods = ['POST'])
def delete_estudiante():
    # Captura los datos del formulario enviado
    print(request)
    form_data = {"id_estudiante": request.json.get('id_estudiante')}

     # Debug: Imprimir el formulario de datos
    print("Form Data: ", form_data)  

    # Enviar los datos a la API
    response = requests.post(API_URL.format(projectName=projectName), json={
        "procedure": "delete_json_entity", 
        "parameters":{
            "table_name":"inv_estudiantes",
            "where_condition": f"id_estudiante = {form_data['id_estudiante']}"
                
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
        error_message = response.json().get("message", "Error desconocido al eliminar el estudiante")
        return jsonify({"message": f"Error al eliminar el estudiante: {error_message}"}), 500
    
@vistaEstudiantes.route("/updateestudiante", methods = ['POST'])
def update_estudiante():
    # Captura los datos del formulario enviado
    print(request)
    # Captura el ID del estudiante y los demás datos del formulario enviado
    id_estudiante = request.form.get('id_estudiante')
    form_data = {
        "id_estudiante": request.form.get('id_estudiante'),  
         "codigo": request.form.get('codigo'),
        "id_facultad": request.form.get('id_facultad'),
        "correo": request.form.get('correo'),
        "identificacion": request.form.get('identificacion'),
        "nombre_estudiante": request.form.get('nombre_estudiante')
    }

     #
     # Debug: Imprimir el formulario de datos
    print("Form Data: ", form_data)
    print("ID Estudiante: ", id_estudiante)  

    # Enviar los datos a la API
    response = requests.post(API_URL.format(projectName=projectName), json={
        "procedure": "update_json_entity",  # Supongamos que tienes un procedimiento almacenado para actualizar
        "parameters": {
            "table_name": "inv_estudiantes",
            "json_data": form_data,
            "where_condition": f"id_estudiante = {id_estudiante}"
                
        }
    })

    print("Response Status Code: ", response.status_code)
    print("Response Content: ", response.content)

    if response.status_code == 200:
        output_params = response.json().get("outputParams", {})
        mensaje = output_params.get("mensaje", "Operación exitosa")
        return jsonify({"message": mensaje}), 200
    else:
        error_message = response.json().get("message", "Error desconocido al actualizar el estudiante")
        return jsonify({"message": f"Error al actualizar el estudiante: {error_message}"}), 500
    

@vistaEstudiantes.route('/get_estudiante', methods=['POST'])
def get_estudiante():
    id=request.form.get('id_estudiante') 
    # Obtener datos de estudiante
    select_data_estudiantes = {
        "projectName": 'SGI',
        "procedure": "select_json_entity",
        "parameters": {
            "table_name": "inv_estudiantes",
            "json_data": {
                "estado": "En Progreso"
            },
            "where_condition": f'id_estudiante={id}',
            "select_columns": "*",
            "order_by": "",
            "limit_clause": ""
        }
    }

    response_estudiantes = requests.post(API_URL, json=select_data_estudiantes)
    if response_estudiantes.status_code != 200:
        return f"Error al consultar la API: {response_estudiantes.status_code}"
    
    data_estudiantes = response_estudiantes.json()
    if 'result' in data_estudiantes and data_estudiantes['result']:
        estudiantes_str = data_estudiantes['result'][0]['result']
        estudiantes = json.loads(estudiantes_str)
    else:
        estudiantes = []
    print(estudiantes)
    return estudiantes