function display_training_samples(update, rating, n_samples=10) {
	$.getJSON('http://localhost:5000/challenge/get_training/', {rating: rating, n_samples: n_samples}, function(data) {
		var samples = data.training_samples;
		for (var i = 0; i < samples.length; i++) {
			update.append('<li>' + samples[i] + '</li>');
		}
		//update.append(samples);
	});
}

$(document).ready(function() {
	display_training_samples($('#nonoffensive .container-tweets'), 0);
	display_training_samples($('#offensive .container-tweets'), 1);
	display_training_samples($('#hatespeech .container-tweets'), 2);
});