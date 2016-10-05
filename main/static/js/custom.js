
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

document.querySelector('input[list="localites_nom"]').addEventListener('input', onInput);
document.querySelector('input[list="localites"]').addEventListener('input', onInput2);

function onInput(e) {
   var input = e.target,
       val = input.value;
       list = input.getAttribute('list');
       options = document.getElementById(list).childNodes;

  for(var i = 0; i < options.length; i++) {
    if(options[i].innerText === val) {
      // An item was selected from the list!
      // yourCallbackHere()

    var value = options[i];

    var id_localite = options[i].getAttribute('data-id');

        $('#localites option').each(function(){

            if ($(this).attr('data-id') == id_localite){
                $('#localite').val($(this).val());
            }
        });


      break;
    }
  }
}

function onInput2(e) {
   var input = e.target,
       val = input.value;
       list = input.getAttribute('list');
       options = document.getElementById(list).childNodes;

  for(var i = 0; i < options.length; i++) {
    if(options[i].innerText === val) {
      // An item was selected from the list!
      // yourCallbackHere()

    var value = options[i];

    var id_localite = options[i].getAttribute('data-id');

        $('#localites_nom option').each(function(){
            if ($(this).attr('data-id') == id_localite){
                $('#localite_nom').val($(this).val());
            }
        });


      break;
    }
  }
}


