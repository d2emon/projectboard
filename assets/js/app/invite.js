$(document).ready(function($){
  invite_accept = $(".accept-invite");
  invite_decline = $(".decline-invite");

  invite_accept.on('click', function(e) {
    invite = {
      project: $(this).data('project'),
      user: $(this).data('user'),
    };

    console.log(e);
    console.log(invite);

    $.post("/api/project_users/accept", invite, function(data) {
      console.log(data);
    });
  });
});

