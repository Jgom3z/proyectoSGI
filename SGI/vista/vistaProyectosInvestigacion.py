from flask import Blueprint, render_template, request, jsonify
import json
import requests
import os
from .functions import paginate, now

API_URL = os.getenv('API_URL')

vistaProyectosInvestigacion = Blueprint('idVistaProyectosInvestigacion', __name__, template_folder='../templates')

@vistaProyectosInvestigacion.route('/listar', methods=['GET', 'POST'])
def listar():
    select_data = {
        "procedure": "select_json_entity",
        "parameters": {
            "table_name": """
                inv_proyectos p 
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
                           search_term=search_term)

@vistaProyectosInvestigacion.route('/detalle/<int:id>', methods=['GET'])
def detalle(id):
    # Aquí deberías implementar la lógica para obtener los detalles del proyecto
    # por su ID y pasarlos a la plantilla
    proyecto = obtener_proyecto_por_id(id)
    return render_template('proyectosInvestigacion/detalle.html', proyecto=proyecto)

@vistaProyectosInvestigacion.route('/crear', methods=['POST'])
def crearProyecto():
    # Implementa la lógica para crear un nuevo proyecto
    pass

@vistaProyectosInvestigacion.route('/editar', methods=['POST'])
def editarProyecto():
    # Implementa la lógica para editar un proyecto existente
    pass

@vistaProyectosInvestigacion.route('/descargar_archivo/<tipo>/<int:id>', methods=['GET'])
def descargar_archivo(tipo, id):
    # Implementar la lógica para descargar archivos
    pass

def obtener_proyecto_por_id(id):
    # Implementar la lógica para obtener un proyecto por su ID
    pass