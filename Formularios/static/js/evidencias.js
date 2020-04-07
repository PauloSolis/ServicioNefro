$(document).ready(function() {
    $('#evidencia').on('change', function() {
        $('#evidencia_label').text(this.files[0].name);
        $('#tipo').val(this.files[0].type);
        $('#size').val(this.files[0].size);
    });
    $('#save').click(function() {
        $('#save').attr('disabled', true);
        let isvalid = true;
        $('#id_nombre').removeClass('is-invalid');
        $('#evidencia').removeClass('is-invalid');
        if (($('#id_nombre').val() == '')) {
            $('#id_nombre').addClass('is-invalid');
            isvalid = false;
        }
        if (($('#evidencia').val() == '')) {
            $('#evidencia').addClass('is-invalid');
            isvalid = false;
        }
        if (isvalid) {
            $.post("", $('#no_ia').serialize(), function(data) {
                let upload = new Upload(document.getElementById('evidencia').files[0]);
                upload.doUpload(data.url);
            }).fail(function(err) {
                $('#evidencia').addClass('is-invalid');
                $('#archivo').text(err.responseJSON.error);
                $('#save').removeAttr('disabled');
            });
        } else {
            $('#save').removeAttr('disabled');
        }
    });
});

var Upload = function(file) {
    this.file = file;
};

Upload.prototype.getType = function() {
    return this.file.type;
};
Upload.prototype.getSize = function() {
    return this.file.size;
};
Upload.prototype.getName = function() {
    return this.file.name;
};
Upload.prototype.doUpload = function(url) {
    var that = this;
    console.warn(url)
    $.ajax({
        type: "PUT",
        url: url,
        xhr: function() {
            var myXhr = $.ajaxSettings.xhr();
            if (myXhr.upload) {
                myXhr.upload.addEventListener('progress', that.progressHandling, false);
            }
            return myXhr;
        },
        success: function(data) {
            redirect();
        },
        error: function(error) {
            $('#save').removeAttr('disabled');
            redirect();
        },
        async: true,
        data: that.file,
        cache: false,
        contentType: that.getType(),
        processData: false,
        timeout: 0
    });
};

Upload.prototype.progressHandling = function(event) {
    var percent = 0;
    console.warn(event);
    var position = event.loaded || event.position;
    var total = event.total;
    var progress_bar_id = "#progress";
    if (event.lengthComputable) {
        percent = Math.ceil(position / total * 100);
    }

    $(progress_bar_id).css("width", +percent + "%");
    $(progress_bar_id).text(percent + "%");
};

let redirect = function() {
    swal({
        title: "Registro exitoso.",
        text: 'Será redirigido al perfil del beneficiario',
        icon: "success",
        buttons: false,
    });
    window.setTimeout(function(ev) {
        window.location.href = '/beneficiarios/' + $('#beneficiario').val();
    }, 1500);
};