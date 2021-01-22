{% extends "mail_templated/base.tpl" %}
{% block subject %} {{ subject }}{% endblock %}
{% block html %} 
{% load static %}

	<table align="center" cellpadding="0" cellspacing="0" class="table-main" style="width: 700px; background: #ffffff; border: 1px solid #cccccc;">
		<tr>
			<td height="5" colspan="2" bgcolor="#3f2aae"></td>
		</tr>
		<tr>
			<td height="80" colspan="2" align="center" valign="middle">
				<img src='{{ BASE_URL }}{% static "images/hoitymoppet-logo.png" %}' alt="hoitymoppet" />
			</td>
		</tr>
		<tr>
			<td height="5" colspan="2" align="center" valign="middle" bgcolor="#f0f0f0"></td>
		</tr>
		<tr>
			<td colspan="2" style="font-size:16px; font-weight:bold; text-align: left; vertical-align: middle; height: 40px;">
				    Hello {{ name }}
			</td>
		</tr>
		<tr>
			<td colspan="2" style="font-size:16px; font-weight:bold; text-align: left; vertical-align: middle; height: 30px; background: #f6f6f6;">
                {% if description %}
                    {{ description.email_description }}
                {% else %}
                    Thanks, your order is placed.
                {% endif %}

			<hr></td>
		</tr>

		<tr style="padding: 5px 15px 5px 15px;">
			<td width="50%" style="padding: 5px 15px 5px 15px;color:#3f2aae; font-weight:bold; text-align: left; vertical-align: middle;">
				Order ID : {{ generated_order.ref_code }}
				{% if ship_charges %}
				<br>
				Shipping Charge : {{ ship_charges }}
				{% endif %}
				<br>
				{% if price_total %}
				Total Price : {{ price_total }}
				{% endif %}
			</td>
			<td width="50%" style="padding: 5px 15px 5px 15px; color:#3f2aae; font-weight:bold;
			text-align: center; vertical-align: middle;">
				Placed on : {{ placed_on }}
				<br>
				Expected in : {{ generated_order.expected_delivery_days }} days
			</td>
		</tr>
		<tr>
			<td colspan="2"><hr></td>
		</tr>

		<tr style="padding: 5px 15px 5px 15px;">
			<td colspan="2" style="font-size:16px; font-weight:bold; text-align: center; vertical-align: middle; height: 30px; background: #f6f6f6;">
				Order Details
			</td>
		</tr>
		<tr>
			<td colspan="2" style="padding: 5px 15px 5px 15px;">
				<table width="100%" border="0" cellpadding="0" cellspacing="0" class="table">
					<thead class="thead-dark" style="">
                        <tr>
                            <th style="color: #ffffff; background-color: #343a40; border-color: #454d55; padding: 10px; font-weight: normal; font-size: 13px; text-align: left;">Image</th>
                            <th style="color: #ffffff; background-color: #343a40; border-color: #454d55; padding: 10px; font-weight: normal; font-size: 13px;">Product / Quantity</th>
                            <th style="color: #ffffff; background-color: #343a40; border-color: #454d55; padding: 10px; font-weight: normal; font-size: 13px;">Size / Color / Custom Size</th>
                            <th style="color: #ffffff; background-color: #343a40; border-color: #454d55; padding: 10px; font-weight: normal; font-size: 13px; text-align: right;">Unit Price</th>
                            <th style="color: #ffffff; background-color: #343a40; border-color: #454d55; padding: 10px; font-weight: normal; font-size: 13px; text-align: right;">Total</th>
                        </tr>
                    </thead>
                    <tbody>
                    {% for order_detail in generated_order_detail_list %}
                    	<tr>
                    		<td style="padding: 5px 15px 5px 15px; font-weight: normal; font-size: 13px;">
                    			<img src='{{ BASE_URL }}{{ order_detail.product_id.productimage.url }}' style="height: 100px; height: 100pt; width: auto;" alt="product image" />
                    		</td>
                    		<td style="padding: 5px 15px 5px 15px; font-weight: normal; font-size: 13px;">
                    			{{ order_detail.product_id }}<br>
                    			Qty : {{ order_detail.quantity }}
                    		</td>
                    		<td style="padding: 5px 15px 5px 15px; font-weight: normal; font-size: 13px;">
                    			{{ order_detail.product_age }}
                    			<br>
                    			{% if order_detail.prod_color %}
                    			Color: <div style="background: {{ order_detail.prod_color }}; width: 12px; height: 12px; margin-right: 5px; display: inline-block; border-radius: 100px;"></div>
                    			{% endif %}
                    			<br>
                    			{% if order_detail.user_custom_size_master %}
                    			{{ order_detail.user_custom_size_master }}
                    			{% endif %}
                    		</td>
                    		<td style="padding: 5px 15px 5px 15px; text-align: right; padding-left: 50px; font-weight: normal;font-size: 13px;">
                    				<i class="fa fa-rupee-sign"></i> {{ order_detail.price }}
                    		</td>

                    		<td style="padding: 5px 15px 5px 15px; text-align: right; padding-left: 50px; font-weight: normal;font-size: 13px;">
                    				<i class="fa fa-rupee-sign"></i> {{ order_detail.total_price }}
                    		</td>
                    	</tr>
                    	{% endfor %}
                       	<tr style="background: #f6f6f6;">
                    		<td colspan="4" style="font-size: 12px; font-weight: normal; text-align: right; padding: 15px;">
                    			<p style="font-weight: bold; font-size: 13px;">Shipping Address :-</p>
                    			<td>
                                    <p>
                                        <span>{{ address.name }} | Mob. - {{ address.mobile_no }}</span><br>
                                        <span>{{ address.address }}, {{ address.user_state }}, {{ address.city }}, {{ address.user_country }} - {{ address.pincode }}</span><br>
                                        {% if address.locality %}
                                        <span>Locality - {{ address.locality }},</span>
                                        {% endif %}
                                        {% if address.alternate_no %} 
                                        <span>Alternate No. - {{ address.alternate_no }}</span>
                                        {% endif %}
                                    </p>
                                </td>
                    		</td>
                    	</tr> 
                    </tbody>
				</table>
			</td>
		</tr>
		<tr style="padding: 5px 15px 5px 15px;">
			<td colspan="2" bgcolor="#3f2aae" style="padding: 5px 15px 5px 15px; color:#ffffff;">
				<p style="font-size:16px; font-weight:normal; text-align: left; vertical-align: middle; color: #ffffff;">
					We look forward to seeing you again soon.<br />
					<span style="padding: 5px 15px 5px 15px; font-size:14px; font-weight:normal; text-align: left; vertical-align: middle; color: #ffffff;">
					Team Hoitymoppet</span>
				</p>
				<p class="light-txt" style="padding: 5px 15px 5px 15px; font-size: 14px; opacity: 0.7; text-align: left; vertical-align: middle; color: #ffffff;">
					Please note : Do not respond to any Phone call/Email/SMS claiming to offer rewards/lucky draw prizes on behalf of Hoitymoppet. We NEVER request our customers for unsolicited financial information or advance payments in exchange of rewards. All our offers are available ONLY on our website and app.
				</p>
				<p style="padding: 5px 15px 5px 15px; color: #8e8e8e;">
					<a href="https://www.facebook.com/hoitymoppet-109901973994632/" target="_blank">
						<img src="http://hoitymoppet.com:9000/static/images/facebook.png" alt="facebook" />
					</a>&nbsp;
					<a href="https://instagram.com/hoitymoppet?igshid=6aafbed8n5mv" target="_blank">
						<img src="http://hoitymoppet.com:9000/static/images/instagram.png" alt="instagram" />
					</a>
				</p>
			</td>
		</tr>
	</table>
{% endblock %}