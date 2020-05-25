from django.views.generic.edit import  FormView
from django.shortcuts import render
from main.forms import ContactForm
# Create your views here.
def home(request):
    return render(request,'main/home.html',{})

def about_us(request):
    return render(request,'main/about_us.html',{})

class ContactPageView(FormView):
    template_name= 'main/contact_form.html'
    form_class = ContactForm
    success_url = '/'

    def form_valid(self,form):
        form.send_mail()
        return super(ContactPageView, self).form_valid(form)
