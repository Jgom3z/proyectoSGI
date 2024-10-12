import requests
from flask import Blueprint, redirect, url_for, request, flash, render_template, jsonify, current_app,send_from_directory,send_file, abort
import os
import json
import io
from docx import Document
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from vista.vistaProyectosInvestigacion import obtener_proyecto_por_id
import asyncio
# Configurar la URL de la API backend
projectName = os.getenv('PROJECT_NAME')
API_URL = os.getenv('API_URL')

files_bp = Blueprint('files', __name__)

from werkzeug.utils import secure_filename

# Extensiones permitidas
ALLOWED_EXTENSIONS = {'pdf', 'docx'}
def allowed_file(filename):
    """
    Verifica si la extensión del archivo es válida.
    
    :param filename: El nombre del archivo.
    :return: True si la extensión es válida, False en caso contrario.
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def handle_file_upload(file, proyecto_id, field_name, base_upload_folder='uploads'):
    if not file:
        flash('No se seleccionó ningún archivo', 'danger')
        return None

    # Obtener la extensión del archivo original (mantener la extensión del archivo subido)
    _, file_extension = os.path.splitext(file.filename)

    # Usar el nombre del campo del formulario para el nombre del archivo
    filename = secure_filename(f"{field_name}{file_extension}")

    if filename == '':
        return None

    if not allowed_file(filename):
        flash('Extensión de archivo no permitida', 'danger')
        return None

    # Crear la carpeta específica para el proyecto
    proyecto_folder = os.path.join(base_upload_folder, str(proyecto_id))

    # Asegurarse de que la carpeta del proyecto exista
    if not os.path.exists(proyecto_folder):
        try:
            os.makedirs(proyecto_folder)
        except Exception as e:
            flash(f'Error al crear la carpeta del proyecto: {e}', 'danger')
            return None

    # Eliminar archivos con el mismo nombre base (sin importar la extensión)
    eliminar_archivos_existentes(proyecto_folder, field_name)

    try:
        # Ruta absoluta completa
        file_path = os.path.join(proyecto_folder, filename)
        
        # Guardar el archivo
        file.save(file_path)

        # Ruta relativa que deseas guardar en la base de datos
        relative_file_path = os.path.join(base_upload_folder, str(proyecto_id), filename)

        return filename  

    except Exception as e:
        current_app.logger.error(f'Error al guardar el archivo: {e}')
        flash(f'Error al guardar el archivo: {e}', 'danger')
        return None

def eliminar_archivos_existentes(proyecto_folder, field_name):
    # Buscar archivos con el mismo nombre base en la carpeta
    for file in os.listdir(proyecto_folder):
        if file.startswith(field_name):
            file_path = os.path.join(proyecto_folder, file)
            try:
                os.remove(file_path)
                current_app.logger.info(f'Archivo eliminado: {file_path}')
            except Exception as e:
                current_app.logger.error(f'Error al eliminar el archivo: {e}')
                
@files_bp.route('/cargarDocumentos', methods=['POST'])
def cargarDocumentos():
    id_proyecto = request.form.get('id_proyecto')
    
    # Diccionario de los archivos posibles a recibir y sus campos en la base de datos
    file_fields = {
        "acta_inicio": "acta_inicio",
        "acta_finalizacion": "acta_finalizacion",
        "presupuesto": "presupuesto",
        "propuesta": "propuesta",
        "acta_comite": "acta_comite",
        "convenio_marco": "convenio_marco",
        "convenio_especifico": "convenio_especifico",
        "carta_de_intencion": "carta_intencion"
    }

    updates = {}  # Diccionario para almacenar las actualizaciones en la base de datos

    # Iterar sobre los campos de archivo
    for field_name, db_column_name in file_fields.items():
        file = request.files.get(field_name)
        
        if file:
            # Guardar el archivo con el nombre del campo del input
            field_name_path = handle_file_upload(file, id_proyecto, field_name)
            
            if field_name_path:
                # Añadir el campo que será actualizado en la base de datos
                updates['nombre_' + db_column_name] = field_name_path

    # Si hay archivos que actualizar en la base de datos
    if updates:
        update_data = {
            "procedure": "update_json_entity",
            "parameters": {
                "table_name": "inv_proyecto",
                "json_data": updates,  # Los campos que serán actualizados
                "where_condition": f"id_proyecto = {id_proyecto}"
            }
        }
        #print(update_data)
        response = requests.post(API_URL, json=update_data)
        if response.status_code == 200:
            flash("El registro se actualizó correctamente", 'success')
        else:            
            error_message = response.json().get("message", "Error desconocido al guardar los datos")
            return jsonify({"message": f"Error al guardar los datos: {error_message}"}), 500
    else:
        flash('No se seleccionaron archivos para cargar.', 'warning')

    return redirect(url_for('idVistaProyectosInvestigacion.detalle', id=id_proyecto))

@files_bp.route('/eliminar-file', methods=['POST'])
def eliminar_file():
    id_proyecto = request.form.get('id_proyecto')
    file_name = request.form.get('filename')
    column_name = request.form.get('columnname')
    
    update_data = {
      "procedure": "update_json_entity",
              "parameters": {
                "table_name": "inv_proyecto",
                "json_data":  {
                    column_name: None,
                },
                "where_condition": f"id_proyecto = {id_proyecto}"
        }
     }
    
    response = requests.post(API_URL, json=update_data)
    if response.status_code ==200:
        file_path = 'uploads/' + id_proyecto + '/'+file_name
        if file_path and os.path.exists(file_path):
            try:
                os.remove(file_path)
                flash(f"El archivo {os.path.basename(file_path)} se eliminó del sistema de archivos.", 'success')
            except Exception as e:
                flash(f"No se pudo eliminar el archivo: {e}", 'danger')
        else:
            flash(f"El archivo no existe en la ruta: {file_path}", 'warning')
    else:
        error_message = response.json().get("message", "Error desconocido al guardar los datos")
        return jsonify({"message": f"Error al guardar los datos: {error_message}"}), 500

    return redirect(url_for('idVistaProyectosInvestigacion.detalle', id=id_proyecto))



@files_bp.route('/download/<int:id_proyecto>/<filename>', methods=['GET'])
def descargar(id_proyecto, filename):
    # Definir el directorio donde se almacenan los archivos del paciente
    upload_folder = os.path.join(os.getcwd(), 'uploads', str(id_proyecto))
    
    # Verificar si el archivo existe en el directorio
    if not os.path.isfile(os.path.join(upload_folder, filename)):
        print(f"Archivo no encontrado: {os.path.join(upload_folder, filename)}")
        abort(404)  # Si no se encuentra el archivo, devolver un error 404

    try:
        # Descargar el archivo desde el directorio
        return send_from_directory(upload_folder, filename, as_attachment=True)
    except Exception as e:
        print(f"Error al descargar el archivo: {e}")
        abort(500)  # Si hay algún error en el proceso, devolver un error 500


@files_bp.route('/view/<int:id_proyecto>/<filename>', methods=['GET'])
def ver_archivo(id_proyecto, filename):
    # Definir la carpeta de subida del proyecto
    upload_folder = os.path.join(os.getcwd(), 'uploads', str(id_proyecto))
    
    # Asegurar que el nombre del archivo es seguro
    filename = secure_filename(filename)
    file_path = os.path.join(upload_folder, filename)

    # Verificar si el archivo existe
    if not os.path.isfile(file_path):
        print(f"Archivo no encontrado: {file_path}")
        abort(404)

    # Validar si el archivo es un .docx
    if filename.lower().endswith('.docx'):
        # Generar el PDF temporalmente en memoria
        pdf_file = convert_docx_to_pdf_in_memory(file_path)

        # Enviar el archivo PDF generado directamente desde memoria
        return send_file(pdf_file, download_name=filename.replace('.docx', '.pdf'), mimetype='application/pdf')

    # Si no es un archivo .docx, se envía el archivo original para ser visualizado
    return send_from_directory(upload_folder, filename)


def convert_docx_to_pdf_in_memory(docx_path):
    # Crear un buffer en memoria
    pdf_buffer = io.BytesIO()

    # Crear el documento PDF en memoria
    c = canvas.Canvas(pdf_buffer, pagesize=letter)
    width, height = letter

    # Leer el archivo .docx
    doc = Document(docx_path)

    y = height - 40  # Margen superior
    
    # Iterar sobre los párrafos del .docx
    for para in doc.paragraphs:
        text = para.text
        if y < 40:  # Si la página está llena, crear una nueva página
            c.showPage()
            y = height - 40
        c.drawString(40, y, text)
        y -= 15  # Ajuste vertical entre líneas

    # Guardar el PDF en el buffer
    c.save()

    # Posicionar el cursor del buffer al inicio
    pdf_buffer.seek(0)

    return pdf_buffer


