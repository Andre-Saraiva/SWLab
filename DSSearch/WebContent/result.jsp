<%@ page language="java" contentType="text/html; charset=ISO-8859-1"
	pageEncoding="ISO-8859-1"%>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<script>
	function previous() {
		var filename = document.getElementById('filename');
		filename.click();
	}
	function next() {
		var filename = document.getElementById('filename');
		filename.click();
	}
</script>
<meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1">
<title>Datasets</title>
</head>
<body>
	<center>
		<h1>Datasets</h1>
	</center>
	<br>
	<hr>
	<center>
		<table>
			<tr>
				<td><a href="http://datahub.io/dataset/rkb-explorer-acm">Association
						for Computing Machinery (ACM) (RKBExplorer)</a></td>
			</tr>
			<tr>
				<td>...</td>
			</tr>
			<tr>
				<td>...</td>
			</tr>
			<tr>
				<td>...</td>
			</tr>
			<tr>
				<td>...</td>
			</tr>
			<tr>
				<td>...</td>
			</tr>
		</table>
	</center>
	<hr>
	<center>
		<a href="javascript:previous();">previous</a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
		<a href="javascript:previous();">top</a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
		<a href="javascript:next();">next</a>
	</center>
</body>
</html>