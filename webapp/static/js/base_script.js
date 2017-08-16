// script for base.html

$(document).ready(function() {

	// Assign base url to document
	var base_url = document.location.origin;
	$('base').href = base_url;

	/* Navbar functionality: if user clicks any navbar element other
	than 'GitHub', page-specific content will fade out and a new
	page will be loaded. Otherwise, the linked GitHub page will
	open in a new tab. */
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