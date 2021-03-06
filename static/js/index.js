$(document).ready(function(){
	$('html').keydown(function(event){
		if (event.which == 27){
			$('#file-name').val('');
			$('#upbtn').text('选择样本');
			$('#upbtn').attr('class','am-btn am-btn-default');
			$('#upbtn').attr('onclick','fileToUpload.click()');
			$('#fileToUpload').val('');
		}
	});
	$('#file-name').val('')
});

function fileSelected() {
    var file = $('#fileToUpload')[0].files[0];
    if (file){
		$('#file-name').val(file.name);
		$('#upbtn').text('上传样本');
		$('#upbtn').attr('class','am-btn am-btn-secondary');
		$('#upbtn').attr('onclick','uploadFile()');
	}
}

function uploadFile() {
    var fd = new FormData();
    fd.append("fileToUpload", document.getElementById('fileToUpload').files[0]);
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "http://"+location.hostname+":81/");
    xhr.send(fd);
    var xhr = new XMLHttpRequest();
    xhr.upload.addEventListener("progress", uploadProgress, false);
    xhr.addEventListener("load", uploadComplete, false);
    xhr.addEventListener("error", uploadFailed, false);
    xhr.addEventListener("abort", uploadCanceled, false);
    xhr.open("POST", "/");
    xhr.send(fd);
}

function uploadProgress(evt) {
    if (evt.lengthComputable) {
        var percentComplete = Math.round(evt.loaded * 100 / evt.total);
        document.getElementById('progressNumber').innerHTML = percentComplete.toString() + '%';
    }
    else {
        document.getElementById('progressNumber').innerHTML = 'unable to compute';
    }
}

function uploadComplete(evt) {
	function post(URL, PARAMS) {      
		var temp = document.createElement("form");      
		temp.action = URL;      
		temp.method = "post";      
		temp.style.display = "none";      
		for (var x in PARAMS) {      
			var opt = document.createElement("textarea");      
			opt.name = x;      
			opt.value = PARAMS[x];  
			temp.appendChild(opt);      
		}      
		document.body.appendChild(temp);      
		temp.submit();      
		return temp;      
	}   
	var resText = evt.target.responseText;
	if( resText.substring(0,5) == 'false' )
		alert('非ELF文件');
	else
		post('inf', {'data': evt.target.responseText});
}

function uploadFailed(evt) {
    alert("There was an error attempting to upload the file.");
}

function uploadCanceled(evt) {
    alert("The upload has been canceled by the user or the browser dropped the connection.");
}
