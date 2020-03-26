M.AutoInit();


$(document).ready(function(){
    $('ul.tabs').tabs();
    $('textarea#message').characterCounter();
    $('.dropdown-trigger').dropdown({
      inDuration: 200,
      outDuration: 200,
      constrain_width: true, // Does not change width of dropdown to that of the activator
      hover: false, // Activate on hover
      coverTrigger: false,
      alignment: 'top' // Displays dropdown with edge aligned to the left of button
    });
    $('.dropdown-trigger2').dropdown({
      inDuration: 200,
      outDuration: 200,
      constrain_width: true, // Does not change width of dropdown to that of the activator
      hover: false, // Activate on hover
      coverTrigger: false,
      alignment: 'top' // Displays dropdown with edge aligned to the left of button
    });


});


$('.alert_close').click(function(){
    $(this).parent().parent().fadeOut( "slow", function() {
  });
});

function set_message_count(n){
  $('#message_count').text(n);
  $('#message_count').css('visibility', n ? 'visible' : 'hidden');
}

function enableButton() {
  // Get the checkbox
  var checkBox = document.getElementById("tos");
  // Get the output text
  var button = document.getElementById("btn_register");

  // If the checkbox is checked, display the output text
  if (checkBox.checked == true){
    button.disabled = false;
  } else {
    button.disabled = true;
  }
}