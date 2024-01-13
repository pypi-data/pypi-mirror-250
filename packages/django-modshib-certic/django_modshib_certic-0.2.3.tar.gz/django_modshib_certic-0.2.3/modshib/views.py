from logging import Logger, INFO

from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.models import User, Group
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import render

logger = Logger(name=__name__, level=INFO)

try:
    CREATE_ACCOUNT = bool(settings.MODSHIB_CREATE_ACCOUNT)
except AttributeError:
    CREATE_ACCOUNT = False

try:
    ACTIVATE_ACCOUNT = bool(settings.MODSHIB_ACTIVATE_ACCOUNT)
except AttributeError:
    ACTIVATE_ACCOUNT = False

context = {"login_url": settings.LOGIN_URL}


def sso(request: HttpRequest) -> HttpResponse:
    # nothing to do here...
    if request.user.is_authenticated:
        logger.info(
            f"User already authenticated, redirecting to {settings.LOGIN_REDIRECT_URL}"
        )
        return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)

    # fetch EPPN from headers, injected by mod_shib
    eppn = request.META.get("HTTP_EPPN", None)
    supann_etablissement = request.META.get("HTTP_SUPANNETABLISSEMENT", None)
    # display_name = request.META.get("HTTP_DISPLAYNAME", None)
    mail = request.META.get("HTTP_MAIL", None)
    last_name = request.META.get("HTTP_SN", None)
    first_name = request.META.get("HTTP_GIVENNAME", None)
    if not eppn:
        return render(request, "registration/sso_fail.html", context)

    # find account
    eppn = eppn.strip()
    user = User.objects.filter(username=eppn).first()
    if not user and CREATE_ACCOUNT:
        logger.info(f"user {eppn} not found, creating account")
        user = User.objects.create_user(eppn)
        user.is_active = False
        if mail:
            user.email = mail
        if last_name:
            user.last_name = last_name
        if first_name:
            user.first_name = first_name
        user.save()
        if supann_etablissement:
            group, created = Group.objects.get_or_create(
                name=f"supann_{supann_etablissement}"
            )
            user.groups.add(group)
    if not user:
        logger.info(f"user {eppn} not found, rejecting auth")
        return render(request, "registration/sso_no_account.html", context)
    if not user.is_active and ACTIVATE_ACCOUNT:
        logger.info(f"user {eppn} not active, activating")
        user.is_active = True
        user.save()
    if not user.is_active:
        logger.info(f"user {eppn} inactive, rejecting auth")
        return render(request, "registration/sso_no_account.html", context)
    if user and user.is_active:
        logger.info(f"active user {eppn} found, login")
        request.session["auth_is_from_modshib"] = True
        login(request, user)
        return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
