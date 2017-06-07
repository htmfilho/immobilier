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
