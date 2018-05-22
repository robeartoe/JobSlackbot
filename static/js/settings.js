$(document).ready(function() {
    //All custom jQuery will go here:
    $(function () {
      $('#clcheck').change(function(){
        if ($(this).is(':checked')) {
          $('#clform').show();
        }
        else {
          $('#clform').hide();
        }
      })
      $('#incheck').change(function(){
        if ($(this).is(':checked')) {
          $('#indeedform').show();
        }
        else {
          $('#indeedform').hide();
        }
      })
     })
});

function update(){
  $.post('/update',{

  }).done(function(update){

  }).fail(function(update){
  })
};

function add(){
  $.post('/update',{

  }).done(function(add){

  }).fail(function(add){

  })
};

function deleteRow(){
  $.post('/update',{

  }).done(function(deleteRow){

  }).fail(function(deleteRow){

  })
};
