# archivo: vistaEstudiante.py
from pprint import pprint
from flask import Blueprint, request, render_template, redirect, url_for
from controlador.ControlEntidad import ControlEntidad

# Crear un Blueprint
vistaEstudiante = Blueprint('idVistaEstudiante', __name__, template_folder='templates')

@vistaEstudiante.route('/vistaEstudiante', methods=['GET', 'POST'])
def vista_Estudiante():
    mensaje = ""
    objControlEntidad = ControlEntidad('estudiante')
    arregloEstudiantes = objControlEntidad.select_data() 

    boton = request.form.get('bt', '')
    id_estudiante = request.form.get('txtId', '')
    codigo = request.form.get('txtCodigo', '')
    id_facultad = request.form.get('txtFacultad', '')
    correo = request.form.get('txtCorreo', '')
    identificacion = request.form.get('txtIdentificacion', '')
    nombre_estudiante = request.form.get('txtNombre', '')

    datosEstudiante = {
        'id_estudiante': id_estudiante,
        'codigo': codigo,
        'id_facultad': id_facultad,
        'correo': correo,
        'identificacion': identificacion,
        'nombre_estudiante': nombre_estudiante
    }

    if boton == 'Guardar':
        objEstudiante = Entidad(datosEstudiante)
        objControlEntidad.insert_data(objEstudiante)
        return redirect(url_for('idVistaEstudiante.vista_Estudiante'))
    elif boton == 'Consultar':
        objEstudiante = objControlEntidad.buscarPorId('id_estudiante', id_estudiante)
        if objEstudiante:
            datosEstudiante = {
                'id_estudiante': objEstudiante.id_estudiante,
                'codigo': objEstudiante.codigo,
                'id_facultad': objEstudiante.id_facultad,
                'correo': objEstudiante.correo,
                'identificacion': objEstudiante.identificacion,
                'nombre_estudiante': objEstudiante.nombre_estudiante
            }
        else:
            mensaje = "El estudiante no se encontró."
    elif boton == 'Modificar':
        objEstudiante = Entidad(datosEstudiante)
        objControlEntidad.update_data('id_estudiante', id_estudiante, objEstudiante)
        return redirect(url_for('idVistaEstudiante.vista_Estudiante'))
    elif boton == 'Borrar':
        objControlEntidad.delete_data('id_estudiante', id_estudiante)
        return redirect(url_for('idVistaEstudiante.vista_Estudiante'))

    # Renderizar la plantilla al final, pasando las variables necesarias
    return render_template('vistaEstudiante.html', arregloEstudiantes=arregloEstudiantes, mensaje=mensaje, estudiante=datosEstudiante)
