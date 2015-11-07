<%@ page language="java" contentType="text/html; charset=ISO-8859-1"
	pageEncoding="ISO-8859-1"%>
<%
	// 
	// TODO Retirar esse trecho
	java.util.List<dssearch.model.Entry> result_temp = null;
	result_temp = new java.util.ArrayList<dssearch.model.Entry>();
	dssearch.model.Entry entry = new dssearch.model.Entry();
	entry.url = "http://datahub.io/dataset/rkb-explorer-acm";
	entry.name = "Association for Computing Machinery (ACM) (RKBExplorer)";
	entry.description = "Linked Data version of publications of the Association for Computing Machinery (ACM), along with details of their authors.";
	result_temp.add(entry);
	request.getSession().setAttribute("result", result_temp);
	request.getSession().setAttribute("limit", 10);
	request.getSession().setAttribute("offset", 0);
	//
	java.util.List<dssearch.model.Entry> result = (java.util.List<dssearch.model.Entry>) request.getSession()
			.getAttribute("result");
	int limit = (Integer) request.getSession().getAttribute("limit");
	int offset = (Integer) request.getSession().getAttribute("offset");
%>
<%!public String getRows(java.util.List<dssearch.model.Entry> result, int limit, int offset) {
		String rows = "";
		int count = 0;
		for (int i = offset; i < result.size() && count < limit; i++) {
			dssearch.model.Entry e = result.get(i);
			rows += "<tr>";
			rows += "<td>";
			rows += "<a href=\"" + e.url + "\">" + e.name + "</a>" + ": " + e.description;
			rows += "</td>";
			rows += "</tr>";
			count++;
		}
		return rows;
	}%>
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
<head>
<script>
	function previous() {
		var command = document.getElementById('command');
		command.value = "previous";
		document.pagination.submit();
	}
	function top() {
		var command = document.getElementById('command');
		command.value = "top";
		document.pagination.submit();
	}
	function next() {
		var command = document.getElementById('command');
		command.value = "next";
		document.pagination.submit();
	}
	function newSearch() {
		var command = document.getElementById('command');
		command.value = "newSearch";
		document.pagination.submit();
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
		<table width="80%">
			<%=getRows(result, limit, offset)%>
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
		<form name="pagination" action="" method="post">
			<input type="hidden" name="command" id="command"> <a
				href="javascript:previous();">previous</a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
			<a href="javascript:top();">top</a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <a
				href="javascript:next();">next</a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <a
				href="javascript:newSearch();">(new search)</a>
		</form>
	</center>
</body>
</html>