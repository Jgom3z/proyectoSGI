from flask import Flask, render_template, request, jsonify, Blueprint
import requests
import json

# Crear un Blueprint
vistaProyectosFormacion = Blueprint('idVistaProyectosFormacion ', __name__, template_folder='templates')

projectName = 'SGI'
API_URL = "http://190.217.58.246:5185/api/{projectName}/procedures/execute"

@vistaProyectosFormacion.route('/vistaProyectosFormacion', methods=['GET'])
def vista_proyectos_formacion():
    # Inicializa la variable
    proyectosf = []

    # Define la estructura de la consulta
    select_data_proyectosf = {
        "projectName": 'SGI',
        "procedure": "select_json_entity",
        "parameters": {
            "table_name": "inv_proyecto_formacion pf "
                        "INNER JOIN inv_proyecto p ON pf.id_proyecto = p.id_proyecto "
                        "INNER JOIN inv_investigador i ON pf.id_investigador = i.id_investigador",
            "json_data": {
                "estado": "En Progreso"  # Ajusta esta condición según sea necesario
            },
            "where_condition": "",
            "select_columns": "pf.nombre_proy_form, pf.nivel, pf.modalidad, pf.cod_proy_form, p.nombre_proyecto, i.nombre_investigador",
            "order_by": "pf.id_proyecto_formacion",  # Asegúrate de usar el campo correcto para el orden
            "limit_clause": ""
        }
    }

    # Realiza la consulta a la API
    try:
        response_proyectosf = requests.post(API_URL, json=select_data_proyectosf)
        response_proyectosf.raise_for_status()  # Lanza un error para códigos de estado 4xx o 5xx
        data_proyectosf = response_proyectosf.json()
        
        # Procesa la respuesta
        if 'result' in data_proyectosf and data_proyectosf['result']:
            proyectosf_str = data_proyectosf['result'][0]['result']
            proyectosf = json.loads(proyectosf_str)
        else:
            proyectosf = []

    except requests.exceptions.RequestException as e:
        print(f"Error al consultar la API: {e}")
    except json.JSONDecodeError:
        print("Error al decodificar la respuesta JSON")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

    # Aquí puedes trabajar con la variable proyectosf
    print(proyectosf)

   
    #obtener datos de investigador 
    
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

    # Define la estructura de la consulta para semilleros
    select_data_semilleros = {
        "projectName": 'SGI',
        "procedure": "select_json_entity",
        "parameters": {
            "table_name": "inv_semilleros",  # Cambia esto por el nombre correcto de tu tabla
            "json_data": {},
            "where_condition": "",
            "select_columns": "id_semillero, nombre_semillero",  # Cambia esto por los nombres de columnas correctos
            "order_by": "id_semillero",  # Asegúrate de usar el campo correcto para el orden
            "limit_clause": ""
        }
    }

    # Realiza la consulta a la API
    response_semilleros = requests.post(API_URL, json=select_data_semilleros)
    if response_semilleros.status_code != 200:
        return f"Error al consultar la API: {response_semilleros.status_code}"

    data_semilleros = response_semilleros.json()
    if 'result' in data_semilleros and data_semilleros['result']:
        semilleros_str = data_semilleros['result'][0]['result']
        semilleros = json.loads(semilleros_str)
    else:
        semilleros = []

 
    # Estructura de la consulta para líneas de investigación
    select_data_lineas = {
        "projectName": 'SGI',
        "procedure": "select_json_entity",
        "parameters": {
            "table_name": "inv_linea_grupo",
            "json_data": {},
            "where_condition": "",
            "select_columns": "id_linea, nombre_linea",
            "order_by": "id_linea",
            "limit_clause": ""
        }
    }

    # Realiza la consulta a la API
    response_lineas = requests.post(API_URL, json=select_data_lineas)
    if response_lineas.status_code != 200:
        print(f"Error al consultar la API: {response_lineas.status_code}")
    else:
        print(response_lineas.text)  # Imprime la respuesta para depuración
        data_lineas = response_lineas.json()
        if 'result' in data_lineas and data_lineas['result']:
            lineas_str = data_lineas['result'][0]['result']
            lineas = json.loads(lineas_str) if lineas_str else []
        else:
            lineas = []

   # Estructura de la consulta para proyectos
    select_data_proyectos = {
        "projectName": 'SGI',
        "procedure": "select_json_entity",
        "parameters": {
            "table_name": "inv_proyecto",
            "json_data": {},
            "where_condition": "",
            "select_columns": "id_proyecto, nombre_proyecto",
            "order_by": "id_proyecto",
            "limit_clause": ""
        }
    }

    # Realiza la consulta a la API
    response_proyectos = requests.post(API_URL, json=select_data_proyectos)
    if response_proyectos.status_code != 200:
        print(f"Error al consultar la API: {response_proyectos.status_code}")
    else:
        print(response_proyectos.text)  # Imprime la respuesta para depuración
        data_proyectos = response_proyectos.json()
        if 'result' in data_proyectos and data_proyectos['result']:
            proyectos_str = data_proyectos['result'][0]['result']
            proyectos = json.loads(proyectos_str) if proyectos_str else []
        else:
            proyectos = []


    # Pasar los datos a la plantilla
    ths = ['grupos de investigacion', 'codigo grup lac', 'categoria colciencias', 'facultad', 'lider del grupo']
    return render_template('vistaProyectosFormacion.html', proyectosf=proyectosf, investigadores = investigadores, semilleros= semilleros, lineas=lineas, proyectos=proyectos, ths=ths)

#PARA EL MODAL
@vistaProyectosFormacion.route("/createproyectof", methods = ['POST'])
def create_proyectof():
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
        return jsonify({"message": "Datos guardados exitosamente"}), 200
    else:
        # Mostrar el mensaje de error detallado
        error_message = response.json().get("message", "Error desconocido al guardar los datos")
        return jsonify({"message": f"Error al guardar los datos: {error_message}"}), 500
    
@vistaProyectosFormacion.route("/deleteproyectof", methods = ['POST'])
def delete_proyectof():
    # Captura los datos del formulario enviado
    print(request)
    form_data = {
        "nombre_grupo": request.form.get('nombre_grupo')  
    } 

     # Debug: Imprimir el formulario de datos
    print("Form Data: ", form_data)  

    # Enviar los datos a la API
    response = requests.post(API_URL.format(projectName=projectName), json={
        "procedure": "delete_json_entity",  # Supongamos que tienes un procedimiento almacenado para insertar
        "parameters":{
            "table_name":"inv_grupos",
            "where_condition": "nombre_grupo = nombre_grupo"
                
        }
    } 
    )

       # Debug: Imprimir el estado de la respuesta y su contenido
    print("Response Status Code: ", response.status_code)
    print("Response Content: ", response.content)

    # Verificar la respuesta de la API
    if response.status_code == 200:
        return jsonify({"message": "Grupo Eliminado exitosamente"}), 200
    else:
        # Mostrar el mensaje de error detallado
        error_message = response.json().get("message", "Error desconocido al eliminar el grupo")
        return jsonify({"message": f"Error al eliminar el grupo: {error_message}"}), 500
    
@vistaProyectosFormacion.route("/updateproyectof", methods = ['POST'])
def update_proyectof():
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

     # Debug: Imprimir el formulario de datos
    print("Form Data: ", form_data)  

    # Enviar los datos a la API
    response = requests.post(API_URL.format(projectName=projectName), json={
        "procedure": "delete_json_entity",  # Supongamos que tienes un procedimiento almacenado para insertar
        "parameters":{
            "table_name":"inv_grupos",
            "json_data": form_data,
            "where_condition": "nombre_grupo = nombre_grupo"
                
        }
    } 
    )

       # Debug: Imprimir el estado de la respuesta y su contenido
    print("Response Status Code: ", response.status_code)
    print("Response Content: ", response.content)

    # Verificar la respuesta de la API
    if response.status_code == 200:
        return jsonify({"message": "Grupo actualizado exitosamente"}), 200
    else:
        # Mostrar el mensaje de error detallado
        error_message = response.json().get("message", "Error desconocido al actualizar el grupo")
        return jsonify({"message": f"Error al actualizar el grupo: {error_message}"}), 500
