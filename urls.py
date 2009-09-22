from django.conf.urls.defaults import *
from django.conf import settings
from nankin.services.feed import LatestJot

# Uncomment the next two lines to enable the admin:



handler404 = 'nankin.views.page_not_found'
feeds = {
    'latest': LatestJot,
}
urlpatterns = patterns('nankin.views',
    # Example:
    # (r'^mindgames/', include('mindgames.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    
    # Core App
    (r'^$', 'index'),
    (r'^about/', 'about'),
    (r'^news/', 'news'),
    (r'^publish/', 'publish'),
    (r'^accounts/login/', 'login'),
    (r'^accounts/logout/', 'logout'),
    (r'^post/', 'post'),
    (r'^view/(?P<key>.*)/', 'view'),
    (r'^comment/(?P<key>.*)/', 'comment'),
    (r'^vote/', 'vote'),
    (r'^404/', 'page_not_found'),
    (r'^edit/(?P<key>.*)/', 'edit'),
    (r'^delete/(?P<key>.*)/', 'delete'),
    (r'rpc_relay.html', 'friend_connect', {'template':'rpc_relay.html'}),
    (r'canvas.html', 'friend_connect', {'template':'canvas.html'}),
    #(r'^wantown/upload/', 'upload'),
)
urlpatterns += patterns('',
                        (r'^feeds/(?P<url>.*)/$',
                            'django.contrib.syndication.views.feed', {'feed_dict': feeds}
                        ),
)