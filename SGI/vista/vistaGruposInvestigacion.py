from flask import Flask, render_template, request, jsonify, Blueprint
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

 
    # Obtener datos de líneas asociadas al grupo
    select_data_lineas = {
        
            "projectName": "SGI",
            "procedure": "select_json_entity",
            "parameters": {
            "table_name": "inv_linea_grupo l INNER JOIN inv_grupos g ON l.id_grupo = g.id_grupo",
            "json_data": {},
            "where_condition": "l.id_grupo = g.id_grupo",  
            "select_columns": "g.id_grupo, l.nombre_linea, l.descripcion",
            "order_by": "g.id_grupo",
            "limit_clause": ""
    }
}
    response_lineas = requests.post(API_URL, json=select_data_lineas)
    if response_lineas.status_code != 200:
        return f"Error al consultar la API: {response_lineas.status_code}"
    
    data_lineas = response_lineas.json()
    if 'result' in data_lineas and data_lineas['result']:
        lineas_str = data_lineas['result'][0]['result']
        lineas = json.loads(lineas_str)
    else:
        lineas = []

    #obtener datos de proyectos asociados al grupo
    # Obtener datos de proyectos asociados al grupo
    # Obtener datos de proyectos asociados al grupo
    select_data_proyectos = {
        "projectName": "SGI",
        "procedure": "select_json_entity",
        "parameters": {
            "table_name": "inv_proyecto p INNER JOIN inv_grupos g ON p.id_grupo_lider = g.id_lider",
            "json_data": {},
            "where_condition": "p.id_grupo_lider = g.id_lider",  # Condición para asegurar que los ids coincidan
            "select_columns": "p.nombre_proyecto, p.id_grupo_lider, p.nombre_convocatoria",
            "order_by": "p.nombre_proyecto",
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

    #obtener datos de investigadores asociados
    select_data_investigadores_asociados ={
    "procedure": "select_json_entity",
    "parameters": {
        "table_name": "inv_investigador_proyecto",
        "json_data": {},
        "where_condition": "", 
        "select_columns": "id_investigador_proyecto, id_investigador, id_proyecto, tipo_participacion, horas_fase_1, horas_fase_2, horas_fase_3, horas_fase_4, horas_fase_5, horas_fase_6, estado",
        "order_by": "id_investigador_proyecto",
        "limit_clause": ""
        }
    }

    response_investigadores_asociados = requests.post(API_URL, json=select_data_investigadores_asociados)
    if  response_investigadores_asociados.status_code != 200:
        return f"Error al consultar la API: { response_investigadores_asociados.status_code}"
    
    data_investigadores_asociados =  response_investigadores_asociados.json()
    if 'result' in data_lineas and data_investigadores_asociados['result']:
        investigadores_asociados_str = data_investigadores_asociados['result'][0]['result']
        investigadores_asociados = json.loads(investigadores_asociados_str)
    else:
        investigadores_asociados = []

    #obtener datos de semilleros
    select_data_semilleros ={
    "procedure": "select_json_entity",
    "parameters": {
        "table_name": "inv_semilleros",
        "json_data": {},
        "where_condition": "", 
        "select_columns": "nombre_semillero, objetivos, descripcion_semillero",
        "order_by": "id_semillero",  
        "limit_clause": ""
        }
    }

    response_semilleros = requests.post(API_URL, json=select_data_semilleros)
    if  response_semilleros.status_code != 200:
        return f"Error al consultar la API: { response_semilleros.status_code}"
    
    data_semilleros =  response_semilleros.json()
    if 'result' in data_semilleros and data_semilleros['result']:
        semilleros_str = data_semilleros['result'][0]['result']
        semilleros = json.loads(semilleros_str)
    else:
        semilleros = []

    # Pasar los datos a la plantilla
    ths = ['grupos de investigacion', 'codigo grup lac', 'categoria colciencias', 'facultad', 'lider del grupo']
    return render_template('vistaGruposInvestigacion.html', grupos=grupos, facultades=facultades, investigadores = investigadores, lineas=lineas, proyectos = proyectos, investigadores_asociados = investigadores_asociados, semilleros = semilleros, ths=ths)

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
    form_data = {
        "id_grupo": request.form.get('id_grupo'),  
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

    print("Form Data: ", form_data)

    if not form_data["id_grupo"]:
        return jsonify({"message": "Error: 'id_grupo' es requerido para actualizar."}), 400

    response = requests.post(API_URL.format(projectName=projectName), json={
        "procedure": "update_json_entity",  # Supongamos que tienes un procedimiento almacenado para actualizar
        "parameters": {
            "table_name": "inv_grupos",
            "json_data": form_data,
            "where_condition": f"id_grupo = {form_data['id_grupo']}"  # Usar 'id_grupo' en la condición
        }
    })

    print("Response Status Code: ", response.status_code)
    print("Response Content: ", response.content)

    if response.status_code == 200:
        output_params = response.json().get("outputParams", {})
        mensaje = output_params.get("mensaje", "Operación exitosa")
        return jsonify({"message": mensaje}), 200
    else:
        error_message = response.json().get("message", "Error desconocido al actualizar el grupo")
        return jsonify({"message": f"Error al actualizar el grupo: {error_message}"}), 500