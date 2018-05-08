$("#bt_save_new_pays").click(function(event) {
    var target = $(event.target);
    var id = target.attr("id");

    var name = $("#txt_nom_pays_other").val();


    $.ajax({
        url: '/pays_create?nom='+name,

    }).then(function (data) {
        if (data.length > 0) {
            var max_id = -1;
            var nom= "";
            var description="";
            $.each(data, function (key, value) {
                var id = value.id;
                if (id > max_id){
                    max_id=id;
                    nom = value.nom;
                }
            });
            if(max_id > 0){
                $("#slt_pays").append(new Option(nom, max_id));
            }

            $('#slt_pays').find('option').each(function() {
                if($(this).val()==max_id){
                    $(this).prop('selected',true);
                }
            });

        }

    });

});

$("#bt_save_new_fonction_2").click(function(event) {
    alert('ici');
    var target = $(event.target);
    var id = target.attr("id");

    var name = $("#txt_nom_fonction_other").val();


    $.ajax({
        url: '/fonction_create?nom='+name,

    }).then(function (data) {
        if (data.length > 0) {
            var max_id = -1;
            var nom= "";

            $.each(data, function (key, value) {
                var id = value.id;
                if (id > max_id){
                    max_id=id;
                    nom = value.nom_fonction;
                }
            });
            if(max_id > 0){
                $("#id_profession").append(new Option(nom, max_id));
                $("#slt_fonction_locataire").append(new Option(nom, max_id));

            }

            $('#id_profession').find('option').each(function() {
                if($(this).val()==max_id){
                    $(this).prop('selected',true);
                }
            });
            $('#slt_fonction_locataire').find('option').each(function() {
                if($(this).val()==max_id){
                    $(this).prop('selected',true);
                }
            });
        }

    });

});

$("#btn_ajouter_personne").click(function(event) {
    $.ajax({
        url: '/validate_personne?nom='+ $('#txt_nom_new_personne').val() + "&prenom=" + $('#txt_prenom_new_personne').val() +"&prenom2=" + $('#txt_prenom2_new_personne').val(),
        success: function(data){

            if(data.valide){
                div_visibility('#txt_msg_error_new_personne', false);
                $("#form_ajouter_personne").submit();
                return true;
            }else{
                div_visibility('#txt_msg_error_new_personne', true);
                return false;
            }
        }

    }).then(function (data) {
    });


});

function div_visibility(id, visible){
    if(visible){
        $(id).css('visibility', 'visible');
        $(id).css('display', 'block');
    }else{
        $(id).css('visibility', 'hidden');
        $(id).css('display', 'none');
    }
}

$("#btn_locataire_ajout_personne").click(function(event) {
    div_visibility('#txt_msg_error_new_personne', false);
    $('#txt_nom_new_personne').val('');
    $('#txt_prenom_new_personne').val('');
    $('#txt_prenom2_new_personne').val('');

});
