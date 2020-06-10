from django.urls import path
from django.views.generic.detail import DetailView
from django.views.generic import TemplateView
from main import models
from . import views


app_name='main'

urlpatterns = [
    path('',TemplateView.as_view(template_name='main/home.html'),name='home'),
    path('about-us/',TemplateView.as_view(template_name='main/about_us.html'),name='about_us'),
    path('contact-us/',views.ContactPageView.as_view(),name='contact_us'),
    path('productos/<slug:tag>/',views.ProductoListView.as_view(),name='productos'),
    path("producto/<slug:slug>/",DetailView.as_view(model=models.Producto),name="producto",),
    path('signup/', views.Signup_view.as_view(), name="signup"),
    path('login/',views.LoginView.as_view(),name='login'),
    path('logout/', views.Logout_view.as_view(), name="logout"),
    path('direccion/',views.DireccionListView.as_view(),name='direcciones_list'),
    path('direccion/<int:pk>/',views.DireccionUptadeView.as_view(),name='direccion_update'),
    path('direccion/<int:pk>/delelete/',views.DeleteDireccion.as_view(),name='confirm_delete'),
    path('direccion/create/',views.DireccionCreateView.as_view(),name='direccion_create')
]
