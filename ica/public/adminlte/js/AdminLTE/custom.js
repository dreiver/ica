$(function() {
	$( document ).ready(function() {
		$(document).pjax('a[data-pjax]', '#main-content')
		//$('a[data-pjax]').pjax()
	});

	$(document).on('submit','#profile_reset_private_token',function(e){
		// prevent native form submission here
		e.preventDefault();

		if ( ask() ) {

			var form = $('#profile_reset_private_token');
			dataString = form.serialize();
			
			$.ajax({
				type: $(this).attr('method'), // <-- get method of form
				url: $(this).attr('action'), // <-- get action of form
				data: $(this).serialize(), // <-- serialize all fields into a string
				beforeSend: function(){
					form.find(".box-footer").append('<img src="/adminlte/img/ajax-loader-custom.gif" />');
				},
				success: function(data)
				{
					setTimeout(function(){
						form.find("#private_token").val( data );
						form.find(".form-group").addClass('has-success');
						//form.find(".form-group").append("<label class='control-label'><i class='fa fa-check-circle'></i> Token updated</label>");
					}, 500);
				},
				error: function(data)
				{
					setTimeout(function(){
						form.find(".form-group").addClass('has-error');
						//form.find(".form-group").append("<label class='control-label'><i class='fa fa-times-circle'></i> There was an error</label>");
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

});


function ask() {
	q = confirm('Are you sure?');
	if (q)
		return true;
	else
		return false; 
}
