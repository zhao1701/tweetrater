$(document).ready(function() {
	$('#submit').click(function(event) {
		var new_message = $('input[name=entry]').val();
		$.getJSON('http://localhost:5000/upper/', {text: new_message}, function(data) {
			var caps_message = data.uppertext;
			$('.messages').prepend('<br/>');
			$('.messages').prepend(caps_message);
			$('.messages').prepend('<br/>');
			$('.messages').prepend(new_message);
		});
		event.preventDefault();
	});

	$('#clear').click(function(event) {
		$('.messages').empty();
		event.preventDefault();
	})
});