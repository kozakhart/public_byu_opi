from django.contrib import admin
from django.urls import path, include

#OTP Authentication Setup
#from two_factor.urls import urlpatterns as tf_urls
from django_otp.admin import OTPAdminSite
from django.contrib.auth.models import User
from django_otp.plugins.otp_totp.models import TOTPDevice

class OTPAdmin(OTPAdminSite):
    pass

otp_admin_site = OTPAdmin(name='OTPAdmin')
otp_admin_site.register(User)
otp_admin_site.register(TOTPDevice)

urlpatterns = [
    path('', include('myapp.urls')),
    path('otpadmin/', otp_admin_site.urls),
    path('admin/', admin.site.urls),
]

#Adding text to admin frontend
admin.site.site_header = "CLS Admin"
admin.site.index_title = "Welcome to CLS"


