
$("#date_finn" ).change(function(event) {
  alert('change');
  var target = $(event.target);
  var id = target.attr("id");
  if (typeof id == 'undefined') {
    target = target.parent();
    id = target.attr("id");
  }
  /*Récupère la valeur du champ*/
  alert(event.target.value || "");
  /*J'ai pas encore modifié ci-dessous pour avoir le nécessaire*/
  if (typeof id != 'undefined') {
    link = id.replace(/-/g , "/");
    link = "/" + link;

      $.ajax({
        type: "POST",
        url: link,
        success: function(msg) {
          url = window.location.href.toString();
          url = url.replace("#", "");
          console.log(url);
          window.location.replace(url);
        }
      });

  }
});

$("#date_debut_location").change(function(event) {
    if($("#date_fin_location")){
        if($("#date_fin_location").val()=='') {
            pos = $("#date_debut_location").val().lastIndexOf("/");
            tt = $("#date_debut_location").val().slice(pos+1);
            tt = parseInt(tt) + 1;
            dd = $("#date_debut_location").val().slice(0,pos);
            $("#date_fin_location").val(dd +"/"+ String(tt));
        }
    }

});



