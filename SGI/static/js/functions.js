function loadData(url, id) {
  $.ajax({
    url: url,
    type: "POST",
    data: { id: id },
    success: function (response) {
      if (response && response.data && response.ids_editar) {
        const data = JSON.parse(response.data);
        const idsFields = response.ids_editar;

        const responseData = Array.isArray(data) ? data[0] : {};

        // Iterar sobre los campos y actualizar los valores
        Object.keys(idsFields).forEach(field => {
          const inputId = idsFields[field]; // Obtener el ID del input
          const value = responseData[field] || ""; // Obtener el valor del campo
          const inputElement = document.getElementById(inputId);
          if (inputElement) {
            // Manejar el tipo de campo y formatear el valor si es necesario
            if (inputElement.type === 'date') {
              inputElement.value = formatDate(value);
            } else {
              inputElement.value = value;
            }
          }
        });

      } else {
        alert("No se encontraron datos");
      }
    },
    error: function () {
      alert("Error al cargar datos");
    }
  });
}
function formatDate(fecha) {
  const date = new Date(fecha);
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate() + 1).padStart(2, "0");
  return `${year}-${month}-${day}`;
}

//Filtro filas en tabla
function TableFilter(searchInputId, searchButtonId, tableId) {
  const searchInput = document.getElementById(searchInputId);
  const searchButton = document.getElementById(searchButtonId);
  const table = document.getElementById(tableId);
  // Verifica si los elementos están presentes
  if (!searchInput || !searchButton || !table) {
    console.error('Uno o más elementos no se encontraron. Asegúrate de que los IDs sean correctos.');
    return;
  }

  const tableBody = table.querySelector('tbody');

  function filterTable() {
    const searchTerm = searchInput.value.toLowerCase();
    const rows = tableBody.querySelectorAll('tr');

    rows.forEach(row => {
      const cells = row.querySelectorAll('td');
      let match = false;

      cells.forEach(cell => {
        if (cell.textContent.toLowerCase().includes(searchTerm)) {
          match = true;
        }
      });

      row.style.display = match ? '' : 'none';
    });
  }

  // Filtrar al hacer clic en el botón de búsqueda
  searchButton.addEventListener('click', filterTable);

  // Opcional: Filtrar en tiempo real mientras se escribe
  searchInput.addEventListener('input', filterTable);
}