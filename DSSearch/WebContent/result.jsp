<%@ page language="java" contentType="text/html; charset=ISO-8859-1"
	pageEncoding="ISO-8859-1"%>
<%
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
<script type="text/javascript">
	function previous_() {
		document.getElementById("command").value = "previous";
		document.getElementById("pagination").submit();
	}
	function top_() {
		document.getElementById("command").value = "top";
		document.getElementById("pagination").submit();
	}
	function next_() {
		document.getElementById("command").value = "next";
		document.getElementById("pagination").submit();
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
		</table>
	</center>
	<hr>
	<center>
		<form name="pagination" id="pagination" action="showresult" method="post">
			<input type="hidden" name="command" id="command"> 
		</form>
		<a href="javascript:previous_();">previous</a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
		<a href="javascript:top_();">top</a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 
		<a href="javascript:next_();">next</a>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 
		<a href="<%=request.getContextPath()%>">(new search)</a>
	</center>
</body>
</html>