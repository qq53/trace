var g_outLines = 0

$('.input').keydown(function(e){
	if( e.which == 13){
		var t = e.target;
		var s = $(this);
		var is = s.find("input");
		var l = is.length;
		if(t == is[l-1]){
			var d = "";
			s.find('input').each(function(){
				d += $(this).val() + '\n';	
			})
			$.post("http://"+location.hostname+":80/input",{data: d},
			function(data,status){
				setTimeout("get_trace_out()",300);
			});
			$.post("http://"+location.hostname+":81/input",{data: d},
			function(data,status){
				s.append('<div class="input-text"><input></input></div>');
				s.find("input")[l].focus();
				$('#state')[0].className = 'am-icon-spinner state-spin';
				setTimeout("get_out("+g_outLines+")",300);
			});
		}
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
	if(t.className == 'am-icon-play'){
		$.get("http://"+location.hostname+":80/start",{},
		function(data,status){
			setTimeout("get_trace_out()",300);
		});
		g_outLines = 0;
		$.get("http://"+location.hostname+":81/start",{},
		function(data,status){
			setTimeout("get_out("+g_outLines+")",300);
		});
		t.className = 'am-icon-spinner state-spin';
	}
});

function get_trace_out(){
	$.get("http://"+location.hostname+":80/getout",{},
	function(data,status){
		if(data == ''){
			$('#state')[0].className = 'am-icon-play';
		}else{
			$('#tab4 .container').append(data);
			setTimeout("get_trace_out()",300);
		}
	});
}

function get_out(n = 0){
	$.get("http://"+location.hostname+":81/getout?n="+n,{},
	function(data,status){
		if(data == ''){
		}else{
			var sl = data.split('\n');
			var r = sl.join('<br />');
			var s = $('#terminator .input');
			var l = s.find("input").length;
			var ns = s.find("input");
			g_outLines += sl.length - 1;
			if (g_outLines == 0)
				g_outLines = 1;
			$(ns[l-1]).parent().remove();
			s.append("<div>"+r+"</div>");
			s.append('<div class="input-text"><input></input></div>');
			ns[l-1].focus();
			setTimeout("get_out("+g_outLines+")",300);
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
						<option value="" select="selected">处理函数</option>\
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
				'func': $(arg_li[i]).find('select').val(),
			});
		}
		
		data['conds'] = []
		if( par.find('.cond-check')[0].checked ){
			var cond_li = par.find('.cond-list li');
			
			for(var i = 0; i < cond_li.length-1; ++i){
				data['conds'].push({
					'arg': $(cond_li[i]).find('select').val(),
					'assign': $(cond_li[i]).find('.cond-list-assign').val(),
					'value': $(cond_li[i]).find('.cond-list-value').val(),					
				});
			}
		}
			
		var bit = '32';
		if ( par.parents('.half')[0].className.search('right') > 0 )
			bit = '64';
		//POST DATA
		$.post("http://"+location.hostname+":80/set_config",{
			'args': JSON.stringify(data['args']),
			'conds': JSON.stringify(data['conds']),
			'name': par.parent().children('label').text(),
			'bit': bit
		},
		function(data,status){
			if(data == 'true'){
				alert('修改成功');
			}else{
				alert('修改失败');
			}
		});
		
	});
}

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
					<select class="cond-list-assign">\
						<option value="" select="selected">-</option>\
						<option value="==">==</option>\
						<option value="!=">!=</option>\
						<option value=">=">>=</option>\
						<option value="<="><=</option>\
					</select>\
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
		console.log(d);
		sum32 = d['sum32'];
		sum64 = d['sum64'];
	}
});*/

$.get("http://"+location.hostname+":80/get_config",{},
function(data,status){
	if(data == ''){
		console.log(sum32,sum64);
	}else{
		data = eval('('+data+')');
		for(var d in data){
			var s = d.split('_');
			var split_len = s.length;
			var bit = s[split_len-1];
			var name = d.substring(0,d.indexOf('_'+bit));
			var args_len = data[d].args.length;
			var sum;

			if ( bit == '32' ){
				sum = sum32;
				var t = $('.container .left:eq(1)').find('ul li label').filter(function(){return $(this).text()==name;})
			}else{
				sum = sum64;
				var t = $('.container .right:eq(1)').find('ul li label').filter(function(){return $(this).text()==name;})
			}
	
			//args length
			var setStr = `
				<div class="settings">
					<label class="arg-label arg-label-len">参数个数</label>
					<select class="arg-lens">
						<option value="0">-</option>`;
			for( var i = 1; i <= sum; ++i ){
				if ( i == args_len )
					setStr += '<option value="'+i+'" selected>'+i+'</option>';
				else
					setStr += '<option value="'+i+'" >'+i+'</option>';
			}
			setStr += `
					</select>
					<div class="arg-list">
						<ul>`;
			//list arg
			for(var i = 0; i < data[d].args.length; ++i){
				if ( data[d].args[i].func == '' )
					setStr += `
					<li>
						<input class="format" type="text" placeholder="输出格式: %d" value="`+data[d].args[i].format+`" />
						<select>
							<option value="" selected>处理函数</option>
							<option value="htol">htol</option>
						</select>
					</li>`;
				else
					setStr += `
					<li>
						<input class="format" type="text" placeholder="输出格式: %d" value="`+data[d].args[i].format+`" />
						<select>
							<option value="">处理函数</option>
							<option value="htol" selected>htol</option>
						</select>
					</li>`;
			}

			if ( data[d].conds.length > 0 )
				setStr += `
							</ul>
						</div>
						<label class="arg-label second">条件跟踪</label><input type="checkbox" value="cond" class="cond-check" checked>
						<ul class="cond-list">`;
			else
				setStr += `
							</ul>
						</div>
						<label class="arg-label second">条件跟踪</label><input type="checkbox" value="cond" class="cond-check">
						<ul class="cond-list">`;

			//list cond
			var zhStr = '一二三四五六七八九';
			for(var i = 0; i < data[d].conds.length; ++i){
				setStr += `
						<li>
							<select>
								<option value="0">-</option>`;
					for( var j = 1; j <= sum; ++j ){
						if ( data[d].conds[i].arg == j )
							setStr += '<option value="'+j+'" selected>参数'+zhStr[j-1]+'</option>';
						else
							setStr += '<option value="'+j+'">参数'+zhStr[j-1]+'</option>';
					}
				setStr += `
							</select>
							<select class="cond-list-assign">`;
				
				assign_arr = ['','==','!=','>=','<='];
				for(var j = 0; j < assign_arr.length; ++j){
					if( data[d].conds[i].assign == assign_arr[j] )
						setStr += '<option value="'+assign_arr[j]+'" selected>'+assign_arr[j]+'</option>';
					else
						setStr += '<option value="'+assign_arr[j]+'">'+assign_arr[j]+'</option>';
				}

				setStr += `
							</select>
							<input class="cond-list-value" type="text" placeholder="数值或变量" value="`+data[d].conds[i].value+`" />
						</li>`;
			}
			
			var afterStr = '';
			if( data[d].conds.length > 0){
				afterStr = `
							<li>
								<select>
								<option value="0" select="selected">-</option>`;
				for( var i = 1; i <= sum; ++i )
					afterStr += '<option value="'+i+'" >参数'+zhStr[i-1]+'</option>';
			}

			setStr += afterStr+`
							</select>\
							<select class="cond-list-assign">\
								<option value="" select="selected">-</option>\
								<option value="==">==</option>\
								<option value="!=">!=</option>\
								<option value=">=">>=</option>\
								<option value="<="><=</option>\
							</select>\
							<input class="cond-list-value" type="text" placeholder="数值或变量" />\
						</li>
					</ul>
					<button type="button" class="btn am-btn am-btn-default cond-confirm">确定</button>
				</div>`;

			t.after(setStr);
			t.next().hide();

			bind_arglens_select();
			bind_condcheck();
			bind_cond_var();
			bind_confirm();
		}
	}
});

$('.container .arg-check').click(function(){
	if (this.checked){
		if ( $(this).nextAll('.settings').length == 0 ){
			//default the left is 32 bit
			var sum = sum32;
			if ( $(this).parents('.half')[0].className.search('right') > 0 )
				sum = sum64;

			var preStr = `
				<div class="settings">
					<label class="arg-label arg-label-len">参数个数</label>
					<select class="arg-lens">
						<option value="0" select="selected">-</option>`;
			for( var i = 1; i <= sum; ++i )
				preStr += '<option value="'+i+'" >'+i+'</option>';
			
			var afterStr = `<select>
							<option value="0" select="selected">-</option>`;
			var zhStr = '一二三四五六七八九';
			for( var i = 1; i <= sum; ++i )
				afterStr += '<option value="'+i+'" >参数'+zhStr[i-1]+'</option>';			
				
			$(this).next('label').after(preStr+`
					</select>
					<div class="arg-list">
						<ul>
						</ul>
					</div>
					<label class="arg-label second">条件跟踪</label><input type="checkbox" value="cond" class="cond-check">
					<ul class="cond-list" style="display:none;">
						<li>`+
						afterStr+`
							</select>
							<select class="cond-list-assign">
								<option value="" select="selected">-</option>
								<option value="==">==</option>
								<option value="!=">!=</option>
								<option value=">=">>=</option>
								<option value="<="><=</option>
							</select>
							<input class="cond-list-value" type="text" placeholder="数值或变量" />
						</li>
					</ul>
					<button type="button" class="btn am-btn am-btn-default cond-confirm">确定</button>
				</div>
			`);
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

$('#refresh').click(function(){
	$.get("http://"+location.hostname+":80/refresh",{},
	function(data,status){
		if(data != ''){
			$('#tab4 .container').html('');
			$('#terminator .input-text:gt(0)').remove();
			$('#terminator .input-text').html('<input></input>');
		}
	});
});
