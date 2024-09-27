from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
import json
import requests
from vista.functions import paginate, now
import os
import logging

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
        return render_template('investigadores/listar.html', data=[], total_pages=0, page=1)

    search_term = request.args.get('search', '').lower()

    data_investigadores = response.json()
    if 'result' in data_investigadores and data_investigadores['result']:
        data = json.loads(data_investigadores['result'][0]['result'])
        if search_term:
            data = [item for item in data if any(search_term in str(value).lower() for value in item.values())]
        route_pagination = 'idVistaInvestigadores.listar'
        investigadores, total_pages, page = paginate(data, route_pagination)
    else:
        investigadores = []
        total_pages = 0
        page = 1

    logging.info(f"Número de investigadores: {len(investigadores)}")
    
    facultades_data = {
        "procedure": "select_json_entity",
        "parameters": {
            "table_name": "inv_facultad",
            "where_condition": "",
            "order_by": "nombre_facultad",
            "limit_clause": "",
            "json_data": {},
            "select_columns": "id_facultad, nombre_facultad"
        }
    }
    facultades_response = requests.post(API_URL, json=facultades_data)
    facultades = json.loads(facultades_response.json()['result'][0]['result']) if facultades_response.status_code == 200 else []

    return render_template('investigadores/listar.html',
                           data=investigadores, total_pages=total_pages,
                           page=page, search_term=search_term,
                           facultades=facultades)

@vistaInvestigadores.route('/ver-detalle/<int:id>', methods=['GET'])
def detalle(id):
    select_data = {
        "procedure": "select_json_entity",
        "parameters": {
            "table_name": "inv_investigadores i INNER JOIN inv_facultad f ON f.id_facultad = i.id_facultad",
            "where_condition": f"i.id_investigador={id}",
            "order_by": "",
            "limit_clause": "",
            "json_data": {},
            "select_columns": "i.*, f.nombre_facultad"
        }
    }

    response = requests.post(API_URL, json=select_data)
    if response.status_code != 200:
        flash(f"Error al consultar la API: {response.status_code}", "error")
        return redirect(url_for('idVistaInvestigadores.listar'))

    data_investigador = response.json()
    if 'result' in data_investigador and data_investigador['result'] and data_investigador['result'][0]['result']:
        investigador = json.loads(data_investigador['result'][0]['result'])[0]
    else:
        flash("Investigador no encontrado", "error")
        return redirect(url_for('idVistaInvestigadores.listar'))

    return render_template('investigadores/detalle.html', investigador=investigador)

@vistaInvestigadores.route('/crear', methods=['POST'])
def crear():
    if request.method == 'POST':
        nuevo_investigador = {
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
            "categoria_colciencias_esperada": request.form.get('categoria_colciencias_esperada'),
            "cvlac": request.form.get('cvlac')
        }

        insert_data = {
            "procedure": "insert_json_entity",
            "parameters": {
                "table_name": "inv_investigadores",
                "json_data": nuevo_investigador
            }
        }

        response = requests.post(API_URL, json=insert_data)

        if response.status_code == 200:
            result = response.json()
            if 'result' in result and result['result']:
                nuevo_id = json.loads(result['result'][0]['result'])[0]['id_investigador']
                flash('Investigador creado exitosamente', 'success')
                return redirect(url_for('idVistaInvestigadores.detalle', id=nuevo_id))
            else:
                flash('Error al crear el investigador', 'error')
        else:
            flash(f'Error en la solicitud: {response.status_code}', 'error')

        return redirect(url_for('idVistaInvestigadores.listar'))

@vistaInvestigadores.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    if request.method == 'GET':
        select_data = {
            "procedure": "select_json_entity",
            "parameters": {
                "table_name": "inv_investigadores",
                "where_condition": f"id_investigador={id}",
                "order_by": "",
                "limit_clause": "",
                "json_data": {},
                "select_columns": "*"
            }
        }
        response = requests.post(API_URL, json=select_data)
        if response.status_code != 200:
            return f"Error al consultar la API: {response.status_code}"

        data_investigador = response.json()
        if 'result' in data_investigador and data_investigador['result']:
            investigador = json.loads(data_investigador['result'][0]['result'])[0]
        else:
            return "Investigador no encontrado", 404

        facultades_data = {
            "procedure": "select_json_entity",
            "parameters": {
                "table_name": "inv_facultad",
                "where_condition": "",
                "order_by": "nombre_facultad",
                "limit_clause": "",
                "json_data": {},
                "select_columns": "id_facultad, nombre_facultad"
            }
        }
        response = requests.post(API_URL, json=facultades_data)
        facultades = json.loads(response.json()['result'][0]['result']) if response.status_code == 200 else []

        return render_template('investigadores/editar.html', investigador=investigador, facultades=facultades)

    elif request.method == 'POST':
        update_data = {
            "procedure": "update_json_entity",
            "parameters": {
                "table_name": "inv_investigadores",
                "where_condition": f"id_investigador={id}",
                "json_data": request.form
            }
        }
        response = requests.post(API_URL, json=update_data)
        if response.status_code != 200:
            return f"Error al actualizar el investigador: {response.status_code}"

        flash('Investigador actualizado exitosamente', 'success')
        return redirect(url_for('idVistaInvestigadores.detalle', id=id))

@vistaInvestigadores.route('/eliminar/<int:id>', methods=['POST'])
def eliminar(id):
    delete_data = {
        "procedure": "delete_json_entity",
        "parameters": {
            "table_name": "inv_investigadores",
            "where_condition": f"id_investigador={id}"
        }
    }

    response = requests.post(API_URL, json=delete_data)

    if response.status_code == 200:
        result = response.json()
        if 'result' in result and result['result']:
            flash('Investigador eliminado exitosamente', 'success')
        else:
            flash('Error al eliminar el investigador', 'error')
    else:
        flash(f'Error en la solicitud: {response.status_code}', 'error')

    return redirect(url_for('idVistaInvestigadores.listar'))