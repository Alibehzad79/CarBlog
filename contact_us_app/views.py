import datetime
from django.shortcuts import render, redirect

# Create your views here.
from contact_us_app.forms import ContactForm
from contact_us_app.models import Contact
from site_settings_app.models import Setting


def contact_us(request):
    setting = Setting.objects.last()
    form = ContactForm(request.POST or None)
    if form.is_valid():
        name = form.cleaned_data.get('name')
        email = form.cleaned_data.get('email')
        subject = form.cleaned_data.get('subject')
        message = form.cleaned_data.get('message')

        new_contact = Contact.objects.create(name=name, email=email, subject=subject, message=message,
                                             date_send=datetime.datetime.now())
        if new_contact is not None:
            new_contact.save()
            return redirect('contact:contact-us')
        form = ContactForm()

    context = {
        'form': form,
        'setting': setting,
    }
    return render(request, 'contact/contact.html', context)
