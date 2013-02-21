
from django.contrib.auth.views import login
from django.shortcuts import render

from accounts.forms import EmailAuthenticationForm

def view_login(request):
    if request.method == 'POST':
        return login(request, authentication_form=EmailAuthenticationForm, template_name='accounts/registration/registration_login.html')
    else:
        form = EmailAuthenticationForm()

    return render(request, 'accounts/registration/registration_login.html', {'form':form})


def view_signup(request):
    if request.method == 'POST':
        pass
