// script for index.html

$(document).ready(function() {

	// fade-in form field and buttons
	$('.form-box').hide().fadeIn(2000);

	// upon submission, rate the input tweet and prepend result to <div class='reults'>
	$('#submit').click(function(event) {
		$('.results').show();

		// get raw tweet text from input field
		var new_tweet = $('input[name=tweet]').val();

		/* pass tweet to predict() function in main.py and get back JSON
		with prediction string and numerical rating */
		$.getJSON('/predict/', {tweet: new_tweet}, function(data) {
			var prediction = data.prediction;
			var rating = data.rating;

			// panel color determined by rating
			if (rating == 0) {
				result = "<div class='panel-transparent panel-success'>";
			}
			else if (rating == 1) {
				result = "<div class='panel-transparent panel-warning'>";
			}
			else {
				result = "<div class='panel-transparent panel-danger'>";
			}

			// within panel, add raw input text and model's prediction
			result = result +
				"<div class='panel-body'>"+new_tweet+"</div>" + 
				"<div class='panel-footer'>"+prediction+"</div>" + 
				"</div>"

			/* prepend panel to <div class='results'> so most recent
			submissions appear first */
			$(result).prependTo('.results').hide().slideDown(1000);
		});

		//empty form after submission and prevent page reload
		$('form')[0].reset();
		event.preventDefault();
	});

	// clear <div class='results'>
	$('#clear').click(function(event) {
		$('.results').hide('drop', {direction: 'down'}, 1000, function(event) {
			$('.results').empty();
		});
		event.preventDefault();
	});
});

