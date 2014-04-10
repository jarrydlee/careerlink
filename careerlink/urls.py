from django.conf.urls import patterns, include, url


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'careerlink.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'careerlink.system.views.home', name='home'),
)
