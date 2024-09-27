//INVESTIGADORES

  document.addEventListener('DOMContentLoaded', function() {
    // Agrega un evento click a todos los enlaces con la clase 'a-td'
    document.querySelectorAll('.a-td').forEach(function(link) {
      link.addEventListener('click', function(event) {
        event.preventDefault(); // Evita el comportamiento por defecto del enlace

        // Obtén la información del investigador desde los atributos de datos del enlace
        var idInvestigador = this.getAttribute('data-id-investigador');
        var categoriaColciencias = this.getAttribute('data-categoria-colciencias');
        var tipoContrato = this.getAttribute('data-tipo-contrato');
        var nivelFormacion = this.getAttribute('data-nivel-formacion');
        var orcid = this.getAttribute('data-orcid');
        var correo = this.getAttribute('data-correo');
        var telefono = this.getAttribute('data-telefono');
        var fechaInicio = this.getAttribute('data-fecha-inicio');
        var fechaFinal = this.getAttribute('data-fecha-final');
        var categoriaColcienciasEsperada = this.getAttribute('data-categoria-colciencias-esperada');
        var cvlac = this.getAttribute('data-cvlac');
        var cedula = this.getAttribute('data-cedula');
        var nombreInvestigador = this.getAttribute('data-nombre-investigador');
        var categoriaInstitucion = this.getAttribute('data-categoria-institucion');
        var idFacultad = this.getAttribute('data-id-facultad');


        // Actualiza el contenido del modal de detalles
        document.getElementById('modalNombreInvestigador').textContent = nombreInvestigador;
        var tableContent = `
         <tr>
            <th>ID Investigador</th>
            <td>${idInvestigador}</td>
        </tr>
        <tr>
            <th>Categoría Colciencias</th>
            <td>${categoriaColciencias}</td>
        </tr>
        <tr>
            <th>Tipo de Contrato</th>
            <td>${tipoContrato}</td>
        </tr>
        <tr>
            <th>Nivel de Formación</th>
            <td>${nivelFormacion}</td>
        </tr>
        <tr>
            <th>ORCID</th>
            <td>${orcid}</td>
        </tr>
        <tr>
            <th>Correo</th>
            <td>${correo}</td>
        </tr>
        <tr>
            <th>Teléfono</th>
            <td>${telefono}</td>
        </tr>
        <tr>
            <th>Fecha de Inicio</th>
            <td>${fechaInicio}</td>
        </tr>
        <tr>
            <th>Fecha Final</th>
            <td>${fechaFinal}</td>
        </tr>
        <tr>
            <th>Categoría Colciencias Esperada</th>
            <td>${categoriaColcienciasEsperada}</td>
        </tr>
        <tr>
            <th>CVLAC</th>
            <td>${cvlac}</td>
        </tr>
        <tr>
            <th>Cédula</th>
            <td>${cedula}</td>
        </tr>
        <tr>
            <th>Nombre Investigador</th>
            <td>${nombreInvestigador}</td>
        </tr>
        <tr>
            <th>Categoría Institución</th>
            <td>${categoriaInstitucion}</td>
        </tr>
        <tr>
            <th>ID Facultad</th>
            <td>${idFacultad}</td>
        </tr>

          <br>
          <button type="submit" class="btn btn-danger" id="deleteButton" style = "margin-left:10px;">Eliminar</button>
          <br>
        `;
        document.getElementById('modalTableBody').innerHTML = tableContent;

        // Agrega el evento click al botón de eliminar
        document.getElementById('deleteButton').addEventListener('click', function() {
          if (confirm('¿Estás seguro de que deseas eliminar este investigador?')) {
            // Aquí debes hacer la llamada a la API para eliminar el investigador utilizando el idinvestigador
            fetch('/deleteinvestigador', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json'
              },
              body: JSON.stringify({ id_investigador: idInvestigador })
            })
            .then(response => response.json().then(data => ({ status: response.status, body: data})))
            .then(data => {
              if (data.status === 200 && data.body.message.includes("correctamente")) {
                alert(data.body.message);

                // Cerrar el modal utilizando JavaScript puro
                let modal = document.getElementById('investigadorModal');
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
                alert('Error al eliminar el investigador: ' + data.body.message);
              }
            })
            .catch(error => {
              console.error('Error:', error);
              alert('Error al eliminar el investigador: ' + error.message);
            });
          }
        });

        // Agrega el evento click al botón de Modificar
        document.querySelector('#modalEditInvestiButton').addEventListener('click', function() {
          // Pasa la información al modal de edición
          document.getElementById('id_investigador_edit').value = idInvestigador;  // Asigna el ID del investigador
          document.getElementById('categoria_colciencias_edit').value = categoriaColciencias;
          document.getElementById('tipo_contrato_edit').value = tipoContrato;
          document.getElementById('nivel_formacion_edit').value = nivelFormacion;
          document.getElementById('orcid_edit').value = orcid;
          document.getElementById('correo_edit').value = correo;
          document.getElementById('telefono_edit').value = telefono;
          document.getElementById('fecha_inicio_edit').value = fechaInicio;
          document.getElementById('fecha_final_edit').value = fechaFinal;
          document.getElementById('categoria_colciencias_esperada_edit').value = categoriaColcienciasEsperada;
          document.getElementById('cvlac_edit').value = cvlac;
          document.getElementById('cedula_edit').value = cedula;
          document.getElementById('nombre_investigador_edit').value = nombreInvestigador;
          document.getElementById('categoria_institucion_edit').value = categoriaInstitucion;
          document.getElementById('id_facultad_edit').value = idFacultad;  // Asegúrate de que el valor coincida con la ID de la facultad

          // Asigna otros campos adicionales
        });

         // Agrega el evento click al botón de finalizar modificacion
         document.getElementById('updateButton').addEventListener('click', function(event) {
            var form = document.getElementById('EditForm');
            var formData = new FormData(form);

            fetch('/updateinvestigador', {
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

        fetch('/createinvestigador', {  // Nota: Verifica que la URL coincida con tu endpoint
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
  
