# -*- coding: utf -*-
"""
URLs for the auth app.
"""
from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from rpg_auth.views import UserCreateView, ActivateFormView


urlpatterns = patterns(
    '',
    url(r'^register/$', UserCreateView.as_view(), name='register'),
    url(
        r'^register/confirmation/$',
        TemplateView.as_view(template_name='rpg_auth/rpguser_form_confirmation.html'),
        name='register_confirmation',
    ),
    url(
        r'^activate/(?P<activation_key>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})/$',
        ActivateFormView.as_view(),
        name='activation',
    ),
    url(
        r'^activate/confirmation/$',
        TemplateView.as_view(template_name='rpg_auth/activate_confirmation.html'),
        name='activation_confirmation',
    ),

)


# Django generic views
urlpatterns += patterns(
    'django.contrib.auth.views',
    url(
        r'^login/$',
        'login',
        {'template_name': 'rpg_auth/login_form.html'},
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
            'template_name': 'rpg_auth/password_change_form.html',
            'post_change_redirect': 'rpg_auth:password_change_form_confirmation',
        },
        name='password_change'),
    url(
        r'^change-password/confirmation/$',
        'password_change_done',
        {
            'template_name': 'rpg_auth/password_change_form_confirmation.html',
        },
        name='password_change_form_confirmation'
    ),
    url(
        r'^password-request/$',
        'password_reset',
        {
            'template_name': 'rpg_auth/password_request_form.html',
            'post_reset_redirect': 'rpg_auth:password_request_form_confirmation',
            'email_template_name': 'rpg_auth/email/password_request_email.txt',
        },
        name='password_request_form'
    ),
    url(
        r'^password-request/confirmation/$',
        'password_reset_done',
        {
            'template_name': 'rpg_auth/password_request_form_confirmation.html',
        },
        name='password_request_form_confirmation'
    ),
    url(
        r'^password-reset/(?P<uidb64>\w+)/(?P<token>[\d\w-]+)/$',
        'password_reset_confirm',
        {
            'template_name': 'rpg_auth/password_reset_form.html',
            'post_reset_redirect': 'rpg_auth:password_reset_form_confirmation',
        },
        name='password_reset_form'
    ),
    url(
        r'^password-reset/confirmation/$',
        'password_reset_complete',
        {
            'template_name': 'rpg_auth/password_reset_form_confirmation.html',
        },
        name='password_reset_form_confirmation'
    )
)
