from django import forms
from django.core.mail  import  send_mail
import logging
from django.contrib.auth.forms import (UserCreationForm,UsernameField)

from django.contrib.auth import (get_user_model, authenticate)

from . import models

logger = logging.getLogger(__name__)

class ContactForm(forms.Form):
    nombre = forms.CharField(label='Nombre',max_length=100)
    email =  forms.EmailField(label="Email")
    mensaje = forms.CharField(label='Mensaje',max_length=600,widget=forms.Textarea)


    def send_mail(self):
        logger.info('Enviando email hacia  mi servicio custumer')
        mensaje = 'De: {0}\n Email:{1}\n mensaje:{2}'.format(
            self.cleaned_data['nombre'],
            self.cleaned_data['email'],
            self.cleaned_data['mensaje'],
        )

        send_mail(
            'Mensaje del Sitio',
            mensaje,
            "site@booktime.domain",
            ["customerservice@booktime.domain"],
            fail_silently=False,
        )

class LoginAutentificationForm(forms.Form):

    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())

    def __init__(self,request=None,*args,**kwargs):
        self.request = request
        self.user =None
        super(LoginAutentificationForm,self).__init__(*args,**kwargs)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        if email is not None and password:
            self.user = authenticate(email=email,password=password)
        if self.user is None:
            raise forms.ValidationError('error de autentificación')
        logger.info("Autentificación éxitosa=%s",email)
        return self.cleaned_data
    def get_user(self):
        return self.user


class SignUpForm(UserCreationForm):

    class Meta:
        model = get_user_model()
        fields=('email','password1', 'password2')


    def send_email(self):
        logger.info("envio un email al usuario que se registro",
        self.cleaned_data["email"])
        mensaje = "{Bienvenido { self.cleaned_data['email']}"

        send_mail(
            "Bienvenido a nuestra tienda en linea",
            mensaje,
            "site@booktime.domain",
            [self.cleaned_data["email"]],
            fail_silently=True)



class UpdateViewForm(forms.ModelForm):
    PAISES_SOPORTADOS = (
             ('mx','Mexico'),
             ('eu','EUA')
        )

    pais = forms.ChoiceField(choices=PAISES_SOPORTADOS,widget=forms.Select(attrs={'class':'form-control'}))

    class Meta:
        model = models.Direccion
        fields=('nombre','direccion1', 'direccion2','codigo_postal','ciudad','pais')
