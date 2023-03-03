from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, authenticate, logout
from django.urls import reverse

from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import  UpdateView

from .forms import SignUpForm, ChangePasswordForm, ResetPasswordForm, PerfilForm
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from .models import CustomUser
from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.contrib import messages
from django.utils.html import strip_tags
# Create your views here.


def loginUser(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse("home"))

    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("home"))
        else:
            messages.add_message(request, messages.ERROR, 'Contraseña o Usuario incorrecto')

    return render(request, "login/login.html")


def newUser(request):

    if request.method == "POST":

        form = SignUpForm(request.POST)
        print(form.errors)
        if form.is_valid():
            print("aca")
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            # agregar message avisando al usuario que tiene que revisar su mail
            current_site = get_current_site(request)
            mail_subject = "Activation link has been sent to your email id"
            message = render_to_string(
                "login/acc_activate_email.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": account_activation_token.make_token(user),
                },
            )
            text_content=strip_tags(message)

            print("lo pase")
            to_email = form.cleaned_data.get("email")

            email = EmailMultiAlternatives(
                mail_subject, 
                text_content,
                to=[to_email]
            )
            email.attach_alternative(message,"text/html")
            email.send()

            return render(request, "login/acc_pending_act.html")
        print("hubo un error")
        context = {
            "form": form,
        }
        return render(request, "login/register.html", context)

    else:
        form = SignUpForm()

        context = {
            "form": form,
        }

        return render(request, "login/register.html", context)


def logOut(request):
    logout(request)

    return render(request, "login/logout.html")


def passwordChange(request):
    user = request.user
    print(user)
    if request.method == "POST":

        form = ChangePasswordForm(user, request.POST)
        if form.is_valid():
            form.save()

            return HttpResponse("Contrasena Cambiada")

    else:
        form = ChangePasswordForm(user)

        context = {
            "form": form,
        }

        return render(request, "login/passwordchange.html", context)


# Vista de testeo de Login
def loginTestingPage(request):

    return render(request, "login/test.html")


def activate(request, uidb64, token):

    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)

    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, "login/acc_succesful.html")
    else:
        return HttpResponse("Activation link is invalid!")


# RECUPERO USUARIO


def recoverPass(request):

    if request.method == "POST":

        print(request.POST["email"])
        mail = request.POST["email"]
        user = CustomUser.objects.get(email=mail)
        print(user.first_name)

        tokenRecoverPass(user, request)
        return render(request,"login/success-envio.html")

    else:

        return render(request, "login/recoverpass.html")


def resetPassword(request, uidb64, token):

    if request.method == "GET":
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):

            form = ResetPasswordForm(user)

            print(form)
            context = {"form": form}
            print("llego aca")
            return render(request, "login/resetpassform.html", context)
    if request.method == "POST":
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
        form = ResetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            return render(request,"login/pass_change_succes.html")
        else:
            return HttpResponse("Error form")
    return HttpResponse("Token expired")


def tokenRecoverPass(user, request):

    current_site = get_current_site(request)
    mail_subject = "Reset Password Link"
    print("aca")
    message = render_to_string(
        "login/reset_pass_email.html",
        {
            "user": user,
            "domain": current_site.domain,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": account_activation_token.make_token(user),
        },
    )
    text_content=strip_tags(message)

    print("lo pase")
    to_email = user.email
    email = EmailMultiAlternatives(
        mail_subject, 
        text_content, 
        to=[to_email]
    )
    email.attach_alternative(message,"text/html")
    email.send()


@login_required
def profile(request):
    if request.method=='POST':
        u_form=PerfilForm(request.POST, instance=request.user)
        if u_form.is_valid() :
            u_form.save()
            messages.success(request,f'¡Tu cuenta ha sido actualizada!')
            return redirect('perfil')
    else:
        u_form=PerfilForm(instance=request.user)
    context={
        "u_form":u_form,
    }

    return render(request,'perfil/perfil.html',context)
    
    