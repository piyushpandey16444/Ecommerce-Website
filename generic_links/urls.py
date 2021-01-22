from django.urls import path
from . import views

urlpatterns = [
    path("company/", views.company, name="company"),
    path("contactus/", views.contactus, name="contactus"),
    path("category/<int:id>", views.homevideo, name="homevideo"),
    path("category/<int:id>", views.slidersdetails, name="slidersdetails"),
    path("category/<int:id>", views.advertisedetails, name="advertisedetails"),
    path("privacypolicy/", views.privacypolicy, name="privacypolicy"),
    path("disclaimer/", views.disclaimer, name="disclaimer"),
    path("termsconditions/", views.termsconditions, name="termsconditions"),
    path("faq/", views.faq, name="faq"),
    path("testimonials", views.testimonials, name="testimonials"),
]