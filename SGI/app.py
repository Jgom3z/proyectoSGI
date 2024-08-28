from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# Configuración de la URL de la API
API_URL = "http://190.217.58.246:5185/api/SGI/procedures/execute"

@app.route('/vistaGruposInvestigacion', methods=['GET', 'POST'])
def vista_grupos_investigacion():
    if request.method == 'POST':
        # Captura los datos del formulario enviado
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

    # Si es un GET, simplemente renderiza la página del formulario
    response = requests.post(API_URL.format(projectName=projectName), json={
        "procedure": "inv_grupos",  # Suponiendo que hay un procedimiento almacenado para listar
        "parameters": []
    })

    data = response.json()

    return render_template('vistaGruposInvestigacion.html', grupos=data)


if __name__ == '__main__':
    app.run(debug=True)

