{% extends "mail_templated/base.tpl" %}
 {% block subject %} Activate your account{% endblock %} 
 {% block html %} 
 {% load static %}
<div style="background: #3f2aae;">
    <div style="background: #ffffff; background-image: url(/static/images/hoitymoppet-logo.png);background-size:cover; width:100%;height:14vh;">
        <img src='{{site}}{% static "images/hoitymoppet-logo.png" %}' alt="hoitymoppet" />
        
    </div>    
    <center><h1 style="text-align:cente;padding:1% 1%;color:#ffffff;">Thank You ! Welcome To Hoitymoppet.</h1></center>

   <strong>
    <p style="color:#ffffff;padding:1% 1%;font-size: 14px;">Dear {{ user.username }}</p>
    </strong>
	<p style="color:#ffffff;padding:1% 1%;font-size: 14px;">Thank you for signing up with hoitymoppet.com. Hoitymoppet.com is leading luxury shopping online store for kids.Please click on below button for user verification.</p><br><br>
    
    <center>
    <a href="http://{{ domain}}{% url 'activate' uidb64=uid token=token %}">
    <button style="font-size: 14px;padding:1%;color:black;height: 30px;background:#9bc225">
       <b> Confirm Your Registration</b>
    </button>  
    </a> 
    </center>        
    <p style="color:#ffffff;font-size: 14px;padding:1% 1%;">Warm Regards.<br /><span>Team Hoitymoppet</span></p>  
</div>
{% endblock %}