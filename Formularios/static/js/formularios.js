function validation() {
    var max = document.getElementsByClassName("maximo");
    var min = document.getElementsByClassName("minimo");
    var i, war = false;
    for (i = 0; i < max.length; i++) {
        if (parseInt(max[i].value) < parseInt(min[i].value)) {
            war = true;
            max[i].style.border="2px solid red";
            min[i].style.border="2px solid red";
        }
        else {
            max[i].style.border="red";
            min[i].style.border="red";
        }
    }

    if (war){
        console.log("error");
        swal({
            title: "El valor máximo no debe ser menor al mínimo",
            icon: "error"
        });
        return false;
    }else{
        console.log("noerror");
        $('.sweet-form').submit();
        return true;
    }
}

function depre() {
    var res = document.getElementsByClassName("resultadoDep");
    for (var i = 0; i < res.length; i++) {
        if (res[i].value == ""){
            document.getElementById("diagRep").className = "";
            document.getElementById("diagRep").innerHTML = "";
        }
        else if (res[i].value >= 0 && res[i].value <= 7){
            document.getElementById("diagRep").className = "alert alert-success";
            document.getElementById("diagRep").innerHTML = "No deprimido";
        }
        else if (res[i].value >= 8 && res[i].value <= 13){
            document.getElementById("diagRep").className = "alert alert-secondary";
            document.getElementById("diagRep").innerHTML = "Depresión ligera/menor";
        }
        else if (res[i].value >= 14 && res[i].value <= 18){
            document.getElementById("diagRep").className = "alert alert-dark";
            document.getElementById("diagRep").innerHTML = "Depresión moderada";
        }
        else if (res[i].value >= 19 && res[i].value <= 22){
            document.getElementById("diagRep").className = "alert alert-warning";
            document.getElementById("diagRep").innerHTML = "Depresión severa";
        }
        else{
            document.getElementById("diagRep").className = "alert alert-danger";
            document.getElementById("diagRep").innerHTML = "Depresión muy severa";
        }
    }
}


$('.btn-form').on('click', function(e) {
    e.preventDefault();
    swal({
        title: "¿Estás seguro que quieres eliminar?",
        text: "No es posible revertir esta acción.",
        icon: "warning",
        buttons: ['Cancelar', 'Confirmar'],
    })
        .then((willDelete) => {
            if (willDelete) {
                if ($(this).data("form") == 'tamizajenutricional'){
                    swal({
                        title: "Aviso",
                        text: "Si ya realizaste la escala de malnutrición-inflamación, revisar los datos del IMC",
                        icon: "warning",
                        buttons: false,
                        timer: 3000,
                    }).then(() => {
                        $('#delete_form').submit()
                    });
                } else {
                    $('#delete_form').submit();
                }
                return true;
            } else {
                return false;
            }
        });
});
