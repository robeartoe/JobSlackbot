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
    var icon = $("#clIcon").val();
    console.log(cities,Areas,Categories,internship,slack,icon);
    parms={
      service:service,
      status:"addRow",
      city:cities,
      areas:Areas,
      categories:Categories,
      internship:internship,
      sChannel:slack,
      icon:icon
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
    var icon = $("#inIcon").val();
    console.log(cities,keywords,slack);
    parms={
      service:service,
      status:"addRow",
      city:cities,
      keywords:keywords,
      sChannel:slack,
      icon:icon
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
    var row = $("#"+row);
    var tds = row.children().closest("td");
    console.log(tds);

    var parms ={
        city: tds[0].outerText,
        area: tds[1].outerText,
        category: tds[2].outerText,
        internship: tds[3].outerText,
        slackChannel: tds[4].outerText,
        icon:tds[5].outerText,
        service:service,
        status:"deleteRow"
    };
    $.ajax({
      type:"POST",
      url:"/update",
      async:false,
      data:JSON.stringify(parms,null,'\t'),
      contentType: 'application/json;charset=UTF-8',
      success: function(){
        SuccessAlert("Row","deleted");
        row.remove();
      },
      error: function(){
        FailureAlert("Row","delete");
      }
    });
  }
  else{
    console.log("IN DELETE");
    var row = $("#"+row);
    var tds = row.children().closest("td");
    console.log(tds);
    var parms ={
        city: tds[0].outerText,
        keyword: tds[1].outerText,
        slackChannel: tds[2].outerText,
        icon:tds[3].outerText,
        service:service,
        status:"deleteRow"
    };
    $.ajax({
      type:"POST",
      url:"/update",
      async:false,
      data:JSON.stringify(parms,null,'\t'),
      contentType: 'application/json;charset=UTF-8',
      success: function(){
        SuccessAlert("Row","deleted");
        row.remove();
      },
      error: function(){
        FailureAlert("Row","delete");
      }
    });




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
