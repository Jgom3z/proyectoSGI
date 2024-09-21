//Scripts para ocultar y desplegar el navbar -->

  document.addEventListener('DOMContentLoaded', function() {
    const sidebarToggle = document.querySelector('.sidebar-toggle');
    const sidebar = document.querySelector('.sidebar');
    const content = document.querySelector('main');

    sidebarToggle.addEventListener('click', function() {
      sidebar.classList.toggle('hidden');
      content.classList.toggle('expanded');
    });

    const dropdownToggle = document.querySelector('.dropdown-toggle');
    const dropdown = document.querySelector('.dropdown');

    dropdownToggle.addEventListener('click', function(e) {
      e.preventDefault();
      dropdown.classList.toggle('active');
    });
  });

 
  document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchInput');
    const searchButton = document.getElementById('searchButton');
    const table = document.getElementById('groupsTable');
    const tableBody = table.querySelector('tbody');

    searchButton.addEventListener('click', function() {
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
    });

    // Opcional: Permitir búsqueda en tiempo real
    searchInput.addEventListener('input', function() {
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
    });
  });

  document.querySelector('.custom-menu-button').addEventListener('click', function() {
    const menuList = document.querySelector('.custom-menu-list');
    menuList.style.display = menuList.style.display === 'block' ? 'none' : 'block';
});
