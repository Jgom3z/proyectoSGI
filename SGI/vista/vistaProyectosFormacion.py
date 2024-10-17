from flask import Blueprint, render_template, request,flash, redirect, url_for,jsonify
import requests
import json
from vista.functions import paginate, now
from vista.select_list import investigadores,lineas,proyectos,semilleros
import os
projectName = os.getenv('PROJECT_NAME')
API_URL = os.getenv('API_URL')

# Crear un Blueprint
vistaProyectosFormacion = Blueprint('idVistaProyectosFormacion', __name__, template_folder='templates')

@vistaProyectosFormacion.route('/listar', methods=['GET', 'POST'])
def listar():
    # Inicializa la variable
    proyectosf = []

    # Define la estructura de la consulta
    select_data = {
        "procedure": "select_json_entity",
        "parameters": {
            "table_name": "inv_proyecto_formacion pf INNER JOIN inv_linea_grupo lg ON pf.id_linea = lg.id_linea_grupo INNER JOIN inv_investigadores i ON pf.id_investigador = i.id_investigador INNER JOIN inv_proyecto pry ON pf.id_proyecto = pry.id_proyecto INNER JOIN inv_semilleros s ON pf.id_semillero = s.id_semillero",
            "json_data": {
                "estado": "En Progreso"  
            },
            "where_condition": "",
            "select_columns": "pf.nombre_proy_form, i.nombre_investigador, pry.nombre_proyecto, pf.nivel, pf.modalidad, pf.cod_proy_form, pf.id_proyecto_formacion",
            "order_by": "pf.id_proyecto_formacion", 
            "limit_clause": ""
        }
    }

    response = requests.post(API_URL, json=select_data)
    if response.status_code != 200:
        return f"Error al consultar la API: {response.status_code}"
    
    search_term = request.args.get('search', '').lower()  

    data_proyectosf = response.json()
    if 'result' in data_proyectosf and data_proyectosf['result']:
        data = data_proyectosf['result'][0]['result']
        data = json.loads(data)
        # Filtrar los datos si hay un término de búsqueda
        if search_term:
            data = [item for item in data if any(search_term in str(value).lower() for value in item.values())]
        route_pagination = 'idVistaProyectosFormacion.listar'        
        ProyectosFormacion, total_pages, route_pagination,page = paginate(data,route_pagination)
        #semilleros = json.loads(items_on_page)
    else:
        ProyectosFormacion = []
    # Renderizar la plantilla al final, pasando las variables necesarias
    return render_template('proyectoFormacion/listar.html', 
                           data=ProyectosFormacion, total_pages=total_pages, 
                           route_pagination=route_pagination, page=page,
                           search_term=search_term
                           )

@vistaProyectosFormacion.route('/ver-detalle/<int:id>', methods=['GET'])
def detalle(id):   
    select_data = {
          "procedure": "select_json_entity",
            "parameters": {
            "table_name": "inv_proyecto_formacion pf INNER JOIN inv_linea_grupo lg ON pf.id_linea = lg.id_linea_grupo INNER JOIN inv_investigadores i ON pf.id_investigador = i.id_investigador INNER JOIN inv_proyecto pry ON pf.id_proyecto = pry.id_proyecto INNER JOIN inv_semilleros s ON pf.id_semillero = s.id_semillero INNER JOIN inv_investigadores c ON pf.id_codirector = c.id_investigador",
            "json_data": {
                "estado": "En Progreso"  
            },
            "where_condition": f"pf.id_proyecto_formacion={id}",
            "select_columns": "pf.nombre_proy_form, pf.fecha_inicio, pf.fecha_terminacion, pf.linea_investigacion, i.nombre_investigador as asesor, pry.nombre_proyecto, s.nombre_semillero, pf.objetivos, pf.nivel, pf.modalidad, pf.cod_proy_form, lg.nombre_linea,c.nombre_investigador as coasesor",
            "order_by": "pf.id_proyecto_formacion", 
            "limit_clause": ""
            }
        }

    response = requests.post(API_URL, json=select_data)
    if response.status_code != 200:
        return f"Error al consultar la API: {response.status_code}"
    
    data_proyectosf = response.json()
    if 'result' in data_proyectosf and data_proyectosf['result']:
        data = data_proyectosf['result'][0]['result']
        ProyectosFormacion = json.loads(data) 
    else:
        ProyectosFormacion = []

   # Renderizar la plantilla al final, pasando las variables necesarias
    return render_template('proyectoFormacion/detalle.html', ProyectosFormacion=ProyectosFormacion[0],
                           investigadores=investigadores(),lineas=lineas(),proyectos=proyectos(),semilleros=semilleros())

@vistaProyectosFormacion.route('/crearProyectoFormacion', methods=[ 'POST'])
def crearProyForm():
    insert_data = {
      "procedure": "insert_json_entity",
              "parameters": {
                "table_name": "inv_proyecto_formacion",
                "json_data":  {
                    "nombre_proy_form": request.form.get('nombre_proy_form'),
                    "fecha_terminacion": request.form.get('fecha_terminacion'),
                    "fecha_inicio": request.form.get('fecha_inicio'),
                    "linea_investigacion": request.form.get('linea_investigacion'),
                    "id_investigador": request.form.get('id_investigador'),
                    "id_proyecto": request.form.get('id_proyecto'),
                    "id_semillero": request.form.get('id_semillero'),
                    "objetivos": request.form.get('objetivos'),
                    "nivel": request.form.get('nivel'),
                    "modalidad": request.form.get('modalidad'),
                    "cod_proy_form": request.form.get('cod_proy_form'),
                    "id_codirector": request.form.get('id_codirector'),
                    "id_linea": request.form.get('id_linea'),
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
    return redirect(url_for('idVistaProyectosFormacion.listar'))

@vistaProyectosFormacion.route('/editarProyectoFormacion', methods=[ 'POST'])
def editarProyForm():
    id_proyecto_formacion =request.form.get('id_proyecto_formacion')
    update_data = {
      "procedure": "update_json_entity",
              "parameters": {
                "table_name": "inv_proyecto_formacion",
                "json_data":  {
                    "nombre_proy_form": request.form.get('nombre_proy_form'),
                    "fecha_terminacion": request.form.get('fecha_terminacion'),
                    "fecha_inicio": request.form.get('fecha_inicio'),
                    "linea_investigacion": request.form.get('linea_investigacion'),
                    "id_investigador": request.form.get('id_investigador'),
                    "id_proyecto": request.form.get('id_proyecto'),
                    "id_semillero": request.form.get('id_semillero'),
                    "objetivos": request.form.get('objetivos'),
                    "nivel": request.form.get('nivel'),
                    "modalidad": request.form.get('modalidad'),
                    "cod_proy_form": request.form.get('cod_proy_form'),
                    "id_codirector": request.form.get('id_codirector'),
                    "id_linea": request.form.get('id_linea'),
                },
                "where_condition": f"id_proyecto_formacion = {id_proyecto_formacion}"
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
    return redirect(url_for('idVistaProyectosFormacion.detalle', id=id_proyecto_formacion))


#<--Estudiantes-->                          
@vistaProyectosFormacion.route('/crearEst_proy_form', methods=[ 'POST'])
def crearEstudianteProyForm():
    id_proyecto_formacion =request.form.get('id_proyecto_formacion')
    insert_data = {
      "procedure": "insert_json_entity",
              "parameters": {
                "table_name": "inv_estudiante_semillero",
                "json_data":  {
                    "id_proyecto_formacion": id_proyecto_formacion,
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
    return redirect(url_for('idVistaProyectosFormacion.detalle', id=id_proyecto_formacion))

@vistaProyectosFormacion.route('/get_integrante', methods=['POST'])
def get_integrante():
    integrante_id = request.form.get('id')
    if not integrante_id:
        return jsonify({"error": "ID is required"}), 400
    response = estudianteIntegranteProyFormById(integrante_id)

    data = response      
    if len(data) > 0:       
        ids_editar = {
                "id_est_proy_form": "int_id_est_proy_form",
                "id_proyecto_formacion": "int_id_proyecto_formacion",
                "id_estudiante": "int_id_estudiante",
                "fecha_final": "int_fecha_final"
        } 
        result = {
                "data": data,  
                "ids_editar": ids_editar 
            }    
        return jsonify(result), 200
    else:
        return jsonify({"error": "Failed to retrieve data"}), 500

@vistaProyectosFormacion.route('/editarEst_proy_form', methods=[ 'POST'])
def editarEst_proy_form():
    id_est_proy_form =request.form.get('int_id_est_proy_form')
    id_proyecto_formacion =request.form.get('int_id_proyecto_formacion')
    update_data = {
      "procedure": "update_json_entity",
              "parameters": {
                "table_name": "inv_estud_proy_formac",
                "json_data":  {
                    "id_estudiante": request.form.get('int_id_estudiante'),                
                    "fecha_final": request.form.get('int_fecha_final'),
            } ,
            "where_condition": f"id_est_proy_form={id_est_proy_form}"
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
    return redirect(url_for('idVistaProyectosFormacion.detalle', id=id_proyecto_formacion))
   
@vistaProyectosFormacion.route('/eliminar-integrante', methods=[ 'POST'])
def eliminarIntegrante():
    id_proyecto_formacion = request.form.get('id_proyecto_formacion')
    delete_data = {
      "procedure": "delete_json_entity",
        "parameters": {
            "table_name": "inv_estud_proy_formac",
            "where_condition": f"id_est_proyform={request.form.get('id_proyecto_formacion')}"
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
    return redirect(url_for('idVistaProyectosFormacion.detalle', id=id_proyecto_formacion))

#<--Consultas-->
#Integrantes del semillero
def estudiantesIntegrantesProyForm(id_proyecto_formacion):    
    select_data = {
      "procedure": "select_json_entity",
      "parameters": {
        "table_name": "inv_proyecto_formacion pf INNER JOIN inv_estud_proy_formac epf ON pf.id_proyecto_formacion = epf.id_proyecto_formacion INNER JOIN  inv_estudiantes es ON es.id_estudiante = epf.id_estudiante",
        "where_condition": f"pf.id_proyecto_formacion ={id_proyecto_formacion}", 
        "order_by": "es.nombre_estudiante",         
        "limit_clause": "",          
        "json_data": {},                           
        "select_columns": "es.nombre_estudiante, epf.fecha_inicio, epf.fecha_final"       
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
def estudianteIntegranteProyFormById(id):    
    select_data = {
      "procedure": "select_json_entity",
      "parameters": {
        "table_name": "inv_proyecto_formacion pf INNER JOIN inv_estud_proy_formac epf ON pf.id_proyecto_formacion = epf.id_proyecto_formacion INNER JOIN  inv_estudiantes es ON es.id_estudiante = epf.id_estudiante",
        "where_condition": f"epf.id_est_proy_form ={id}",  
        "order_by": "es.nombre_estudiante",         
        "limit_clause": "",          
        "json_data": {},                           
        "select_columns": "es.nombre_estudiante, epf.fecha_inicio, epf.fecha_final"       
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


#<--Producto-->
@vistaProyectosFormacion.route('/crearProductoFormacion', methods=[ 'POST'])
def crearProdForm():
    id_proyecto_formacion =request.form.get('id_proyecto_formacion')
    insert_data = {
      "procedure": "insert_json_entity",
              "parameters": {
                "table_name": "inv_producto_formacion",
                "json_data":  {
                    "id_proyecto_formacion": id_proyecto_formacion,
                    "id_tipo_producto": request.form.get('id_tipo_producto'),
                    "fecha_entrega": request.form.get('fecha_entrega'),                    
                    "nombre_soporte": request.form.get('nombre_soporte'),                    
                    "soporte_pf": request.form.get('soporte_pf'),
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
    return redirect(url_for('idVistaProyectosFormacion.detalle', id=id_proyecto_formacion))

@vistaProyectosFormacion.route('/get_ProdForm', methods=['POST'])
def get_ProdForm():
    id_producto_formacion = request.form.get('id')
    if not id_producto_formacion:
        return jsonify({"error": "ID is required"}), 400
    response = ProductoFomracionById(id_producto_formacion)

    data = response      
    if len(data) > 0:       
        ids_editar = {
                "id_tipo_producto": "prod_id_tipo_producto",
                "fecha_entregaemillero": "prod_fecha_entrega",
                "id_proyecto_formacion": "prod_id_proyecto_formacion",
                "nombre_soporte": "prod_nombre_soporte",
                "soporte_pf": "prod_soporte_pf",
        } 
        result = {
                "data": data,  
                "ids_editar": ids_editar 
            }    
        return jsonify(result), 200
    else:
        return jsonify({"error": "Failed to retrieve data"}), 500

@vistaProyectosFormacion.route('/editarProductoFormacion', methods=[ 'POST'])
def editarProdForm():
    id_producto = request.form.get('prod_id_producto')
    id_producto_formacion = request.form.get('prod_id_producto_formacion')
    insert_data = {
      "procedure": "update_json_entity",
              "parameters": {
                "table_name": "inv_producto_formacion",
                "json_data":  {
                   "id_producto_formacion": id_producto_formacion,
                    "id_tipo_producto": request.form.get('id_tipo_producto'),
                    "fecha_entrega": request.form.get('fecha_entrega'),                    
                    "nombre_soporte": request.form.get('nombre_soporte'),                    
                    "soporte_pf": request.form.get('soporte_pf'),
            },
           "where_condition": f"id_plan_trabajo={id_producto}"
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
    return redirect(url_for('idVistaProyectosFormacion.detalle', id=id_producto_formacion))


@vistaProyectosFormacion.route('/eliminar-producto', methods=[ 'POST'])
def eliminarProducto():
    id_producto_formacion = request.form.get('prod_id_producto_formacion')
    print(f"id_producto_formacion{id_producto_formacion}")
    delete_data = {
      "procedure": "delete_json_entity",
        "parameters": {
            "table_name": "inv_producto_formacion",
            "where_condition": f"id_producto_formacion={request.form.get('prod_eliminar_id')}"
        }
     }
    print(delete_data)
    print(id_producto_formacion)
    response = requests.post(API_URL, json=delete_data)
    if response.status_code ==200:
        flash("El registro se eliminó correctamente", 'success')
    else:
        #flash("Algo salió mal, no pudimos realizar la operación solipersonada", "danger")
        # Mostrar el mensaje de error detallado
        error_message = response.json().get("message", "Error desconocido al guardar los datos")
        return jsonify({"message": f"Error al guardar los datos: {error_message}"}), 500
    return redirect(url_for('idVistaProyectosFormacion.detalle', id=id_producto_formacion))

#<--Consultas-->
#Planes vinculados al semilelro
def ProductoFomracionById(id):    
    select_data = {
      "procedure": "select_json_entity",
      "parameters": {
        "table_name": "inv_producto_formacion",
        "where_condition": f"id_proyecto_formacion={id}",
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
        result = json.loads(data_str)
    else:
        result = []
    return result

#Consulta para editar plan
def productosFormacionByid(id):    
    select_data = {
      "procedure": "select_json_entity",
      "parameters": {
        "table_name": "inv_producto_formacion",
        "where_condition": f"id_producto_formacion ={id}",  
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

