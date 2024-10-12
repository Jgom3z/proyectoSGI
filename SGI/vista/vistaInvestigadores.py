# SGI/vista/vistaInvestigadores.py

from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
import json
import requests
from vista.functions import paginate, now
import os
import logging
from vista.select_list import facultad

API_URL = os.getenv('API_URL')
if not API_URL:
    raise ValueError("API_URL no está configurada en las variables de entorno")

vistaInvestigadores = Blueprint('idVistaInvestigadores', __name__, template_folder='templates')

@vistaInvestigadores.route('/listar', methods=['GET', 'POST'])
def listar():
    select_data = {
        "procedure": "select_json_entity",
        "parameters": {
            "table_name": "inv_investigadores i INNER JOIN inv_facultad f ON f.id_facultad = i.id_facultad",
            "where_condition": "",
            "order_by": "i.nombre_investigador",
            "limit_clause": "",
            "json_data": {},
            "select_columns": "i.id_investigador, i.cedula, i.nombre_investigador, i.categoria_institucion, f.nombre_facultad, i.categoria_colciencias, i.orcid, i.nivel_de_formacion, i.correo, i.telefono"
        }
    }

    try:
        response = requests.post(API_URL, json=select_data)
        response.raise_for_status()
    except requests.RequestException as e:
        logging.error(f"Error al consultar la API: {str(e)}")
        flash(f"Error al consultar la API: {str(e)}", "error")
        return render_template('investigadores/listar.html', data=[], 
                               total_pages=0, page=1)

    search_term = request.args.get('search', '').lower()

    data_investigadores = response.json()
    if 'result' in data_investigadores and data_investigadores['result']:
        data = json.loads(data_investigadores['result'][0]['result'])
        if search_term:
            data = [item for item in data if any(search_term in str(value).lower() for value in item.values())]
        route_pagination = 'idVistaInvestigadores.listar'
        investigadores, total_pages, route_pagination, page = paginate(data, route_pagination)
    else:
        investigadores = []
        total_pages = 0
        page = 1
        route_pagination = 'idVistaInvestigadores.listar'

    

    return render_template('investigadores/listar.html',
                           data=investigadores, 
                           total_pages=total_pages,
                           page=page, 
                           search_term=search_term,
                           route_pagination=route_pagination,
                           facultad=facultad())

@vistaInvestigadores.route('/crear', methods=['POST'])
def crear():
    if request.method == 'POST':
        nuevo_investigador = {
            "cedula": request.form['cedula'],
            "nombre_investigador": request.form['nombre_investigador'],
            "id_facultad": request.form['id_facultad'],
            "categoria_institucion": request.form['categoria_institucion'],
            "categoria_colciencias": request.form['categoria_colciencias'],
            "orcid": request.form['orcid'],
            "nivel_de_formacion": request.form['nivel_de_formacion'],
            "correo": request.form['correo'],
            "telefono": request.form['telefono']
        }

        insert_data = {
            "procedure": "insert_json_entity",
            "parameters": {
                "table_name": "inv_investigadores",
                "json_data": json.dumps(nuevo_investigador)
            }
        }

        try:
            response = requests.post(API_URL, json=insert_data)
            response.raise_for_status()
            flash('Investigador creado con éxito', 'success')
        except requests.RequestException as e:
            logging.error(f"Error al crear investigador: {str(e)}")
            flash(f"Error al crear investigador: {str(e)}", "error")

    return redirect(url_for('idVistaInvestigadores.listar', facultad = facultad()))

@vistaInvestigadores.route('/detalle/<int:id>', methods=['GET'])
def detalle(id):
    select_data = {
        "procedure": "select_json_entity",
        "parameters": {
            "table_name": "inv_investigadores i INNER JOIN inv_facultad f ON f.id_facultad = i.id_facultad",
            "where_condition": f"i.id_investigador = {id}",
            "order_by": "",
            "limit_clause": "",
            "json_data": {},
            "select_columns": "i.*, f.nombre_facultad"
        }
    }

    try:
        response = requests.post(API_URL, json=select_data)
        response.raise_for_status()
        data = response.json()
        if 'result' in data and data['result']:
            investigador = json.loads(data['result'][0]['result'])[0]
        else:
            flash('Investigador no encontrado', 'error')
            return redirect(url_for('idVistaInvestigadores.listar'))
    except requests.RequestException as e:
        logging.error(f"Error al obtener detalles del investigador: {str(e)}")
        flash(f"Error al obtener detalles del investigador: {str(e)}", "error")
        return redirect(url_for('idVistaInvestigadores.listar'))

    # Aquí puedes agregar la lógica para obtener proyectos y productos del investigador

    return render_template('investigadores/detalle.html', investigador=investigador)

# ... (mantener las otras rutas como estaban)
@vistaInvestigadores.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    if request.method == 'GET':
        # Obtener los datos del investigador
        select_data = {
            "procedure": "select_json_entity",
            "parameters": {
                "table_name": "inv_investigadores i INNER JOIN inv_facultad f ON f.id_facultad = i.id_facultad",
                "where_condition": f"i.id_investigador = {id}",
                "order_by": "",
                "limit_clause": "",
                "json_data": {},
                "select_columns": "i.*, f.nombre_facultad"
            }
        }

        try:
            response = requests.post(API_URL, json=select_data)
            response.raise_for_status()
            data = response.json()
            if 'result' in data and data['result']:
                investigador = json.loads(data['result'][0]['result'])[0]
            else:
                flash('Investigador no encontrado', 'error')
                return redirect(url_for('idVistaInvestigadores.listar'))
        except requests.RequestException as e:
            logging.error(f"Error al obtener detalles del investigador: {str(e)}")
            flash(f"Error al obtener detalles del investigador: {str(e)}", "error")
            return redirect(url_for('idVistaInvestigadores.listar'))

       

        return render_template('investigadores/editar.html', investigador=investigador, facultad=facultad)

    elif request.method == 'POST':
        # Procesar el formulario de edición
        investigador_actualizado = {
            "cedula": request.form['cedula'],
            "nombre_investigador": request.form['nombre_investigador'],
            "id_facultad": request.form['id_facultad'],
            "categoria_institucion": request.form['categoria_institucion'],
            "categoria_colciencias": request.form['categoria_colciencias'],
            "orcid": request.form['orcid'],
            "nivel_de_formacion": request.form['nivel_de_formacion'],
            "correo": request.form['correo'],
            "telefono": request.form['telefono']
        }

        update_data = {
            "procedure": "update_json_entity",
            "parameters": {
                "table_name": "inv_investigadores",
                "where_condition": f"id_investigador={id}",
                "json_data": json.dumps(investigador_actualizado)
            }
        }

        try:
            response = requests.post(API_URL, json=update_data)
            response.raise_for_status()
            flash('Investigador actualizado exitosamente', 'success')
        except requests.RequestException as e:
            logging.error(f"Error al actualizar el investigador: {str(e)}")
            flash(f"Error al actualizar el investigador: {str(e)}", "error")

        return redirect(url_for('idVistaInvestigadores.detalle', id=id))
