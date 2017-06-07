

$("#date_debut").blur(function() {

    if(isDate($(this).val())){
        var currVal = $(this).val();
        var rxDatePattern = /^(\d{1,2})(\/|-)(\d{1,2})(\/|-)(\d{4})$/; //Declare Regex
        var dtArray = currVal.match(rxDatePattern); // is format OK?

        if (dtArray == null)
            return false;

        //Checks for mm/dd/yyyy format.
        dtDay = dtArray[1];
        dtMonth= dtArray[3];
        dtYear = dtArray[5];

        var result_plus_one = new Date(dtYear, dtMonth, dtDay);
        var result = new Date(dtYear, dtMonth, dtDay);

        result_plus_one.setDate(result_plus_one.getDate() + 365);
        var dd = result_plus_one.getDate();
        var mm = result_plus_one.getMonth();
        var y = result_plus_one.getFullYear();

        /*var someFormattedDate = dd + '/'+ mm + '/'+ y;
        $('#date_fin').val(someFormattedDate);

        result.setDate(result.getDate() + 355);

        dd = result.getDate();
        mm = result.getMonth();
        y = result.getFullYear();

        someFormattedDate = dd + '/'+ mm + '/'+ y;
        $('#renonciation').val(someFormattedDate);*/

    }
});

    function isDate(txtDate){
        var currVal = txtDate;
        if(currVal == '')
            return false;

        var rxDatePattern = /^(\d{1,2})(\/|-)(\d{1,2})(\/|-)(\d{4})$/; //Declare Regex
        var dtArray = currVal.match(rxDatePattern); // is format OK?

        if (dtArray == null)
            return false;

        //Checks for mm/dd/yyyy format.
        dtDay = dtArray[1];
        dtMonth= dtArray[3];
        dtYear = dtArray[5];

        if (dtMonth < 1 || dtMonth > 12) {
            return false;
        } else if (dtDay < 1 || dtDay> 31) {
            return false;
        } else if ((dtMonth==4 || dtMonth==6 || dtMonth==9 || dtMonth==11) && dtDay ==31) {
            return false;
        } else if (dtMonth == 2) {
            var isleap = (dtYear % 4 == 0 && (dtYear % 100 != 0 || dtYear % 400 == 0));
            if (dtDay> 29 || (dtDay ==29 && !isleap)) {
                return false;
            }
        }
        if (dtYear< 1900){
            return false;
        }
        return true;
    }

    $("#bt_save_new_assurance").click(function(event) {
        //event.preventDefault();
        var target = $(event.target);
        var id = target.attr("id");

        var form = target.form;
        var description = $("#txt_description_assurance_other").val();
        var name = $("#txt_nom_assurance_other").val();

        var data = new FormData();
        data.append('description', description);
        data.append('nom', name);
        var loc = location.href;
        var url = "{% url 'assurance_create' %}";
        url = "http://127.0.0.1:8000/assurance_create/";
        $.ajax({
            url: '/assurance_create?nom='+name+'&description='+description,

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
                        description = value.description;
                    }
                });
                if(max_id > 0){
                    $("#slt_assurances").append(new Option(nom + '-' + description,max_id));
                }

                $('#slt_assurances').find('option').each(function() {
                    if($(this).val()==max_id){
                        $(this).prop('selected',true);
                    }
                });

            }

        });

    });

    $("#bt_prolongation_submit").click(function(event) {
        event.preventDefault();
        var id_location = $("#id_location_prolongation").val();
        var type_prolongation = $( "#slt_type_prolongation option:selected" ).val();
        if (type_prolongation=='1'){
            $.ajax({

                url: "/prolongation?id_location=" + id_location + "&type_prolongation="+type_prolongation,
                processData: false,
                complete: function(xhr, statusText){
                    if(xhr.status=='0'){
                        //problem occured

                    }else{
                        /*$.ajax({
                            url: "/location/prepare/update/all/" + id_location,

                        });*/
                    }

            }
            });
        }
    });
    $("#bt_prolongation").click(function(event) {
        $("#txt_msg_error_slt_type_prolongation" ).html('');
        $("#txt_msg_error_slt_type_prolongation").css('visibility', 'hidden').css('display','none');
        if ($( "#slt_type_prolongation").prop('selectedIndex') <= 0 ){
            $("#txt_msg_error_slt_type_prolongation").html('Faut sélectionner une durée de prolongation');
            $("#txt_msg_error_slt_type_prolongation").css('visibility', 'visible').css('display','block');
            return false;
        }
        return true;
    });
    $("#etat_suivi").click(function(event) {
        var etat = $("#etat_suivi option:selected" ).val();

        if(etat=='PAYE'){
            $("#txt_loyer_percu").val(parseFloat($("#spn_loyer_percu").html()));
        }
    });

    $("#bt_save_new_fonction").click(function(event) {

        event.preventDefault();
        var target = $(event.target);
        var id = target.attr("id");
        var form = target.form;

        var name = $("#txt_nom_fonction_other").val();
        var data = new FormData();
        data.append('nom', name);
        var loc = location.href;
        var url = "{% url 'assurance_create' %}";
        url = "http://127.0.0.1:8000/fonction_create/?nom="+name;
        $.ajax({
            url: url,
            type: 'GET',
            processData: false,
            success: function(data){
            console.log(data);
                alert('i'+data.id);
                $('#slt_profession').append('<option val="1" selected>'+name+'</option>');
            },


        });

    });
    $("#btn_clean_personnes").click(function(event) {
        $("#nom").val('');
        $("#prenom").val('');
    });

    $("#bt_honoraire_search").click(function() {
        $("#spn_date_limite").html();
        if ($("#txt_date_limite").val() != '') {
            if (isDate($("#txt_date_limite").val())) {
                return true;
            } else {
                $("#spn_date_limite").html('Date invalide');
                return false;
            }
        }
        return true;
    });
    $("#bt_fraismaintenance_save").click(function() {
        $("#spn_date_realisation").html();
        if($("#txt_date_realisation").val()!=''){
            if(isDate($("#txt_date_realisation").val())){
                return true;
            }else{
                $("#spn_date_realisation").html('Date invalide');
                return false;
            }
        }
    });
    $("#date_debut_suivi").dblclick(function() {
        $("#date_debut_suivi").val(date_jour());

    });
    $("#date_fin_suivi").dblclick(function() {
        $("#date_fin_suivi").val(date_jour());

    });
    function date_jour(){
        var d = new Date();
        var strDate = d.getDate() + "/"+ (d.getMonth()+1)+"/" +d.getFullYear() ;
        return strDate;
    }
    $("#bt_contrat_gestion_update").click(function() {
        if($("#slt_batiment_id").val()=='' || $("#txt_montant_mensuel").val()=='' || $("#date_debut").val()=='' || $("#date_fin").val()==''){
            return false;
        }
        return true;
    });



