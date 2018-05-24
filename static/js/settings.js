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
    $("#alert").addClass('alert alert-success fade show alert-dismissable');
    $("#alert").attr('role','alert');
    $(".alert").alert("Service has been changed successfully!");
    // $("#alert").append("Service has been changed successfully!");
    // $("#alertButton").show();
  }).fail(function(update){
    $("#alert").addClass('alert alert-danger fade show alert-dismissable');
    $("#alert").attr('role','alert');
    $("#alert").text("Service has failed to change!");
  })
  return false;
};

function add(){
  $.post('/update',{

    service:service,
    status:"addRow"
  }).done(function(add){
    $("#alert").addClass('alert alert-success fade show alert-dismissable');
    $("#alert").attr('role','alert');
    $("#alert").append("Row has been added successfully!");

  }).fail(function(add){
    $("#alert").addClass('alert alert-danger fade show alert-dismissable');
    $("#alert").attr('role','alert');
    $("#alert").append("Row has failed to add!");
  })
  return false;
};

function deleteRow(){
  $.post('/update',{

    service:service,
    status:"deleteRow"
  }).done(function(deleteRow){
    $("#alert").addClass('alert alert-success fade show alert-dismissable');
    $("#alert").attr('role','alert');
    $("#alert").append("Row has been deleted successfully!");

  }).fail(function(deleteRow){
    $("#alert").addClass('alert alert-danger fade show alert-dismissable');
    $("#alert").attr('role','alert');
    $("#alert").append("Row has failed to delete!");
  })
  return false;
};
