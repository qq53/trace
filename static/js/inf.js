$('.input-text').keydown(function(e){
	s = $(this);
	if( e.which == 13){
		if($('#state')[0].className == 'stop'){
			alert("running");
			return;
		}
		$.post("http://"+location.hostname+":81/input",
		{
			data:s.children('input').val()
		},
		function(data,status){
			//alert("Data: " + data + "\nStatus: " + status);
			s.append('<div class="input-text"><input></input></div>');
			var inputLast = $(".input-text input").length - 1;
			$(".input-text input")[inputLast].focus();
			$('#state')[0].className = 'stop';
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
		$.get("http://"+location.hostname+":80/start",{},
		function(data,status){
			//setTimeout("get_trace_out()",500);
			console.log(data)
		});
		$.get("http://"+location.hostname+":81/start",{},
		function(data,status){
			//setTimeout("get_out()",500);
			console.log(data)
		});
		t.className = 'stop';
	}else{
		$.get("http://"+location.hostname+":80/stop",{},
		function(data,status){
		});
		$.get("http://"+location.hostname+":81/stop",{},
		function(data,status){
		});
		t.className = 'start';
	}
});

function get_trace_out(){
	$.get("http://"+location.hostname+":80/getout",{},
	function(data,status){
		if(data == ''){
			$('#state')[0].className = 'start';
		}else{
			setTimeout("get_trace_out()",500);
		}
	});
}

function get_out(){
	$.get("http://"+location.hostname+":81/getout",{},
	function(data,status){
		if(data == ''){
			$('#state')[0].className = 'start';
		}else{
			setTimeout("get_out()",500);
		}
	});
}
