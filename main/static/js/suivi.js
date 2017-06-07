/**
 * Created by verpoorten on 7/06/17.
 */


$("#txt_loyer_percu").dblclick(function(event) {
    var loyerAttendu = $("#hdn_loyer_attendu").val();
    loyerAttendu = loyerAttendu.replace(",", ".");
    $("#txt_loyer_percu").val(loyerAttendu);
    $("#etat_suivi").val('PAYE');
});