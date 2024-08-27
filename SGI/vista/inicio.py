
from pprint import pprint
from flask import Blueprint, request, render_template, redirect, url_for
from controlador.ControlEntidad import ControlEntidad

# Crear un Blueprint
vistaInicio = Blueprint('idVistaInicio', __name__, template_folder='templates')

@vistaInicio.route('/vistaInicio', methods=['GET', 'POST'])
def vista_Inicio():
    
    mensaje = ""
    #objControlEntidad=ControlEntidad('rol')
    #arregloEntidades = objControlEntidad.listar() 
    #print("arregloEntidades")
    #pprint(arregloEntidades)
    boton = request.form.get('bt', '')
    id_rol = request.form.get('txtId', '')
    nombre_rol = request.form.get('txtNombre', '')
    listbox1 = request.form.getlist('listbox1') 
    datosEntidad = {'id': id_rol, 'nombre': nombre_rol}
    # Lógica del switch/case se maneja con if/elif en Python

    if boton == 'Guardar':
        datosEntidad = {'nombre': nombre_rol} #solo el nombre ya que la clave primaria es una secuencia
        objEntidad=Entidad(datosEntidad)
        """
        payload = {
            "procedure": "insert_json_entity",
            "parameters": {
                "table_name": "usuario",
                "select_columns": "email, contrasena",
                "where_condition": f"email = '{email}'"
            }
        }

        """


        #objControlEntidad.guardar(objEntidad)
        return redirect(url_for('idVistaInicio.vista_inicio'))
    











    elif boton == 'Consultar':
        #objControlEntidad = ControlEntidad('rol')         
        #objEntidad = objControlEntidad.buscarPorId('id',id_rol)
        if objEntidad:
            nombre_rol = objEntidad.nombre
            datosEntidad = {'id': id_rol, 'nombre': nombre_rol}
        else:
            mensaje = "La Entidad no se encontró."
    elif boton == 'Modificar':
        datosEntidad = {'id': id_rol, 'nombre': nombre_rol}
        objEntidad=Entidad(datosEntidad)
        #objControlEntidad = ControlEntidad('rol') 
        #objControlEntidad.modificar('id',id_rol, objEntidad)
        return redirect(url_for('idVistaRol.vista_Rol'))

    elif boton == 'Borrar':
        #objControlEntidad.borrar('id',id_rol)
        return redirect(url_for('idVistaRol.vista_Rol'))

    # Renderizar la plantilla al final, pasando las variables necesarias
    #return render_template('vistaInicio.html', arregloRoles=arregloEntidades, mensaje=mensaje,rol=datosEntidad)
    return render_template('inicio.html', mensaje=mensaje,rol=datosEntidad)

