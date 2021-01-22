{% extends "mail_templated/base.tpl" %}
{% block subject %} {{ subject }}{% endblock %}
{% block html %} 
{% load static %}
	<table align="center" cellpadding="0" cellspacing="0" class="table-main" style="width: 700px; background: #ffffff; border: 1px solid #cccccc;">
		<tr>
			<td height="5" bgcolor="#3f2aae"></td>
		</tr>
		<tr style="padding: 5px 15px 5px 15px;">
			<td style="font-size:16px; font-weight:bold; text-align: center; vertical-align: middle; height: 30px; background: #f6f6f6;">
				Query Details
			</td>
		</tr>
		<tr>
			<td style="padding: 5px 15px 5px 15px;">
				User Name : {{ user }}
				<hr>
				User Email : {{ user_email }}
				<hr>
				Query Type : {{ order_id }}
				<hr>
				Query Summary : {{ query_summary }}
				<hr>
				Query Details : {{ query_details }}
			</td>
		</tr>
	</table>
{% endblock %}