$(document).ready(function() {
	$('a').click(function(event) {
		event.preventDefault();
		var href = this.href;

		if (href.search("github") > -1) {
			window.open(href, '_blank');
		}
		else {
			$('.flash').fadeOut(1000, function() {
				window.location = href;
			});
		}	
	});

	$('#footer').hide().fadeIn(6000);
});