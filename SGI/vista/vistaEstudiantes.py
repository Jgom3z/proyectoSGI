from flask import Flask, render_template, request, jsonify, Blueprint
import requests
import json

# Crear un Blueprint
vistaEstudiantes = Blueprint('idVistaEstudiantes', __name__, template_folder='templates')

projectName = 'SGI'
API_URL = "http://190.217.58.246:5185/api/{projectName}/procedures/execute"

@vistaEstudiantes.route('/vistaEstudiantes', methods=['GET'])
def vista_estudiantes():
    # Obtener datos de estudiante
    select_data_estudiantes = {
        "projectName": 'SGI',
        "procedure": "select_json_entity",
        "parameters": {
            "table_name": "inv_estudiantes",
            "json_data": {
                "estado": "En Progreso"  # Ajusta según las necesidades del filtro si aplica
            },
            "where_condition": "",  # Añade condiciones de filtro si las hay
            "select_columns": "identificacion,nombre_estudiante, codigo, correo,id_facultad",
            "order_by": "id_estudiante",  # Puedes ordenar por el campo que prefieras
            "limit_clause": ""  # Agrega un límite si es necesario  
        }
        # "parameters": {
        #     "table_name": "inv_estudiantes e INNER JOIN inv_facultad f ON e.id_facultad::integer = f.id_facultad",
        #     "json_data": {
        #         "estado": "En Progreso"  # Ajusta según las necesidades del filtro si aplica
        #     },
        #     "where_condition": "",  # Añade condiciones de filtro si las hay
        #     "select_columns": "e.identificacion, e.nombre_estudiante AS nombre_completo, e.codigo, e.correo, f.nombre_facultad",
        #     "order_by": "e.id_estudiante",  # Puedes ordenar por el campo que prefieras
        #     "limit_clause": ""  # Agrega un límite si es necesario  
        # }
    }

    try:
        response_estudiantes = requests.post(API_URL.format(projectName=projectName), json=select_data_estudiantes)
        response_estudiantes.raise_for_status()  # Lanza un error si la respuesta es un error HTTP
        data_estudiantes = response_estudiantes.json()
        
        # Verificar la estructura de los datos recibidos
        if 'result' in data_estudiantes and data_estudiantes['result']:
            estudiantes_str = data_estudiantes['result'][0].get('result', '')
            if estudiantes_str:
                estudiantes = json.loads(estudiantes_str)
            else:
                estudiantes = []
        else:
            estudiantes = []
    except (requests.RequestException, json.JSONDecodeError) as e:
        print(f"Error al consultar la API de estudiantes: {e}")
        estudiantes = []

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

    try:
        response_facultades = requests.post(API_URL.format(projectName=projectName), json=select_data_facultades)
        response_facultades.raise_for_status()  # Lanza un error si la respuesta es un error HTTP
        data_facultades = response_facultades.json()
        
        # Verificar la estructura de los datos recibidos
        if 'result' in data_facultades and data_facultades['result']:
            facultades_str = data_facultades['result'][0].get('result', '')
            if facultades_str:
                facultades = json.loads(facultades_str)
            else:
                facultades = []
        else:
            facultades = []
    except (requests.RequestException, json.JSONDecodeError) as e:
        print(f"Error al consultar la API de facultades: {e}")
        facultades = []

    # Pasar los datos a la plantilla
    ths = ['Identificación', 'Nombre completo', 'Código', 'Correo', 'Facultad']
    return render_template('vistaEstudiantes.html', estudiantes=estudiantes, facultades=facultades, ths=ths)

# Métodos para crear, actualizar y eliminar estudiantes
@vistaEstudiantes.route("/createestudiante", methods=['POST'])
def create_estudiante():
    form_data = {
        "codigo": request.form.get('codigo'),
        "id_facultad": request.form.get('id_facultad'),
        "correo": request.form.get('correo'),
        "identificacion": request.form.get('identificacion'),
        "nombre_estudiante": request.form.get('nombre_estudiante')
    }

    try:
        response = requests.post(API_URL.format(projectName=projectName), json={
            "procedure": "insert_json_entity",
            "parameters": {
                "table_name": "inv_estudiantes",
                "json_data": form_data
            }
        })
        response.raise_for_status()
        return jsonify({"message": "Datos guardados exitosamente"}), 200
    except (requests.RequestException, json.JSONDecodeError) as e:
        print(f"Error al guardar los datos del estudiante: {e}")
        return jsonify({"message": "Error al guardar los datos"}), 500

@vistaEstudiantes.route("/deleteestudiante", methods=['POST'])
def delete_estudiante():
    form_data = {
        "codigo": request.form.get('codigo')
    }

    try:
        response = requests.post(API_URL.format(projectName=projectName), json={
            "procedure": "delete_json_entity",
            "parameters": {
                "table_name": "inv_estudiantes",
                "where_condition": f"codigo = '{form_data['codigo']}'"
            }
        })
        response.raise_for_status()
        return jsonify({"message": "Estudiante Eliminado exitosamente"}), 200
    except (requests.RequestException, json.JSONDecodeError) as e:
        print(f"Error al eliminar el estudiante: {e}")
        return jsonify({"message": "Error al eliminar el estudiante"}), 500

@vistaEstudiantes.route("/updateestudiante", methods=['POST'])
def update_estudiante():
    form_data = {
        "codigo": request.form.get('codigo'),
        "id_facultad": request.form.get('id_facultad'),
        "correo": request.form.get('correo'),
        "identificacion": request.form.get('identificacion'),
        "nombre_estudiante": request.form.get('nombre_estudiante')
    }

    try:
        response = requests.post(API_URL.format(projectName=projectName), json={
            "procedure": "update_json_entity",  # Cambiado de delete a update
            "parameters": {
                "table_name": "inv_estudiantes",
                "json_data": form_data,
                "where_condition": f"codigo = '{form_data['codigo']}'"
            }
        })
        response.raise_for_status()
        return jsonify({"message": "Estudiante actualizado exitosamente"}), 200
    except (requests.RequestException, json.JSONDecodeError) as e:
        print(f"Error al actualizar el estudiante: {e}")
        return jsonify({"message": "Error al actualizar el estudiante"}), 500
