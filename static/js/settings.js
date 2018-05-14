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
