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
        url: '/societe_create?nom='+nom + '&description='+description + '&rue='+rue+'&numero='+numero+'&boite='+boite+'&localite='+localite+'&cp='+localite_cp+'&type='+type,

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
                alert('kk');
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
