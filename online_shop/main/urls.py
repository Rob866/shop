from django.urls import path
from django.views.generic import TemplateView
from . import views


app_name='main'

urlpatterns = [
    path('',TemplateView.as_view(template_name='main/home.html'),name='home'),
    path('about-us/',TemplateView.as_view(template_name='main/about_us.html'),name='about_us'),
    path('contact-us/',views.ContactPageView.as_view(),name='contact_us')
]
