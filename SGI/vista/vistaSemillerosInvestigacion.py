from flask import Blueprint, render_template, request,flash, redirect, url_for,jsonify
import json
import requests
from vista.functions import paginate, now
from vista.select_list import investigadores,lineas,estudiantes 
import os
projectName = os.getenv('PROJECT_NAME')
API_URL = os.getenv('API_URL')


# Crear un Blueprint
vistaSemillerosInvestigacion = Blueprint('idVistaSemillerosInvestigacion', __name__, template_folder='templates')

@vistaSemillerosInvestigacion.route('/listar', methods=['GET', 'POST'])
def listar():   
    select_data = {
          "procedure": "select_json_entity",
          "parameters": {
            "table_name": "inv_semilleros s INNER JOIN inv_linea_grupo l ON l.id_linea_grupo = s.id_linea_grupo INNER JOIN inv_investigadores i ON i.id_investigador = s.id_lider INNER JOIN inv_grupos g ON g.id_grupo = l.id_grupo    INNER JOIN inv_facultad f ON f.id_facultad = g.id_facultad",
            "where_condition": "", 
            "order_by": "nombre_semillero",          
            "limit_clause": "",           
            "json_data": {},                             
            "select_columns": "s.id_semillero, s.nombre_semillero,l.nombre_linea,s.fecha_inicio,s.fecha_final, i.nombre_investigador, f.nombre_facultad,g.nombre_grupo"       
          }
        }

    response = requests.post(API_URL, json=select_data)
    if response.status_code != 200:
        return f"Error al consultar la API: {response.status_code}"
    

    search_term = request.args.get('search', '').lower()  
    
    data_semilleros = response.json()
    if 'result' in data_semilleros and data_semilleros['result']:
        data = data_semilleros['result'][0]['result']
        data = json.loads(data)
        # Filtrar los datos si hay un término de búsqueda
        if search_term:
            data = [item for item in data if any(search_term in str(value).lower() for value in item.values())]
        route_pagination = 'idVistaSemillerosInvestigacion.listar'        
        semilleros, total_pages, route_pagination,page = paginate(data,route_pagination)
        #semilleros = json.loads(items_on_page)
    else:
        semilleros = []
    # Renderizar la plantilla al final, pasando las variables necesarias
    return render_template('semilleros/listar.html', 
                           data=semilleros, total_pages=total_pages, 
                           route_pagination=route_pagination, page=page,
                           investigadores=investigadores(),lineas=lineas(),
                           search_term=search_term
                           )

@vistaSemillerosInvestigacion.route('/ver-detalle/<int:id>', methods=['GET'])
def detalle(id):   
    select_data = {
          "procedure": "select_json_entity",
          "parameters": {
            "table_name": "inv_semilleros s INNER JOIN inv_linea_grupo l ON l.id_linea_grupo = s.id_linea_grupo INNER JOIN inv_investigadores i ON i.id_investigador = s.id_lider INNER JOIN inv_grupos g ON g.id_grupo = l.id_grupo    INNER JOIN inv_facultad f ON f.id_facultad = g.id_facultad",
            "where_condition": f"id_semillero={id}", 
            "order_by": "nombre_semillero",          
            "limit_clause": "",           
            "json_data": {},                             
            "select_columns": "s.id_semillero, s.nombre_semillero,l.nombre_linea,s.fecha_inicio,s.fecha_final, i.nombre_investigador, f.nombre_facultad,g.nombre_grupo"       
          }
        }

    response = requests.post(API_URL, json=select_data)
    if response.status_code != 200:
        return f"Error al consultar la API: {response.status_code}"
   
    data_semilleros = response.json()
    if 'result' in data_semilleros and data_semilleros['result']:
        data = data_semilleros['result'][0]['result']
        semillero = json.loads(data)
    else:
        semillero = []
    
 
   
    # Renderizar la plantilla al final, pasando las variables necesarias
    return render_template('semilleros/detalle.html', semillero=semillero[0],
                           investigadores=investigadores(),lineas=lineas(), estudiantes=estudiantes(),
                           estudiantesNotInSemillero=estudiantesNotExistsSimellero(id),
                           integrantes=estudiantesIntegrantesSemilleros(id), planes=planesSemilleroById(id), proyectos=proyectosFormacionSemillero(id))


@vistaSemillerosInvestigacion.route('/crearSemillero', methods=[ 'POST'])
def crearSemillero():
    insert_data = {
      "procedure": "insert_json_entity",
              "parameters": {
                "table_name": "inv_semilleros",
                "json_data":  {
                    "id_lider": request.form.get('id_lider'),
                    "objetivos": request.form.get('objetivos'),
                    "fecha_final": request.form.get('fecha_final'),
                    "fecha_inicio": request.form.get('fecha_inicio'),
                    "id_linea_grupo": request.form.get('id_linea_grupo'),
                    "areas_de_trabajo": request.form.get('areas_de_trabajo'),
                    "nombre_semillero": request.form.get('nombre_semillero'),
                    "descripcion_semillero": request.form.get('descripcion_semillero'),
            } 
        }
     }
    response = requests.post(API_URL, json=insert_data)
    if response.status_code ==200:
        flash("El registro se guardó correctamente", 'success')
    else:
        #flash("Algo salió mal, no pudimos realizar la operación solipersonada", "danger")
        # Mostrar el mensaje de error detallado
        error_message = response.json().get("message", "Error desconocido al guardar los datos")
        return jsonify({"message": f"Error al guardar los datos: {error_message}"}), 500
    return redirect(url_for('idVistaSemillerosInvestigacion.listar'))

@vistaSemillerosInvestigacion.route('/editarSemillero', methods=[ 'POST'])
def editarSemillero():
    id_semillero =request.form.get('id_semillero')
    update_data = {
      "procedure": "update_json_entity",
              "parameters": {
                "table_name": "inv_semilleros",
                "json_data":  {
                    "id_lider": request.form.get('id_lider'),
                    "objetivos": request.form.get('objetivos'),
                    "fecha_final": request.form.get('fecha_final'),
                    "fecha_inicio": request.form.get('fecha_inicio'),
                    "id_linea_grupo": request.form.get('id_linea_grupo'),
                    "areas_de_trabajo": request.form.get('areas_de_trabajo'),
                    "nombre_semillero": request.form.get('nombre_semillero'),
                    "descripcion_semillero": request.form.get('descripcion_semillero'),
                },
                "where_condition": f"id_semillero = {id_semillero}"
        }
     }
    response = requests.post(API_URL, json=update_data)
    if response.status_code ==200:
        flash("El registro se actualizó correctamente", 'success')
    else:
        #flash("Algo salió mal, no pudimos realizar la operación solipersonada", "danger")
        # Mostrar el mensaje de error detallado
        error_message = response.json().get("message", "Error desconocido al guardar los datos")
        return jsonify({"message": f"Error al guardar los datos: {error_message}"}), 500
    return redirect(url_for('idVistaSemillerosInvestigacion.detalle', id=id_semillero))


@vistaSemillerosInvestigacion.route('/crearEstudianteSemillero', methods=[ 'POST'])
def crearEstudianteSemillero():
    id_semillero =request.form.get('id_semillero')
    insert_data = {
      "procedure": "insert_json_entity",
              "parameters": {
                "table_name": "inv_estudiante_semillero",
                "json_data":  {
                    "id_semillero": id_semillero,
                    "id_estudiante": request.form.get('id_estudiante'),
                    "fecha_inicio": now(),                    
                    "fecha_final": request.form.get('fecha_final'),
            } 
        }
     }
    response = requests.post(API_URL, json=insert_data)
    if response.status_code ==200:
        flash("El registro se guardó correctamente", 'success')
    else:
        #flash("Algo salió mal, no pudimos realizar la operación solipersonada", "danger")
        # Mostrar el mensaje de error detallado
        error_message = response.json().get("message", "Error desconocido al guardar los datos")
        return jsonify({"message": f"Error al guardar los datos: {error_message}"}), 500
    return redirect(url_for('idVistaSemillerosInvestigacion.detalle', id=id_semillero))

@vistaSemillerosInvestigacion.route('/get_integrante', methods=['POST'])
def get_integrante():
    integrante_id = request.form.get('id')
    if not integrante_id:
        return jsonify({"error": "ID is required"}), 400
    response = estudianteIntegranteSemilleroById(integrante_id)

    data = response      
    if len(data) > 0:       
        ids_editar = {
                "id_estud_semillero": "int_id_estud_semillero",
                "id_estudiante": "int_id_estudiante",
                "id_semillero": "int_id_semillero",
                "fecha_final": "int_fecha_final"
        } 
        result = {
                "data": data,  
                "ids_editar": ids_editar 
            }    
        return jsonify(result), 200
    else:
        return jsonify({"error": "Failed to retrieve data"}), 500

@vistaSemillerosInvestigacion.route('/editarEstudianteSemillero', methods=[ 'POST'])
def editarEstudianteSemillero():
    id_estud_semillero =request.form.get('int_id_estud_semillero')
    id_semillero =request.form.get('int_id_semillero')
    update_data = {
      "procedure": "update_json_entity",
              "parameters": {
                "table_name": "inv_estudiante_semillero",
                "json_data":  {
                    "id_estudiante": request.form.get('int_id_estudiante'),                
                    "fecha_final": request.form.get('int_fecha_final'),
            } ,
            "where_condition": f"id_estud_semillero={id_estud_semillero}"
        }
     }
    response = requests.post(API_URL, json=update_data)
    if response.status_code ==200:
        flash("El registro se actualizó correctamente", 'success')
    else:
        #flash("Algo salió mal, no pudimos realizar la operación solipersonada", "danger")
        # Mostrar el mensaje de error detallado
        error_message = response.json().get("message", "Error desconocido al guardar los datos")
        return jsonify({"message": f"Error al guardar los datos: {error_message}"}), 500
    return redirect(url_for('idVistaSemillerosInvestigacion.detalle', id=id_semillero))
   
@vistaSemillerosInvestigacion.route('/crearPlanSemillero', methods=[ 'POST'])
def crearPlanSemillero():
    id_semillero =request.form.get('id_semillero')
    insert_data = {
      "procedure": "insert_json_entity",
              "parameters": {
                "table_name": "inv_plan_trabajo_semillero",
                "json_data":  {
                    "id_semillero": id_semillero,
                    "proyecto_activos": request.form.get('proyecto_activos'),
                    "metas_periodo": request.form.get('metas_periodo'),                    
                    "resultados_obtenidos": request.form.get('resultados_obtenidos'),                    
                    "periodo": request.form.get('periodo'),
            } 
        }
     }
    print(insert_data)
    response = requests.post(API_URL, json=insert_data)
    if response.status_code ==200:
        flash("El registro se guardó correctamente", 'success')
    else:
        #flash("Algo salió mal, no pudimos realizar la operación solipersonada", "danger")
        # Mostrar el mensaje de error detallado
        error_message = response.json().get("message", "Error desconocido al guardar los datos")
        return jsonify({"message": f"Error al guardar los datos: {error_message}"}), 500
    return redirect(url_for('idVistaSemillerosInvestigacion.detalle', id=id_semillero))

@vistaSemillerosInvestigacion.route('/get_plan', methods=['POST'])
def get_plan():
    plan_id = request.form.get('id')
    if not plan_id:
        return jsonify({"error": "ID is required"}), 400
    response = planSemillerosByid(plan_id)

    data = response      
    if len(data) > 0:       
        ids_editar = {
                "id_plan_trabajo": "plan_id_plan_trabajo",
                "id_semillero": "plan_id_semillero",
                "periodo": "plan_periodo",
                "metas_periodo": "plan_metas_periodo",
                "proyecto_activos": "plan_proyecto_activos",
                "resultados_obtenidos": "plan_resultados_obtenidos",
        } 
        result = {
                "data": data,  
                "ids_editar": ids_editar 
            }    
        return jsonify(result), 200
    else:
        return jsonify({"error": "Failed to retrieve data"}), 500

@vistaSemillerosInvestigacion.route('/editarPlanSemillero', methods=[ 'POST'])
def editarPlanSemillero():
    id_plan_trabajo = request.form.get('plan_id_plan_trabajo')
    id_semillero = request.form.get('plan_id_semillero')
    insert_data = {
      "procedure": "update_json_entity",
              "parameters": {
                "table_name": "inv_plan_trabajo_semillero",
                "json_data":  {
                    "proyecto_activos": request.form.get('plan_proyecto_activos'),
                    "metas_periodo": request.form.get('plan_metas_periodo'),                    
                    "resultados_obtenidos": request.form.get('plan_resultados_obtenidos'),                    
                    "periodo": request.form.get('plan_periodo'),
            },
           "where_condition": f"id_plan_trabajo={id_plan_trabajo}"
        }
     }
    print(insert_data)
    response = requests.post(API_URL, json=insert_data)
    if response.status_code ==200:
        flash("El registro se actualizó correctamente", 'success')
    else:
        #flash("Algo salió mal, no pudimos realizar la operación solipersonada", "danger")
        # Mostrar el mensaje de error detallado
        error_message = response.json().get("message", "Error desconocido al guardar los datos")
        return jsonify({"message": f"Error al guardar los datos: {error_message}"}), 500
    return redirect(url_for('idVistaSemillerosInvestigacion.detalle', id=id_semillero))


@vistaSemillerosInvestigacion.route('/eliminar-plan', methods=[ 'POST'])
def eliminarPlan():
    id_semillero = request.form.get('plan_semillero_id')
    print(f"idsemillero{id_semillero}")
    delete_data = {
      "procedure": "delete_json_entity",
        "parameters": {
            "table_name": "inv_plan_trabajo_semillero",
            "where_condition": f"id_plan_trabajo={request.form.get('plan_eliminar_id')}"
        }
     }
    print(delete_data)
    print(id_semillero)
    response = requests.post(API_URL, json=delete_data)
    if response.status_code ==200:
        flash("El registro se eliminó correctamente", 'success')
    else:
        #flash("Algo salió mal, no pudimos realizar la operación solipersonada", "danger")
        # Mostrar el mensaje de error detallado
        error_message = response.json().get("message", "Error desconocido al guardar los datos")
        return jsonify({"message": f"Error al guardar los datos: {error_message}"}), 500
    return redirect(url_for('idVistaSemillerosInvestigacion.detalle', id=id_semillero))

@vistaSemillerosInvestigacion.route('/eliminar-integrante', methods=[ 'POST'])
def eliminarIntegrante():
    id_semillero = request.form.get('inv_semillero_id')
    delete_data = {
      "procedure": "delete_json_entity",
        "parameters": {
            "table_name": "inv_estudiante_semillero",
            "where_condition": f"id_estud_semillero={request.form.get('inv_eliminar_id')}"
        }
     }
    response = requests.post(API_URL, json=delete_data)
    if response.status_code ==200:
        flash("El registro se eliminó correctamente", 'success')
    else:
        #flash("Algo salió mal, no pudimos realizar la operación solipersonada", "danger")
        # Mostrar el mensaje de error detallado
        error_message = response.json().get("message", "Error desconocido al guardar los datos")
        return jsonify({"message": f"Error al guardar los datos: {error_message}"}), 500
    return redirect(url_for('idVistaSemillerosInvestigacion.detalle', id=id_semillero))

    
    
    
"""-----------------------------------------------------"""
#<--Consultas-->
#Integrantes del semillero
def estudiantesIntegrantesSemilleros(id_semillero):    
    select_data = {
      "procedure": "select_json_entity",
      "parameters": {
        "table_name": "inv_semilleros s INNER JOIN inv_estudiante_semillero e ON e.id_semillero = s.id_semillero INNER JOIN  inv_estudiantes es ON es.id_estudiante = e.id_estudiante",
        "where_condition": f"s.id_semillero ={id_semillero}", 
        "order_by": "es.nombre_estudiante",         
        "limit_clause": "",          
        "json_data": {},                           
        "select_columns": "es.nombre_estudiante, e.fecha_inicio, e.fecha_final, e.id_estud_semillero,s.id_semillero "       
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

#Consulta estudiante para editar
def estudianteIntegranteSemilleroById(id):    
    select_data = {
      "procedure": "select_json_entity",
      "parameters": {
        "table_name": "inv_semilleros s INNER JOIN inv_estudiante_semillero e ON e.id_semillero = s.id_semillero INNER JOIN  inv_estudiantes es ON es.id_estudiante = e.id_estudiante",
        "where_condition": f"e.id_estud_semillero ={id}",  
        "order_by": "es.nombre_estudiante",         
        "limit_clause": "",          
        "json_data": {},                           
        "select_columns": "es.nombre_estudiante, e.fecha_inicio, e.fecha_final"       
      }
    }
    
    response = requests.post(API_URL, json=select_data)
    if response.status_code != 200:
        return f"Error al consultar la API: {response.status_code}"

    select_data = response.json()
    if 'result' in select_data and select_data['result']:
        data_str = select_data['result'][0]['result']
        result = data_str
    else:
        result = []
    return result

#Planes vinculados al semilelro
def planesSemilleroById(id):    
    select_data = {
      "procedure": "select_json_entity",
      "parameters": {
        "table_name": "inv_plan_trabajo_semillero",
        "where_condition": f"id_semillero={id}",
        "order_by": "",         
        "limit_clause": "",          
        "json_data": {},                           
        "select_columns": "periodo, metas_periodo, id_plan_trabajo, proyecto_activos, resultados_obtenidos,id_semillero"       
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

#Consulta para editar plan
def planSemillerosByid(id):    
    select_data = {
      "procedure": "select_json_entity",
      "parameters": {
        "table_name": "inv_plan_trabajo_semillero",
        "where_condition": f"id_plan_trabajo ={id}",  
        "order_by": "",         
        "limit_clause": "",          
        "json_data": {},                           
        "select_columns": ""       
      }
    }
    
    response = requests.post(API_URL, json=select_data)
    if response.status_code != 200:
        return f"Error al consultar la API: {response.status_code}"

    select_data = response.json()
    if 'result' in select_data and select_data['result']:
        data_str = select_data['result'][0]['result']
        result = data_str
    else:
        result = []
    return result


#Consulta para editar plan
def proyectosFormacionSemillero(id):    
    select_data = {
      "procedure": "select_json_entity",
      "parameters": {
        "table_name": "inv_proyecto_formacion p INNER JOIN inv_investigadores i ON i.id_investigador = p.id_investigador",
        "where_condition": f"p.id_semillero = {id}", 
        "order_by": "p.nombre_proy_form",
        "limit_clause": "",
        "json_data": {},
        "select_columns": "p.id_proyecto_formacion, p.nombre_proy_form, i.nombre_investigador, p.fecha_inicio, p.fecha_terminacion"       
      }
    }
    
    response = requests.post(API_URL, json=select_data)
    if response.status_code != 200:
        return f"Error al consultar la API: {response.status_code}"

    select_data = response.json()
    if 'result' in select_data and select_data['result']:
        data_str = select_data['result'][0]['result']
        result = data_str
    else:
        result = []
    return result

"!!!!Importante, Cambiar cuando e arregle lo del filtro de columnas!!!!"
#Investigadores que no existen en inv_investigadores para ese semillero específico
def estudiantesNotExistsSimellero(id):    
    select_data = {
    "procedure": "select_json_entity",
    "parameters": {
        "table_name": f"inv_estudiantes es LEFT JOIN inv_estudiante_semillero e ON es.id_estudiante = e.id_estudiante  AND e.id_semillero = {id}",
        "where_condition": "e.id_estudiante IS NULL",
        "order_by": "es.nombre_estudiante",
        "limit_clause": "",
        "json_data": {},
        "select_columns": "es.id_estudiante, es.nombre_estudiante"
        }
    }
    
    response = requests.post(API_URL, json=select_data)
    if response.status_code != 200:
        return f"Error al consultar la API: {response.status_code}"

    select_data = response.json()
    if 'result' in select_data and select_data['result']:
        data_str = select_data['result'][0]['result']
        result = json.loads(data_str)
        print(result)
    else:
        result = []
    return result

