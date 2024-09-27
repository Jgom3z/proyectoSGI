//LINEAS DE INVESTIGACIÓN 

  document.addEventListener('DOMContentLoaded', function() {
    // Agrega un evento click a todos los enlaces con la clase 'a-td'
    document.querySelectorAll('.a-td').forEach(function(link) {
      link.addEventListener('click', function(event) {
        event.preventDefault(); // Evita el comportamiento por defecto del enlace
        var idLinea = this.getAttribute('data-id_linea');
        var nombreLinea = this.getAttribute('data-nombre');
        var idGrupo = this.getAttribute('data-id_grupo');
        var descripcion = this.getAttribute('data-descripcion');
        var idLider = this.getAttribute('data-id_lider');
        var temasDeTrabajo = this.getAttribute('data-temas_de_trabajo');
        var objetivos = this.getAttribute('data-objetivos');
        var vision = this.getAttribute('data-vision');
        var estado = this.getAttribute('data-estado');
        var mision = this.getAttribute('data-mision');

        // Actualiza el contenido del modal de detalles
        document.getElementById('modalNombreLinea').textContent = nombreLinea;
        var tableContent = `
          <tr>
          <th>ID Línea</th>
          <td>${idLinea}</td>
      </tr>
      <tr>
          <th>Nombre Línea</th>
          <td>${nombreLinea}</td>
      </tr>
      <tr>
          <th>ID Grupo</th>
          <td>${idGrupo}</td>
      </tr>
      <tr>
          <th>Descripción</th>
          <td>${descripcion}</td>
      </tr>
      <tr>
          <th>ID Líder</th>
          <td>${idLider}</td>
      </tr>
      <tr>
          <th>Temas de Trabajo</th>
          <td>${temasDeTrabajo}</td>
      </tr>
      <tr>
          <th>Objetivos</th>
          <td>${objetivos}</td>
      </tr>
      <tr>
          <th>Visión</th>
          <td>${vision}</td>
      </tr>
      <tr>
          <th>Estado</th>
          <td>${estado}</td>
      </tr>
      <tr>
          <th>Misión</th>
          <td>${mision}</td>
      </tr>
      <br>

          <button type="submit" class="btn btn-danger" id="deleteButton">Eliminar</button>
          <br>
        `;
        document.getElementById('modalTableBody').innerHTML = tableContent;

        document.getElementById('deleteButton').addEventListener('click', function() {
          if (confirm('¿Estás seguro de que deseas eliminar esta linea?')) {
            fetch('/deletelinea', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json'
              },
              body: JSON.stringify({ id_linea_grupo: idLinea })
            })
            .then(response => response.json().then(data => ({ status: response.status, body: data})))
            .then(data => {
              if (data.status === 200 && data.body.message.includes("correctamente")) {
                alert(data.body.message);

                // Cerrar el modal utilizando JavaScript puro
                let modal = document.getElementById('lineaModal');
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
                alert('Error al eliminar la linea: ' + data.body.message);
              }
            })
            .catch(error => {
              console.error('Error:', error);
              alert('Error al eliminar la linea: ' + error.message);
            });
          }
        });

        // Agrega el evento click al botón de Modificar
          
      // function loadData(id) {
      //         // Llama al backend para obtener los datos de la cita usando el ID
      //         $.ajax({
      //           url: "/get_lineaGrupo",
      //           type: "POST",
      //           data: { id_linea_grupo: id },
      //           success: function (data) {
      //             // Asignar valores a los campos
      //             document.getElementById('id_linea_grupo_edit').value = data[0].id_linea_grupo;  // Asigna el ID del grupo
      //             document.getElementById('nombre_linea_edit').value = data[0].nombre_linea;
      //             document.getElementById('id_linea_grupo_edit').value = data[0].id_linea_grupo;
      //             document.getElementById('descripcion_edit').value = data[0].descripcion;
      //             document.getElementById('id_lider_edit').value = data[0].id_lider;
      //             document.getElementById('temas_de_trabajo_edit').value = data[0].temas_de_trabajo;
      //             document.getElementById('objetivos_edit').value = data[0].objetivos; 
      //             document.getElementById('vision_edit').value = data[0].vision; 
      //             document.getElementById('estado_edit').value = data[0].estado;
      //             document.getElementById('mision_edit').value = data[0].mision;
      //           },
      //           error: function () {
      //             alert("Error al cargar datos");
      //           },
      //         });
      //       }




            document.querySelector('#modalEditLineButton').addEventListener('click', function() {
              // Pasa la información al modal de edición
              document.getElementById('id_linea_grupo_edit').value = idLinea;  // Asigna el ID de la línea
              document.getElementById('nombre_linea_edit').value = nombreLinea;
              document.getElementById('id_grupo_edit').value = idGrupo;  // Asigna el ID del grupo
              document.getElementById('descripcion_edit').value = descripcion;
              document.getElementById('id_lider_edit').value = idLider;  // Asegúrate de que el valor coincida con la ID del líder
              document.getElementById('temas_de_trabajo_edit').value = temasDeTrabajo;
              document.getElementById('objetivos_edit').value = objetivos;
              document.getElementById('vision_edit').value = vision;
              document.getElementById('estado_edit').value = estado;
              document.getElementById('mision_edit').value = mision;

              // Asigna otros campos adicionales
             });

         // Agrega el evento click al botón de finalizar modificacion
         document.getElementById('updateButton').addEventListener('click', function(event) {
            var form = document.getElementById('EditForm');
            var formData = new FormData(form);

            fetch('/updatelinea', {
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

        fetch('/createlinea', {  // Nota: Verifica que la URL coincida con tu endpoint
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
  
