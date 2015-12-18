$('.input-text').keydown(function(e){
	if( e.which == 13){
		$(this).append('<div class="input-text"><input></input></div>');
		var inputLast = $(".input-text input").length - 1;
		$(".input-text input")[inputLast].focus();
	}else if( e.ctrlKey && e.which == 67){
		console.log('exit');
	}
});

$('#terminator').click(function(e){
	this.classList.remove('termin-hidden');
	e.stopPropagation();
});

$('#tab4').click(function(){
	if( this.classList.contains('tab-show') )
		$('#terminator')[0].classList.add('termin-hidden');
});