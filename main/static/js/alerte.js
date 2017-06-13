
$(document).ready(function() {
    $('#tbl_data_alertes').dataTable({
        "columnDefs": [{
            "targets": 'no-sort',
            "orderable": false,
        }],
        "lengthChange": false,
        "language": {
            "url": "/static/i18n/French.json"
        }
    });
} );

$("#slt_etat_alerte").change(function(event) {
    $("#hdn_etat_alerte").val($("#slt_etat_alerte").val());
});


$("button[id^='btn_update_alerte_']").click(function(event) {
    var target = $(event.target);
    var id = target.attr("id");
    if (typeof id === 'undefined') {
        target = target.parent();
        id = target.attr("id");
    }
    var alerte_id = id.substring(id.lastIndexOf("_") + 1);
    $("#hdn_alerte_id").val(alerte_id);
    $("#form_alerte_update").submit();
});
