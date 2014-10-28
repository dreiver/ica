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
						form.find(".form-group").addClass('has-success');
						form.find(".box-footer > img").remove();
						form.find("#private_token").val( data );
						//form.find(".form-group").append("<label class='control-label' for='inputSuccess'><i class='fa fa-check'></i> Token updated</label>");
					}, 500);
					/*$.pjax({
						timeout: 2000,
						url: data.url,
						container: '#main-content'
					});*/
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
