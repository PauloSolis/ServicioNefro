$('.btn-submit').on('click', function(e) {
    e.preventDefault();
    let clasificacion = e.target.value;
    swal({
            title: "¿Estás seguro que quieres seleccionar "+clasificacion+" como clasificación?",
            text: "No es posible revertir esta acción.",
            icon: "warning",
            buttons: ['Cancelar', 'Confirmar'],
        })
        .then((willDelete) => {
            if (willDelete) {
                let clasificacion_input = document.createElement('input');
                clasificacion_input.name = 'clasificacion';
                clasificacion_input.value = clasificacion;
                clasificacion_input.type = 'hidden';

                document.getElementById('clasificacion_form').appendChild(clasificacion_input)

                $('#clasificacion_form').submit();
                return true;
            } else {
                return false;
            }
        });
});
