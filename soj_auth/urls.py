# ~*~ coding: utf ~*~
"""
URLs for the auth app.
"""
from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from soj_auth.views import UserCreateView


urlpatterns = patterns(
    '',
    url(r'^register/$', UserCreateView.as_view(), name='register'),
    url(
        r'^register/confirmation/$',
        TemplateView.as_view(template_name='soj_auth/sojuser_form_confirmation.html'),
        name='register-confirmation',
    ),
)


# Django generic views
urlpatterns += patterns(
    'django.contrib.auth.views',
    url(
        r'^login/$',
        'login',
        {'template_name': 'soj_auth/login_form.html'},
        name='login',
    ),
    url(
        r'^logout/$',
        'logout_then_login',
        name='logout'
    ),
    url(
        r'^change-password/$',
        'password_change',
        {
            'template_name': 'soj_auth/password_change_form.html',
            'post_change_redirect': 'soj_auth:password_change_form_confirmation',
        },
        name='password_change'),
    url(
        r'^change-password/confirmation/$',
        'password_change_done',
        {
            'template_name': 'soj_auth/password_change_form_confirmation.html',
        },
        name='password_change_form_confirmation'
    ),
    url(
        r'^password-request/$',
        'password_reset',
        {
            'template_name': 'soj_auth/password_request_form.html',
            'post_reset_redirect': 'soj_auth:password_request_form_confirmation',
            'email_template_name': 'soj_auth/email/password_request_email.txt',
        },
        name='password_request_form'
    ),
    url(
        r'^password-request/confirmation/$',
        'password_reset_done',
        {
            'template_name': 'soj_auth/password_request_form_confirmation.html',
        },
        name='password_request_form_confirmation'
    ),
    url(
        r'^password-reset/(?P<uidb64>\w+)/(?P<token>[\d\w-]+)/$',
        'password_reset_confirm',
        {
            'template_name': 'soj_auth/password_reset_form.html',
            'post_reset_redirect': 'soj_auth:password_reset_form_confirmation',
        },
        name='password_reset_form'
    ),
    url(
        r'^password-reset/confirmation/$',
        'password_reset_complete',
        {
            'template_name': 'soj_auth/password_reset_form_confirmation.html',
        },
        name='password_reset_form_confirmation'
    )
)
