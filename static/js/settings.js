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
  parms={
    service:service,
    currSetting:currSetting,
    status:"updateService"
  };
  $.ajax({
    type:"POST",
    url:"/update",
    async:false,
    data:JSON.stringify(parms,null,'\t'),
    contentType: 'application/json;charset=UTF-8',
    success:function(){
      SuccessAlert("Service","changed");
    },
    error:function(){
      FailureAlert("Service","change");
    }
  });
  return false;
};

function add(service){
  if (service == "craigslist") {
    var cities = $('#clCities').val();
    var Areas = $("#clAreas").val().split(',');
    var Categories = $("#clCategories").val().split(',');
    var internship = $("#clIntern").is(':checked')?1:0;
    var slack = $("#clslack").val();
    console.log(cities,Areas,Categories,internship,slack);
    parms={
      service:service,
      status:"addRow",
      city:cities,
      areas:Areas,
      categories:Categories,
      internship:internship,
      sChannel:slack
    };
    $.ajax({
      type:"POST",
      url:"/update",
      async:false,
      data:JSON.stringify(parms,null,'\t'),
      contentType: 'application/json;charset=UTF-8',
      success:function(){
        SuccessAlert("Row","added");
      },
      error:function(){
        FailureAlert("Row","add");
      }
    });
  }
  else{
    var cities = $('#indeedCities').val();
    var keywords = $("#indeedKeywords").val().split(',');
    var slack = $("#inSlack").val();
    console.log(cities,keywords,slack);
    parms={
      service:service,
      status:"addRow",
      city:cities,
      keywords:keywords,
      sChannel:slack
    }
    $.ajax({
      type:"POST",
      url:"/update",
      async:false,
      data:JSON.stringify(parms,null,'\t'),
      contentType: 'application/json;charset=UTF-8',
      success: function(){
        SuccessAlert("Row","added");
      },
      error: function(){
        FailureAlert("Row","add");
      }
    });
  }
  return false;
};

function deleteRow(service,row){
  if (service == "craigslist") {
    console.log("CL DELETE");
    $.post('/update',{
      service:service,
      status:"deleteRow"
    }).done(function(deleteRow){
      SuccessAlert("Row","deleted");
    }).fail(function(deleteRow){
      FailureAlert("Row","delete");
    })
  }
  else{
    console.log("IN DELETE");
    $.post('/update',{
      service:service,
      status:"deleteRow"
    }).done(function(deleteRow){
      SuccessAlert("Row","deleted");
    }).fail(function(deleteRow){
      FailureAlert("Row","delete");
    })
  }
  return false;
};

function SuccessAlert(eventType,eventAction){
  $('#alert').html("<div class = 'alert alert-success fade show alert-dismissable' role='alert'><button type='button' class='close' data-dismiss='alert' aria-hidden='true'>&times;</button><span>" + eventType + " has been " + eventAction + " successfully!</span></div>");
  $(".alert").alert();
}

function FailureAlert(eventType,eventAction){
  $('#alert').html("<div class = 'alert alert-danger fade show alert-dismissable' role='alert'><button type='button' class='close' data-dismiss='alert' aria-hidden='true'>&times;</button><span>" + eventType + " has failed to " + eventAction + "!</span></div>" );
  $(".alert").alert();
}
