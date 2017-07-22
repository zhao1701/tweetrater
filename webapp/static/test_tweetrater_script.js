$(document).ready(function() {
	$('.form-box').hide().fadeIn(2000);

	$('#submit').click(function(event) {
		$('.results').show();
		var new_tweet = $('input[name=tweet]').val();

		$.getJSON('http://localhost:5000/predict/', {tweet: new_tweet}, function(data) {
			var prediction = data.prediction;
			var rating = data.rating;
			// result = "<div class='result'>" + new_tweet + "<br/>" + prediction + "<br/></div>";

			if (rating == 0) {
				result = "<div class='panel-transparent panel-success'>";
			}
			else if (rating == 1) {
				result = "<div class='panel-transparent panel-warning'>";
			}
			else {
				result = "<div class='panel-transparent panel-danger'>";
			}

			result = result +
				"<div class='panel-body'>"+new_tweet+"</div>" + 
				"<div class='panel-footer'>"+prediction+"</div>" + 
				"</div>"

			$(result).prependTo('.results').hide().slideDown(1000);
			// $('.results').prepend(result);
		});
		$('form')[0].reset();
		event.preventDefault();
	});

	$('#clear').click(function(event) {
		$('.results').hide('drop', {direction: 'down'}, 1000, function(event) {
			$('.results').empty();
		});
		event.preventDefault();
	});
});

