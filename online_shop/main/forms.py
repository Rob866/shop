from django import forms
from django.core.mail  import  send_mail
import logging

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
