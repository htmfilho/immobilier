$("#txt_nom_societe").change(function() {
    if ($("#txt_nom_societe").val()) {
        $("#bt_save_new_societe_new").removeAttr('disabled');
    }else{
        $("#bt_save_new_societe_new").attr('disabled','disabled');
    }
});

$("#txt_nom_societe").blur(function() {
    if ($("#txt_nom_societe").val() != '') {
        nom = $("#txt_nom_societe").val();
        $("#msg_nom").hide();
        $("#msg_nom").removeClass("invisible");
        $('#msg_nom').html('');

        if (nom.length > 3) {

            $.ajax({
                url: '/check_societe?nom=' + nom,

            }).then(function (data) {
                if (data.length > 0) {
                    var existing_society = ""
                    var cpt = 1;
                    $.each(data, function (key, value) {
                        if (cpt > 1) {
                            existing_society = existing_society + ", " + value.nom;
                        } else {
                            existing_society = existing_society + value.nom;
                        }
                        cpt = cpt + 1;
                    });
                    alert(existing_society);
                    $('#msg_nom').html('<p>Attention il existe déjà des sociétés avec le nom ci-dessus :</p><p> ' + existing_society + '</p>');
                    $("#msg_nom").show();
                }

            });
        }
    }
});

$("#bt_save_new_societe_new").click(function(event) {
    var target = $(event.target);
    var id = target.attr("id");

    var nom = $("#txt_nom_societe").val();
    var description = $("#txt_description_societe").val();
    var rue = $("#txt_rue_societe").val();
    var numero = $("#txt_numero_societe").val();
    var boite = $("#txt_boite_societe").val();
    var localite = $("#txt_localite_societe").val();
    var localite_cp = $("#txt_localite_cp_societe").val();

    var type = $("#slt_type").val();

    $.ajax({
        url: '/societe_create?nom='+nom + '&description='+description + '&rue='+rue+'&numero='+numero+'&boite='+boite+'&localite='+localite+'&localite_cp='+localite_cp+'&type='+type,

    }).then(function (data) {
        if (data.length > 0) {
            var max_id = -1;
            var nom= "";

            $.each(data, function (key, value) {
                var id = value.id;
                if (id > max_id){
                    max_id=id;
                    nom = value.nom;
                }
            });
            if(max_id > 0){
               $("#slt_societes").append(new Option(nom, max_id));
                $("#slt_societes_locataire").append(new Option(nom, max_id));
            }

            $('#slt_societes').find('option').each(function() {

                if($(this).val()==max_id){
                    $(this).prop('selected',true);
                }
            });
            $('#slt_societes_locataire').find('option').each(function() {

                if($(this).val()==max_id){
                    $(this).prop('selected',true);
                }
            });
        }

    });

});
