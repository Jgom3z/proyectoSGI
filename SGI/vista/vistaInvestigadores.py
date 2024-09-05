from flask import Flask, render_template, request, jsonify, Blueprint
import requests
import json

# Crear un Blueprint
vistaInvestigadores = Blueprint('idVistaInvestigadores', __name__, template_folder='templates')

projectName = 'SGI'
API_URL = "http://190.217.58.246:5185/api/{projectName}/procedures/execute"

@vistaInvestigadores.route('/vistaInvestigadores', methods=['GET'])
def vista_investigadores():
    select_data_investigadores = {
    "projectName": "SGI",
    "procedure": "select_json_entity",
    "parameters": {
        "table_name": "inv_investigadores i INNER JOIN inv_linea_investigador li ON i.id_investigador = li.id_investigador INNER JOIN inv_linea_grupo lg ON li.id_linea = li.id_linea",
        "json_data": {
            "estado": "En Progreso"
        },
        "where_condition": "",
        "select_columns": "i.nombre_investigador, lg.nombre_linea, li.estado",
        "order_by": "i.nombre_investigador",
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

   
    ths = ['Investigador', 'Linea de investigación', 'Estado']
    return render_template('vistaInvestigadores.html',  facultades=facultades, investigadores = investigadores, ths=ths)

@vistaInvestigadores.route("/createinvestigador", methods = ['POST'])
def create_investigador():
    print(request)
    form_data = {       
    "cedula": request.form.get('cedula'),
    "nombre_investigador": request.form.get('nombre_investigador'),
    "categoria_institucion": request.form.get('categoria_institucion'),
    "id_facultad": request.form.get('id_facultad'),
    "categoria_colciencias": request.form.get('categoria_colciencias'),
    "orcid": request.form.get('orcid'),
    "tipo_contrato": request.form.get('tipo_contrato'),
    "nivel_de_formacion": request.form.get('nivel_de_formacion'),
    "correo": request.form.get('correo'),
    "telefono": request.form.get('telefono'),
    "fecha_inicio": request.form.get('fecha_inicio'),
    "fecha_final": request.form.get('fecha_final'),
    "cvlac": request.form.get('cvlac'),
    "categoria_colciencias_esperada": request.form.get('categoria_colciencias_esperada')
    } 

    if not form_data["fecha_final"]:
        form_data["fecha_final"] = None

    print("Form Data: ", form_data)  

    response = requests.post(API_URL.format(projectName=projectName), json={
        "procedure": "insert_json_entity", 
        "parameters":{
            "table_name":"inv_investigadores",
            "json_data": form_data
                
        }
    } 
    )

    print("Response Status Code: ", response.status_code)
    print("Response Content: ", response.content)

    if response.status_code == 200:
        return ({"message": "Datos guardados exitosamente"}), 200
    else:
        error_message = response.json().get("message", "Error desconocido al guardar los datos")
        return jsonify({"message": f"Error al guardar los datos: {error_message}"}), 500
    
@vistaInvestigadores.route("/deleteinvestigador", methods = ['POST'])
def delete_investigador():
    print(request)  
    form_data = {
        "nombre_investigador": request.form.get('nombre_investigador')  
    } 

    print("Form Data: ", form_data)  

    response = requests.post(API_URL.format(projectName=projectName), json={
        "procedure": "delete_json_entity",  
        "parameters":{
            "table_name":"inv_investigadores",
            "where_condition": "nombre_investigador = nombre_investigador"
                
        }
    } 
    )

      
    print("Response Status Code: ", response.status_code)
    print("Response Content: ", response.content)

    
    if response.status_code == 200:
        return jsonify({"message": "Investigador Eliminado exitosamente"}), 200
    else:
        error_message = response.json().get("message", "Error desconocido al eliminar el investigador")
        return jsonify({"message": f"Error al eliminar el investigador: {error_message}"}), 500
    
@vistaInvestigadores.route("/updateinvestigador", methods = ['POST'])
def update_investigador():
    print(request)
    form_data = {
    "cedula": request.form.get('cedula'),
    "nombre_investigador": request.form.get('nombre_investigador'),
    "categoria_institucion": request.form.get('categoria_institucion'),
    "id_facultad": request.form.get('id_facultad'),
    "categoria_colciencias": request.form.get('categoria_colciencias'),
    "orcid": request.form.get('orcid'),
    "tipo_contrato": request.form.get('tipo_contrato'),
    "nivel_de_formacion": request.form.get('nivel_de_formacion'),
    "correo": request.form.get('correo'),
    "telefono": request.form.get('telefono'),
    "fecha_inicio": request.form.get('fecha_inicio'),
    "fecha_final": request.form.get('fecha_finalizacion'),
    "cvlac": request.form.get('cvlac'),
    "categoria_colciencias_esperada": request.form.get('categoria_colciencias_esperada')

    }  

    print("Form Data: ", form_data)  

    response = requests.post(API_URL.format(projectName=projectName), json={
        "procedure": "delete_json_entity",  # Supongamos que tienes un procedimiento almacenado para insertar
        "parameters":{
            "table_name":"inv_investigadores",
            "json_data": form_data,
            "where_condition": "nombre_investigador = nombre_investigador"
                
        }
    } 
    )

    print("Response Status Code: ", response.status_code)
    print("Response Content: ", response.content)

    if response.status_code == 200:
        return jsonify({"message": "Investigador actualizado exitosamente"}), 200
    else:
        # Mostrar el mensaje de error detallado
        error_message = response.json().get("message", "Error desconocido al actualizar el investigador")
        return jsonify({"message": f"Error al actualizar el investigador: {error_message}"}), 500
