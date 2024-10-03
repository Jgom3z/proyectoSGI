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
            "select_columns": "pf.nombre_proy_form, i.nombre_investigador, pry.nombre_proyecto, pf.nivel, pf.modalidad, pf.cod_proy_form",
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
            "table_name": "inv_proyecto_formacion pf INNER JOIN inv_linea_grupo lg ON pf.id_linea = lg.id_linea_grupo INNER JOIN inv_investigadores i ON pf.id_investigador = i.id_investigador INNER JOIN inv_proyecto pry ON pf.id_proyecto = pry.id_proyecto INNER JOIN inv_semilleros s ON pf.id_semillero = s.id_semillero",
            "json_data": {
                "estado": "En Progreso"  
            },
            "where_condition": "",
            "select_columns": "pf.nombre_proy_form, i.nombre_investigador, pry.nombre_proyecto, pf.nivel, pf.modalidad, pf.cod_proy_form",
            "order_by": "pf.id_proyecto_formacion", 
            "limit_clause": ""
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
                           estudiantesNotInSemillero=estudiantes(),#estudiantesNotExistsSimellero(id),
                           integrantes=estudiantesIntegrantesSemilleros(id), planes=planesSemilleroById(id), proyectos=proyectosFormacionSemillero(id))

