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

function bind_arglens_select(){
	$('.container .arg-lens').change(function(){
		var l = this.value;
		var len = $(this).parent().find('.arg-list ul li').length;
		
		if ( len < l )
			//add
			$(this).parent().find('.arg-list ul').append('\
				<li>\
					<input class="format" type="text" placeholder="输出格式: %d"/>\
					<select>\
						<option select="selected">处理函数</option>\
						<option value="htol">htol</option>\
					</select>\
				</li>\
			'.repeat(l-len));
		else{
			//remove
			if ( l == 0)
				$(this).parent().find('.arg-list ul li').remove();
			else
				$(this).parent().find('.arg-list ul li:gt('+(l-1)+')').remove();
		}
	});
}

function bind_condcheck(){
	$('.container .settings .cond-check').click(function(){
		if (this.checked){
			$(this).nextAll('#cond-add,.cond-list').show();
		}else{
			$(this).nextAll('#cond-add,.cond-list').hide();
		}
	});
}

$('.container .arg-check').click(function(){
	if (this.checked){
		if ( $(this).nextAll('.settings') ){
			$(this).next('label').after('\
				<div class="settings">\
					<label class="arg-label arg-label-len second">参数个数</label>\
					<select class="arg-lens">\
						<option value="0" select="selected">-</option>\
						<option value="1" >1</option>\
						<option value="2" >2</option>\
					</select>\
					<div class="arg-list">\
						<ul>\
						</ul>\
					</div>\
					<label class="arg-label second">条件跟踪</label><input type="checkbox" value="cond" id="cond-check" class="cond-check">\
					<ul class="cond-list">\
						<li>\
							<select>\
								<option value="0" select="selected">-</option>\
								<option value="1" >参数一</option>\
								<option value="2" >参数二</option>\
							</select>\
							<input type="text" placeholder="例如: == >= <=" class="cond-list-assign" />\
							<input class="cond-list-value" type="text" placeholder="数值或变量" />\
						</li>\
					</ul>\
					<button type="button" class="btn am-btn am-btn-default" id="cond-confirm">确定</button>\
				</div>\
			');
			bind_arglens_select();
			bind_condcheck();
			bind_cond_var();
		}else{
			if ( $(this).nextAll('.settings') )
				$(this).nextAll('.settings').show();
		}
	}else{
		if ( $(this).nextAll('.settings') )
			$(this).nextAll('.settings').hide();
	}
});

function bind_cond_var(){
	function finish(s){
		var p = s.parent();
		var f = p.find('select').val()!=0 && p.find('.cond-list-assign').val()!='' && p.find('.cond-list-value').val()!= '';
		if ( f ){
			s.unbind();
			p.find('.cond-list-assign').unbind();
			p.find('.cond-list-value').unbind();
			p.after('\
				<li>\
					<select>\
						<option value="0" select="selected">-</option>\
						<option value="1" >参数一</option>\
						<option value="2" >参数二</option>\
					</select>\
					<input type="text" placeholder="例如: == >= <=" class="cond-list-assign" />\
					<input class="cond-list-value" type="text" placeholder="数值或变量" />\
				</li>\
			');
			var u = p.next();
			u.find('select').blur(function(){finish($(this))});
			u.find('.cond-list-assign').blur(function(){finish($(this))});
			u.find('.cond-list-value').blur(function(){finish($(this))});
		}
	}
	$('.cond-list li select').blur(function(){finish($(this))});
	$('.cond-list-assign').blur(function(){finish($(this))});
	$('.cond-list-value').blur(function(){finish($(this))});
}