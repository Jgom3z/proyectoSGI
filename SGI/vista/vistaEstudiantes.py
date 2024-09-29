# SGI/vista/vistaEstudiantes.py

from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
import json
import requests
from vista.functions import paginate, now
import os
import logging

API_URL = os.getenv('API_URL')
if not API_URL:
    raise ValueError("API_URL no está configurada en las variables de entorno")

vistaEstudiantes = Blueprint('idVistaEstudiantes', __name__, template_folder='templates')

@vistaEstudiantes.route('/listar', methods=['GET', 'POST'])
def listar():
    select_data = {
        "procedure": "select_json_entity",
        "parameters": {
            "table_name": "inv_estudiantes e INNER JOIN inv_facultad f ON f.id_facultad = e.id_facultad",
            "where_condition": "",
            "order_by": "e.nombre_estudiante",
            "limit_clause": "",
            "json_data": {},
            "select_columns": "e.id_estudiante, e.identificacion, e.nombre_estudiante, e.codigo, e.correo, f.nombre_facultad"
        }
    }

    try:
        response = requests.post(API_URL, json=select_data)
        response.raise_for_status()
        data_estudiantes = response.json()
    except requests.RequestException as e:
        logging.error(f"Error al consultar la API: {str(e)}")
        flash(f"Error al consultar la API: {str(e)}", "error")
        return render_template('estudiantes/listar.html', data=[], total_pages=0, page=1, facultades=[])

    search_term = request.args.get('search', '').lower()

    if 'result' in data_estudiantes and data_estudiantes['result']:
        try:
            data = json.loads(data_estudiantes['result'][0]['result'])
        except (json.JSONDecodeError, TypeError) as e:
            logging.error(f"Error al decodificar JSON: {str(e)}")
            flash("Error al procesar los datos de estudiantes", "error")
            return render_template('estudiantes/listar.html', data=[], total_pages=0, page=1, facultades=[])

        if search_term:
            data = [item for item in data if any(search_term in str(value).lower() for value in item.values())]
        route_pagination = 'idVistaEstudiantes.listar'
        estudiantes, total_pages, route_pagination, page = paginate(data, route_pagination)
    else:
        estudiantes = []
        total_pages = 0
        page = 1
        route_pagination = 'idVistaEstudiantes.listar'

    # Obtener lista de facultades para el formulario de creación
    facultades_data = {
        "procedure": "select_json_entity",
        "parameters": {
            "table_name": "inv_facultad",
            "select_columns": "id_facultad, nombre_facultad",
            "order_by": "nombre_facultad"
        }
    }

    try:
        facultades_response = requests.post(API_URL, json=facultades_data)
        facultades_response.raise_for_status()
        facultades_result = facultades_response.json()
        if 'result' in facultades_result and facultades_result['result']:
            facultades = json.loads(facultades_result['result'][0]['result'])
        else:
            facultades = []
    except (requests.RequestException, json.JSONDecodeError) as e:
        logging.error(f"Error al obtener facultades: {str(e)}")
        facultades = []

    return render_template('estudiantes/listar.html', 
                           data=estudiantes, 
                           total_pages=total_pages, 
                           page=page, 
                           search_term=search_term,
                           route_pagination=route_pagination,
                           facultades=facultades)

@vistaEstudiantes.route('/crear', methods=['POST'])
def crear():
    if request.method == 'POST':
        nuevo_estudiante = {
            "identificacion": request.form['identificacion'],
            "nombre_estudiante": request.form['nombre_estudiante'],
            "codigo": request.form['codigo'],
            "id_facultad": request.form['id_facultad'],
            "correo": request.form['correo']
        }

        insert_data = {
            "procedure": "insert_json_entity",
            "parameters": {
                "table_name": "inv_estudiantes",
                "json_data": json.dumps(nuevo_estudiante)
            }
        }

        try:
            response = requests.post(API_URL, json=insert_data)
            response.raise_for_status()
            flash('Estudiante creado exitosamente', 'success')
        except requests.RequestException as e:
            logging.error(f"Error al crear el estudiante: {str(e)}")
            flash(f"Error al crear el estudiante: {str(e)}", "error")

    return redirect(url_for('idVistaEstudiantes.listar'))

