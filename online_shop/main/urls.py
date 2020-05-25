from django.urls import path
from . import views

app_name='main'

urlpatterns = [
    path('',views.home,name='home'),
    path('about-us/',views.about_us,name='about_us'),
    path('contact-us/',views.ContactPageView.as_view(),name='contact_us')
]
