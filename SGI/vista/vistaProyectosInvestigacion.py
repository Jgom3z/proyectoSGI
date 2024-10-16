from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
import json
import requests
from datetime import datetime
import os
from vista.functions import paginate, now
from vista.select_list import grupos, lineas,investigadores,productos,cofinanciadores,estudiantes
from vista.documentos_proyecto import handle_file_upload_seguimiento,eliminar_soporte_seguimiento

projectName = os.getenv('PROJECT_NAME')
API_URL = os.getenv('API_URL')

vistaProyectosInvestigacion = Blueprint('idVistaProyectosInvestigacion', __name__, template_folder='../templates')

@vistaProyectosInvestigacion.route('/listar', methods=['GET', 'POST'])
def listar():
    select_data = {
       "procedure": "select_json_entity",
        "parameters": {
            "table_name": """
                inv_proyecto p 
                INNER JOIN inv_grupos g ON g.id_grupo = p.id_grupo_lider 
                INNER JOIN inv_linea_grupo l ON l.id_linea_grupo = p.id_linea_investigacion 
                INNER JOIN inv_facultad f ON f.id_facultad = g.id_facultad
            """,
            "where_condition": "",
            "order_by": "p.nombre_proyecto",
            "limit_clause": "",
            "json_data": {},
            "select_columns": """
                p.id_proyecto, p.nombre_proyecto, p.codigo, g.nombre_grupo, 
                l.nombre_linea, f.nombre_facultad, p.fecha_inicio, p.fecha_final, 
                p.estado, p.convocatoria
            """
        }
    }

    try:
        response = requests.post(API_URL, json=select_data)
        response.raise_for_status()
        data_proyectos = response.json()
    except requests.RequestException as e:
        return jsonify({"error": f"Error al consultar la API: {str(e)}"}), 500
    except json.JSONDecodeError:
        return jsonify({"error": "La respuesta de la API no es un JSON válido"}), 500

    print("Respuesta de la API:", response.text)
    print("data_proyectos:", data_proyectos)

    search_term = request.args.get('search', '').lower()

    if data_proyectos and 'result' in data_proyectos and data_proyectos['result']:
        result = data_proyectos['result'][0].get('result')
        if result is not None:
            try:
                data = json.loads(result)
            except json.JSONDecodeError:
                return jsonify({"error": "Error al procesar los datos de la API"}), 500
        else:
            data = []
    else:
        data = []

    if search_term:
        data = [item for item in data if any(search_term in str(value).lower() for value in item.values())]
    
    route_pagination = 'idVistaProyectosInvestigacion.listar'
    proyectos, total_pages, route_pagination, page = paginate(data, route_pagination)

    return render_template('proyectosInvestigacion/listar.html',
                           data=proyectos, 
                           total_pages=total_pages,
                           route_pagination=route_pagination, 
                           page=page,
                           search_term=search_term,
                           grupos=grupos(), lineas = lineas())

@vistaProyectosInvestigacion.route('/detalle/<int:id>', methods=['GET'])
def detalle(id):
    select_data = {
         "procedure": "select_json_entity",
        "parameters": {
            "table_name": "inv_proyecto p INNER JOIN inv_grupos g ON g.id_grupo = p.id_grupo_lider INNER JOIN inv_linea_grupo l ON l.id_linea_grupo = p.id_linea_investigacion INNER JOIN inv_facultad f ON f.id_facultad = g.id_facultad",
            "where_condition": f"p.id_proyecto = {id}",
            "order_by": "",
            "limit_clause": "",
            "json_data": {},
            "select_columns": "p.id_proyecto, p.nombre_proyecto, p.codigo, g.nombre_grupo, l.nombre_linea, p.fecha_inicio, p.fecha_final, p.estado, p.convocatoria, p.nombre_acta_inicio, p.nombre_acta_finalizacion, p.nombre_presupuesto, p.nombre_propuesta, p.nombre_acta_comite, p.nombre_convenio_marco, p.nombre_convenio_especifico, p.nombre_carta_intencion, p.nombre_convocatoria"
        }
    }
    #print(select_data)

    try:
        response = requests.post(API_URL, json=select_data)
        response.raise_for_status()
        data_proyecto = response.json()
    except requests.RequestException as e:
        return jsonify({"error": f"Error al consultar la API: {str(e)}"}), 500
    except json.JSONDecodeError:
        return jsonify({"error": "La respuesta de la API no es un JSON válido"}), 500

    #print("Respuesta de la API para detalle:", response.text)

    if data_proyecto and 'result' in data_proyecto and data_proyecto['result']:
        result = data_proyecto['result'][0].get('result')
        if result is not None:
            try:
                proyecto = json.loads(result)
            except json.JSONDecodeError:
                return jsonify({"error": "Error al procesar los datos de la API"}), 500
        else:
            proyecto = {}
    else:
        proyecto = {}
    #print(result)

    return render_template('proyectosInvestigacion/detalle.html', 
                           proyecto=proyecto[0], 
                           grupos=grupos(), lineas = lineas(),
                           investigadores_crear=investigadoresNotInProyecto(id), 
                           investigadores=investigadores(), 
                           investigadoresProyecto=investigadoresProyecto(id),
                           productosProyecto=productosProyecto(id),
                           cofinanciadoresProyecto=cofinanciadoresProyecto(id),
                           AuxiliaresProyecto=AuxiliaresProyecto(id),
                           productos=productos(),
                           cofinanciadores=cofinanciadores(),
                           estudiantes=estudiantesNotInProyecto(id),
                           #seguimiento=seguimiento(),
                           )


@vistaProyectosInvestigacion.route('/crear', methods=['POST'])
def crearProyecto():
    insert_data = {
      "procedure": "insert_json_entity",
              "parameters": {
                "table_name": "inv_proyecto",
                "json_data":  {
                    "nombre_proyecto": request.form.get('nombre_proyecto'),                    
                    "codigo": request.form.get('codigo'),
                    "estado": request.form.get('estado'),
                    "fecha_inicio": request.form.get('fecha_inicio'),
                    "fecha_final": request.form.get('fecha_final'),
                    "convocatoria": request.form.get('convocatoria'),
                    "id_grupo_lider": request.form.get('id_grupo_lider'),
                    "id_linea_investigacion": request.form.get('id_linea_investigacion'),
                    "nombre_convocatoria": request.form.get('nombre_convocatoria'),
            }
        }
     }
    #print(insert_data)
    response = requests.post(API_URL, json=insert_data)
    if response.status_code ==200:
        flash("El registro se guardó correctamente", 'success')
    else:      
        error_message = response.json().get("message", "Error desconocido al guardar los datos")
        return jsonify({"message": f"Error al guardar los datos: {error_message}"}), 500
    return redirect(url_for('idVistaProyectosInvestigacion.listar'))
   

@vistaProyectosInvestigacion.route('/editar', methods=['POST'])
def editarProyecto():
    id_proyecto =request.form.get('id_proyecto')
    update_data = {
      "procedure": "update_json_entity",
              "parameters": {
                "table_name": "inv_proyecto",
                "json_data":  {
                    "nombre_proyecto": request.form.get('nombre_proyecto'),                    
                    "codigo": request.form.get('codigo'),
                    "estado": request.form.get('estado'),
                    "fecha_inicio": request.form.get('fecha_inicio'),
                    "fecha_final": request.form.get('fecha_final'),
                    "convocatoria": request.form.get('convocatoria'),
                    "id_grupo_lider": request.form.get('id_grupo_lider'),
                    "id_linea_investigacion": request.form.get('id_linea_investigacion'),
                    "nombre_convocatoria": request.form.get('nombre_convocatoria'),
                },
                "where_condition": f"id_proyecto = {id_proyecto}"
        }
     }
    #print(update_data)
    response = requests.post(API_URL, json=update_data)
    if response.status_code ==200:
        flash("El registro se actualizó correctamente", 'success')
    else:
        #flash("Algo salió mal, no pudimos realizar la operación solipersonada", "danger")
        # Mostrar el mensaje de error detallado
        error_message = response.json().get("message", "Error desconocido al guardar los datos")
        return jsonify({"message": f"Error al guardar los datos: {error_message}"}), 500
    return redirect(url_for('idVistaProyectosInvestigacion.detalle', id=id_proyecto))

"""def obtener_proyecto_por_id(id):
    select_data = {
        "procedure": "select_json_entity",
        "parameters": {
            "table_name": "inv_proyecto",
            "where_condition": f"id_proyecto = {id}",
            "order_by": "",
            "limit_clause": "",
            "json_data": {},
            "select_columns": "*"
        }
    }
    # Aquí iría la lógica para hacer la consulta a la API y devolver el proyecto"""
    
@vistaProyectosInvestigacion.route('/crearInvestigador', methods=['POST'])
def crearInvestigador():
    id_proyecto = request.form.get('id_proyecto')
    insert_data = {
      "procedure": "insert_json_entity",
              "parameters": {
                "table_name": "inv_investigador_proyecto",
                "json_data":  {
                    "id_investigador": request.form.get('id_investigador'),                    
                    "id_proyecto": id_proyecto,
                    "tipo_participacion": request.form.get('tipo_participacion'),
                    "estado": request.form.get('estado'),
                    "horas_fase_1": request.form.get('horas_fase_1') if request.form.get('horas_fase_1') else 0,
                    "horas_fase_2": request.form.get('horas_fase_2') if request.form.get('horas_fase_2') else 0,
                    "horas_fase_3": request.form.get('horas_fase_3') if request.form.get('horas_fase_3') else 0,
                    "horas_fase_4": request.form.get('horas_fase_4') if request.form.get('horas_fase_4') else 0,
                    "horas_fase_5": request.form.get('horas_fase_5') if request.form.get('horas_fase_5') else 0,
                    "horas_fase_6": request.form.get('horas_fase_5') if request.form.get('horas_fase_6') else 0,
            }
        }
     }
    #print(insert_data)
    response = requests.post(API_URL, json=insert_data)
    if response.status_code ==200:
        flash("El registro se guardó correctamente", 'success')
    else:      
        error_message = response.json().get("message", "Error desconocido al guardar los datos")
        return jsonify({"message": f"Error al guardar los datos: {error_message}"}), 500
    

    return redirect(url_for('idVistaProyectosInvestigacion.detalle', id=id_proyecto))

@vistaProyectosInvestigacion.route('/editarInvestigador', methods=['POST'])
def editarInvestigador():
    id_proyecto = request.form.get('inv_id_proyecto')
    inv_id_investigador_proyecto = request.form.get('inv_id_investigador_proyecto')
    update_data = {
      "procedure": "update_json_entity",
              "parameters": {
                "table_name": "inv_investigador_proyecto",
                "json_data":  {
                    "tipo_participacion": request.form.get('inv_tipo_participacion'),
                    "estado": request.form.get('inv_estado'),
                    "horas_fase_1": request.form.get('inv_horas_fase_1') if request.form.get('inv_horas_fase_1') else 0,
                    "horas_fase_2": request.form.get('inv_horas_fase_2') if request.form.get('inv_horas_fase_2') else 0,
                    "horas_fase_3": request.form.get('inv_horas_fase_3') if request.form.get('inv_horas_fase_3') else 0,
                    "horas_fase_4": request.form.get('inv_horas_fase_4') if request.form.get('inv_horas_fase_4') else 0,
                    "horas_fase_5": request.form.get('inv_horas_fase_5') if request.form.get('inv_horas_fase_5') else 0,
                    "horas_fase_6": request.form.get('inv_horas_fase_5') if request.form.get('inv_horas_fase_6') else 0,
            },
                "where_condition": f"id_investigador_proyecto = {inv_id_investigador_proyecto}"
        }
     }
    #print(update_data)
    response = requests.post(API_URL, json=update_data)
    if response.status_code ==200:
        flash("El registro se guardó correctamente", 'success')
    else:      
        error_message = response.json().get("message", "Error desconocido al guardar los datos")
        return jsonify({"message": f"Error al guardar los datos: {error_message}"}), 500
    

    return redirect(url_for('idVistaProyectosInvestigacion.detalle', id=id_proyecto))
  
@vistaProyectosInvestigacion.route('/eliminarInvestigador', methods=[ 'POST'])
def eliminarInvestigador():
    id_proyecto = request.form.get('inv_proyecto_id')
    delete_data = {
      "procedure": "delete_json_entity",
        "parameters": {
            "table_name": "inv_investigador_proyecto",
            "where_condition": f"id_investigador_proyecto={request.form.get('inv_eliminar_id')}"
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
    
    return redirect(url_for('idVistaProyectosInvestigacion.detalle', id=id_proyecto))

    
@vistaProyectosInvestigacion.route('/crearProducto', methods=['POST'])
def crearProducto():
    id_proyecto = request.form.get('id_proyecto')
    insert_data = {
      "procedure": "insert_json_entity",
              "parameters": {
                "table_name": "inv_producto_proyecto",
                "json_data":  {
                    "id_producto": request.form.get('id_producto'),                    
                    "id_proyecto": id_proyecto,
                    "fecha_inicio": request.form.get('fecha_inicio'),
                    "fecha_entrega": request.form.get('fecha_entrega'),
                    "observacion": request.form.get('observacion'),
                    "fecha_publicacion": request.form.get('fecha_publicacion'),
            }
        }
     }
    #print(insert_data)
    response = requests.post(API_URL, json=insert_data)
    if response.status_code ==200:
        flash("El registro se guardó correctamente", 'success')
    else:      
        error_message = response.json().get("message", "Error desconocido al guardar los datos")
        return jsonify({"message": f"Error al guardar los datos: {error_message}"}), 500
    

    return redirect(url_for('idVistaProyectosInvestigacion.detalle', id=id_proyecto))
  
@vistaProyectosInvestigacion.route('/editarProducto', methods=['POST'])
def editarProducto():
    id_proyecto = request.form.get('pro_id_proyecto')
    update_data = {
      "procedure": "update_json_entity",
              "parameters": {
                "table_name": "inv_producto_proyecto",
                "json_data":  {
                    "id_producto": request.form.get('pro_id_producto'), 
                    "fecha_inicio": request.form.get('pro_fecha_inicio'),
                    "fecha_entrega": request.form.get('pro_fecha_entrega'),
                    "observacion": request.form.get('pro_observacion'),
                    "fecha_publicacion": request.form.get('pro_fecha_publicacion'),
            },
                "where_condition": f"id_prod_proy = {request.form.get('pro_id_prod_proy')}"
        }
     }
    
    response = requests.post(API_URL, json=update_data)
    if response.status_code ==200:
        flash("El registro se guardó correctamente", 'success')
    else:      
        error_message = response.json().get("message", "Error desconocido al guardar los datos")
        return jsonify({"message": f"Error al guardar los datos: {error_message}"}), 500
    

    return redirect(url_for('idVistaProyectosInvestigacion.detalle', id=id_proyecto))
 
    
@vistaProyectosInvestigacion.route('/crearCofinanciador', methods=['POST'])
def crearCofinanciador():
    id_proyecto = request.form.get('id_proyecto')
    insert_data = {
      "procedure": "insert_json_entity",
              "parameters": {
                "table_name": "inv_cofinanciador_proyecto",
                "json_data":  {
                    "id_cofinanciador": request.form.get('id_cofinanciador'),                    
                    "id_proyecto": id_proyecto,
                    "contrapartida_especie": request.form.get('contrapartida_especie'),
                    "contrapartida_dinero": request.form.get('contrapartida_dinero')
            }
        }
     }
    #print(insert_data)
    response = requests.post(API_URL, json=insert_data)
    if response.status_code ==200:
        flash("El registro se guardó correctamente", 'success')
    else:      
        error_message = response.json().get("message", "Error desconocido al guardar los datos")
        return jsonify({"message": f"Error al guardar los datos: {error_message}"}), 500
    

    return redirect(url_for('idVistaProyectosInvestigacion.detalle', id=id_proyecto))
  
@vistaProyectosInvestigacion.route('/editarCofinanciador', methods=['POST'])
def editarCofinanciador():
    id_proyecto = request.form.get('cof_id_proyecto')
    update_data = {
      "procedure": "update_json_entity",
              "parameters": {
                "table_name": "inv_cofinanciador_proyecto",
                "json_data":  {
                    "id_cofinanciador": request.form.get('cof_id_cofinanciador'), 
                    "contrapartida_especie": request.form.get('cof_contrapartida_especie'),
                    "contrapartida_dinero": request.form.get('cof_contrapartida_dinero')
            },
                "where_condition": f"id_cofinan_proyecto = {request.form.get('cof_id_cofinan_proyecto')}"
        }
     }
    
    response = requests.post(API_URL, json=update_data)
    if response.status_code ==200:
        flash("El registro se guardó correctamente", 'success')
    else:      
        error_message = response.json().get("message", "Error desconocido al guardar los datos")
        return jsonify({"message": f"Error al guardar los datos: {error_message}"}), 500
    

    return redirect(url_for('idVistaProyectosInvestigacion.detalle', id=id_proyecto))
 
@vistaProyectosInvestigacion.route('/eliminarCofinanciador', methods=[ 'POST'])
def eliminarCofinanciador():
    id_proyecto = request.form.get('cofe_proyecto_id')
    delete_data = {
      "procedure": "delete_json_entity",
        "parameters": {
            "table_name": "inv_cofinanciador_proyecto",
            "where_condition": f"id_cofinan_proyecto={request.form.get('cofe_eliminar_id')}"
        }
     }

    print(id_proyecto)
    
    response = requests.post(API_URL, json=delete_data)
    if response.status_code ==200:
        flash("El registro se eliminó correctamente", 'success')
    else:
        #flash("Algo salió mal, no pudimos realizar la operación solipersonada", "danger")
        # Mostrar el mensaje de error detallado
        error_message = response.json().get("message", "Error desconocido al guardar los datos")
        return jsonify({"message": f"Error al guardar los datos: {error_message}"}), 500
    
    return redirect(url_for('idVistaProyectosInvestigacion.detalle', id=id_proyecto))

   
  
@vistaProyectosInvestigacion.route('/crearAuxiliar', methods=['POST'])
def crearAuxiliar():
    id_proyecto = request.form.get('id_proyecto')
    insert_data = {
      "procedure": "insert_json_entity",
              "parameters": {
                "table_name": "inv_auxiliar_proyecto",
                "json_data":  {
                    "id_estudiante": request.form.get('id_estudiante'),                    
                    "id_proyecto": id_proyecto,
                    "fecha": now(),
            }
        }
     }
    #print(insert_data)
    response = requests.post(API_URL, json=insert_data)
    if response.status_code ==200:
        flash("El registro se guardó correctamente", 'success')
    else:      
        error_message = response.json().get("message", "Error desconocido al guardar los datos")
        return jsonify({"message": f"Error al guardar los datos: {error_message}"}), 500
    

    return redirect(url_for('idVistaProyectosInvestigacion.detalle', id=id_proyecto))
  
@vistaProyectosInvestigacion.route('/crearSeguimiento', methods=['POST'])
def crearSeguimiento():
    id_proyecto = request.form.get('seg_id_proyecto')
    file = request.files.get('file_seguimiento')
    observacion = request.form.get('observacion_seguimiento')

    if not file:
        flash('No se seleccionó ningún archivo', 'danger')
        return redirect(url_for('ruta_donde_redirigir_en_caso_de_error'))

    # Definir la carpeta donde se guardará el archivo
    folder_path = f'uploads/{id_proyecto}/seguimiento_productos'
      # Obtener la fecha y hora actual en formato 'YYYYMMDD_HHMMSS'
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Obtener la extensión original del archivo
    _, file_extension = os.path.splitext(file.filename)

    # Crear un nombre de archivo único utilizando la fecha, hora y extensión
    filename = timestamp
    # Utilizar el nombre original del archivo
    file_path = handle_file_upload_seguimiento(file, id_proyecto, filename, custom_folder=folder_path)
    
    file_path = file_path.replace('\\', '/')
    if not file_path:
        flash('Error al subir el archivo', 'danger')
        return redirect(url_for('ruta_donde_redirigir_en_caso_de_error'))

    update_data = {
        "procedure": "insert_json_entity",
        "parameters": {
            "table_name": "inv_seguimiento",
            "json_data": {                  
                "id_producto_proyecto": request.form.get('seg_id_producto_proyecto'),
                "observacion_seguimiento": request.form.get('observacion_seguimiento'),
                "nombre_soporte": file_path,
                "fecha": now()
            }
        }
    }
    #print(update_data)
    response = requests.post(API_URL, json=update_data)
    if response.status_code == 200:
        flash("El registro se guardó correctamente", 'success')
    else:            
        error_message = response.json().get("message", "Error desconocido al guardar los datos")
        return jsonify({"message": f"Error al guardar los datos: {error_message}"}), 500


    return redirect(url_for('idVistaProyectosInvestigacion.detalle', id=id_proyecto))

@vistaProyectosInvestigacion.route('/eliminarSeguimiento', methods=[ 'POST'])
def eliminarSeguimiento():
    json_data = productoProyectoById(request.form.get('seg_proyecto_id'))
    data = json.loads(json_data)
    id_proyecto = data[0].get('id_proyecto')
    delete_data = {
      "procedure": "delete_json_entity",
        "parameters": {
            "table_name": "inv_seguimiento",
            "where_condition": f"id_seguimiento={request.form.get('seg_eliminar_id')}"
        }
     }
    path = request.form.get('seg_path')
    eliminar_soporte_seguimiento(path)
    #print(id_proyecto)
    
    response = requests.post(API_URL, json=delete_data)
    if response.status_code ==200:
        flash("El registro se eliminó correctamente", 'success')
    else:
        #flash("Algo salió mal, no pudimos realizar la operación solipersonada", "danger")
        # Mostrar el mensaje de error detallado
        error_message = response.json().get("message", "Error desconocido al guardar los datos")
        return jsonify({"message": f"Error al guardar los datos: {error_message}"}), 500
    
    return redirect(url_for('idVistaProyectosInvestigacion.detalle', id=id_proyecto))



#Get Data
@vistaProyectosInvestigacion.route('/get_investigador', methods=['POST'])
def get_investigador():
    investigador_id = request.form.get('id')
    if not investigador_id:
        return jsonify({"error": "ID is required"}), 400
    response = investigadorProyectoById(investigador_id)

    data = response     
    #print(data) 
    if len(data) > 0:       
        ids_editar = {
                "id_investigador_proyecto": "inv_id_investigador_proyecto",
                "id_proyecto": "inv_id_proyecto",
                "id_investigador": "inv_id_investigador",
                "tipo_participacion": "inv_tipo_participacion",
                "estado": "inv_estado",
                "horas_fase_1": "inv_horas_fase_1",
                "horas_fase_2": "inv_horas_fase_2",
                "horas_fase_3": "inv_horas_fase_3",
                "horas_fase_4": "inv_horas_fase_4",
                "horas_fase_5": "inv_horas_fase_5",
                "horas_fase_6": "inv_horas_fase_6",
        } 
        result = {
                "data": data,  
                "ids_editar": ids_editar 
            }    
        #print(result)
        return jsonify(result), 200
    else:
        return jsonify({"error": "Failed to retrieve data"}), 500

@vistaProyectosInvestigacion.route('/get_producto', methods=['POST'])
def get_producto():
    producto_id = request.form.get('id')
    if not producto_id:
        return jsonify({"error": "ID is required"}), 400
    response = productoProyectoById(producto_id)

    data = response     
    #print(data) 
    if len(data) > 0:       
        ids_editar = {
                "id_prod_proy": "pro_id_prod_proy",
                "id_producto": "pro_id_producto",
                "id_proyecto": "pro_id_proyecto",
                "fecha_inicio": "pro_fecha_inicio",
                "fecha_entrega": "pro_fecha_entrega",
                "observacion": "pro_observacion",
                "fecha_publicacion": "pro_fecha_publicacion"
        } 
        result = {
                "data": data,  
                "ids_editar": ids_editar 
            }    
        #print(result)
        return jsonify(result), 200
    else:
        return jsonify({"error": "Failed to retrieve data"}), 500

@vistaProyectosInvestigacion.route('/get_producto_seguimiento', methods=['POST'])
def get_producto_seguimiento():
    producto_id = request.form.get('id')
    if not producto_id:
        return jsonify({"error": "ID is required"}), 400
    response = productoProyectoById(producto_id)
    data = response     
    
    seguimiento= seguimientoProducto(producto_id)
    if len(data) > 0:       
        ids_editar = {
                "id_prod_proy": "seg_id_producto_proyecto",
                "id_proyecto": "seg_id_proyecto",
        } 
        result = {
                "data": data,  
                "ids_editar": ids_editar,
                "seguimiento": seguimiento
            }    
        #print(result)
        return jsonify(result), 200
    else:
        return jsonify({"error": "Failed to retrieve data"}), 500

@vistaProyectosInvestigacion.route('/get_cofinanciador', methods=['POST'])
def get_cofinanciador():
    cofinanciador_id = request.form.get('id')
    if not cofinanciador_id:
        return jsonify({"error": "ID is required"}), 400
    response = cofinanciadorById(cofinanciador_id)
    data = response     
    
    if len(data) > 0:       
        ids_editar = {
                "id_cofinan_proyecto": "cof_id_cofinan_proyecto",
                "id_cofinanciador": "cof_id_cofinanciador",
                "contrapartida_especie": "cof_contrapartida_especie",
                "contrapartida_dinero": "cof_contrapartida_dinero",
        } 
        result = {
                "data": data,  
                "ids_editar": ids_editar
            }    
        print(result)
        return jsonify(result), 200
    else:
        return jsonify({"error": "Failed to retrieve data"}), 500

#Select list Proyectos
def investigadoresProyecto(id):
    select_data = {
            "projectName": projectName,
            "procedure": "select_json_entity",
            "parameters": {
                "table_name": "inv_investigador_proyecto i INNER JOIN inv_investigadores p ON p.id_investigador = i.id_investigador",
                "json_data": {},
                "where_condition": f"id_proyecto={id}",
                "select_columns": "p.nombre_investigador,p.id_investigador, id_investigador_proyecto, id_proyecto, tipo_participacion, estado, horas_fase_1, horas_fase_2, horas_fase_3, horas_fase_4, horas_fase_5, horas_fase_6 ",
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

def productosProyecto(id):
    select_data = {
            "projectName": projectName,
            "procedure": "select_json_entity",
            "parameters": {
                "table_name": "inv_producto_proyecto p INNER JOIN inv_producto d ON d.id_producto = p.id_producto ",
                "json_data": {},
                "where_condition":  f"id_proyecto={id}",
                "select_columns": "id_prod_proy, d.subtipo, d.id_producto, id_proyecto, fecha_inicio, fecha_entrega, observacion, fecha_publicacion, investigador, horas_adicionales, soporte_verifica, nombre_soporte, created, created_by, updated, updated_by, avance",
                "order_by": "id_prod_proy",
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

def cofinanciadoresProyecto(id):
    select_data = {
            "projectName": projectName,
            "procedure": "select_json_entity",
            "parameters": {
                "table_name": "inv_cofinanciador_proyecto c INNER JOIN inv_cofinanciador p ON p.id_cofinanciador = c.id_cofinanciador",
                "json_data": {},
                "where_condition":  f"c.id_proyecto={id}",
                "select_columns": "c.id_proyecto,p.institucion, p.nit, c.id_cofinanciador, c.contrapartida_especie, c.contrapartida_dinero, c.id_cofinan_proyecto",
                "order_by": "p.institucion",
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

def AuxiliaresProyecto(id):
    select_data = {
            "projectName": projectName,
            "procedure": "select_json_entity",
            "parameters": {
                "table_name": "inv_auxiliar_proyecto c INNER JOIN inv_estudiantes p ON p.id_estudiante = c.id_estudiante",
                "json_data": {},
                "where_condition":  f"c.id_proyecto={id}",
                "select_columns": "p.id_estudiante,p.identificacion, p.nombre_estudiante, c.id_auxiliar_proyecto, c.fecha",
                "order_by": "p.nombre_estudiante",
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

def investigadorProyectoById(id):
    select_data = {
            "projectName": projectName,
            "procedure": "select_json_entity",
            "parameters": {
                "table_name": "inv_investigador_proyecto",
                "json_data": {},
                "where_condition":  f"id_investigador_proyecto={id}",
                "select_columns": "",
                "order_by": "",
                "limit_clause": ""
            }
        }
    #print(select_data)
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

def productoProyectoById(id):
    select_data = {
            "projectName": projectName,
            "procedure": "select_json_entity",
            "parameters": {
                "table_name": "inv_producto_proyecto",
                "json_data": {},
                "where_condition":  f"id_prod_proy={id}",
                "select_columns": "",
                "order_by": "",
                "limit_clause": ""
            }
        }
    #print(select_data)
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


def investigadoresNotInProyecto(id):    
    select_data = {
            "projectName": projectName,
            "procedure": "select_json_entity",
            "parameters": {
                "table_name": f"inv_investigadores i LEFT JOIN inv_investigador_proyecto p ON i.id_investigador = p.id_investigador AND p.id_proyecto = {id}",
                "json_data": {},
                "where_condition": "p.id_investigador IS NULL",
                "select_columns": "i.id_investigador, i.nombre_investigador",
                "order_by": "i.nombre_investigador",
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


def estudiantesNotInProyecto(id):    
    select_data = {
            "projectName": projectName,
            "procedure": "select_json_entity",
            "parameters": {
                "table_name": f"inv_estudiantes e LEFT JOIN inv_auxiliar_proyecto p ON p.id_estudiante = e.id_estudiante AND p.id_proyecto = {id}",
                "json_data": {},
                "where_condition": "p.id_estudiante IS NULL",
                "select_columns": "e.id_estudiante, e.nombre_estudiante",
                "order_by": "e.nombre_estudiante",
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


def seguimientoProducto(id):    
    select_data = {
            "projectName": projectName,
            "procedure": "select_json_entity",
            "parameters": {
                "table_name": "inv_seguimiento",
                "json_data": {},
                "where_condition": f"id_producto_proyecto ={id}",
                "select_columns": "",
                "order_by": "fecha",
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

def cofinanciadorById(id):
    select_data = {
            "projectName": projectName,
            "procedure": "select_json_entity",
            "parameters": {
                "table_name": "inv_cofinanciador_proyecto",
                "json_data": {},
                "where_condition":  f"id_cofinan_proyecto={id}",
                "select_columns": "",
                "order_by": "",
                "limit_clause": ""
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