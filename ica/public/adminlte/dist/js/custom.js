$(function() {

	var img_loader = "/adminlte/dist/img/ajax-loader-custom.gif";

	$(document).ready(function() {
		notifications_global_iCheck();
		$(document).pjax('a[data-pjax]', '#main-content')

		$(document).on('pjax:complete', function() {
			NProgress.done();
			if ( $(location).attr('pathname') == "/profile/notifications" ){
				notifications_global_iCheck(); // Load plugin for specific page
			}
		})

		$(document).on('pjax:beforeSend', function() {
			NProgress.start();
		})
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
					form.find(".box-footer").append('<img src="'+img_loader+'" />');
				},
				success: function(data)
				{
					setTimeout(function(){
						form.find("#private_token").val( data );
						form.find(".form-group").addClass('has-success');
						form.find("#label_msg").remove();
						form.find(".form-group").append("<label id='label_msg' class='control-label'><i class='fa fa-check-circle'></i> Token updated</label>");
					}, 300);
				},
				error: function(data)
				{
					setTimeout(function(){
						form.find(".form-group").addClass('has-error');
						form.find("#label_msg").remove();
						form.find(".form-group").append("<label id='label_msg' class='control-label'><i class='fa fa-times-circle'></i> There was an error</label>");
					}, 300);
				},
				complete: function(data)
				{
					setTimeout(function(){
						form.find(".box-footer > img").remove();
					}, 300);
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
				form.find(".box-footer").append('<img src="'+img_loader+'" />');
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
					$(document).scrollTop(0);
				}, 300);
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
				}, 300);
			},
			complete: function(data)
			{
				setTimeout(function(){
					form.find(".box-footer > img").remove();
				}, 300);
			}
		});
		return false;
	});

	$(document).on('ifChecked','input[name=notifications_global]:radio',function(e){
		var id = $(this).attr('id');
		var type = $(this).val();
		var form = $('#notifications_global');
		dataString = form.serialize();
		
		$.ajax({
			type: form.attr('method'),
			url: form.attr('action'),
			data: form.serialize(),
			beforeSend: function(){
				form.find("#loading_"+id).append('<img src="'+img_loader+'" />');
			},
			success: function(data)
			{
				setTimeout(function(){
					form.find("#status_"+id).empty();
				}, 300);
			},
			error: function(data)
			{
				setTimeout(function(){
					form.find("#status_"+id).empty();
					form.find("#status_"+id).append('<i class="fa fa-times-circle text-warning"></i>');
				}, 300);
			},
			complete: function(data)
			{
				setTimeout(function(){
					form.find("#loading_"+id).empty();
				}, 300);
			}
		});
	});

	$(document).on('change','.notifications-level',function(e){
		var action = $(this).attr('name');
		var value = $(this).val();
		var main = $(this);

		$('#notifications_level_custom_fail').remove();
		main.parent().append('<img id="loading_notifications_level_custom" src="'+img_loader+'" />');

		$.post("/profile/notifications_level", { "action": action, "value": value })
		.fail(function() {
			setTimeout(function(){
				main.parent().append('<i id="notifications_level_custom_fail" class="fa fa-times-circle text-warning"></i>');
			}, 300);
		})
		.always(function() {
			setTimeout(function(){
				$('#loading_notifications_level_custom').remove();
			}, 300);
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

function notifications_global_iCheck (argument) {
	if (typeof $.fn.iCheck != 'undefined') {
		$("#r1, #r2").iCheck({
			checkboxClass: 'icheckbox_square-blue',
			radioClass: 'iradio_square-blue',
			increaseArea: '10%'
		});
	}
}
