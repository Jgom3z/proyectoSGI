//PARA PROYECTOS DE FORMACIÓN
document.addEventListener('DOMContentLoaded', function() {
    // Agrega un evento click a todos los enlaces con la clase 'a-td'
    document.querySelectorAll('.a-td').forEach(function(link) {
      link.addEventListener('click', function(event) {
        event.preventDefault(); // Evita el comportamiento por defecto del enlace

        // Obtén la información del estudiante desde los atributos de datos del enlace
        var idProyectoFormacion = this.getAttribute('data-id');
        var nombreProyectoFormacion = this.getAttribute('data-nombre');
        var fechaInicio = this.getAttribute('data-fecha-inicio');
        var fechaTerminacion = this.getAttribute('data-fecha-terminacion');
        var lineaInvestigacion = this.getAttribute('data-linea-investigacion');
        var idInvestigador = this.getAttribute('data-id-investigador');
        var idProyecto = this.getAttribute('data-id-proyecto');
        var idSemillero = this.getAttribute('data-id-semillero');
        var objetivos = this.getAttribute('data-objetivos');
        var nivel = this.getAttribute('data-nivel');
        var modalidad = this.getAttribute('data-modalidad');
        var codigo = this.getAttribute('data-codigo');
        var idCodirector = this.getAttribute('data-id-codirector');
        var idLinea = this.getAttribute('data-id-linea');



        // Actualiza el contenido del modal de detalles
        document.getElementById('modalNombreEstudiante').textContent = nombreEstudiante;
        var tableContent = `
            <table>
        <tr>
            <th>ID Proyecto Formación</th>
            <td>${idProyectoFormacion}</td>
        </tr>
        <tr>
            <th>Nombre del Proyecto</th>
            <td>${nombreProyectoFormacion}</td>
        </tr>
        <tr>
            <th>Fecha de Inicio</th>
            <td>${fechaInicio}</td>
        </tr>
        <tr>
            <th>Fecha de Terminación</th>
            <td>${fechaTerminacion}</td>
        </tr>
        <tr>
            <th>Línea de Investigación</th>
            <td>${lineaInvestigacion}</td>
        </tr>
        <tr>
            <th>ID Investigador</th>
            <td>${idInvestigador}</td>
        </tr>
        <tr>
            <th>ID Proyecto</th>
            <td>${idProyecto}</td>
        </tr>
        <tr>
            <th>ID Semillero</th>
            <td>${idSemillero}</td>
        </tr>
        <tr>
            <th>Objetivos</th>
            <td>${objetivos}</td>
        </tr>
        <tr>
            <th>Nivel</th>
            <td>${nivel}</td>
        </tr>
        <tr>
            <th>Modalidad</th>
            <td>${modalidad}</td>
        </tr>
        <tr>
            <th>Código del Proyecto</th>
            <td>${codigo}</td>
        </tr>
        <tr>
            <th>ID Codirector</th>
            <td>${idCodirector}</td>
        </tr>
        <tr>
            <th>ID Línea de Investigación</th>
            <td>${idLinea}</td>
        </tr>
    </table>


          <br>
          <button type="submit" class="btn btn-danger" id="deleteButton">Eliminar</button>
          <br>
        `;
        document.getElementById('modalTableBody').innerHTML = tableContent;

        // Agrega el evento click al botón de eliminar
        document.getElementById('deleteButton').addEventListener('click', function() {
          if (confirm('¿Estás seguro de que deseas eliminar este estudiante?')) {
            // Aquí debes hacer la llamada a la API para eliminar el estudiante utilizando el idestudiante
            fetch('/deleteestudiante', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json'
              },
              body: JSON.stringify({ id_estudiante: idEstudiante })
            })
            .then(response => response.json().then(data => ({ status: response.status, body: data})))
            .then(data => {
              if (data.status === 200 && data.body.message.includes("correctamente")) {
                alert(data.body.message);

                // Cerrar el modal utilizando JavaScript puro
                let modal = document.getElementById('estudianteModal');
                let backdrop = document.querySelector('.modal-backdrop');
                modal.classList.remove('show');
                modal.setAttribute('aria-hidden', 'true');
                modal.style.display = 'none';
                if (backdrop) {
                    backdrop.remove();
                }
                document.body.classList.remove('modal-open');
                document.body.style.removeProperty('padding-right');
                
                // Recargar la página después de cerrar el modal
                setTimeout(() => location.reload(), 500); 
              } else {
                alert('Error al eliminar el estudiante: ' + data.body.message);
              }
            })
            .catch(error => {
              console.error('Error:', error);
              alert('Error al eliminar el estudiante: ' + error.message);
            });
          }
        });

        // Agrega el evento click al botón de Modificar
        document.querySelector('#modalEditproyectoftiButton').addEventListener('click', function() {
          // Pasa la información al modal de edición
        document.getElementById('id_proyecto_formacion_edit').value = idProyectoFormacion;  // Asigna el ID del proyecto de formación
        document.getElementById('nombre_proy_form_edit').value = nombreProyectoFormacion;  // Asigna el nombre del proyecto
        document.getElementById('fecha_inicio_edit').value = fechaInicio;  // Asigna la fecha de inicio
        document.getElementById('fecha_terminacion_edit').value = fechaTerminacion;  // Asigna la fecha de terminación
        document.getElementById('linea_investigacion_edit').value = lineaInvestigacion;  // Asigna la línea de investigación
        document.getElementById('id_investigador_edit').value = idInvestigador;  // Asigna el ID del investigador
        document.getElementById('id_proyecto_edit').value = idProyecto;  // Asigna el ID del proyecto
        document.getElementById('id_semillero_edit').value = idSemillero;  // Asigna el ID del semillero
        document.getElementById('objetivos_edit').value = objetivos;  // Asigna los objetivos
        document.getElementById('nivel_edit').value = nivel;  // Asigna el nivel
        document.getElementById('modalidad_edit').value = modalidad;  // Asigna la modalidad
        document.getElementById('codigo_edit').value = codigo;  // Asigna el código del proyecto
        document.getElementById('id_codirector_edit').value = idCodirector;  // Asigna el ID del codirector
        document.getElementById('id_linea_edit').value = idLinea;  // Asigna el ID de la línea


          // Asigna otros campos adicionales
        });

         // Agrega el evento click al botón de finalizar modificacion
         document.getElementById('updateButton').addEventListener('click', function(event) {
            var form = document.getElementById('EditForm');
            var formData = new FormData(form);

            fetch('/updateestudiante', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.message) {
                    // Mostrar un mensaje de confirmación
                    alert(data.message);
                    // Recargar la página
                    window.location.reload();
                } else {
                    alert("Error al procesar la solicitud.");
                }
            })
            .catch((error) => {
                console.error('Error:', error);
                alert("Ocurrió un error al procesar la solicitud.");
            });
        });

        // Agrega el evento click al botón de finalizar cracion
        document.getElementById('createButton').addEventListener('click', function(event) {
        console.log('Botón clickeado'); // Verificar si el evento se está capturando
        var form = document.getElementById('createForm');
        var formData = new FormData(form);

        fetch('/createestudiante', {  // Nota: Verifica que la URL coincida con tu endpoint
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                // Mostrar un mensaje de confirmación
                alert(data.message);
                // Recargar la página
                window.location.reload();
            } else {
                alert("Error al procesar la solicitud.");
            }
        })
        .catch((error) => {
            console.error('Error:', error);
            alert("Ocurrió un error al procesar la solicitud.");
        });
    });
          

          
        });
      });
    });
  
