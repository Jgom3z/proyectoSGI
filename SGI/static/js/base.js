$(document).ready(function(){
    // Activate tooltip
    $('[data-toggle="tooltip"]').tooltip();
    
    // Select/Deselect checkboxes
    var checkbox = $('table tbody input[type="checkbox"]');
    $("#selectAll").click(function(){
        if(this.checked){
            checkbox.each(function(){
                this.checked = true;                        
            });
        } else{
            checkbox.each(function(){
                this.checked = false;                        
            });
        } 
    });

    checkbox.click(function(){
        if(!this.checked){
            $("#selectAll").prop("checked", false);
        }
    });

    // Función para agregar y remover elementos de listas
    function agregarItem(IDdesde, IDhasta){
        var option = document.createElement("option");
        option.text = document.getElementById(IDdesde).value;
        document.getElementById(IDhasta).add(option);
        removerItem(IDdesde);
        selectTodos(IDhasta);
    }

    function removerItem(IDelemento){
        var comboBox = document.getElementById(IDelemento);
        comboBox = comboBox.options[comboBox.selectedIndex];
        comboBox.remove();
        selectTodos(IDelemento);
    }



    function selectTodos(IDelemento) {
        var elementos = document.getElementById(IDelemento);
        elementos = elementos.options;
        for (var i = 0; i < elementos.length; i++) {
            elementos[i].selected = "true";
        }
    }

    function actualizarValorSeleccionado(combo,txtOculto) {
        var select = document.getElementById(combo);
        var valorSeleccionado = select.value;
        document.getElementById(txtOculto).value = valorSeleccionado;
    }

    // Asignar las funciones de agregar y borrar a los botones correspondientes
    $("#btnAgregarItem").click(function(event) {
        agregarItem('combo1','ListBox1');
        return false;
    });

    $("#btnBorrarItem").click(function(event) {
        removerItem('ListBox1');
        return false;
    });

    
    $("#btnAgregarItems").click(function(event) {
        agregarItem('combos','ListBoxs');
        return false;
    });

    $("#btnBorrarItems").click(function(event) {
        removerItem('ListBoxs');
        return false;
    });

    $("#btnAgregarItem3").click(function(event) {
        agregarItem('combo3','ListBox3');
        return false;
    });

    $("#btnBorrarItem3").click(function(event) {
        removerItem('ListBox3');
        return false;
    });

    $("#btnAgregarItem4").click(function(event) {
        agregarItem('combo4','ListBox4');
        return false;
    });

    $("#btnBorrarItem4").click(function(event) {
        removerItem('ListBox4');
        return false;
    });
    
});



  