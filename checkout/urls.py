from django.urls import path
from checkout import views

urlpatterns = [
    path("", views.home, name="home"),
    path("payu_demo/", views.payu_demo, name="payu_demo"),
    path("checkout/success/", views.payu_success, name="payu_success"),
    path("checkout/failure/", views.payu_failure, name="payu_failure"),
]