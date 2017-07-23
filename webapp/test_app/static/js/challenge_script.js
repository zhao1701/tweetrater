function display_training_samples(update, rating, n_samples=10) {
	$.getJSON('/challenge/get_training/', {rating: rating, n_samples: n_samples}, function(data) {
		$(update).slideUp(1000, function() {
			$(update).empty();
			$(update).slideDown(1000);
			var samples = data.training_samples;
			for (var i = 0; i < samples.length; i++) {
				update.append("<li class='list-group-item'>" + samples[i] + '</li>');
			}
			$('.user-label').fadeIn(2000);
			$('h3').fadeIn(1000);
			$('.glyphicon').fadeIn(1000);
			$('.more-examples').fadeIn(1000);
		});
	});
}

function display_test_tweets(n_tweets=20) {
	$.getJSON('/challenge/get_test/', {n_tweets: n_tweets}, function(data) {
		var new_tweets = data.test_tweets;
		$update = $('form .container-tweets');

		var label_buttons = 
		"<div class='btn-group answer-choices' data-toggle='buttons'>" +
			"<label class='btn btn-success active'>" +
				"<input type='radio' name='user-label-{}' value='0' checked>" +
					" <span class='glyphicon glyphicon-ok-sign'></span>" + 
				"</input>" + 
			"</label>" +
			"<label class='btn btn-warning'>" +
				"<input type='radio' name='user-label-{}' value='1'>" + 
					" <span class='glyphicon glyphicon-exclamation-sign'></span>" +
				"</input>" +	
			"</label>" +
			"<label class='btn btn-danger'>" +
				"<input type='radio' name='user-label-{}' value='2'>" + 
					" <span class='glyphicon glyphicon-remove-sign'></span>" +
				"</input>" +
			"</label>"
		"</div>";

		for (var i = 0; i < new_tweets.length; i++) {
			var label_buttons_new = label_buttons.replace(/{}/g, String(i));
			$update.append("<li class='list-group-item'>" +
				"<div class='tweet-box'>" +
					new_tweets[i] +
				"</div>" +
				label_buttons_new +
				'</li>');
		}

		$('.answer-choices .btn').click(function() {
			$(this).addClass('active');
			$(this).siblings().removeClass('active');
			var rating = Number($(this).find('input').attr('value'));
			if (rating == 0) {
				$(this).parent().parent().animate({backgroundColor: 'hsla(102, 50%, 95%, 0.95)'}, 1000);
			}
			else if (rating == 1) {
				$(this).parent().parent().animate({backgroundColor:'hsla(50, 80%, 95%, 0.95)'}, 1000);
			}
			else {
				$(this).parent().parent().animate({backgroundColor: 'hsla(0, 40%, 95%, 0.95)'}, 1000);
			}
		});
	});
}

$(document).ready(function() {

	$('.instructions').hide().fadeIn(2000);
	$('.user-label').hide();
	$('h3').hide();
	$('.glyphicon').hide();
	$('.more-examples').hide();

	display_training_samples($('#inoffensive .list-group'), 0);
	display_training_samples($('#offensive .list-group'), 1);
	display_training_samples($('#hatespeech .list-group'), 2);

	display_test_tweets(20);

	$('.more-examples').click(function() {
		$update = $(this).next();
		$rating = Number($(this).parent().data('rating'));
		display_training_samples($update, $rating);
	});
});