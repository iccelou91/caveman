from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'caveman.views.home', name='home'),
    # url(r'^caveman/', include('caveman.foo.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    (r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'registration/login.html'}),
    (r'^$', 'checkin.views.checkIn'),
    (r'^test/$', 'checkin.views.test')
)
