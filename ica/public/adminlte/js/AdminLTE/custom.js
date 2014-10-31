$(function() {
	$( document ).ready(function() {
		$(document).pjax('a[data-pjax]', '#main-content')
	});

	$(document).on('submit','#profile_reset_private_token',function(e){
		e.preventDefault();

		if ( ask() ) {

			var form = $('#profile_reset_private_token');
			dataString = form.serialize();
			
			$.ajax({
				type: $(this).attr('method'),
				url: $(this).attr('action'),
				data: $(this).serialize(),
				beforeSend: function(){
					form.find(".box-footer").append('<img src="/adminlte/img/ajax-loader-custom.gif" />');
				},
				success: function(data)
				{
					setTimeout(function(){
						form.find("#private_token").val( data );
						form.find(".form-group").addClass('has-success');
						form.find("#label_msg").remove();
						form.find(".form-group").append("<label id='label_msg' class='control-label'><i class='fa fa-check-circle'></i> Token updated</label>");
					}, 500);
				},
				error: function(data)
				{
					setTimeout(function(){
						form.find(".form-group").addClass('has-error');
						form.find("#label_msg").remove();
						form.find(".form-group").append("<label id='label_msg' class='control-label'><i class='fa fa-times-circle'></i> There was an error</label>");
					}, 500);
				},
				complete: function(data)
				{
					setTimeout(function(){
						form.find(".box-footer > img").remove();
					}, 500);
				}
			});
		}
		return false;
	});


	$(document).on('submit','#profile_update_settings',function(e){
		e.preventDefault();
		var form = $('#profile_update_settings');
		dataString = form.serialize();
		
		$.ajax({
			type: $(this).attr('method'),
			url: $(this).attr('action'),
			data: $(this).serialize(),
			beforeSend: function(){
				form.find(".box-footer").append('<img src="/adminlte/img/ajax-loader-custom.gif" />');
			},
			success: function(data)
			{
				setTimeout(function(){
					$('.content').find("#updated_response").empty();
					$('.content').find("#updated_response").append("\
						<div class='alert alert-success alert-dismissable'>\
							<i class='fa fa-check'></i>\
							<button type='button' class='close' data-dismiss='alert' aria-hidden='true'>&times;</button>\
							Profile updated successfully\
						</div>");
					$(document).find('.cname').text(data);
				}, 500);
			},
			error: function(data)
			{
				setTimeout(function(){
					$('.content').find("#updated_response").empty();
					$('.content').find("#updated_response").append("\
					<div class='alert alert-danger alert-dismissable'>\
						<i class='fa fa-ban'></i>\
						<button type='button' class='close' data-dismiss='alert' aria-hidden='true'>&times;</button>\
						There was an error, the profile was not updated\
					</div>");
				}, 500);
			},
			complete: function(data)
			{
				setTimeout(function(){
					form.find(".box-footer > img").remove();
				}, 500);
			}
		});
		return false;
	});

	$(document).on('ifChecked','input[name=notifications]:radio',function(e){
		var id = $(this).attr('id');
		var type = $(this).val();
		var form = $('#notofications_global');
		dataString = form.serialize();
		
		$.ajax({
			type: $(this).attr('method'),
			url: $(this).attr('action'),
			data: $(this).serialize(),
			beforeSend: function(){
				form.find("#loading_"+id).append('<img src="/adminlte/img/ajax-loader-custom.gif" />');
			},
			complete: function(data)
			{
				setTimeout(function(){
					form.find("#loading_"+id).empty();
				}, 300);
			}
		});
	});
	

});


function ask() {
	q = confirm('Are you sure?');
	if (q)
		return true;
	else
		return false; 
}
