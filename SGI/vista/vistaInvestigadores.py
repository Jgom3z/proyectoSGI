from pprint import pprint
from flask import Blueprint, request, render_template, redirect, url_for
from controlador.ControlEntidad import ControlEntidad

# Crear un Blueprint
vistaInvestigadores = Blueprint('idVistaInvestigadores', __name__, template_folder='templates')

@vistaInvestigadores.route('/vistaInvestigadores', methods=['GET', 'POST'])
def vista_Investigadores():
    mensaje = ""
    objControlEntidad = ControlEntidad('investigador')
    arregloInvestigadores = objControlEntidad.select_data()
    
    boton = request.form.get('bt', '')
    id_investigador = request.form.get('txtIdInvestigador', '')
    cedula = request.form.get('txtCedula', '')
    nombre_investigador = request.form.get('txtNombreInvestigador', '')
    categoria_institucion = request.form.get('txtCategoriaInstitucion', '')
    id_facultad = request.form.get('txtIdFacultad', '')
    categoria_colciencias = request.form.get('txtCategoriaColciencias', '')
    orcid = request.form.get('txtOrcid', '')
    tipo_contrato = request.form.get('txtTipoContrato', '')
    nivel_de_formacion = request.form.get('txtNivelDeFormacion', '')
    correo = request.form.get('txtCorreo', '')
    telefono = request.form.get('txtTelefono', '')
    fecha_inicio = request.form.get('txtFechaInicio', '')
    fecha_final = request.form.get('txtFechaFinal', '')
    cvlac = request.form.get('txtCvlac', '')
    categoria_colciencias_esperada = request.form.get('txtCategoriaColcienciasEsperada', '')

    datosInvestigador = {
        'id_investigador': id_investigador,
        'cedula': cedula,
        'nombre_investigador': nombre_investigador,
        'categoria_institucion': categoria_institucion,
        'id_facultad': id_facultad,
        'categoria_colciencias': categoria_colciencias,
        'orcid': orcid,
        'tipo_contrato': tipo_contrato,
        'nivel_de_formacion': nivel_de_formacion,
        'correo': correo,
        'telefono': telefono,
        'fecha_inicio': fecha_inicio,
        'fecha_final': fecha_final,
        'cvlac': cvlac,
        'categoria_colciencias_esperada': categoria_colciencias_esperada
    }

    if boton == 'Guardar':
        objInvestigador = Entidad(datosInvestigador)
        objControlEntidad.insert_data(objInvestigador)
        return redirect(url_for('idVistaInvestigadores.vista_Investigadores'))
    
    elif boton == 'Consultar':
        objInvestigador = objControlEntidad.buscarPorId('id_investigador', id_investigador)
        if objInvestigador:
            datosInvestigador = objInvestigador.__dict__
        else:
            mensaje = "El Investigador no se encontró."
    
    elif boton == 'Modificar':
        objInvestigador = Entidad(datosInvestigador)
        objControlEntidad.update_data('id_investigador', id_investigador, objInvestigador)
        return redirect(url_for('idVistaInvestigadores.vista_Investigadores'))
    
    elif boton == 'Borrar':
        objControlEntidad.delete_data('id_investigador', id_investigador)
        return redirect(url_for('idVistaInvestigadores.vista_Investigadores'))

    # Renderizar la plantilla al final, pasando las variables necesarias
    return render_template('vistaInvestigadores.html', arregloInvestigadores=arregloInvestigadores, mensaje=mensaje, investigador=datosInvestigador)
