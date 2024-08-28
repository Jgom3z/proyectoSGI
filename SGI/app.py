from flask import Flask, render_template, request, jsonify
import requests
import json

app = Flask(__name__)

# Configuración de la URL de la API
API_URL = "http://190.217.58.246:5185/api/SGI/procedures/"

@app.route('/vistaGruposInvestigacion', methods=['GET'])
def vista_grupos_investigacion():
    select_data = {
        "projectName": 'SGI',
        "procedure": "select_json_entity",
        "parameters": {
            "table_name": "inv_grupos g INNER JOIN inv_investigadores p ON p.id_investigador = g.id_lider INNER JOIN inv_facultad f ON f.id_facultad = g.id_facultad",
            "json_data": {
                "estado": "En Progreso"
            },
            "where_condition": "",
            "select_columns": "g.nombre_proyecto, g.codigo_grup_lac, g.categoria_colciencias, f.nombre_facultad, p.nombre_investigador, g.id_grupo",
            "order_by": "g.id_grupo",
            "limit_clause": ""
        }
    }

    response = requests.post(API_URL, json=select_data)

    # Manejo de errores en la respuesta
    if response.status_code != 200:
        return f"Error al consultar la API: {response.status_code}"

    # Parsear la respuesta a JSON
    data = response.json()
    
    # Verifica si 'result' existe y contiene datos
    if 'result' in data and data['result']:
        # Extraer el string JSON y cargarlo como objeto Python
        grupos_str = data['result'][0]['result']
        grupos = json.loads(grupos_str)
    else:
        grupos = []

    # Pasar los datos a la plantilla
    return render_template('vistaGruposInvestigacion.html', grupos=grupos)

if __name__ == '__main__':
    app.run(debug=True)
