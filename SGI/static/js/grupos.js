//GRUPOS DE INVESTIGACIÓN 

  // // Agrega el evento click al botón de Modificar
  function loadData(id) {
          // Llama al backend para obtener los datos de la cita usando el ID
          $.ajax({
            url: "/get_grupoInvestigacion",
            type: "POST",
            data: { id_grupo: id },
            success: function (data) {
              // Asignar valores a los campos
              document.getElementById('id_grupo_edit').value = data[0].id_grupo;  // Asigna el ID del grupo
              document.getElementById('nombre_grupo_edit').value = data[0].nombre_grupo;
              document.getElementById('codigo_grup_lac_edit').value = data[0].codigo_grup_lac;
              document.getElementById('categoria_colciencias_edit').value = data[0].categoria_colciencias;
              document.getElementById('fecha_creacion_edit').value = data[0].fecha_creacion;
              document.getElementById('fecha_finalizacion_edit').value = data[0].fecha_finalizacion;
              document.getElementById('id_facultad_edit').value = data[0].id_facultad; // Asegúrate de que el valor coincida con la ID de la facultad
              document.getElementById('id_lider_edit').value = data[0].id_lider; // Asegúrate de que el valor coincida con la ID del líder
              document.getElementById('area_conocimiento_edit').value = data[0].area_conocimiento;
              document.getElementById('plan_estrategico_edit').value = data[0].plan_estrategico;
              document.getElementById('categoria_meta_edit').value = data[0].categoria_meta;
              document.getElementById('estrategia_meta_edit').value = data[0].estrategia_meta;
              document.getElementById('vision_edit').value = data[0].vision;
              document.getElementById('objetivos_edit').value = data[0].objetivos;
            
            },
            error: function () {
              alert("Error al cargar datos");
            },
          });
        }

  document.addEventListener('DOMContentLoaded', function() {
    // Agrega un evento click a todos los enlaces con la clase 'a-td'
    document.querySelectorAll('.a-td').forEach(function(link) {
      link.addEventListener('click', function(event) {
        event.preventDefault(); // Evita el comportamiento por defecto del enlace

        // Obtén la información del grupo desde los atributos de datos del enlace
        var idGrupo = this.getAttribute('data-id'); // Obtén el ID del grupo
        var nombreGrupo = this.getAttribute('data-nombre');
        var codigoGrupo = this.getAttribute('data-codigo');
        var categoriaColciencias = this.getAttribute('data-categoria');
        var fechaCreacion = this.getAttribute('data-fecha-creacion');
        var fechaFinalizacion = this.getAttribute('data-fecha-finalizacion');
        var nombreFacultad = this.getAttribute('data-facultad');
        var nombreLider = this.getAttribute('data-lider');
        var areaConocimiento = this.getAttribute('data-area');
        var planEstrategico = this.getAttribute('data-plan');
        var categoriaMeta = this.getAttribute('data-categoriaMeta');
        var estrategiaMeta = this.getAttribute('data-estrategiaMeta');
        var vision = this.getAttribute('data-vision');
        var objetivos = this.getAttribute('data-objetivos');
        

        // Actualiza el contenido del modal de detalles
        document.getElementById('modalNombreGrupo').textContent = nombreGrupo;
        var tableContent = `
          <tr>
            <th>ID Grupo</th>
            <td>${idGrupo}</td>
          </tr>
          <tr>
            <th>Código Grupo</th>
            <td>${codigoGrupo}</td>
          </tr>
          <tr>
            <th>Categoría Colciencias</th>
            <td>${categoriaColciencias}</td>
          </tr>
          <tr>
            <th>Fecha de Creación</th>
            <td>${fechaCreacion}</td>
          </tr>
          <tr>
            <th>Fecha de Finalización</th>
            <td>${fechaFinalizacion}</td>
          </tr>
          <tr>
            <th>Facultad</th>
            <td>${nombreFacultad}</td>
          </tr>
          <tr>
            <th>Líder del Grupo</th>
            <td>${nombreLider}</td>
          </tr>
          <tr>
            <th>Área de Conocimiento</th>
            <td>${areaConocimiento}</td>
          </tr>
          <tr>
            <th>Plan Estratégico</th>
            <td>${planEstrategico}</td>
          </tr>
          <tr>
            <th>Categoría Meta</th>
            <td>${categoriaMeta}</td>
          </tr>
          <tr>
            <th>Estrategia Meta</th>
            <td>${estrategiaMeta}</td>
          </tr>
          <tr>
            <th>Visión</th>
            <td>${vision}</td>
          </tr>
          <tr>
            <th>Objetivos</th>
            <td>${objetivos}</td>
          </tr>
          <br>
          <button type="submit" class="btn btn-danger" id="deleteButton" style = "margin-left:10px;">Eliminar</button>
          <br>
        `;
        document.getElementById('modalTableBody').innerHTML = tableContent;

        // Agrega el evento click al botón de eliminar
        document.getElementById('deleteButton').addEventListener('click', function() {
          if (confirm('¿Estás seguro de que deseas eliminar este grupo?')) {
            // Aquí debes hacer la llamada a la API para eliminar el grupo utilizando el idGrupo
            fetch('/deletegrupo', {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json'
              },
              body: JSON.stringify({ id_grupo: idGrupo })
            })
            .then(response => response.json().then(data => ({ status: response.status, body: data})))
            .then(data => {
              if (data.status === 200 && data.body.message.includes("correctamente")) {
                alert(data.body.message);

                // Cerrar el modal utilizando JavaScript puro
                let modal = document.getElementById('grupoModal');
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
                alert('Error al eliminar el grupo: ' + data.body.message);
              }
            })
            .catch(error => {
              console.error('Error:', error);
              alert('Error al eliminar el grupo: ' + error.message);
            });
          }
        });
        document.querySelector('#modalEditGroupButton').addEventListener('click', function() {
        // Pasa la información al modal de edición
        console.log(nombreFacultad);
        document.getElementById('id_grupo_edit').value = idGrupo;  // Asigna el ID del grupo
        document.getElementById('nombre_grupo_edit').value = nombreGrupo;
        document.getElementById('codigo_grup_lac_edit').value = codigoGrupo;
        document.getElementById('categoria_colciencias_edit').value = categoriaColciencias;
        document.getElementById('fecha_creacion_edit').value = fechaCreacion;
        document.getElementById('fecha_finalizacion_edit').value = fechaFinalizacion;
        document.getElementById('id_facultad_edit').value = nombreFacultad; // Asegúrate de que el valor coincida con la ID de la facultad
        document.getElementById('id_lider_edit').value = nombreLider; // Asegúrate de que el valor coincida con la ID del líder
        document.getElementById('area_conocimiento_edit').value = areaConocimiento;
        document.getElementById('plan_estrategico_edit').value = planEstrategico;
        document.getElementById('categoria_meta_edit').value = categoriaMeta;
        document.getElementById('estrategia_meta_edit').value = estrategiaMeta;
        document.getElementById('vision_edit').value = vision;
        document.getElementById('objetivos_edit').value = objetivos;
        //   // Asigna otros campos adicionales
         });

         

         // Agrega el evento click al botón de finalizar modificacion
         document.getElementById('updateButton').addEventListener('click', function(event) {
            var form = document.getElementById('EditForm');
            var formData = new FormData(form);

            fetch('/updategrupo', {
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

        fetch('/createGrupo', {  // Nota: Verifica que la URL coincida con tu endpoint
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
  
//LINEAS DE INVESTIGACIÓN PARA GRUPOS 

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
  
