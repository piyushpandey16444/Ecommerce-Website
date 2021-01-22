{% extends "mail_templated/base.tpl" %}
{% block subject %} {{ subject }} {% endblock %}
{% block html %} 
{% load static %}

<div style="background: #3f2aae;">
    <div style="background: #ffffff; background-image: url(/static/images/hoitymoppet-logo.png); background-size:cover; width:100%; height:14vh;">
        <img src='{{site}}{% static "images/hoitymoppet-logo.png" %}' alt="hoitymoppet" />
    </div>
    <center>
        <h1 style="text-align:cente; padding: 1% 1%; color:#ffffff;">
            Thank You ! Welcome To Hoitymoppet.
        </h1>
    </center>
    <strong>
        <p style="color:#ffffff; padding: 1% 2%; font-size: 15px;">
            Dear {{ user.username }}
        </p>
    </strong>
    <p style="color:#ffffff; padding: 1% 2%; font-size: 14px;">
    {% if description %}
        {{ description.email_description }}
    {% else %}
        Thank you for signing up with hoitymoppet.com. Hoitymoppet.com is leading luxury shopping online store for kids.Please click on below button for user verification.
    {% endif %}
    </p>
    <br><br>
    <center>
        <a href="http://{{ domain}}{% url 'activate' uidb64=uid token=token %}" style="font-size: 14px; background: #9bc225; border-radius: 5px; border: 1px solid #9bc225; padding: 13px 200px; font-weight: 600; text-decoration: none; color: #000000; text-transform: uppercase; box-shadow: 0 0 10px rgba(0,0,0,.2);">
            Confirm Your Registration
        </a> 
    </center>
    <p style="color:#ffffff; font-size: 14px; padding:1% 2%;">
        Warm Regards.<br />
        <span>Team Hoitymoppet</span>
    </p>  
</div>
{% endblock %}