var running = false;

$('.input-text').keydown(function(e){
	s = $(this);
	if( e.which == 13){
		if(running == false){
			alert("not running");
			return;
		}
		$.post("/input",
		{
			data:s.children('input').val()
		},
		function(data,status){
			//alert("Data: " + data + "\nStatus: " + status);
			s.append('<div class="input-text"><input></input></div>');
			var inputLast = $(".input-text input").length - 1;
			$(".input-text input")[inputLast].focus();
		});
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

$('#terminator').click(function(e){
	e.stopPropagation();
});

$('#state').click(function(){
	t = this;
	if(t.className == 'start'){
		$.get("http://"+location.hostname+":81/start",{},
		function(data,status){
			//setTimeout("getout()",500);
		});
		t.className = 'stop';
	}else{
		$.get("/stop",{},
		function(data,status){
			t.className = 'start';
		});
	}
});

function getout(){
	$.get("/running",{},
	function(data,status){
		if(data.substring(0,3) == 'not'){
			$('#state')[0].className = 'start';
		}else{
			setTimeout("getout()",500);
		}
	});
}
