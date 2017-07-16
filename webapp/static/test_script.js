$(document).ready(function() {
	$('#submit').click(function(event) {
		var new_tweet = $('input[name=tweet]').val();

		var prediction = $.getJSON('http://localhost:5000/predict/', {tweet: new_tweet}, function(data) {
			var prediction = data.prediction;
			result = "<div class='result'>" + new_tweet + "<br/>" + prediction + "<br/></div>";
			$('.results').prepend(result);
		})
		$('form').children('input[name=tweet]').val('');
		event.preventDefault();
	});

	$('#clear').click(function(event) {
		$('.results').empty();
		event.preventDefault();
	})
});

