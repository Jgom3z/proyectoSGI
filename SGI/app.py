from flask import Flask, render_template, request, jsonify
import requests
import json

app = Flask(__name__)

# Configuración de la URL de la API
projectName = 'SGI'
API_URL = "http://190.217.58.246:5185/api/{projectName}/procedures/execute"

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
    print(grupos)
    # Pasar los datos a la plantilla
    ths = ['grupos de investigacion', 'codigo gruplac', 'categoria colciencias', 'facultad', 'lider de grupo']
    
    return render_template('vistaGruposInvestigacion.html', tds=grupos, ths= ths)

@app.route("/creategrupo", methods = ['POST'])
def create_grupo():
    # Captura los datos del formulario enviado
    print(request)
    form_data = {
        "nombre_grupo": request.form.get('nombre_grupo'),
        "codigo_grup_lac": request.form.get('codigo_grup_lac'),
        "categoria_colciencias": request.form.get('categoria_colciencias'),
        "area_conocimiento": request.form.get('area_conocimiento'),
        "id_facultad": request.form.get('id_facultad'),
        "fecha_creacion": request.form.get('fecha_creacion'),
        "fecha_finalizacion": request.form.get('fecha_finalizacion'),
        "id_lider": request.form.get('id_lider'),
        "plan_estrategico": request.form.get('plan_estrategico'),
        "categoria_meta": request.form.get('categoria_meta'),
        "estrategia_meta": request.form.get('estrategia_meta'),
        "vision": request.form.get('vision'),
        "objetivos": request.form.get('objetivos')
    }

    # Enviar los datos a la API
    response = requests.post(API_URL.format(projectName=projectName), json={
        "procedure": "insert_inv_grupos",  # Supongamos que tienes un procedimiento almacenado para insertar
        "parameters": [form_data]
    })

    # Verificar la respuesta de la API
    if response.status_code == 200:
        return jsonify({"message": "Datos guardados exitosamente"}), 200
    else:
        return jsonify({"message": "Error al guardar los datos"}), 500

if __name__ == '__main__':
    app.run(debug=True)
