$(document).ready(function() {
    //All custom jQuery will go here:
    $(function () {
      $('#clcheck').change(function(){
        if ($(this).is(':checked')) {
          $('#clform').show();
          update("craigslist",1);
        }
        else {
          $('#clform').hide();
          update("craigslist",0);
        }
      })
      $('#incheck').change(function(){
        if ($(this).is(':checked')) {
          $('#indeedform').show();
          update("indeed",1);
        }
        else {
          $('#indeedform').hide();
          update("indeed",0);
        }
      })
     })
});

function update(service,currSetting){
  $.post('/update',{
    service:service,
    currSetting:currSetting,
    status:"updateService"
  }).done(function(update){
    $('#alert').html('<div class = "alert alert-success fade show alert-dismissable" role="alert"><button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button><span>Service has been changed successfully!</span></div>')
    $(".alert").alert();
  }).fail(function(update){
    $('#alert').html('<div class = "alert alert-success fade show alert-dismissable" role="alert"><button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button><span>Service has failed to change!</span></div>')
    $(".alert").alert();
  })
  return false;
};

function add(){
  $.post('/update',{

    service:service,
    status:"addRow"
  }).done(function(add){
    $('#alert').html('<div class = "alert alert-success fade show alert-dismissable" role="alert"><button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button><span>Row has been added successfully!</span></div>')
    $(".alert").alert();

  }).fail(function(add){
    $('#alert').html('<div class = "alert alert-success fade show alert-dismissable" role="alert"><button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button><span>Row has failed to add!</span></div>')
    $(".alert").alert();
  })
  return false;
};

function deleteRow(){
  $.post('/update',{

    service:service,
    status:"deleteRow"
  }).done(function(deleteRow){
    $('#alert').html('<div class = "alert alert-success fade show alert-dismissable" role="alert"><button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button><span>Row has been deleted successfully!</span></div>')
    $(".alert").alert();

  }).fail(function(deleteRow){
    $('#alert').html('<div class = "alert alert-success fade show alert-dismissable" role="alert"><button type="button" class="close" data-dismiss="alert" aria-hidden="true">&times;</button><span>Row has failed to delete!</span></div>')
    $(".alert").alert();
  })
  return false;
};
