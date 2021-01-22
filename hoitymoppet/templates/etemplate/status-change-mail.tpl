{% extends "mail_templated/base.tpl" %}
{% block subject %} Order status changed{% endblock %}
{% block html %}
{% load static %}
<body style="height: 100%; font-family: sans-serif; backgroung: #11659e;">
	<table cellpadding="0" cellspacing="0" width="100%" style="border:1px solid #cccccc; background:#ececec; border-radius:5px;">
		<tr>
			<td style="padding:30px;">
				<h2 style="text-align:left;">
						Hi {{ details.user }}, Your order status is changed to {{ order.status_name }}
				</h2>
				<h4 style="text-align:left;">Order Id : {{ details.order_id }}</h4>
				<h4 style="text-align:left;">Order Date : {{ details.ordered_date }}</h4>
				<h4 style="text-align:left;">Product : {{ details.product_id }} </h4>
				<h4 style="text-align:left;">Product Size : {{ details.product_size }} </h4>
				<h4 style="text-align:left;">Total Price : {{ details.total_price }}/- </h4>
			</td>
		</tr>
	</table>
	<table style="margin-top:30px;">
		<tr>
			<td style="font-weight:bold;">
				We look forward to seeing you again soon.<br>
				Team Hoitymoppet
			</td>
		</tr>
	</table
</body>
{% endblock html %}