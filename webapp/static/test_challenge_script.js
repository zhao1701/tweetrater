function display_training_samples(update, rating, n_samples=10) {
	$.getJSON('http://localhost:5000/challenge/get_training/', {rating: rating, n_samples: n_samples}, function(data) {
		$(update).empty();
		var samples = data.training_samples;
		for (var i = 0; i < samples.length; i++) {
			update.append('<li>' + samples[i] + '</li>');
		}
	});
}

function display_test_tweets(n_tweets=20) {
	$.getJSON('http://localhost:5000/challenge/get_test/', {n_tweets: n_tweets}, function(data) {
		var new_tweets = data.test_tweets;
		$update = $('form .container-tweets');

		var label_buttons = 
		"<div class = 'answer-choices'>" +
			"<input type='radio' name='user-label-{}' value='0'>INOFFENSIVE</input>" + 
			"<input type='radio' name='user-label-{}' value='1'>OFFENSIVE</input>" +	
			"<input type='radio' name='user-label-{}' value='2'>HATE SPEECH</input>" +
		"</div>";

		for (var i = 0; i < new_tweets.length; i++) {
			var label_buttons_new = label_buttons.replace(/{}/g, String(i));
			$update.append('<li>'+new_tweets[i]+label_buttons_new+'</li>');
		}
	});
}

$(document).ready(function() {
	display_training_samples($('#inoffensive .container-tweets'), 0);
	display_training_samples($('#offensive .container-tweets'), 1);
	display_training_samples($('#hatespeech .container-tweets'), 2);

	display_test_tweets(20);

	$('.more-examples').click(function() {
		$update = $(this).next();
		$rating = Number($(this).parent().data('rating'));
		display_training_samples($update, $rating);
	});

	$('.container-test > .more-examples').click(function() {
		display_test_tweets(10);
	});
});