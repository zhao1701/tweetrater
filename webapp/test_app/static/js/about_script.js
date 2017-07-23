$(document).ready(function() {
	$('.section').hide().show('drop', 2000);
	$('.col-sm-6').hide().fadeIn(3000);
	$('.navbar').click(function() {
		$('col-sm-6').fadeOut(3000);
	});
});