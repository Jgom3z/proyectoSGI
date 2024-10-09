from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
import json
import requests
import os
from .functions import paginate, now
from vista.select_list import grupos, lineas

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
    print(select_data)

    try:
        response = requests.post(API_URL, json=select_data)
        response.raise_for_status()
        data_proyecto = response.json()
    except requests.RequestException as e:
        return jsonify({"error": f"Error al consultar la API: {str(e)}"}), 500
    except json.JSONDecodeError:
        return jsonify({"error": "La respuesta de la API no es un JSON válido"}), 500

    print("Respuesta de la API para detalle:", response.text)

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
    print(result)

    return render_template('proyectosInvestigacion/detalle.html', proyecto=proyecto[0], grupos=grupos(), lineas = lineas() )


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
    print(update_data)
    response = requests.post(API_URL, json=update_data)
    if response.status_code ==200:
        flash("El registro se actualizó correctamente", 'success')
    else:
        #flash("Algo salió mal, no pudimos realizar la operación solipersonada", "danger")
        # Mostrar el mensaje de error detallado
        error_message = response.json().get("message", "Error desconocido al guardar los datos")
        return jsonify({"message": f"Error al guardar los datos: {error_message}"}), 500
    return redirect(url_for('idVistaProyectosInvestigacion.detalle', id=id_proyecto))

def obtener_proyecto_por_id(id):
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
    # Aquí iría la lógica para hacer la consulta a la API y devolver el proyecto