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

<<<<<<< HEAD
    response = requests.post(API_URL, json=select_data)

    if response.status_code != 200:
        return f"Error al consultar la API: {response.status_code}"

    data = response.json()
    if 'result' in data and data['result']:
        data_str = data['result'][0].get('result')
        if data_str:
=======
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
>>>>>>> 48d1917806ebf9f8935346552748eb850a8a59f9
            try:
                result = json.loads(data_str)
            except json.JSONDecodeError:
                return "Error al decodificar el JSON de la API."
        else:
<<<<<<< HEAD
            result = []
=======
            result = []  # Si data_str es None, devuelve una lista vacía
>>>>>>> 48d1917806ebf9f8935346552748eb850a8a59f9
    else:
        result = []

    return result

def productos():
    select_data = {
        "projectName": projectName,
        "procedure": "select_json_entity",
        "parameters": {
            "table_name": "inv_producto",
            "json_data": {},
            "where_condition": "",
            "select_columns": "id_producto, subtipo",
            "order_by": "subtipo",
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

    return result

def cofinanciadores():
    select_data = {
        "projectName": projectName,
        "procedure": "select_json_entity",
        "parameters": {
            "table_name": "inv_cofinanciador",
            "json_data": {},
            "where_condition": "",
            "select_columns": "id_cofinanciador, institucion",
            "order_by": "institucion",
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

    return result

def productos():
    select_data = {
        "projectName": projectName,
        "procedure": "select_json_entity",
        "parameters": {
            "table_name": "inv_producto",
            "json_data": {},
            "where_condition": "",
            "select_columns": "id_producto, subtipo",
            "order_by": "subtipo",
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

    return result

def cofinanciadores():
    select_data = {
        "projectName": projectName,
        "procedure": "select_json_entity",
        "parameters": {
            "table_name": "inv_cofinanciador",
            "json_data": {},
            "where_condition": "",
            "select_columns": "id_cofinanciador, institucion",
            "order_by": "institucion",
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

    return result



