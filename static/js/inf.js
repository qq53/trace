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
			$(this).nextAll('.cond-list').show();
		}else{
			$(this).nextAll('.cond-list').hide();
		}
	});
}

function bind_confirm(){
	$('.settings .cond-confirm').click(function(){
		var par = $(this).parents('.settings');
		var data = {};
		
		var arg_li = par.find('.arg-list ul li');
		data['args'] = []
		
		for(var i = 0; i < arg_li.length; ++i){
			data['args'].push({
				'format': $(arg_li[i]).find('.format').val(),
				'deal_func': $(arg_li[i]).find('select').val(),
			});
		}
		
		data['conds'] = []
		if( par.find('.cond-check')[0].checked ){
			var cond_li = par.find('.cond-list li');
			
			for(var i = 0; i < cond_li.length; ++i){
				data['conds'].push({
					'arg': $(cond_li[i]).find('select').val(),
					'assign': $(cond_li[i]).find('.cond-list-assign').val(),
					'value': $(cond_li[i]).find('.cond-list-value').val(),					
				});
			}
		}
		
		console.log(JSON.stringify(data));
		
	});
}

$('.container .arg-check').click(function(){
	if (this.checked){
		if ( $(this).nextAll('.settings') ){
			//default the left is 32 bit
			var sum = sum32;
			if ( $(this).parents('.half')[0].className.search('right') > 0 )
				sum = sum64;

			var preStr = '\
				<div class="settings">\
					<label class="arg-label arg-label-len second">参数个数</label>\
					<select class="arg-lens">\
						<option value="0" select="selected">-</option>';
			for( var i = 1; i <= sum; ++i )
				preStr += '<option value="'+i+'" >'+i+'</option>';
			
			var afterStr = '<select>\
							<option value="0" select="selected">-</option>';
			zhStr = '一二三四五六七八九';
			for( var i = 1; i <= sum; ++i )
				afterStr += '<option value="'+i+'" >参数'+zhStr[i-1]+'</option>';			
				
			$(this).next('label').after(preStr+'\
					</select>\
					<div class="arg-list">\
						<ul>\
						</ul>\
					</div>\
					<label class="arg-label second">条件跟踪</label><input type="checkbox" value="cond" class="cond-check">\
					<ul class="cond-list">\
						<li>'+
						afterStr+'\
							</select>\
							<input type="text" placeholder="例如: == >= <=" class="cond-list-assign" />\
							<input class="cond-list-value" type="text" placeholder="数值或变量" />\
						</li>\
					</ul>\
					<button type="button" class="btn am-btn am-btn-default cond-confirm">确定</button>\
				</div>\
			');
			bind_arglens_select();
			bind_condcheck();
			bind_cond_var();
			bind_confirm();
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
			p.find('select').unbind();
			p.find('.cond-list-assign').unbind();
			p.find('.cond-list-value').unbind();
			
			//default the left is 32 bit
			var sum = sum32;
			if ( $(s).parents('.half')[0].className.search('right') > 0 )
				sum = sum64;
			
			var afterStr = '<select>\
				<option value="0" select="selected">-</option>';
			zhStr = '一二三四五六七八九';
			for( var i = 1; i <= sum; ++i )
				afterStr += '<option value="'+i+'" >参数'+zhStr[i-1]+'</option>';
			
			p.after('\
				<li>\
					'+afterStr+'\
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

var sum32=5,sum64=6;
/*var sum32,sum64;

$.get("http://"+location.hostname+":80/get_args_sum",{},
function(data,status){
	if(data == ''){
	}else{
		var d = eval('('+data+')');
		sum32 = d['sum32'];
		sum64 = d['sum64'];
	}
});*/