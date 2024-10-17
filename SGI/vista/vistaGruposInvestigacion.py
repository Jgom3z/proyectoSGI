from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
import json
import requests
from vista.functions import paginate, now
import os
from vista.select_list import investigadores
from vista.select_list import facultad
from vista.select_list import grupos


API_URL = os.getenv('API_URL')

vistaGruposInvestigacion = Blueprint('idVistaGruposInvestigacion', __name__, template_folder='templates')

@vistaGruposInvestigacion.route('/listar', methods=['GET', 'POST'])
def listar():
    select_data = {
        "procedure": "select_json_entity",
        "parameters": {
            "table_name": "inv_grupos g INNER JOIN inv_facultad f ON f.id_facultad = g.id_facultad INNER JOIN inv_investigadores i ON i.id_investigador = g.id_lider",
            "where_condition": "",
            "order_by": "g.nombre_grupo",
            "limit_clause": "",
            "json_data": {},
            "select_columns": "g.id_grupo, g.nombre_grupo, g.codigo_grup_lac, g.categoria_colciencias, f.nombre_facultad, i.nombre_investigador"
        }
    }

    response = requests.post(API_URL, json=select_data)
    if response.status_code != 200:
        return f"Error al consultar la API: {response.status_code}"

    search_term = request.args.get('search', '').lower()

    data_grupos = response.json()
    if 'result' in data_grupos and data_grupos['result']:
        data = json.loads(data_grupos['result'][0]['result'])
        if search_term:
            data = [item for item in data if any(search_term in str(value).lower() for value in item.values())]
        route_pagination = 'idVistaGruposInvestigacion.listar'
        grupos, total_pages, route_pagination, page = paginate(data, route_pagination)
    else:
        grupos = []
        total_pages = 0
        page = 1

    return render_template('grupos/listar.html',
                           data=grupos, total_pages=total_pages,
                           route_pagination=route_pagination, page=page,
                           search_term=search_term, investigadores = investigadores(),
                           facultad = facultad())

@vistaGruposInvestigacion.route('/ver-detalle/<int:id>', methods=['GET'])
def detalle(id):
    # Obtener detalles del grupo
    select_data = {
        "procedure": "select_json_entity",
        "parameters": {
            "table_name": "inv_grupos g INNER JOIN inv_facultad f ON f.id_facultad = g.id_facultad INNER JOIN inv_investigadores i ON i.id_investigador = g.id_lider",
            "where_condition": f"g.id_grupo={id}",
            "order_by": "",
            "limit_clause": "",
            "json_data": {},
            "select_columns": "g.*, f.nombre_facultad, i.nombre_investigador"
        }
    }

    response = requests.post(API_URL, json=select_data)
    if response.status_code != 200:
        return f"Error al consultar la API: {response.status_code}"
   
    data_grupos = response.json()
    if 'result' in data_grupos and data_grupos['result']:
        data = data_grupos['result'][0]['result']
        grupo = json.loads(data)[0]
    else:
        return "Grupo no encontrado", 404


 
    lineas_data = {
        "procedure": "select_json_entity",
        "parameters": {
            "table_name": "inv_linea_grupo",
            "where_condition": f"id_grupo={id}",
            "order_by": "nombre_linea",
            "limit_clause": "",
            "json_data": {},
            "select_columns": "id_linea_grupo, nombre_linea, descripcion, estado"
        }
    }
    response = requests.post(API_URL, json=lineas_data)
    lineas = json.loads(response.json()['result'][0]['result']) if response.status_code == 200 and response.json()['result'][0]['result'] else []

    # Obtener proyectos de investigación
    proyectos_data = {
        "procedure": "select_json_entity",
        "parameters": {
            "table_name": "inv_proyectos p INNER JOIN inv_grupos g ON p.id_grupo = g.id_grupo",
            "where_condition": f"g.id_grupo={id}",
            "order_by": "p.nombre_proy_form",
            "limit_clause": "",
            "json_data": {},
            "select_columns": "p.id_proyecto, p.nombre_proy_form, p.codigo, p.fecha_inicio, p.fecha_fin, p.convocatoria"
        }
    }
    response = requests.post(API_URL, json=proyectos_data)
    proyectos = json.loads(response.json()['result'][0]['result']) if response.status_code == 200 and response.json()['result'][0]['result'] else []

    # Obtener investigadores
    investigadores_data = {
        "procedure": "select_json_entity",
        "parameters": {
            "table_name": "inv_investigadores i INNER JOIN inv_linea_grupo l ON i.id_linea_grupo = l.id_linea_grupo",
            "where_condition": f"l.id_grupo={id}",
            "order_by": "i.nombre_investigador",
            "limit_clause": "",
            "json_data": {},
            "select_columns": "i.id_investigador, i.nombre_investigador, l.nombre_linea, i.estado"
        }
    }
    response = requests.post(API_URL, json=investigadores_data)
    investigadores = json.loads(response.json()['result'][0]['result']) if response.status_code == 200 and response.json()['result'][0]['result'] else []

    # Obtener semilleros
    semilleros_data = {
        "procedure": "select_json_entity",
        "parameters": {
            "table_name": "inv_semilleros s INNER JOIN inv_linea_grupo l ON s.id_linea_grupo = l.id_linea_grupo LEFT JOIN inv_investigadores i ON s.id_lider = i.id_investigador",
            "where_condition": f"l.id_grupo={id}",
            "order_by": "s.nombre_semillero",
            "limit_clause": "",
            "json_data": {},
            "select_columns": "s.id_semillero, s.nombre_semillero, s.fecha_inicio, s.fecha_final, i.nombre_investigador as lider_semillero"
        }
    }
    response = requests.post(API_URL, json=semilleros_data)
    semilleros = json.loads(response.json()['result'][0]['result']) if response.status_code == 200 and response.json()['result'][0]['result'] else []

  # Obtener líneas de investigación
    lineas_data = {
        "procedure": "select_json_entity",
        "parameters": {
            "table_name": "inv_linea_grupo",
            "where_condition": f"id_grupo={id}",
            "order_by": "nombre_linea",
            "limit_clause": "",
            "json_data": {},
            "select_columns": "id_linea_grupo, nombre_linea, descripcion, estado"
        }
    }
    response = requests.post(API_URL, json=lineas_data)
    if response.status_code == 200 and response.json()['result'][0]['result']:
        lineas = json.loads(response.json()['result'][0]['result'])
        
        # Eliminar duplicados
        seen = set()
        unique_lineas = []
        for linea in lineas:
            if linea['nombre_linea'] not in seen:
                seen.add(linea['nombre_linea'])
                unique_lineas.append(linea)
        lineas = unique_lineas
    else:
        lineas = []

    investigadores_data = {
        "procedure": "select_json_entity",
        "parameters": {
            "table_name": "inv_investigadores i INNER JOIN inv_linea_grupo l ON i.id_linea_grupo = l.id_linea_grupo",
            "where_condition": f"l.id_grupo={id}",
            "order_by": "i.nombre_investigador",
            "limit_clause": "",
            "json_data": {},
            "select_columns": "i.id_investigador, i.nombre_investigador, l.nombre_linea, i.estado"
        }
    }
    response = requests.post(API_URL, json=investigadores_data)
    investigadores = json.loads(response.json()['result'][0]['result']) if response.status_code == 200 and response.json()['result'][0]['result'] else []
    
    return render_template('grupos/detalle.html', 
                           grupo=grupo,
                           lineas=lineas,  # Asegúrate de que esto se pase a la plantilla
                           proyectos=proyectos,
                           investigadores=investigadores,
                           semilleros=semilleros)

@vistaGruposInvestigacion.route('/crear', methods=['GET', 'POST'])
def crear():
    if request.method == 'GET':
       

        return render_template('grupos/crear.html', facultad = facultad(), investigadores= investigadores())

    elif request.method == 'POST':
        nuevo_grupo = {
            "nombre_grupo": request.form.get('nombre_grupo'),
            "codigo_grup_lac": request.form.get('codigo_grup_lac'),
            "categoria_colciencias": request.form.get('categoria_colciencias'),
            "area_conocimiento": request.form.get('area_conocimiento'),
            "id_facultad": request.form.get('id_facultad'),
            "id_lider": request.form.get('id_lider'),
            "fecha_creacion": request.form.get('fecha_creacion'),
            "fecha_finalizacion": request.form.get('fecha_finalizacion'),
            "plan_estrategico": request.form.get('plan_estrategico'),
            "categoria_meta": request.form.get('categoria_meta'),
            "estrategia_meta": request.form.get('estrategia_meta'),
            "vision": request.form.get('vision'),
            "objetivos": request.form.get('objetivos')
        }

        insert_data = {
            "procedure": "insert_json_entity",
            "parameters": {
                "table_name": "inv_grupos",
                "json_data": nuevo_grupo
            }
        }
        response = requests.post(API_URL, json=insert_data)
        if response.status_code == 200:
            flash("El grupo de investigación se creó correctamente", 'success')
        else:
            error_message = response.json().get("message", "Error desconocido al guardar los datos")
            flash(f"Error al crear el grupo: {error_message}", "danger")
        return redirect(url_for('idVistaGruposInvestigacion.listar'))

@vistaGruposInvestigacion.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    if request.method == 'GET':
        # Obtener detalles del grupo
        select_data = {
            "procedure": "select_json_entity",
            "parameters": {
                "table_name": "inv_grupos",
                "where_condition": f"id_grupo={id}",
                "order_by": "",
                "limit_clause": "",
                "json_data": {},
                "select_columns": "*"
            }
        }
        response = requests.post(API_URL, json=select_data)
        if response.status_code != 200:
            return f"Error al consultar la API: {response.status_code}"

        data_grupo = response.json()
        if 'result' in data_grupo and data_grupo['result']:
            grupo = json.loads(data_grupo['result'][0]['result'])[0]
        else:
            return "Grupo no encontrado", 404

    
        
        return render_template('grupos/editar.html', grupos=grupos(), facultad=facultad(), investigadores=investigadores())

    elif request.method == 'POST':
        # Procesar el formulario de edición
        grupo_actualizado = {
            "nombre_grupo": request.form.get('nombre_grupo'),
            "codigo_grup_lac": request.form.get('codigo_grup_lac'),
            "categoria_colciencias": request.form.get('categoria_colciencias'),
            "area_conocimiento": request.form.get('area_conocimiento'),
            "id_facultad": request.form.get('id_facultad'),
            "id_lider": request.form.get('id_lider'),
            "fecha_creacion": request.form.get('fecha_creacion'),
            "fecha_finalizacion": request.form.get('fecha_finalizacion'),
            "plan_estrategico": request.form.get('plan_estrategico'),
            "categoria_meta": request.form.get('categoria_meta'),
            "estrategia_meta": request.form.get('estrategia_meta'),
            "vision": request.form.get('vision'),
            "objetivos": request.form.get('objetivos')
        }
        update_data = {
            "procedure": "update_json_entity",
            "parameters": {
                "table_name": "inv_grupos",
                "where_condition": f"id_grupo={id}",
                "json_data": grupo_actualizado
            }
        }
        response = requests.post(API_URL, json=update_data)
        if response.status_code == 200:
            flash('Grupo actualizado exitosamente', 'success')
        else:
            flash('Error al actualizar el grupo', 'danger')
        return redirect(url_for('idVistaGruposInvestigacion.detalle', id=id))

@vistaGruposInvestigacion.route('/eliminar/<int:id>', methods=['POST'])
def eliminar(id):
    delete_data = {
        "procedure": "delete_json_entity",
        "parameters": {
            "table_name": "inv_grupos",
            "where_condition": f"id_grupo={id}"
        }
    }

    response = requests.post(API_URL, json=delete_data)

    if response.status_code == 200:
        result = response.json()
        if 'result' in result and result['result']:
            flash('Grupo de investigación eliminado exitosamente', 'success')
        else:
            flash('Error al eliminar el grupo de investigación', 'error')
    else:
        flash(f'Error en la solicitud: {response.status_code}', 'error')

    return redirect(url_for('idVistaGruposInvestigacion.listar'))