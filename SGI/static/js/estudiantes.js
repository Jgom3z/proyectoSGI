//PARA ESTUDIANTES
  document.addEventListener('DOMContentLoaded', function() {
    // Agrega un evento click a todos los enlaces con la clase 'a-td'
    document.querySelectorAll('.a-td').forEach(function(link) {
      link.addEventListener('click', function(event) {
        event.preventDefault(); // Evita el comportamiento por defecto del enlace

        // Obtén la información del estudiante desde los atributos de datos del enlace
        var idEstudiante = this.getAttribute('data-id-estudiante'); // Obtén el ID del grupo
        var codigo = this.getAttribute('data-codigo');
        var idFacultad = this.getAttribute('data-id-facultad');
        var correo = this.getAttribute('data-correo');
        var identificacion = this.getAttribute('data-identificacion');
        var nombreEstudiante = this.getAttribute('data-nombre-estudiante');


        // Actualiza el contenido del modal de detalles
        document.getElementById('modalNombreEstudiante').textContent = nombreEstudiante;
        var tableContent = `
         <table>
          <tr>
            <th>ID Grupo</th>
            <td>${idEstudiante}</td>
          </tr>
          <tr>
              <th>Código</th>
              <td>${codigo}</td>
          </tr>
          <tr>
              <th>ID Facultad</th>
              <td>${idFacultad}</td>
          </tr>
          <tr>
              <th>Correo</th>
              <td>${correo}</td>
          </tr>
          <tr>
              <th>Identificación</th>
              <td>${identificacion}</td>
          </tr>
          <tr>
              <th>Nombre del Estudiante</th>
              <td>${nombreEstudiante}</td>
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
        document.querySelector('#modalEditInvestiButton').addEventListener('click', function() {
          // Pasa la información al modal de edición
          document.getElementById('id_estudiante_edit').value = idEstudiante;  // Asigna el ID del grupo
          document.getElementById('codigo_edit').value = codigo;
          document.getElementById('id_facultad_edit').value = idFacultad;  // Asegúrate de que el valor coincida con la ID de la facultad
          document.getElementById('correo_edit').value = correo;
          document.getElementById('identificacion_edit').value = identificacion;
          document.getElementById('nombre_estudiante_edit').value = nombreEstudiante;

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
  
