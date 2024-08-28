from flask import Blueprint, render_template, request, redirect, url_for
from controlador.ControlEntidad import ControlEntidad
def create_blueprint_entidad(tipo_entidad):
    vistaEntidad = Blueprint(f"vista_{tipo_entidad}", __name__, static_folder="static", template_folder="templates")

    @vistaEntidad.route(f"/vista_{tipo_entidad}", methods=['GET', 'POST'])
    @vistaEntidad.route("/")
    def vista():
        mensaje = ""
        objControlEntidad = ControlEntidad(tipo_entidad)
        arregloEntidades = objControlEntidad.listar()

        # Tendrías que adaptar esta parte para trabajar de forma genérica con los datos de las entidades
        datosEntidad = {key: request.form.get(f'txt{key.capitalize()}', '') for key in objControlEntidad.camposRequeridos()}

        boton = request.form.get('bt', '')

        # Aquí iría la lógica para manejar las acciones del formulario, similar a como lo tienes arriba.
        # ...

        return render_template(f'vista_{tipo_entidad}.html', arregloEntidades=arregloEntidades, mensaje=mensaje, entidad=datosEntidad)

    return vistaEntidad

