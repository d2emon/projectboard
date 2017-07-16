var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();

$.ajaxSetup({
  beforeSend: function(xhr, settings) {
    if(!this.crossDomain) {
      xhr.setRequestHeader("X-CSRFToken", csrftoken);
    }
  }
});

$(document).ready(function($){
  var alerts = $("#invite-alerts");
  var invite_accept = $(".accept-invite");
  var invite_decline = $(".decline-invite");
  var projectlist = $("#projectlist tbody")

  function update_project_users(data) {
    console.log(data);
    if(data.error) {
      error_message = '<div class="alert alert-danger">' + data.error + '</div>';
      alerts.append(error_message);
      return false;
    }else{
      return true;
    }	  
  }

  invite_accept.on('click', function(e) {
    invite = {
      projectname: $(this).data('project'),
      username: $(this).data('user'),
    };
    url = "/api/project_users/accept/"
    $.post(url, invite, function(data){
    	if(update_project_users(data)){
            project = data.project
            if(project.end_date){
          	project_dates = project.start_date + ' - ' + project.end_date;
            }else{
            	project_dates = project.start_date;    	  
            }
            project_owner = '<a href="' + project.owner.url + '">' +
              '<div class="avatar">' +
              '<img src="' + project.owner.profile.avatar + '" class="img-avatar" alt="' + project.owner.email + '">' +
              '<span class="avatar-status badge-success"></span>' + 
              '</div>' +
              '<div><small>' + project.owner.username + '</small></div>' +
              '</a>';
            projecttable = '<tr>' +
          	'<td><a href="' + project.url + '">' + project.name + '</a></td>' +
          	'<td>&nbsp;</td>' +
          	'<td>(' + project_dates + ')</td>' +
          	'<td>' + project_owner + '</td>' +
          	'<td>&nbsp;</td>' +
          	'</tr>';
            for(i=0; i<3; i++){
          	projecttable += '<tr>' +
             	  '<td><a href="' + project.url + '">' + project.name + '</a></td>' +
          	  '<td><a href="#">Task Name</a></td>' +
          	  '<td>' + project.start_date + '</td>' +
          	  '<td>' + project_owner + '</td>' +
          	  '<td>&nbsp;</td>' +
          	  '</tr>';
            }
            projectlist.append(projecttable);    		
    	}
    });
  });

  invite_decline.on('click', function(e) {
    invite = {
      projectname: $(this).data('project'),
      username: $(this).data('user'),
    };
    url = "/api/project_users/decline/"
    $.post(url, invite, update_project_users);    
  });
});

