import requests
import json
import os
projectName = os.getenv('PROJECT_NAME')
API_URL = os.getenv('API_URL')


def investigadores():    
    select_data = {
            "projectName": projectName,
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
    
    response = requests.post(API_URL, json=select_data)
    if response.status_code != 200:
        return f"Error al consultar la API: {response.status_code}"

    select_data = response.json()
    if 'result' in select_data and select_data['result']:
        data_str = select_data['result'][0]['result']
        result = json.loads(data_str)
    else:
        result = []
    
    return result

def lineas():    
    select_data = {
            "projectName": projectName,
            "procedure": "select_json_entity",
            "parameters": {
                "table_name": "inv_linea_grupo",
                "json_data": {},
                "where_condition": "",
                "select_columns": "id_linea_grupo, nombre_linea",
                "order_by": "nombre_linea",
                "limit_clause": ""
            }
        }
    
    response = requests.post(API_URL, json=select_data)
    if response.status_code != 200:
        return f"Error al consultar la API: {response.status_code}"

    data = response.json()
    if 'result' in data and data['result']:
        data_str = data['result'][0]['result']
        result = json.loads(data_str)
    else:
        result = []
    
    return result

def estudiantes():    
    select_data = {
            "projectName": projectName,
            "procedure": "select_json_entity",
            "parameters": {
                "table_name": "INV_ESTUDIANTES",
                "json_data": {},
                "where_condition": "",
                "select_columns": "id_estudiante, nombre_estudiante",
                "order_by": "nombre_estudiante",
                "limit_clause": ""
            }
        }
    
    response = requests.post(API_URL, json=select_data)
    if response.status_code != 200:
        return f"Error al consultar la API: {response.status_code}"

    select_data = response.json()
    if 'result' in select_data and select_data['result']:
        data_str = select_data['result'][0]['result']
        result = json.loads(data_str)
    else:
        result = []
    return result

def proyectos():    
    select_data = {
            "projectName": projectName,
            "procedure": "select_json_entity",
            "parameters": {
                "table_name": "inv_proyecto",
                "json_data": {},
                "where_condition": "",
                "select_columns": "id_proyecto, nombre_proyecto",
                "order_by": "nombre_proyecto",
                "limit_clause": ""
            }
        }
    
    response = requests.post(API_URL, json=select_data)
    if response.status_code != 200:
        return f"Error al consultar la API: {response.status_code}"

    select_data = response.json()
    if 'result' in select_data and select_data['result']:
        data_str = select_data['result'][0]['result']
        result = json.loads(data_str)
    else:
        result = []
    return result

def semilleros():    
    select_data = {
            "projectName": projectName,
            "procedure": "select_json_entity",
            "parameters": {
                "table_name": "inv_semilleros",
                "json_data": {},
                "where_condition": "",
                "select_columns": "id_semillero, nombre_semillero",
                "order_by": "nombre_semillero",
                "limit_clause": ""
            }
        }
    
    response = requests.post(API_URL, json=select_data)
    if response.status_code != 200:
        return f"Error al consultar la API: {response.status_code}"

    select_data = response.json()
    if 'result' in select_data and select_data['result']:
        data_str = select_data['result'][0]['result']
        result = json.loads(data_str)
    else:
        result = []
    return result


def grupos():    
    select_data = {
            "projectName": projectName,
            "procedure": "select_json_entity",
            "parameters": {
                "table_name": "inv_grupos",
                "json_data": {},
                "where_condition": "",
                "select_columns": "id_grupo, nombre_grupo",
                "order_by": "nombre_grupo",
                "limit_clause": ""
            }
        }
    
    response = requests.post(API_URL, json=select_data)
    if response.status_code != 200:
        return f"Error al consultar la API: {response.status_code}"

    data = response.json()
    if 'result' in data and data['result']:
        data_str = data['result'][0]['result']
        result = json.loads(data_str)
    else:
        result = []
    
    return result

def facultad():
    select_data = {
        "projectName": projectName,
        "procedure": "select_json_entity",
        "parameters": {
            "table_name": "inv_facultad",
            "json_data": {},
            "where_condition": "",
            "select_columns": "id_facultad, nombre_facultad",
            "order_by": "nombre_facultad",
            "limit_clause": ""
        }
    }

    # Realiza la solicitud a la API
    response = requests.post(API_URL, json=select_data)

    # Verifica si la solicitud fue exitosa
    if response.status_code != 200:
        return f"Error al consultar la API: {response.status_code}"

    # Verifica si el contenido de la respuesta es válido
    data = response.json()
    if 'result' in data and data['result']:
        data_str = data['result'][0].get('result')  # Utiliza get() para evitar errores si 'result' es None
        if data_str:  # Verifica que data_str no sea None o vacío
            try:
                result = json.loads(data_str)
            except json.JSONDecodeError:
                return "Error al decodificar el JSON de la API."
        else:
            result = []  # Si data_str es None, devuelve una lista vacía
    else:
        result = []
