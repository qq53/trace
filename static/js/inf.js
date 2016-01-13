	$('.input-text').keydown(function(e){
		s = $(this);
		if( e.which == 13){
		$.post("syn_trace",
		{
			data:s.children('input').val()
		},
		function(data,status){
			//alert("Data: " + data + "\nStatus: " + status);
			s.append('<div class="input-text"><input></input></div>');
			var inputLast = $(".input-text input").length - 1;
			$(".input-text input")[inputLast].focus();
		});
	}else if( e.ctrlKey && e.which == 67){
		console.log('exit');
	}
});

$('#termin-toggle').click(function(e){
	$('#terminator')[0].classList.remove('termin-hidden');
	$('#termin-toggle')[0].classList.add('termin-toggle-hidden');
	e.stopPropagation();
});

$('#tab4').click(function(e){
	if( this.classList.contains('tab-show') ){
		$('#terminator')[0].classList.add('termin-hidden');
		$('#termin-toggle')[0].classList.remove('termin-toggle-hidden');
	}
});

$('.input-text input').click(function(e){
	e.stopPropagation();
});
