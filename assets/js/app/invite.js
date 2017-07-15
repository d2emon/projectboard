var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();

$.ajaxSetup({
  beforeSend: function(xhr, settings) {
    if(!this.crossDomain) {
      xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
  }
});

$(document).ready(function($){
  invite_accept = $(".accept-invite");
  invite_decline = $(".decline-invite");

  invite_accept.on('click', function(e) {
    invite = {
      projectname: $(this).data('project'),
      username: $(this).data('user'),
    };

    console.log(invite);
    
    $.post("/ru/api/project_users/accept/", invite, function(data) {
      console.log(data);
    });
    
  });
});

