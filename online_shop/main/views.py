from django.views.generic import   (ListView,RedirectView)
from django.views.generic.edit import (FormView,CreateView,UpdateView,DeleteView,)

from django.shortcuts import render,get_object_or_404,redirect
from main import models
from main.forms import (ContactForm,SignUpForm,LoginAutentificationForm,UpdateViewForm)
import logging
from django.contrib.auth import login, authenticate,logout
from django.contrib import messages
logger = logging.getLogger(__name__)
from django.http import  HttpResponseRedirect
from django.urls import  reverse,reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

class ContactPageView(FormView):
    template_name= 'main/contact_form.html'
    form_class = ContactForm
    success_url = '/'

    def form_valid(self,form):
        form.send_mail()
        return super(ContactPageView, self).form_valid(form)


class ProductoListView(ListView):
    template_name = "main/producto_list.html"
    model= models.Producto
    paginate_by= 4

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['tag'] = self.kwargs['tag']
        return data

    def get_queryset(self):
        tag = self.kwargs['tag']
        self.tag = None
        queryset = super().get_queryset()

        if tag != 'all':
            self.tag = get_object_or_404(models.ProductoTag,slug=tag)

            if self.tag:
                productos = queryset.filter(activo=True).filter(tags=self.tag)

        else:
            productos = queryset.filter(activo=True)
        return productos.order_by('nombre')



class Logout_view(RedirectView):
    pattern_name = 'main:home'

    def get(self,request,*args,**kwargs):
        logout(request)
        return super(Logout_view,self).get(request,*args,**kwargs)


class Signup_view(FormView):
    template_name = "main/signup.html"
    form_class = SignUpForm

    def dispatch(self,request,*args,**kwargs):
        if request.user.is_authenticated:
            return redirect("/")
        else:
            return super(Signup_view,self).dispatch(request,*args,**kwargs)

    def get_success_url(self):
        return self.request.GET.get("next", "/")


    def form_valid(self, form):
        response = super().form_valid(form)
        form.save()
        email = form.cleaned_data.get("email")
        raw_password = form.cleaned_data.get("password1")
        logger.info(
            "New signup for email=%s through SignupView", email
        )
        user = authenticate(email=email, password=raw_password)
        login(self.request, user)
        form.send_email()
        messages.info(
            self.request, "Haz creado una cuenta de manera exitosa"
        )
        return response

class LoginView(FormView):
    form_class = LoginAutentificationForm
    template_name = "main/login.html"
    success_url =  '/'

    def dispatch(self,request,*args,**kwargs):
        if request.user.is_authenticated:
            return redirect("/")
        else:
            return super(LoginView,self).dispatch(request,*args,**kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())
        messages.info(
                self.request, "login exitoso"
        )
        return super(LoginView, self).form_valid(form)

class DireccionListView(LoginRequiredMixin,ListView):
    model = models.Direccion
    template_name = "main/direccion_list.html"
    context_object_name = 'direcciones'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(usuario=self.request.user)


class DireccionUptadeView(LoginRequiredMixin,UpdateView):
    template_name = "main/direccion_update.html"
    model= models.Direccion
    form_class = UpdateViewForm

    success_url = reverse_lazy("main:direcciones_list")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(usuario=self.request.user)


class DeleteDireccion(LoginRequiredMixin,DeleteView):
     template_name = "main/confirm_delete.html"
     model = models.Direccion
     success_url = reverse_lazy("main:direcciones_list")

     def  get_queryset(self):
         queryset = super().get_queryset()
         return queryset.filter(usuario=self.request.user)


class DireccionCreateView(LoginRequiredMixin,CreateView):
    template_name = "main/direccion_create.html"
    model = models.Direccion
    form_class = UpdateViewForm
    success_url = reverse_lazy("main:direcciones_list")


    def form_valid(self,form):
        obj = form.save(commit=False)
        obj.usuario = self.request.user
        obj.save()
        messages.success(self.request,"nueva Dirección creada")
        return super().form_valid(form)


def add_to_basket(request):
    producto = get_object_or_404(models.Producto,pk=request.GET.get('producto_id'))
    basket =  request.basket
    if not  basket:
        if request.user.is_authenticated:
            usuario = request.user
        else:
            usuario = None
        basket = models.Basket.objects.create(usuario=usuario)
        request.session['basket_id'] = basket.id
    basket_line ,created = models.BasketLine.objects.get_or_create(basket=basket,producto=producto)

    if not created:
        basket_line.cantidad +=1
        basket_line.save()
    return HttpResponseRedirect(reverse('main:producto',args=(producto.slug,)))
