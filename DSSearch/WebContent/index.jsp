<%@ page language="java" contentType="text/html; charset=ISO-8859-1"
	pageEncoding="ISO-8859-1"%>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<script type="text/javascript">
	function selectFile() {
		var filename = document.getElementById('filename');
		filename.click();
	}
	function setURL(){
		var filename = document.getElementById('filename');
		var url = document.getElementById('url');
		var void_ = document.getElementById('void');
		url.value = "file:///".concat(filename.value);
		if (window.File && window.FileReader && window.FileList && window.Blob) {
			var reader = new FileReader();
			reader.onload = function(e) {
				void_.value = reader.result;
	        	};
	    	reader.readAsText(filename.files[0]);
		} else {
			alert('The File APIs are not fully supported by your browser.');
		}
	}
</script>
<meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1">
<title>Dataset Search</title>
</head>
<body>
	<center>
		<h1>Dataset Search</h1>
	</center>
	<br>
	<br>
	<br>
	<center>
		<table>
			<tr align="center">
				<td>
					<img src="./img/LOD_Cloud_Diagram.png" alt="LOD Cloud Diagram" style="width: 404px; height: 228px;">
				</td>
			</tr>
			<tr>
				<td>
					<form name="search" action="newsearch" method="post">
						<input type="hidden" name="void" id="void"/>
						<input type="url" name="url" id="url" size="60" placeholder="void URL of the target dataset" />
						<input list="methods" name="method" value="colaborative" size="12" placeholder="method">
						<datalist id="methods">
    						<option value="colaborative" default>
    						<option value="similarity">
						</datalist>
						<input type="submit" value="Search"><br> 
					</form>
					<input type="file" id=filename style="display:none;" onchange="javascript:setURL();"> 
					<a href="javascript:selectFile();">local file</a>
				</td>
			</tr>
		</table>
	</center>
</body>
</html>