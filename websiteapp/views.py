from website import settings
from django.shortcuts import  render, redirect
from .forms import NewUserForm
from django.contrib.auth import login
from django.contrib import messages #import messages
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import get_template
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse


import os

TEMPLATE_DIR_WEBSITE = os.path.join(settings.TEMPLATES_DIR, 'websiteapp')
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UserModel = get_user_model()


def index(request):
    return render(request, os.path.join(TEMPLATE_DIR_WEBSITE, 'homepage.html'), {'title':'Title of the database with more text as a place holder etc.',
                                                                                 'content': """(General descriptions or part of the text from the article) Lorem ipsum dolor sit amet, consectetuer
                    adipiscing elit, sed diam nonummy nibh euismod tincid- unt ut laoreet dolore magna aliquam erat
                    volutpat. Ut wisi enim ad minim veniam, quis nostrud exerci tation ullamcorper suscipit lobortis
                    nisl ut aliquip ex ea commodo consequat. Duis autem vel eum iriure dolor in hendrerit in vul- putate
                    velit esse molestie consequat, vel illum dolore eu feugiat nulla facilisis at vero eros et accumsan
                    et iusto odio dignissim qui blandit praesent luptatum zzril delenit augue duis dolore te feugait
                    facilisi.""",
                                                                                 'hyperlink':'#'})

def about(request):
    return render(request, os.path.join(TEMPLATE_DIR_WEBSITE, "about.html"))

def publications(request):
    return render(request, os.path.join(TEMPLATE_DIR_WEBSITE, "publications.html"))

def publications(request):
    return render(request, os.path.join(TEMPLATE_DIR_WEBSITE, "publications.html"))

def productdescription(request):
    return render(request, os.path.join(TEMPLATE_DIR_WEBSITE, "productdescription.html"))

def news(request):
    return render(request, os.path.join(TEMPLATE_DIR_WEBSITE, "news.html"))

def contactus(request):
    return render(request, os.path.join(TEMPLATE_DIR_WEBSITE, "contactus.html"))

def database(request):
    return render(request, os.path.join(TEMPLATE_DIR_WEBSITE, "database.html"))

def comingsoon(request):
    return render(request, os.path.join(TEMPLATE_DIR_WEBSITE, "comingsoon.html"))

def privacypolicy(request):
    return render(request, os.path.join(TEMPLATE_DIR_WEBSITE, "privacypolicy.html"))

def university(request):
    return render(request, os.path.join(TEMPLATE_DIR_WEBSITE, "university.html"))

def job(request):
    return render(request, os.path.join(TEMPLATE_DIR_WEBSITE, "job.html"))

def practicioners(request):
    return render(request, os.path.join(TEMPLATE_DIR_WEBSITE, "practicioners.html"))

def organisations(request):
    return render(request, os.path.join(TEMPLATE_DIR_WEBSITE, "organisations.html"))

def merchandise(request):
    return render(request, os.path.join(TEMPLATE_DIR_WEBSITE, "merchandise.html"))

def product(request):
    return render(request, os.path.join(TEMPLATE_DIR_WEBSITE, "product.html"))

# def (request):
# 	form = NewUserForm
# 	if request.method == "POST":
# 		if request.method == 'POST':
# 			form = NewUserForm(request.POST)
# 			if form.is_valid():
# 				user = form.save(commit=True)
# 				login(request, user)
# 				return HttpResponse("Registration successful." )
# 			else:
# 				return HttpResponse("Unsuccessful registration. Invalid information.")
#
# 	return render (request=request, template_name=os.path.join(TEMPLATE_DIR_WEBSITE, "signup.html"), context={"register_form":form})

def signup(request):

    form = NewUserForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string(os.path.join(TEMPLATE_DIR_WEBSITE, 'acc_active_email.html'), {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })

            html_message = get_template(os.path.join(TEMPLATE_DIR_WEBSITE, "acc_active_email.html")).render({
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, html_message, to=[to_email]
            )
            email.content_subtype = "html"
            email.send()
            return render(request, os.path.join(TEMPLATE_DIR_WEBSITE, "registeredsuccess.html"),
                          {'info': 'Please confirm your email address to complete the registration'})

            login(request,user)
            return HttpResponse("Success")

    return render(request,os.path.join(TEMPLATE_DIR_WEBSITE, "signup.html"),context={"register_form":form})


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = UserModel._default_manager.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, os.path.join(TEMPLATE_DIR_WEBSITE, "registeredsuccess.html"),
                      {'info': 'Thank you for your email confirmation. Now you can login your account.'})
    else:
        return render(request, os.path.join(TEMPLATE_DIR_WEBSITE, "registeredsuccess.html"),
                      {'info': 'Activation link is invalid!'})

def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))

            else:
                return HttpResponse("Account Not Active")
        else:
            print('someone tried login and failed!')
            print("username {} and password {}".format(username, password))
            return HttpResponse("Invalid login details were supplied")
    else:
        return render(request, os.path.join(TEMPLATE_DIR_WEBSITE, "signin.html"), {})

@login_required
def signout(request):
    logout(request)
    return render(request, os.path.join(TEMPLATE_DIR_WEBSITE, 'homepage.html'))